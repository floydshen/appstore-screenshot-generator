"""Tests for layout system."""

import pytest
from PIL import Image

from appscreen.layouts import (
    BaseLayout,
    DuoHorizontalLayout,
    DuoVerticalLayout,
    FanLayout,
    Grid2x2Layout,
    PerspectiveLayout,
    SingleLayout,
    Stack3DLayout,
    TripleRowLayout,
    get_layout,
)


@pytest.fixture
def sample_screenshot():
    """Create a sample screenshot image."""
    return Image.new('RGB', (400, 800), color='blue')


@pytest.fixture
def sample_screenshots(sample_screenshot):
    """Create multiple sample screenshots."""
    colors = ['red', 'green', 'blue', 'yellow']
    return [Image.new('RGB', (400, 800), color=c) for c in colors]


class TestSingleLayout:
    """Tests for SingleLayout."""

    def test_render_single_screenshot(self, sample_screenshot):
        """Test rendering a single screenshot."""
        layout = SingleLayout(width=1200, height=1600)
        result = layout.render([sample_screenshot])

        assert result.size == (1200, 1600)
        assert result.mode == 'RGB'

    def test_render_scales_large_screenshot(self):
        """Test that large screenshots are scaled down."""
        large_screenshot = Image.new('RGB', (2000, 4000), color='blue')
        layout = SingleLayout(width=1200, height=1600, padding=40)
        result = layout.render([large_screenshot])

        # Image should be scaled to fit within canvas
        # The result should still have the canvas size
        assert result.size == (1200, 1600)

    def test_render_empty_screenshots_raises_error(self):
        """Test that empty screenshots list raises error."""
        layout = SingleLayout(width=1200, height=1600)
        with pytest.raises(ValueError, match="at least one screenshot"):
            layout.render([])

    def test_custom_background_color(self):
        """Test custom background color."""
        layout = SingleLayout(width=1200, height=1600, background_color=(255, 0, 0))
        screenshot = Image.new('RGB', (100, 200), color='blue')
        result = layout.render([screenshot])

        # Check that background color appears in corners
        assert result.getpixel((0, 0)) == (255, 0, 0)

    def test_custom_padding(self):
        """Test custom padding."""
        layout = SingleLayout(width=1200, height=1600, padding=100)
        screenshot = Image.new('RGB', (400, 800), color='blue')
        result = layout.render([screenshot])

        assert result.size == (1200, 1600)


class TestDuoHorizontalLayout:
    """Tests for DuoHorizontalLayout."""

    def test_render_two_screenshots(self, sample_screenshots):
        """Test rendering two screenshots side by side."""
        layout = DuoHorizontalLayout(width=1600, height=1200)
        result = layout.render(sample_screenshots[:2])

        assert result.size == (1600, 1200)
        assert result.mode == 'RGB'

    def test_require_exactly_two_screenshots(self, sample_screenshots):
        """Test that exactly two screenshots are required."""
        layout = DuoHorizontalLayout(width=1600, height=1200)

        with pytest.raises(ValueError, match="exactly 2 screenshots"):
            layout.render([sample_screenshots[0]])

        with pytest.raises(ValueError, match="exactly 2 screenshots"):
            layout.render(sample_screenshots)

    def test_custom_spacing(self, sample_screenshots):
        """Test custom spacing between screenshots."""
        layout = DuoHorizontalLayout(width=1600, height=1200, spacing=40)
        result = layout.render(sample_screenshots[:2])

        assert result.size == (1600, 1200)


class TestDuoVerticalLayout:
    """Tests for DuoVerticalLayout."""

    def test_render_two_screenshots(self, sample_screenshots):
        """Test rendering two screenshots stacked vertically."""
        layout = DuoVerticalLayout(width=1200, height=1600)
        result = layout.render(sample_screenshots[:2])

        assert result.size == (1200, 1600)
        assert result.mode == 'RGB'

    def test_require_exactly_two_screenshots(self, sample_screenshots):
        """Test that exactly two screenshots are required."""
        layout = DuoVerticalLayout(width=1200, height=1600)

        with pytest.raises(ValueError, match="exactly 2 screenshots"):
            layout.render([sample_screenshots[0]])


