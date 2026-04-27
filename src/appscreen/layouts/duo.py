"""Dual screenshot layouts."""

from PIL import Image

from .base import BaseLayout


class DuoHorizontalLayout(BaseLayout):
    """Layout for two screenshots side by side."""

    def __init__(
        self,
        width: int,
        height: int,
        background_color: tuple[int, int, int] = (255, 255, 255),
        spacing: int = 20,
        padding: int = 40,
    ):
        """Initialize horizontal duo layout.

        Args:
            width: Canvas width
            height: Canvas height
            background_color: Background color as RGB tuple
            spacing: Space between screenshots (default: 20px)
            padding: Padding around screenshots (default: 40px)
        """
        super().__init__(width, height, background_color)
        self.spacing = spacing
        self.padding = padding

    def render(self, screenshots: list[Image.Image], **kwargs) -> Image.Image:
        """Render two screenshots side by side.

        Args:
            screenshots: List containing two screenshots
            **kwargs: Ignored

        Returns:
            Rendered image

        Raises:
            ValueError: If screenshots list doesn't contain exactly two images
        """
        if len(screenshots) != 2:
            raise ValueError(
                f"DuoHorizontalLayout requires exactly 2 screenshots, got {len(screenshots)}"
            )

        canvas = self.create_canvas()

        # Calculate available space for each screenshot
        available_width = (self.width - 2 * self.padding - self.spacing) // 2
        available_height = self.height - 2 * self.padding

        # Scale both screenshots to the same size
        scaled = [self._scale_to_fit(s, available_width, available_height) for s in screenshots]

        # Calculate positions (centered vertically)
        y_positions = [(self.height - s.height) // 2 for s in scaled]
        x1 = self.padding
        x2 = self.padding + scaled[0].width + self.spacing

        # Paste screenshots
        canvas.paste(scaled[0], (x1, y_positions[0]))
        canvas.paste(scaled[1], (x2, y_positions[1]))

        return canvas


class DuoVerticalLayout(BaseLayout):
    """Layout for two screenshots stacked vertically."""

    def __init__(
        self,
        width: int,
        height: int,
        background_color: tuple[int, int, int] = (255, 255, 255),
        spacing: int = 20,
        padding: int = 40,
    ):
        """Initialize vertical duo layout.

        Args:
            width: Canvas width
            height: Canvas height
            background_color: Background color as RGB tuple
            spacing: Space between screenshots (default: 20px)
            padding: Padding around screenshots (default: 40px)
        """
        super().__init__(width, height, background_color)
        self.spacing = spacing
        self.padding = padding

    def render(self, screenshots: list[Image.Image], **kwargs) -> Image.Image:
        """Render two screenshots stacked vertically.

        Args:
            screenshots: List containing two screenshots
            **kwargs: Ignored

        Returns:
            Rendered image

        Raises:
            ValueError: If screenshots list doesn't contain exactly two images
        """
        if len(screenshots) != 2:
            raise ValueError(
                f"DuoVerticalLayout requires exactly 2 screenshots, got {len(screenshots)}"
            )

        canvas = self.create_canvas()

        # Calculate available space for each screenshot
        available_width = self.width - 2 * self.padding
        available_height = (self.height - 2 * self.padding - self.spacing) // 2

        # Scale both screenshots to the same size
        scaled = [self._scale_to_fit(s, available_width, available_height) for s in screenshots]

        # Calculate positions (centered horizontally)
        x_positions = [(self.width - s.width) // 2 for s in scaled]
        y1 = self.padding
        y2 = self.padding + scaled[0].height + self.spacing

        # Paste screenshots
        canvas.paste(scaled[0], (x_positions[0], y1))
        canvas.paste(scaled[1], (x_positions[1], y2))

        return canvas
