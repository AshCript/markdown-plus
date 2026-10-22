*This project has been created by RAKOTONDRABE As Manjaka Josvah ([@AshCript](https://github.com/AshCript), as-rakot).*

---

## Description

**markdown+** is an interactive Markdown viewer built for the terminal. It reads a `.md` file, renders it with rich formatting, and transforms a custom `:::modal{...}` syntax into **clickable buttons that open real modal windows inside your terminal** — no browser, no GUI, no HTML rendering.

The problem it solves is simple: Markdown is a static format. When you want to embed interactive content — a help popup, a definition, a confirmation dialog — you either leave the terminal for a browser or lose interactivity entirely. markdown+ keeps you in the terminal while restoring the ability to click a button and see a modal pop up with fully rendered Markdown inside.

**Key features:**

- Terminal-native Markdown rendering via Rich (headings, lists, emphasis, code blocks, blockquotes).
- Custom modal syntax: `:::modal{id="..." title="..."}` blocks are invisible until triggered.
- Clickable trigger buttons: `[Label](#id){.modal-btn}` becomes a real button in the terminal.
- Native modal screens with scrollable content, a Close button, and `ESC` to dismiss.
- Zero external services: no server, no browser, no network.

---

## Instructions

### Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | ≥ 3.10 | Uses modern typing syntax (`list[str]`, `str | None`). |
| pip | any recent | For installing the package and its dependencies. |
| Terminal | any | Must support ANSI colors. Mouse events are optional (keyboard navigation works). |

No system-level dependencies. Rich and Textual are installed automatically as Python packages.

### Installation

```bash
# Clone the repository
~$ git clone https://github.com/AshCript/markdown-plus.git
~$ cd markdown-plus

# Install in editable mode (recommended for development)
~$ pip install -e ".[dev]"
```

If you only want to use the CLI without development tools:

```bash
~$ pip install -e .
```

### Execution

```bash
~$ markdown-plus examples/hello.md
```

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE)
file for the full text.