class TestGrid2x2Layout:
    """Tests for Grid2x2Layout."""

    def test_render_four_screenshots(self, sample_screenshots):
        """Test rendering four screenshots in a grid."""
        layout = Grid2x2Layout(width=1600, height=1600)
        result = layout.render(sample_screenshots)

        assert result.size == (1600, 1600)
        assert result.mode == 'RGB'

    def test_require_exactly_four_screenshots(self, sample_screenshots):
        """Test that exactly four screenshots are required."""
        layout = Grid2x2Layout(width=1600, height=1600)

        with pytest.raises(ValueError, match="exactly 4 screenshots"):
            layout.render(sample_screenshots[:2])

    def test_custom_spacing(self, sample_screenshots):
        """Test custom spacing in grid."""
        layout = Grid2x2Layout(width=1600, height=1600, spacing=30)
        result = layout.render(sample_screenshots)

        assert result.size == (1600, 1600)


class TestGetLayout:
    """Tests for get_layout factory function."""

    def test_get_single_layout(self):
        """Test getting single layout."""
        layout = get_layout("single", width=1200, height=1600)
        assert isinstance(layout, SingleLayout)
        assert layout.width == 1200
        assert layout.height == 1600

    def test_get_duo_horizontal_layout(self):
        """Test getting duo-horizontal layout."""
        layout = get_layout("duo-horizontal", width=1600, height=1200)
        assert isinstance(layout, DuoHorizontalLayout)

    def test_get_duo_vertical_layout(self):
        """Test getting duo-vertical layout."""
        layout = get_layout("duo-vertical", width=1200, height=1600)
        assert isinstance(layout, DuoVerticalLayout)

    def test_get_grid_2x2_layout(self):
        """Test getting grid-2x2 layout."""
        layout = get_layout("grid-2x2", width=1600, height=1600)
        assert isinstance(layout, Grid2x2Layout)

    def test_get_fan_layout(self):
        """Test getting fan layout."""
        layout = get_layout("fan", width=1600, height=1200)
        assert isinstance(layout, FanLayout)

    def test_get_perspective_layout(self):
        """Test getting perspective layout."""
        layout = get_layout("perspective", width=1200, height=1600)
        assert isinstance(layout, PerspectiveLayout)

    def test_get_stack_3d_layout(self):
        """Test getting stack-3d layout."""
        layout = get_layout("stack-3d", width=1600, height=1200)
        assert isinstance(layout, Stack3DLayout)

    def test_get_triple_row_layout(self):
        """Test getting triple-row layout."""
        layout = get_layout("triple-row", width=1800, height=1200)
        assert isinstance(layout, TripleRowLayout)

    def test_unknown_layout_raises_error(self):
        """Test that unknown layout name raises error."""
        with pytest.raises(ValueError) as exc_info:
            get_layout("unknown", width=1200, height=1600)

        assert "Unknown layout 'unknown'" in str(exc_info.value)
        assert "Available layouts:" in str(exc_info.value)

    def test_passes_kwargs_to_layout(self):
        """Test that kwargs are passed to layout constructor."""
        layout = get_layout(
            "single",
            width=1200,
            height=1600,
            background_color=(128, 128, 128),
            padding=100,
        )
        assert layout.background_color == (128, 128, 128)
        assert layout.padding == 100


class TestFanLayout:
    """Tests for FanLayout."""

    def test_render_multiple_screenshots(self, sample_screenshots):
        """Test rendering multiple screenshots in fan pattern."""
        layout = FanLayout(width=1600, height=1200)
        result = layout.render(sample_screenshots[:3])

        assert result.size == (1600, 1200)
        assert result.mode == 'RGB'

    def test_render_single_screenshot(self, sample_screenshot):
        """Test rendering a single screenshot."""
        layout = FanLayout(width=1200, height=1600)
        result = layout.render([sample_screenshot])

        assert result.size == (1200, 1600)

    def test_render_empty_screenshots_raises_error(self):
        """Test that empty screenshots list raises error."""
        layout = FanLayout(width=1200, height=1600)
        with pytest.raises(ValueError, match="at least one screenshot"):
            layout.render([])

    def test_custom_angle_and_radius(self, sample_screenshots):
        """Test custom angle and radius parameters."""
        layout = FanLayout(width=1600, height=1200, angle=45, radius=150)
        result = layout.render(sample_screenshots[:3])

        assert result.size == (1600, 1200)

    def test_different_directions(self, sample_screenshots):
        """Test different fan directions."""
        for direction in ['up', 'down', 'left', 'right']:
            layout = FanLayout(width=1600, height=1200, direction=direction)
            result = layout.render(sample_screenshots[:3])

            assert result.size == (1600, 1200)


