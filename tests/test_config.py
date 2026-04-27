"""Tests for configuration parsing and validation."""

import tempfile

import pytest

from appscreen.config import (
    AppConfig,
    BackgroundConfig,
    Config,
    FontConfig,
    FrameConfig,
    IconConfig,
    LayoutConfig,
    OutputConfig,
    ScreenshotConfig,
    ShadowConfig,
    ThemeConfig,
    load_config,
)


class TestIconConfig:
    """Tests for IconConfig."""

    def test_default_values(self):
        """Test default icon configuration values."""
        icon = IconConfig()
        assert icon.show is True
        assert icon.position == "top-right"
        assert icon.size == 100
        assert icon.margin_x == 20
        assert icon.margin_y == 20
        assert icon.shadow is True
        assert icon.x is None
        assert icon.y is None
        assert icon.source is None

    def test_custom_values(self):
        """Test custom icon configuration values."""
        icon = IconConfig(show=False, size=150, position="bottom-left", x=100, y=200)
        assert icon.show is False
        assert icon.size == 150
        assert icon.position == "bottom-left"
        assert icon.x == 100
        assert icon.y == 200

    def test_size_validation(self):
        """Test icon size validation."""
        with pytest.raises(Exception):  # ValidationError
            IconConfig(size=5)  # Below minimum

        with pytest.raises(Exception):  # ValidationError
            IconConfig(size=600)  # Above maximum


class TestLayoutConfig:
    """Tests for LayoutConfig."""

    def test_default_values(self):
        """Test default layout configuration values."""
        layout = LayoutConfig()
        assert layout.type == "single"
        assert layout.spacing == 20
        assert layout.align == "center"
        assert layout.angle == 0.0
        assert layout.radius == 40
        assert layout.direction == "horizontal"
        assert layout.skew_x == 0.0
        assert layout.skew_y == 0.0
        assert layout.shadow is None

    def test_with_shadow(self):
        """Test layout with shadow configuration."""
        shadow = ShadowConfig(enabled=True, blur=15, opacity=0.5)
        layout = LayoutConfig(type="duo", shadow=shadow)
        assert layout.shadow is not None
        assert layout.shadow.blur == 15
        assert layout.shadow.opacity == 0.5


class TestScreenshotConfig:
    """Tests for ScreenshotConfig."""

    def test_single_file(self):
        """Test screenshot with single file."""
        screenshot = ScreenshotConfig(file="screenshot1.png")
        assert screenshot.file == "screenshot1.png"
        assert screenshot.files is None
        assert screenshot.get_files() == ["screenshot1.png"]

    def test_multiple_files(self):
        """Test screenshot with multiple files."""
        screenshot = ScreenshotConfig(files=["screenshot1.png", "screenshot2.png"])
        assert screenshot.file is None
        assert len(screenshot.files) == 2
        assert len(screenshot.get_files()) == 2

    def test_must_have_file_or_files(self):
        """Test that screenshot must have file or files."""
        with pytest.raises(Exception, match="must have either 'file' or 'files'"):
            ScreenshotConfig()

    def test_cannot_have_both_file_and_files(self):
        """Test that screenshot cannot have both file and files."""
        with pytest.raises(Exception, match="cannot have both"):
            ScreenshotConfig(file="single.png", files=["multi1.png", "multi2.png"])

    def test_with_caption(self):
        """Test screenshot with caption."""
        screenshot = ScreenshotConfig(file="screenshot.png", caption="Amazing Feature")
        assert screenshot.caption == "Amazing Feature"


