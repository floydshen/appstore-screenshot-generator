"""Frame manager for applying device frames to screenshots."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFilter


@dataclass
class FrameConfig:
    """Configuration for a device frame.

    Defines the screen region where the screenshot should be placed
    within the device frame image.
    """

    name: str
    screen_x: int
    screen_y: int
    screen_width: int
    screen_height: int
    frame_path: str


# Predefined frame configurations
# These define where the screen area is within each frame image
DEFAULT_FRAME_CONFIGS: dict[str, FrameConfig] = {
    "iphone-15-pro-max": FrameConfig(
        name="iphone-15-pro-max",
        screen_x=50,
        screen_y=50,
        screen_width=430,
        screen_height=932,
        frame_path="iphone-15-pro-max.png",
    ),
    "iphone-14-pro": FrameConfig(
        name="iphone-14-pro",
        screen_x=45,
        screen_y=45,
        screen_width=393,
        screen_height=852,
        frame_path="iphone-14-pro.png",
    ),
    "ipad-pro-13": FrameConfig(
        name="ipad-pro-13",
        screen_x=80,
        screen_y=80,
        screen_width=1024,
        screen_height=1366,
        frame_path="ipad-pro-13.png",
    ),
    "ipad-pro-11": FrameConfig(
        name="ipad-pro-11",
        screen_x=60,
        screen_y=60,
        screen_width=834,
        screen_height=1194,
        frame_path="ipad-pro-11.png",
    ),
}


class FrameManager:
    """Manages device frames and applies them to screenshots.

    The frame manager loads device frame images and composites
    screenshots into the screen area of the frames.
    """

    def __init__(self, frames_dir: Optional[Path] = None):
        """Initialize the frame manager.

        Args:
            frames_dir: Directory containing frame images.
                       Defaults to 'frames/' in project root.
        """
        if frames_dir is None:
            # Default to frames/ directory in project root
            self.frames_dir = Path(__file__).parent.parent.parent.parent / "frames"
        else:
            self.frames_dir = Path(frames_dir)

        self._frame_cache: dict[str, Image.Image] = {}
        self._configs = DEFAULT_FRAME_CONFIGS.copy()

    def register_frame(self, config: FrameConfig) -> None:
        """Register a custom frame configuration.

        Args:
            config: Frame configuration to register
        """
        self._configs[config.name] = config

    def get_frame_config(self, device_name: str) -> Optional[FrameConfig]:
        """Get frame configuration for a device.

        Args:
            device_name: Device/frame name

        Returns:
            FrameConfig if found, None otherwise
        """
        return self._configs.get(device_name)

    def get_frame(self, device_name: str) -> Optional[Image.Image]:
        """Load frame image for a device.

        Args:
            device_name: Device/frame name

        Returns:
            Frame image as PIL Image, or None if not found
        """
        if device_name in self._frame_cache:
            return self._frame_cache[device_name].copy()

        config = self._configs.get(device_name)
        if config is None:
            return None

        frame_path = self.frames_dir / config.frame_path
        if not frame_path.exists():
            return None

        frame = Image.open(frame_path).convert("RGBA")
        self._frame_cache[device_name] = frame
        return frame.copy()

    def apply_frame(
        self,
        screenshot: Image.Image,
        device_name: str,
        shadow: bool = True,
        shadow_offset: tuple[int, int] = (10, 10),
        shadow_blur: int = 20,
        shadow_opacity: int = 80,
    ) -> Image.Image:
        """Apply device frame to a screenshot.

        Args:
            screenshot: Screenshot image to frame
            device_name: Device/frame name
            shadow: Whether to add shadow effect
            shadow_offset: Shadow offset (x, y)
            shadow_blur: Shadow blur radius
            shadow_opacity: Shadow opacity (0-255)

        Returns:
            Framed screenshot as PIL Image

        Raises:
            ValueError: If frame not found for device
        """
        config = self._configs.get(device_name)
        if config is None:
            raise ValueError(f"No frame configuration found for '{device_name}'")

        frame = self.get_frame(device_name)
        if frame is None:
            raise ValueError(f"Frame image not found for '{device_name}'")

        # Resize screenshot to fit screen area
        screenshot_rgba = screenshot.convert("RGBA")
        resized_screenshot = screenshot_rgba.resize(
            (config.screen_width, config.screen_height),
            Image.Resampling.LANCZOS,
        )

        # Create output image (frame size)
        output = Image.new("RGBA", frame.size, (0, 0, 0, 0))

        # Add shadow if enabled
        if shadow:
            shadow_layer = self._create_shadow(
                config.screen_width,
                config.screen_height,
                shadow_offset,
                shadow_blur,
                shadow_opacity,
            )
            output.paste(shadow_layer, (config.screen_x, config.screen_y), shadow_layer)

        # Paste screenshot at screen position
        output.paste(resized_screenshot, (config.screen_x, config.screen_y), resized_screenshot)

        # Paste frame on top
        output.paste(frame, (0, 0), frame)

        return output

    def _create_shadow(
        self,
        width: int,
        height: int,
        offset: tuple[int, int],
        blur: int,
        opacity: int,
    ) -> Image.Image:
        """Create a shadow layer for the screen area.

        Args:
            width: Screen width
            height: Screen height
            offset: Shadow offset (x, y)
            blur: Blur radius
            opacity: Shadow opacity

        Returns:
            Shadow layer as PIL Image
        """
        # Create a slightly larger image for shadow
        shadow_size = (width + offset[0] + blur * 2, height + offset[1] + blur * 2)
        shadow = Image.new("RGBA", shadow_size, (0, 0, 0, 0))

        # Draw black rectangle for shadow
        draw = ImageDraw.Draw(shadow)
        draw.rectangle(
            [blur, blur, blur + width, blur + height],
            fill=(0, 0, 0, opacity),
        )

        # Apply blur
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur))

        # Crop to original size with offset
        final_shadow = Image.new("RGBA", (width + abs(offset[0]), height + abs(offset[1])), (0, 0, 0, 0))
        paste_x = max(0, -offset[0])
        paste_y = max(0, -offset[1])
        final_shadow.paste(shadow, (paste_x, paste_y))

        return final_shadow

    def list_available_frames(self) -> list[str]:
        """List all available frame names.

        Returns:
            List of frame names that have both config and image file
        """
        available = []
        for name, config in self._configs.items():
            frame_path = self.frames_dir / config.frame_path
            if frame_path.exists():
                available.append(name)
        return sorted(available)

    def list_registered_frames(self) -> list[str]:
        """List all registered frame names (may not have image files).

        Returns:
            List of all registered frame names
        """
        return sorted(self._configs.keys())
