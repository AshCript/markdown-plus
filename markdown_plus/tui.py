"""
markdown_plus.tui
~~~~~~~~~~~~~~~~~

Textual UI for markdown+.

Composes a scrollable document out of Markdown blocks and button
widgets; clicking a button pushes a modal `ModalScreen` with the
corresponding modal's Markdown body.
"""

from __future__ import annotations

from pathlib import Path

from rich.markdown import Markdown as RichMarkdown
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Static

from .parser import Document, Modal, parse_document


# ---------------------------------------------------------------------------
# Widgets
# ---------------------------------------------------------------------------

class MarkdownBlock(Static):
    """A static widget that renders one chunk of Markdown."""

    def __init__(self, source: str, **kwargs):
        super().__init__(RichMarkdown(source), **kwargs)


class ModalView(ModalScreen):
    """A terminal-native modal that holds rendered Markdown."""

    BINDINGS = [("escape", "dismiss", "Close")]

    def __init__(self, modal: Modal):
        super().__init__()
        self.modal = modal

    def compose(self) -> ComposeResult:
        with Vertical(id="modal-box"):
            if self.modal.title:
                yield Static(f"[bold]{self.modal.title}[/bold]", id="modal-title")
            with VerticalScroll(id="modal-body"):
                yield MarkdownBlock(self.modal.body)
            yield Button("Close", id="modal-close", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "modal-close":
            self.dismiss()

    DEFAULT_CSS = """
    ModalView {
        align: center middle;
    }
    #modal-box {
        width: 70%;
        max-width: 100;
        height: auto;
        max-height: 85%;
        border: thick $accent;
        background: $surface;
        padding: 1 2;
    }
    #modal-title {
        padding-bottom: 1;
    }
    #modal-body {
        height: auto;
        max-height: 60vh;
        padding-bottom: 1;
    }
    """


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------

class MarkdownPlusApp(App):
    """Lays out a Document as a scrollable page with clickable buttons."""

    TITLE = "markdown+"
    SUB_TITLE = ""

    DEFAULT_CSS = """
    Screen { padding: 1 2; }
    Button.modal-trigger { width: auto; margin: 0 0 1 0; }
    """

    def __init__(self, document: Document):
        super().__init__()
        self.document = document

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with VerticalScroll(id="doc"):
            for i, seg in enumerate(self.document.segments):
                if seg.kind == "md":
                    yield MarkdownBlock(seg.content)
                else:
                    if seg.target == "__close__":
                        continue
                    yield Button(
                        seg.label,
                        id=f"trigger-{i}",
                        classes="modal-trigger",
                        variant="primary",
                    )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id or ""
        if not btn_id.startswith("trigger-"):
            return
        idx = int(btn_id.split("-", 1)[1])
        seg = self.document.segments[idx]
        modal = self.document.modals.get(seg.target)
        if modal is None:
            self.notify(
                f"No modal found for '#{seg.target}'", severity="error"
            )
            return
        self.push_screen(ModalView(modal))


# ---------------------------------------------------------------------------
# Convenience entry point
# ---------------------------------------------------------------------------

def run(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    doc = parse_document(text)
    app = MarkdownPlusApp(doc)
    app.SUB_TITLE = path.name
    app.run()
    return 0