class TestBackgroundConfig:
    """Tests for BackgroundConfig."""

    def test_solid_background(self):
        """Test solid background configuration."""
        bg = BackgroundConfig(type="solid", color="#FF0000")
        assert bg.type == "solid"
        assert bg.color == "#FF0000"

    def test_gradient_background(self):
        """Test gradient background configuration."""
        bg = BackgroundConfig(type="gradient", gradient=["#FF0000", "#0000FF"])
        assert bg.type == "gradient"
        assert len(bg.gradient) == 2

    def test_image_background(self):
        """Test image background configuration."""
        bg = BackgroundConfig(type="image", image="background.png")
        assert bg.type == "image"
        assert bg.image == "background.png"

    def test_solid_requires_color(self):
        """Test that solid background requires color."""
        with pytest.raises(Exception, match="requires 'color'"):
            BackgroundConfig(type="solid")

    # Gradient has default value, so no validation error expected
    # If someone wants to clear gradient, they need to change type

    def test_image_requires_image(self):
        """Test that image background requires image path."""
        with pytest.raises(Exception, match="requires 'image'"):
            BackgroundConfig(type="image")


class TestThemeConfig:
    """Tests for ThemeConfig."""

    def test_default_values(self):
        """Test default theme configuration values."""
        theme = ThemeConfig()
        assert theme.name == "default"
        assert theme.text_padding == 40
        assert isinstance(theme.background, BackgroundConfig)
        assert isinstance(theme.font, FontConfig)
        assert isinstance(theme.frame, FrameConfig)

    def test_custom_theme(self):
        """Test custom theme configuration."""
        theme = ThemeConfig(
            name="dark",
            background=BackgroundConfig(type="solid", color="#000000"),
            font=FontConfig(family="SF Pro Display", size=80, color="#FFFFFF"),
        )
        assert theme.name == "dark"
        assert theme.background.color == "#000000"
        assert theme.font.size == 80


class TestOutputConfig:
    """Tests for OutputConfig."""

    def test_default_values(self):
        """Test default output configuration values."""
        output = OutputConfig()
        assert output.fastlane_compatible is True
        assert output.output_dir == "./fastlane/metadata"
        assert "en-US" in output.locale_mapping

    def test_custom_locale_mapping(self):
        """Test custom locale mapping."""
        output = OutputConfig(
            locale_mapping={
                "en-US": "en-US",
                "zh-Hans": "zh-Hans",
            }
        )
        assert len(output.locale_mapping) == 2


class TestAppConfig:
    """Tests for AppConfig."""

    def test_required_fields(self):
        """Test that app name and bundle_id are required."""
        with pytest.raises(Exception):
            AppConfig()

        app = AppConfig(name="MyApp", bundle_id="com.example.myapp")
        assert app.name == "MyApp"
        assert app.bundle_id == "com.example.myapp"

    def test_optional_fields(self):
        """Test optional app configuration fields."""
        app = AppConfig(
            name="MyApp", bundle_id="com.example.myapp", version="1.0.0", icon="icon.png"
        )
        assert app.version == "1.0.0"
        assert app.icon == "icon.png"


