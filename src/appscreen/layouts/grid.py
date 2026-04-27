"""Grid layout for multiple screenshots."""

from PIL import Image

from .base import BaseLayout


class Grid2x2Layout(BaseLayout):
    """Layout for four screenshots in a 2x2 grid."""

    def __init__(
        self,
        width: int,
        height: int,
        background_color: tuple[int, int, int] = (255, 255, 255),
        spacing: int = 20,
        padding: int = 40,
    ):
        """Initialize 2x2 grid layout.

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
        """Render four screenshots in a 2x2 grid.

        Args:
            screenshots: List containing four screenshots
            **kwargs: Ignored

        Returns:
            Rendered image

        Raises:
            ValueError: If screenshots list doesn't contain exactly four images
        """
        if len(screenshots) != 4:
            raise ValueError(f"Grid2x2Layout requires exactly 4 screenshots, got {len(screenshots)}")

        canvas = self.create_canvas()

        # Calculate available space for each cell
        available_width = (self.width - 2 * self.padding - self.spacing) // 2
        available_height = (self.height - 2 * self.padding - self.spacing) // 2

        # Scale all screenshots to the same size
        scaled = [self._scale_to_fit(s, available_width, available_height) for s in screenshots]

        # Calculate positions for each cell
        # Grid layout:
        # [0] [1]
        # [2] [3]
        positions = [
            # Top-left
            (
                self.padding + (available_width - scaled[0].width) // 2,
                self.padding + (available_height - scaled[0].height) // 2,
            ),
            # Top-right
            (
                self.padding + available_width + self.spacing + (available_width - scaled[1].width) // 2,
                self.padding + (available_height - scaled[1].height) // 2,
            ),
            # Bottom-left
            (
                self.padding + (available_width - scaled[2].width) // 2,
                self.padding + available_height + self.spacing + (available_height - scaled[2].height) // 2,
            ),
            # Bottom-right
            (
                self.padding + available_width + self.spacing + (available_width - scaled[3].width) // 2,
                self.padding + available_height + self.spacing + (available_height - scaled[3].height) // 2,
            ),
        ]

        # Paste screenshots
        for i, (img, pos) in enumerate(zip(scaled, positions)):
            canvas.paste(img, pos)

        return canvas
