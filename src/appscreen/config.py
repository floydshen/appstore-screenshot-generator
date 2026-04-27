"""Configuration models for AppStore Screenshot Generator using Pydantic."""

from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, Field, model_validator


class IconConfig(BaseModel):
    """Icon configuration for screenshots."""

    show: bool = Field(default=True, description="Whether to show the app icon")
    position: str = Field(default="top-right", description="Icon position on screenshot")
    size: int = Field(default=100, ge=10, le=500, description="Icon size in pixels")
    margin_x: int = Field(default=20, ge=0, description="Horizontal margin in pixels")
    margin_y: int = Field(default=20, ge=0, description="Vertical margin in pixels")
    shadow: bool = Field(default=True, description="Whether to add shadow to icon")
    x: Optional[int] = Field(default=None, description="Absolute X position (overrides position)")
    y: Optional[int] = Field(default=None, description="Absolute Y position (overrides position)")
    source: Optional[str] = Field(default=None, description="Path or URL to custom icon image")


class ShadowConfig(BaseModel):
    """Shadow configuration for screenshots."""

    enabled: bool = Field(default=True, description="Whether shadow is enabled")
    blur: int = Field(default=10, ge=0, le=100, description="Shadow blur radius")
    offset_x: int = Field(default=5, description="Shadow X offset")
    offset_y: int = Field(default=5, description="Shadow Y offset")
    opacity: float = Field(default=0.3, ge=0.0, le=1.0, description="Shadow opacity (0-1)")
    color: str = Field(default="#000000", description="Shadow color")


class LayoutConfig(BaseModel):
    """Layout configuration for screenshots."""

    type: str = Field(
        default="single", description="Layout type (single, duo, grid, fan, perspective, etc.)"
    )
    spacing: int = Field(default=20, ge=0, le=200, description="Spacing between devices in pixels")
    align: str = Field(default="center", description="Alignment (left, center, right)")
    angle: float = Field(default=0.0, ge=-180.0, le=180.0, description="Rotation angle in degrees")
    radius: int = Field(default=40, ge=0, le=200, description="Corner radius for devices")
    direction: str = Field(
        default="horizontal", description="Layout direction (horizontal, vertical)"
    )
    skew_x: float = Field(default=0.0, ge=-45.0, le=45.0, description="X-axis skew angle")
    skew_y: float = Field(default=0.0, ge=-45.0, le=45.0, description="Y-axis skew angle")
    shadow: Optional[ShadowConfig] = Field(default=None, description="Device shadow configuration")


class ScreenshotConfig(BaseModel):
    """Screenshot configuration."""

    file: Optional[str] = Field(default=None, description="Single screenshot file path")
    files: Optional[List[str]] = Field(default=None, description="Multiple screenshot file paths")
    caption: Optional[str] = Field(default=None, description="Caption text for the screenshot")
    layout: Optional[LayoutConfig] = Field(
        default=None, description="Layout configuration for this screenshot"
    )
    icon: Optional[IconConfig] = Field(
        default=None, description="Icon configuration for this screenshot"
    )

    @model_validator(mode="after")
    def validate_file_or_files(self) -> "ScreenshotConfig":
        """Ensure either file or files is provided, but not both."""
        if self.file is None and self.files is None:
            raise ValueError("Screenshot must have either 'file' or 'files' specified")
        if self.file is not None and self.files is not None:
            raise ValueError("Screenshot cannot have both 'file' and 'files'; use one or the other")
        return self

    def get_files(self) -> List[str]:
        """Get list of files for this screenshot."""
        if self.file:
            return [self.file]
        return self.files or []


class FontConfig(BaseModel):
    """Font configuration."""

    family: str = Field(default="SF Pro Display", description="Font family name")
    size: int = Field(default=60, ge=8, le=200, description="Font size in points")
    color: str = Field(default="#FFFFFF", description="Font color (hex)")
    weight: str = Field(default="bold", description="Font weight")
    style: str = Field(default="normal", description="Font style (normal, italic)")


class TextPositionConfig(BaseModel):
    """Text position configuration."""

    x: Optional[int] = Field(default=None, description="X position (None for auto)")
    y: Optional[int] = Field(default=None, description="Y position (None for auto)")
    align: str = Field(default="center", description="Text alignment (left, center, right)")
    vertical_align: str = Field(
        default="top", description="Vertical alignment (top, center, bottom)"
    )


