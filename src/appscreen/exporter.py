"""Fastlane-compatible exporter for AppStore screenshots."""

from pathlib import Path
from typing import List, Tuple

from PIL import Image

from .config import Config
from .devices import get_device


class Exporter:
    """Export screenshots in Fastlane-compatible format."""

    def __init__(self, config: Config):
        """Initialize exporter with configuration.

        Args:
            config: Configuration object containing output settings
        """
        self.config = config
        self.output_dir = Path(config.output.output_dir)

    def export(
        self,
        image: Image.Image,
        device_name: str,
        index: int,
        locale: str,
    ) -> Path:
        """Export a single screenshot.

        Args:
            image: PIL Image to export
            device_name: Device name (e.g., "iphone-6.9")
            index: Screenshot index (1-based)
            locale: Locale code (e.g., "en", "zh", "zh-Hans")

        Returns:
            Path to the exported file
        """
        device = get_device(device_name)
        fastlane_locale = self.config.output.locale_mapping.get(locale, locale)

        # Create output directory
        output_path = self.output_dir / fastlane_locale
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate filename
        filename = f"{device.fastlane_name}-{index:02d}.png"
        filepath = output_path / filename

        # Resize if needed
        if image.size != (device.width, device.height):
            image = image.resize((device.width, device.height), Image.Resampling.LANCZOS)

        image.save(filepath, "PNG")
        return filepath

    def export_all(
        self,
        images: List[Tuple[Image.Image, str, int, str]],
    ) -> List[Path]:
        """Export multiple screenshots.

        Args:
            images: List of tuples (image, device_name, index, locale)

        Returns:
            List of paths to exported files
        """
        return [self.export(img, dev, idx, loc) for img, dev, idx, loc in images]
