"""Tests for theme system."""

import pytest
from PIL import Image

from appscreen.themes import Theme, PRESET_THEMES, get_theme


class TestGetTheme:
    """Test get_theme function."""

    def test_get_gradient_blue_theme(self):
        """Test getting gradient-blue theme."""
        theme = get_theme("gradient-blue")
        assert theme.name == "gradient-blue"
        assert theme.background_type == "gradient"
        assert theme.colors == ["#667eea", "#764ba2"]

    def test_get_solid_white_theme(self):
        """Test getting solid-white theme."""
        theme = get_theme("solid-white")
        assert theme.name == "solid-white"
        assert theme.background_type == "solid"
        assert theme.colors == ["#ffffff"]

    def test_get_unknown_theme_raises_error(self):
        """Test that getting unknown theme raises KeyError."""
        with pytest.raises(KeyError) as exc_info:
            get_theme("unknown-theme")

        assert "Unknown theme" in str(exc_info.value)
        assert "unknown-theme" in str(exc_info.value)


class TestThemeRenderGradient:
    """Test rendering gradient backgrounds."""

    def test_render_gradient_background(self):
        """Test rendering a gradient background."""
        theme = get_theme("gradient-blue")
        img = theme.render_background(100, 100)

        assert isinstance(img, Image.Image)
        assert img.size == (100, 100)
        assert img.mode == "RGB"

    def test_gradient_has_color_variation(self):
        """Test that gradient has color variation."""
        theme = get_theme("gradient-blue")
        img = theme.render_background(100, 100)

        # Get pixels at different positions
        top_left = img.getpixel((0, 0))
        bottom_right = img.getpixel((99, 99))

        # They should be different due to gradient
        assert top_left != bottom_right

    def test_gradient_horizontal_direction(self):
        """Test horizontal gradient direction."""
        theme = Theme(
            name="test-horizontal",
            background_type="gradient",
            colors=["#ff0000", "#0000ff"],
            direction="horizontal",
        )
        img = theme.render_background(100, 50)

        # Left side should be more red, right side more blue
        left_pixel = img.getpixel((0, 25))
        right_pixel = img.getpixel((99, 25))

        # Left should have more red
        assert left_pixel[0] > right_pixel[0]
        # Right should have more blue
        assert right_pixel[2] > left_pixel[2]

    def test_gradient_vertical_direction(self):
        """Test vertical gradient direction."""
        theme = Theme(
            name="test-vertical",
            background_type="gradient",
            colors=["#ff0000", "#0000ff"],
            direction="vertical",
        )
        img = theme.render_background(50, 100)

        # Top should be more red, bottom more blue
        top_pixel = img.getpixel((25, 0))
        bottom_pixel = img.getpixel((25, 99))

        # Top should have more red
        assert top_pixel[0] > bottom_pixel[0]
        # Bottom should have more blue
        assert bottom_pixel[2] > top_pixel[2]


class TestThemeRenderSolid:
    """Test rendering solid color backgrounds."""

    def test_render_solid_background(self):
        """Test rendering a solid color background."""
        theme = get_theme("solid-white")
        img = theme.render_background(100, 100)

        assert isinstance(img, Image.Image)
        assert img.size == (100, 100)
        assert img.mode == "RGB"

    def test_solid_white_is_uniform(self):
        """Test that solid white is uniform."""
        theme = get_theme("solid-white")
        img = theme.render_background(100, 100)

        # All pixels should be white
        for y in range(0, 100, 10):
            for x in range(0, 100, 10):
                assert img.getpixel((x, y)) == (255, 255, 255)

    def test_solid_black_is_uniform(self):
        """Test that solid black is uniform."""
        theme = get_theme("solid-black")
        img = theme.render_background(100, 100)

        # All pixels should be black
        for y in range(0, 100, 10):
            for x in range(0, 100, 10):
                assert img.getpixel((x, y)) == (0, 0, 0)


class TestHexToRGB:
    """Test hex to RGB conversion."""

    def test_hex_to_rgb_white(self):
        """Test converting white hex to RGB."""
        rgb = Theme._hex_to_rgb("#ffffff")
        assert rgb == (255, 255, 255)

    def test_hex_to_rgb_black(self):
        """Test converting black hex to RGB."""
        rgb = Theme._hex_to_rgb("#000000")
        assert rgb == (0, 0, 0)

    def test_hex_to_rgb_without_hash(self):
        """Test converting hex without hash prefix."""
        rgb = Theme._hex_to_rgb("667eea")
        assert rgb == (102, 126, 234)

    def test_hex_to_rgb_with_hash(self):
        """Test converting hex with hash prefix."""
        rgb = Theme._hex_to_rgb("#667eea")
        assert rgb == (102, 126, 234)


class TestPresetThemes:
    """Test preset themes configuration."""

    def test_all_preset_themes_exist(self):
        """Test that all expected preset themes exist."""
        expected_themes = [
            "gradient-blue",
            "gradient-purple",
            "gradient-sunset",
            "gradient-green",
            "gradient-dark",
            "solid-white",
            "solid-black",
        ]

        for theme_name in expected_themes:
            assert theme_name in PRESET_THEMES
            theme = PRESET_THEMES[theme_name]
            assert isinstance(theme, Theme)
            assert theme.name == theme_name

    def test_all_preset_themes_renderable(self):
        """Test that all preset themes can render backgrounds."""
        for theme_name, theme in PRESET_THEMES.items():
            img = theme.render_background(100, 100)
            assert isinstance(img, Image.Image)
            assert img.size == (100, 100)