class TestPerspectiveLayout:
    """Tests for PerspectiveLayout."""

    def test_render_single_screenshot(self, sample_screenshot):
        """Test rendering a screenshot with perspective effect."""
        layout = PerspectiveLayout(width=1200, height=1600)
        result = layout.render([sample_screenshot])

        assert result.size == (1200, 1600)
        assert result.mode == 'RGB'

    def test_render_empty_screenshots_raises_error(self):
        """Test that empty screenshots list raises error."""
        layout = PerspectiveLayout(width=1200, height=1600)
        with pytest.raises(ValueError, match="at least one screenshot"):
            layout.render([])

    def test_custom_skew_parameters(self, sample_screenshot):
        """Test custom skew parameters."""
        layout = PerspectiveLayout(width=1200, height=1600, skew_x=0.1, skew_y=0.2)
        result = layout.render([sample_screenshot])

        assert result.size == (1200, 1600)

    def test_shadow_disabled(self, sample_screenshot):
        """Test rendering without shadow."""
        layout = PerspectiveLayout(width=1200, height=1600, shadow=False)
        result = layout.render([sample_screenshot])

        assert result.size == (1200, 1600)


class TestStack3DLayout:
    """Tests for Stack3DLayout."""

    def test_render_multiple_screenshots(self, sample_screenshots):
        """Test rendering multiple screenshots with 3D stack effect."""
        layout = Stack3DLayout(width=1600, height=1200)
        result = layout.render(sample_screenshots[:3])

        assert result.size == (1600, 1200)
        assert result.mode == 'RGB'

    def test_render_single_screenshot(self, sample_screenshot):
        """Test rendering a single screenshot."""
        layout = Stack3DLayout(width=1200, height=1600)
        result = layout.render([sample_screenshot])

        assert result.size == (1200, 1600)

    def test_render_empty_screenshots_raises_error(self):
        """Test that empty screenshots list raises error."""
        layout = Stack3DLayout(width=1200, height=1600)
        with pytest.raises(ValueError, match="at least one screenshot"):
            layout.render([])

    def test_custom_depth_and_rotation(self, sample_screenshots):
        """Test custom depth and rotation parameters."""
        layout = Stack3DLayout(width=1600, height=1200, depth=50, rotation=10)
        result = layout.render(sample_screenshots[:3])

        assert result.size == (1600, 1200)


class TestTripleRowLayout:
    """Tests for TripleRowLayout."""

    def test_render_three_screenshots(self, sample_screenshots):
        """Test rendering three screenshots side by side."""
        layout = TripleRowLayout(width=1800, height=1200)
        result = layout.render(sample_screenshots[:3])

        assert result.size == (1800, 1200)
        assert result.mode == 'RGB'

    def test_require_exactly_three_screenshots(self, sample_screenshots):
        """Test that exactly three screenshots are required."""
        layout = TripleRowLayout(width=1800, height=1200)

        with pytest.raises(ValueError, match="exactly 3 screenshots"):
            layout.render([sample_screenshots[0]])

        with pytest.raises(ValueError, match="exactly 3 screenshots"):
            layout.render(sample_screenshots)

    def test_custom_spacing(self, sample_screenshots):
        """Test custom spacing between screenshots."""
        layout = TripleRowLayout(width=1800, height=1200, spacing=40)
        result = layout.render(sample_screenshots[:3])

        assert result.size == (1800, 1200)


class TestBaseLayout:
    """Tests for BaseLayout abstract class."""

    def test_create_canvas(self):
        """Test canvas creation."""
        layout = SingleLayout(width=800, height=600)
        canvas = layout.create_canvas()

        assert canvas.size == (800, 600)
        assert canvas.mode == 'RGB'

    def test_scale_to_fit_smaller(self):
        """Test scaling down an image."""
        layout = SingleLayout(width=800, height=600)
        large_image = Image.new('RGB', (1600, 1200), color='red')

        scaled = layout._scale_to_fit(large_image, 400, 300)

        assert scaled.width <= 400
        assert scaled.height <= 300
        # Aspect ratio should be preserved
        assert abs(scaled.width / scaled.height - 4 / 3) < 0.01

    def test_scale_to_fit_no_scaling_needed(self):
        """Test that small images are not scaled up."""
        layout = SingleLayout(width=800, height=600)
        small_image = Image.new('RGB', (100, 100), color='blue')

        scaled = layout._scale_to_fit(small_image, 400, 400)

        # Should remain the same size (no upscaling)
        assert scaled.size == (100, 100)
