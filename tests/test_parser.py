from markdown_plus.parser import parse_document


def test_single_modal_and_button():
    src = (
        "# Title\n\n"
        "[Open](#m1){.modal-btn}\n\n"
        ':::modal{id="m1" title="Hi"}\n'
        "Body **content**.\n"
        ":::\n"
    )
    doc = parse_document(src)

    assert "m1" in doc.modals
    assert doc.modals["m1"].title == "Hi"
    assert "Body **content**." in doc.modals["m1"].body

    buttons = [s for s in doc.segments if s.kind == "button"]
    assert len(buttons) == 1
    assert buttons[0].label == "Open"
    assert buttons[0].target == "m1"


def test_close_link_is_marked_close():
    src = "[Close](#){.modal-close}"
    doc = parse_document(src)
    buttons = [s for s in doc.segments if s.kind == "button"]
    assert buttons[0].target == "__close__"


def test_unterminated_modal_is_tolerated():
    src = ':::modal{id="x"}\nunclosed body\n'
    doc = parse_document(src)
    assert "x" in doc.modals
    assert "unclosed body" in doc.modals["x"].body


def test_no_modals_still_produces_markdown_segment():
    doc = parse_document("# Just a heading\n\nSome text.\n")
    md_segments = [s for s in doc.segments if s.kind == "md"]
    assert len(md_segments) == 1
    assert "# Just a heading" in md_segments[0].content


def test_markdown_between_buttons_is_preserved():
    src = (
        "Before.\n\n"
        "[Open](#m1){.modal-btn}\n\n"
        "Between.\n\n"
        "[Close](#){.modal-close}\n\n"
        "After.\n\n"
        ':::modal{id="m1"}\nbody\n:::\n'
    )
    doc = parse_document(src)
    md_chunks = "".join(s.content for s in doc.segments if s.kind == "md")
    assert "Before." in md_chunks
    assert "Between." in md_chunks
    assert "After." in md_chunks