class TestConfig:
    """Tests for root Config model."""

    def test_minimal_config(self):
        """Test minimal valid configuration."""
        config = Config(
            app=AppConfig(name="MyApp", bundle_id="com.example.myapp"),
        )
        assert config.app.name == "MyApp"
        assert len(config.devices) == 3  # Default devices
        assert isinstance(config.theme, ThemeConfig)
        assert isinstance(config.output, OutputConfig)

    def test_default_devices(self):
        """Test default device list."""
        config = Config(
            app=AppConfig(name="MyApp", bundle_id="com.example.myapp"),
        )
        assert "iphone-65" in config.devices
        assert "iphone-67" in config.devices
        assert "ipad-pro-13" in config.devices

    def test_custom_devices(self):
        """Test custom device list."""
        config = Config(
            app=AppConfig(name="MyApp", bundle_id="com.example.myapp"),
            devices=["iphone-67", "ipad-pro-13"],
        )
        assert len(config.devices) == 2
        assert "iphone-67" in config.devices

    def test_with_screenshots(self):
        """Test configuration with screenshots."""
        config = Config(
            app=AppConfig(name="MyApp", bundle_id="com.example.myapp"),
            screenshots=[
                ScreenshotConfig(file="screen1.png", caption="Feature 1"),
                ScreenshotConfig(files=["screen2.png", "screen3.png"], caption="Feature 2"),
            ],
        )
        assert len(config.screenshots) == 2
        assert config.screenshots[0].caption == "Feature 1"

    def test_from_yaml(self):
        """Test loading configuration from YAML file."""
        yaml_content = """
app:
  name: MyApp
  bundle_id: com.example.myapp
  version: 1.0.0

screenshots:
  - file: screenshot1.png
    caption: Main Feature
  - files:
      - screenshot2.png
      - screenshot3.png
    caption: Gallery View

devices:
  - iphone-67
  - ipad-pro-13

theme:
  name: dark
  background:
    type: solid
    color: "#000000"
  font:
    size: 80
    color: "#FFFFFF"

output:
  output_dir: ./output
  fastlane_compatible: true
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()
            config = Config.from_yaml(f.name)

        assert config.app.name == "MyApp"
        assert config.app.version == "1.0.0"
        assert len(config.screenshots) == 2
        assert len(config.devices) == 2
        assert config.theme.name == "dark"
        assert config.output.output_dir == "./output"

    def test_from_yaml_file_not_found(self):
        """Test error when YAML file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            Config.from_yaml("/nonexistent/path/config.yaml")

    def test_to_yaml(self):
        """Test saving configuration to YAML file."""
        config = Config(
            app=AppConfig(name="MyApp", bundle_id="com.example.myapp"),
            screenshots=[ScreenshotConfig(file="screen.png")],
        )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            config.to_yaml(f.name)

            # Load it back
            loaded = Config.from_yaml(f.name)
            assert loaded.app.name == "MyApp"
            assert len(loaded.screenshots) == 1

    def test_load_config_function(self):
        """Test the load_config convenience function."""
        yaml_content = """
app:
  name: TestApp
  bundle_id: com.test.app
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()
            config = load_config(f.name)

        assert config.app.name == "TestApp"


class TestYAMLIntegration:
    """Integration tests for YAML loading."""

    def test_complete_config_yaml(self):
        """Test loading a complete configuration from YAML."""
        yaml_content = """
app:
  name: MyApp
  bundle_id: com.example.myapp
  version: 2.0.0
  icon: assets/icon.png

screenshots:
  - file: screenshots/home.png
    caption: Welcome Screen
    layout:
      type: single
      shadow:
        enabled: true
        blur: 20
        opacity: 0.4
    icon:
      show: true
      position: top-right
      size: 120

  - files:
      - screenshots/feature1.png
      - screenshots/feature2.png
      - screenshots/feature3.png
    caption: Key Features
    layout:
      type: grid
      spacing: 30
      direction: horizontal

devices:
  - iphone-65
  - iphone-67

theme:
  name: premium
  background:
    type: gradient
    gradient:
      - "#667eea"
      - "#764ba2"
    gradient_direction: diagonal
  font:
    family: SF Pro Display
    size: 70
    color: "#FFFFFF"
    weight: bold
  text_position:
    align: center
    vertical_align: top
  text_padding: 50
  frame:
    show: true
    device: iphone-15-pro
    color: natural
    scale: 1.0

output:
  fastlane_compatible: true
  output_dir: ./fastlane/metadata
  locale_mapping:
    en-US: en-US
    zh-Hans: zh-Hans
  filename_template: "{device}_{index}.{ext}"
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()
            config = Config.from_yaml(f.name)

        # Verify all parts loaded correctly
        assert config.app.name == "MyApp"
        assert config.app.icon == "assets/icon.png"

        assert len(config.screenshots) == 2
        assert config.screenshots[0].layout.type == "single"
        assert config.screenshots[0].layout.shadow.blur == 20
        assert config.screenshots[0].icon.size == 120

        assert config.screenshots[1].layout.type == "grid"
        assert len(config.screenshots[1].get_files()) == 3

        assert config.theme.name == "premium"
        assert config.theme.background.type == "gradient"
        assert len(config.theme.background.gradient) == 2

        assert config.output.fastlane_compatible is True
        assert len(config.output.locale_mapping) == 2