class FrameConfig(BaseModel):
    """Device frame configuration."""

    show: bool = Field(default=True, description="Whether to show device frame")
    device: str = Field(default="iphone-15-pro", description="Device type for frame")
    color: str = Field(default="natural", description="Frame color")
    scale: float = Field(default=1.0, ge=0.1, le=2.0, description="Frame scale factor")


class BackgroundConfig(BaseModel):
    """Background configuration."""

    type: str = Field(default="gradient", description="Background type (solid, gradient, image)")
    color: Optional[str] = Field(default=None, description="Solid background color")
    gradient: Optional[List[str]] = Field(
        default_factory=lambda: ["#667eea", "#764ba2"],
        description="Gradient colors (list of hex colors)",
    )
    gradient_direction: str = Field(
        default="vertical", description="Gradient direction (vertical, horizontal, diagonal)"
    )
    image: Optional[str] = Field(default=None, description="Background image path or URL")
    opacity: float = Field(default=1.0, ge=0.0, le=1.0, description="Background opacity")

    @model_validator(mode="after")
    def validate_background(self) -> "BackgroundConfig":
        """Validate background configuration based on type."""
        if self.type == "solid" and not self.color:
            raise ValueError("Solid background requires 'color' field")
        if self.type == "image" and not self.image:
            raise ValueError("Image background requires 'image' field")
        # Gradient is optional - has default value
        return self


class ThemeConfig(BaseModel):
    """Theme configuration."""

    name: str = Field(default="default", description="Theme name")
    background: BackgroundConfig = Field(
        default_factory=BackgroundConfig, description="Background configuration"
    )
    font: FontConfig = Field(default_factory=FontConfig, description="Font configuration")
    text_position: TextPositionConfig = Field(
        default_factory=TextPositionConfig, description="Text position"
    )
    text_padding: int = Field(default=40, ge=0, le=200, description="Text padding in pixels")
    frame: FrameConfig = Field(
        default_factory=FrameConfig, description="Device frame configuration"
    )


class OutputConfig(BaseModel):
    """Output configuration."""

    fastlane_compatible: bool = Field(
        default=True, description="Output in fastlane-compatible format"
    )
    output_dir: str = Field(default="./fastlane/metadata", description="Output directory")
    locale_mapping: Dict[str, str] = Field(
        default_factory=lambda: {
            "en-US": "en-US",
            "zh-Hans": "zh-Hans",
            "zh-Hant": "zh-Hant",
            "ja": "ja",
            "ko": "ko",
        },
        description="Locale code mapping",
    )
    filename_template: str = Field(
        default="{device}_{index}.{ext}",
        description="Filename template for output files",
    )


class AppConfig(BaseModel):
    """App configuration."""

    name: str = Field(..., description="App name")
    bundle_id: str = Field(..., description="App bundle identifier")
    version: Optional[str] = Field(default=None, description="App version")
    icon: Optional[str] = Field(default=None, description="Path to app icon")


class Config(BaseModel):
    """Root configuration model."""

    app: AppConfig = Field(..., description="App configuration")
    screenshots: List[ScreenshotConfig] = Field(
        default_factory=list, description="List of screenshot configurations"
    )
    devices: List[str] = Field(
        default_factory=lambda: [
            "iphone-65",
            "iphone-67",
            "ipad-pro-13",
        ],
        description="List of target devices",
    )
    theme: ThemeConfig = Field(default_factory=ThemeConfig, description="Theme configuration")
    output: OutputConfig = Field(default_factory=OutputConfig, description="Output configuration")

    @classmethod
    def from_yaml(cls, path: Union[str, Path]) -> "Config":
        """Load configuration from YAML file.

        Args:
            path: Path to YAML configuration file

        Returns:
            Config instance

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the YAML is invalid
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if data is None:
            raise ValueError(f"Empty configuration file: {path}")

        return cls.model_validate(data)

    def to_yaml(self, path: Union[str, Path]) -> None:
        """Save configuration to YAML file.

        Args:
            path: Path to output YAML file
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(
                self.model_dump(mode="json", exclude_none=True),
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )


def load_config(config_path: Union[str, Path]) -> Config:
    """Load configuration from file.

    This is a convenience function that wraps Config.from_yaml().

    Args:
        config_path: Path to configuration file

    Returns:
        Config instance
    """
    return Config.from_yaml(config_path)
