"""Base layout class for screenshot rendering."""

from abc import ABC, abstractmethod
from typing import Tuple

from PIL import Image


class BaseLayout(ABC):
    """Abstract base class for all layout types.

    Each layout defines how screenshots are arranged on the canvas.
    """

    def __init__(
        self, width: int, height: int, background_color: Tuple[int, int, int] = (255, 255, 255)
    ):
        """Initialize the layout with canvas dimensions.

        Args:
            width: Canvas width in pixels
            height: Canvas height in pixels
            background_color: Background color as RGB tuple
        """
        self.width = width
        self.height = height
        self.background_color = background_color

    @abstractmethod
    def render(self, screenshots: list[Image.Image], **kwargs) -> Image.Image:
        """Render screenshots on the canvas.

        Args:
            screenshots: List of PIL Image objects to render
            **kwargs: Additional layout-specific options

        Returns:
            Rendered PIL Image
        """
        pass

    def create_canvas(self) -> Image.Image:
        """Create a blank canvas with the layout's dimensions.

        Returns:
            New PIL Image (RGB mode)
        """
        return Image.new("RGB", (self.width, self.height), self.background_color)

    def _scale_to_fit(self, image: Image.Image, max_width: int, max_height: int) -> Image.Image:
        """Scale image to fit within given dimensions while preserving aspect ratio.

        Args:
            image: Image to scale
            max_width: Maximum width
            max_height: Maximum height

        Returns:
            Scaled image
        """
        ratio = min(max_width / image.width, max_height / image.height)
        if ratio < 1.0:
            new_size = (int(image.width * ratio), int(image.height * ratio))
            return image.resize(new_size, Image.Resampling.LANCZOS)
        return image.copy()
