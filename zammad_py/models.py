"""Model classes."""

from dataclasses import dataclass, asdict

@dataclass
class KnowledgeBaseSettings:
    iconset: str = None
    color_highlight: str = None
    color_header_link: str = None
    homepage_layout: str = None
    category_layout: str = None
    active: bool = None
    show_feed_icon: bool = None
    custom_address: str = None

    def to_json(self):
        """
        Returns a dictionary of the settings, excluding any fields that are None.
        This ensures the PATCH request only updates provided fields.
        """
        return asdict(
            self,
            dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
