from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

SITE_URL = "https://site-web-hth.com.cn"
KEYWORD = "华体会"


@dataclass
class KeywordNote:
    """Represents a single keyword note."""
    title: str
    content: str
    keyword: str = KEYWORD
    source_url: str = SITE_URL
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    importance: int = 3

    def __post_init__(self):
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be between 1 and 5")

    def summary(self, max_length: int = 60) -> str:
        """Return a truncated summary of the content."""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length - 3] + "..."

    def formatted(self, include_url: bool = True) -> str:
        """Return a formatted string representation of the note."""
        lines = [
            f"Title: {self.title}",
            f"Keyword: {self.keyword}",
            f"Importance: {'★' * self.importance}{'☆' * (5 - self.importance)}",
            f"Content: {self.content}",
        ]
        if include_url:
            lines.append(f"Source: {self.source_url}")
        if self.tags:
            lines.append(f"Tags: {', '.join(self.tags)}")
        lines.append(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}")
        return "\n".join(lines)


@dataclass
class NoteCollection:
    """A collection of keyword notes with formatting utilities."""
    notes: List[KeywordNote] = field(default_factory=list)
    collection_name: str = "My Notes"

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_importance(self, min_importance: int) -> List[KeywordNote]:
        return [n for n in self.notes if n.importance >= min_importance]

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def generate_report(self, include_url: bool = True) -> str:
        """Generate a full text report of all notes."""
        if not self.notes:
            return f"Collection '{self.collection_name}' is empty."

        lines = [
            f"=== {self.collection_name} ===",
            f"Total Notes: {len(self.notes)}",
            f"Keyword Focus: {KEYWORD}",
            f"Associated URL: {SITE_URL}",
            "",
        ]
        for i, note in enumerate(self.notes, 1):
            lines.append(f"[Note {i}]")
            lines.append(note.formatted(include_url=include_url))
            lines.append("")
        return "\n".join(lines).strip()

    def export_as_markdown(self) -> str:
        """Export all notes as Markdown content."""
        md_lines = [
            f"# {self.collection_name}",
            f"",
            f"**Keyword:** {KEYWORD}  ",
            f"**Source:** [{SITE_URL}]({SITE_URL})  ",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"",
            "---",
            "",
        ]
        for note in self.notes:
            md_lines.append(f"## {note.title}")
            md_lines.append(f"")
            md_lines.append(f"- **Keyword:** {note.keyword}")
            md_lines.append(f"- **Importance:** {note.importance}/5")
            md_lines.append(f"- **Created:** {note.created_at.strftime('%Y-%m-%d %H:%M')}")
            if note.tags:
                md_lines.append(f"- **Tags:** {', '.join(note.tags)}")
            md_lines.append(f"")
            md_lines.append(note.content)
            md_lines.append(f"")
            md_lines.append(f"[Source]({note.source_url})")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
        return "\n".join(md_lines)


def demo_usage() -> None:
    """Demonstrate typical usage of the data classes."""
    note1 = KeywordNote(
        title="Introduction to 华体会",
        content="华体会 is a key concept related to our main platform at site-web-hth.com.cn.",
        tags=["introduction", "basics"],
        importance=4,
    )
    note2 = KeywordNote(
        title="Advanced Features",
        content="Exploring deeper aspects of 华体会 with practical examples and use cases.",
        tags=["advanced", "examples"],
        importance=5,
    )
    note3 = KeywordNote(
        title="Community Notes",
        content="User feedback and community contributions about 华体会 and related services.",
        tags=["community", "feedback"],
        importance=2,
    )

    collection = NoteCollection(collection_name="华体会 Knowledge Base")
    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)

    print(collection.generate_report(include_url=True))

    print("\n--- Filtered by importance >= 3 ---")
    for note in collection.filter_by_importance(3):
        print(note.summary())
        print()

    print("--- Markdown Export (first 500 chars) ---")
    md = collection.export_as_markdown()
    print(md[:500])


if __name__ == "__main__":
    demo_usage()