"""Single screenshot layout."""

from PIL import Image

from .base import BaseLayout


class SingleLayout(BaseLayout):
    """Layout for a single centered screenshot with automatic scaling."""

    def __init__(
        self,
        width: int,
        height: int,
        background_color: tuple[int, int, int] = (255, 255, 255),
        padding: int = 40,
    ):
        """Initialize single layout.

        Args:
            width: Canvas width
            height: Canvas height
            background_color: Background color as RGB tuple
            padding: Padding around the screenshot (default: 40px)
        """
        super().__init__(width, height, background_color)
        self.padding = padding

    def render(self, screenshots: list[Image.Image], **kwargs) -> Image.Image:
        """Render a single screenshot centered on the canvas.

        Args:
            screenshots: List containing one screenshot
            **kwargs: Ignored

        Returns:
            Rendered image

        Raises:
            ValueError: If screenshots list is empty or contains more than one image
        """
        if not screenshots:
            raise ValueError("SingleLayout requires at least one screenshot")

        canvas = self.create_canvas()

        # Take the first screenshot
        screenshot = screenshots[0]

        # Calculate available space
        available_width = self.width - 2 * self.padding
        available_height = self.height - 2 * self.padding

        # Scale to fit
        scaled = self._scale_to_fit(screenshot, available_width, available_height)

        # Center on canvas
        x = (self.width - scaled.width) // 2
        y = (self.height - scaled.height) // 2

        canvas.paste(scaled, (x, y))

        return canvas
