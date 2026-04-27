"""Frame layout for single screenshot with device frame."""

from typing import Optional

from PIL import Image

from .base import BaseLayout
from ..frames import FrameManager


class FrameSingleLayout(BaseLayout):
    """Layout for a single screenshot with device frame applied."""

    def __init__(
        self,
        width: int,
        height: int,
        background_color: tuple[int, int, int] = (255, 255, 255),
        device_name: str = "iphone-15-pro-max",
        shadow: bool = True,
        padding: int = 40,
        frames_dir: Optional[str] = None,
    ):
        """Initialize frame single layout.

        Args:
            width: Canvas width
            height: Canvas height
            background_color: Background color as RGB tuple
            device_name: Device frame to use
            shadow: Whether to apply shadow effect
            padding: Padding around the framed device
            frames_dir: Optional custom frames directory
        """
        super().__init__(width, height, background_color)
        self.device_name = device_name
        self.shadow = shadow
        self.padding = padding
        self.frame_manager = FrameManager(frames_dir)

    def render(self, screenshots: list[Image.Image], **kwargs) -> Image.Image:
        """Render a single screenshot with device frame.

        Args:
            screenshots: List containing one screenshot
            **kwargs: Optional overrides:
                - device_name: Override device frame
                - shadow: Override shadow setting

        Returns:
            Rendered image with device frame

        Raises:
            ValueError: If no screenshot provided or frame not found
        """
        if not screenshots:
            raise ValueError("FrameSingleLayout requires at least one screenshot")

        # Allow kwargs to override defaults
        device_name = kwargs.get("device_name", self.device_name)
        shadow = kwargs.get("shadow", self.shadow)

        # Take the first screenshot
        screenshot = screenshots[0]

        # Apply frame
        framed = self.frame_manager.apply_frame(
            screenshot,
            device_name,
            shadow=shadow,
        )

        # Create canvas
        canvas = self.create_canvas()

        # Calculate available space
        available_width = self.width - 2 * self.padding
        available_height = self.height - 2 * self.padding

        # Scale framed device to fit canvas
        scaled = self._scale_to_fit(framed, available_width, available_height)

        # Center on canvas
        x = (self.width - scaled.width) // 2
        y = (self.height - scaled.height) // 2

        # Convert to RGB for pasting onto canvas
        if scaled.mode == "RGBA":
            # Create a temporary RGB image for compositing
            temp = Image.new("RGB", scaled.size, self.background_color)
            temp.paste(scaled, (0, 0), scaled)
            scaled = temp

        canvas.paste(scaled, (x, y))

        return canvas
