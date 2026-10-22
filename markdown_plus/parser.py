"""
markdown_plus.parser
~~~~~~~~~~~~~~~~~~~~

Turn a Markdown source string into a `Document` composed of segments
(regular markdown chunks and button triggers) plus a map of modals.

The syntax we recognize:

    :::modal{id="m1" title="Hello"}
    Modal body in Markdown.
    :::

    [Open](#m1){.modal-btn}
    [Close](#){.modal-close}
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


_ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')
_OPEN_RE = re.compile(r"^:::modal\{([^}]*)\}\s*$", re.M)
_LINK_RE = re.compile(
    r"\[([^\]]+)\]\(#?([^)]*)\)\{\.(modal-btn|modal-close)\}"
)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Modal:
    id: str
    title: str
    body: str


@dataclass
class Segment:
    kind: str
    content: str = ""
    label: str = ""
    target: str = ""


@dataclass
class Document:
    segments: list[Segment] = field(default_factory=list)
    modals: dict[str, Modal] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def parse_document(text: str) -> Document:
    doc = Document()

    remaining: list[str] = []
    pos = 0
    for match in _OPEN_RE.finditer(text):
        remaining.append(text[pos:match.start()])
        attrs = dict(_ATTR_RE.findall(match.group(1)))

        close_idx = text.find("\n:::", match.end())
        if close_idx == -1:
            body = text[match.end():]
            pos = len(text)
        else:
            body = text[match.end():close_idx]
            pos = close_idx + len("\n:::")

        modal_id = attrs.get("id") or f"md-modal-{len(doc.modals)}"
        doc.modals[modal_id] = Modal(
            id=modal_id,
            title=attrs.get("title", ""),
            body=body.strip("\n"),
        )
    remaining.append(text[pos:])
    cleaned = "".join(remaining)

    segments: list[Segment] = []
    cursor = 0
    for m in _LINK_RE.finditer(cleaned):
        if m.start() > cursor:
            chunk = cleaned[cursor:m.start()]
            if chunk.strip():
                segments.append(Segment(kind="md", content=chunk))
        label, target, kind = m.group(1), m.group(2), m.group(3)
        if kind == "modal-btn":
            segments.append(Segment(kind="button", label=label, target=target))
        else:  # modal-close
            segments.append(
                Segment(kind="button", label=label, target="__close__")
            )
        cursor = m.end()
    if cursor < len(cleaned):
        tail = cleaned[cursor:]
        if tail.strip():
            segments.append(Segment(kind="md", content=tail))

    doc.segments = segments
    return doc
