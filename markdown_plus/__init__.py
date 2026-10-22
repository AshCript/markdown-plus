"""markdown+ — interactive Markdown viewer for the terminal."""

from .parser import Document, Modal, Segment, parse_document

__all__ = ["Document", "Modal", "Segment", "parse_document"]
__version__ = "0.1.0"
