"""Layout factory and exports."""

from typing import Type

from .base import BaseLayout
from .creative import FanLayout, PerspectiveLayout, Stack3DLayout, TripleRowLayout
from .duo import DuoHorizontalLayout, DuoVerticalLayout
from .grid import Grid2x2Layout
from .single import SingleLayout

__all__ = [
    "BaseLayout",
    "SingleLayout",
    "DuoHorizontalLayout",
    "DuoVerticalLayout",
    "Grid2x2Layout",
    "FanLayout",
    "PerspectiveLayout",
    "Stack3DLayout",
    "TripleRowLayout",
    "get_layout",
]

LAYOUT_MAP: dict[str, Type[BaseLayout]] = {
    "single": SingleLayout,
    "duo-horizontal": DuoHorizontalLayout,
    "duo-vertical": DuoVerticalLayout,
    "grid-2x2": Grid2x2Layout,
    "fan": FanLayout,
    "perspective": PerspectiveLayout,
    "stack-3d": Stack3DLayout,
    "triple-row": TripleRowLayout,
}


def get_layout(name: str, width: int, height: int, **kwargs) -> BaseLayout:
    """Get a layout instance by name.

    Args:
        name: Layout name (e.g., "single", "duo-horizontal", "grid-2x2")
        width: Canvas width
        height: Canvas height
        **kwargs: Additional arguments passed to the layout constructor

    Returns:
        Layout instance

    Raises:
        ValueError: If layout name is unknown
    """
    if name not in LAYOUT_MAP:
        available = ", ".join(sorted(LAYOUT_MAP.keys()))
        raise ValueError(f"Unknown layout '{name}'. Available layouts: {available}")

    layout_class = LAYOUT_MAP[name]
    return layout_class(width=width, height=height, **kwargs)
