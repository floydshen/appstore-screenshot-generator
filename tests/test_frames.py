"""Tests for device frame system."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image

from appscreen.frames import FrameManager
from appscreen.frames.manager import FrameConfig


class TestFrameConfig:
    """Tests for FrameConfig dataclass."""

    def test_frame_config_creation(self):
        """Test creating a frame config."""
        config = FrameConfig(
            name="test-device",
            screen_x=50,
            screen_y=50,
            screen_width=400,
            screen_height=800,
            frame_path="test-device.png",
        )
        assert config.name == "test-device"
        assert config.screen_x == 50
        assert config.screen_y == 50
        assert config.screen_width == 400
        assert config.screen_height == 800
        assert config.frame_path == "test-device.png"


class TestFrameManager:
    """Tests for FrameManager class."""

    def test_init_default_frames_dir(self):
        """Test FrameManager initializes with default frames directory."""
        manager = FrameManager()
        assert manager.frames_dir.name == "frames"

    def test_init_custom_frames_dir(self):
        """Test FrameManager initializes with custom frames directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = FrameManager(frames_dir=Path(tmpdir))
            assert manager.frames_dir == Path(tmpdir)

    def test_list_registered_frames(self):
        """Test listing all registered frame names."""
        manager = FrameManager()
        frames = manager.list_registered_frames()
        assert "iphone-15-pro-max" in frames
        assert "iphone-14-pro" in frames
        assert "ipad-pro-13" in frames
        assert "ipad-pro-11" in frames

    def test_list_available_frames(self):
        """Test listing frames that have image files."""
        manager = FrameManager()
        frames = manager.list_available_frames()
        # Should include our placeholder frames
        assert "iphone-15-pro-max" in frames
        assert "iphone-14-pro" in frames
        assert "ipad-pro-13" in frames
        assert "ipad-pro-11" in frames

    def test_get_frame_config(self):
        """Test getting frame configuration."""
        manager = FrameManager()
        config = manager.get_frame_config("iphone-15-pro-max")
        assert config is not None
        assert config.name == "iphone-15-pro-max"
        assert config.screen_width == 430
        assert config.screen_height == 932

    def test_get_frame_config_unknown(self):
        """Test getting config for unknown device returns None."""
        manager = FrameManager()
        config = manager.get_frame_config("unknown-device")
        assert config is None

    def test_get_frame(self):
        """Test loading a frame image."""
        manager = FrameManager()
        frame = manager.get_frame("iphone-15-pro-max")
        assert frame is not None
        assert isinstance(frame, Image.Image)
        assert frame.mode == "RGBA"

    def test_get_frame_unknown(self):
        """Test getting unknown frame returns None."""
        manager = FrameManager()
        frame = manager.get_frame("unknown-device")
        assert frame is None

    def test_register_custom_frame(self):
        """Test registering a custom frame configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test frame image
            frame_path = Path(tmpdir) / "custom-frame.png"
            img = Image.new("RGBA", (500, 1000), (100, 100, 100, 255))
            img.save(frame_path)

            manager = FrameManager(frames_dir=Path(tmpdir))
            config = FrameConfig(
                name="custom-device",
                screen_x=50,
                screen_y=50,
                screen_width=400,
                screen_height=900,
                frame_path="custom-frame.png",
            )
            manager.register_frame(config)

            # Verify it's registered
            assert "custom-device" in manager.list_registered_frames()
            assert manager.get_frame_config("custom-device") == config

            # Verify we can load the frame
            frame = manager.get_frame("custom-device")
            assert frame is not None

    def test_apply_frame(self):
        """Test applying a frame to a screenshot."""
        manager = FrameManager()

        # Create a test screenshot
        screenshot = Image.new("RGB", (430, 932), (255, 0, 0))

        # Apply frame
        result = manager.apply_frame(screenshot, "iphone-15-pro-max", shadow=False)

        assert result is not None
        assert isinstance(result, Image.Image)
        assert result.mode == "RGBA"
        # Result should be frame-sized, not screenshot-sized
        config = manager.get_frame_config("iphone-15-pro-max")
        assert result.width > screenshot.width
        assert result.height > screenshot.height

    def test_apply_frame_with_shadow(self):
        """Test applying a frame with shadow effect."""
        manager = FrameManager()

        screenshot = Image.new("RGB", (430, 932), (0, 255, 0))

        # Apply frame with shadow
        result = manager.apply_frame(
            screenshot,
            "iphone-15-pro-max",
            shadow=True,
            shadow_offset=(10, 10),
            shadow_blur=20,
            shadow_opacity=80,
        )

        assert result is not None
        assert result.mode == "RGBA"

    def test_apply_frame_unknown_device_raises(self):
        """Test applying frame with unknown device raises ValueError."""
        manager = FrameManager()
        screenshot = Image.new("RGB", (400, 800), (255, 255, 255))

        with pytest.raises(ValueError, match="No frame configuration found"):
            manager.apply_frame(screenshot, "unknown-device")

    def test_apply_frame_missing_image_raises(self):
        """Test applying frame when image file is missing raises ValueError."""
        manager = FrameManager()

        # Register a config without creating the image file
        config = FrameConfig(
            name="missing-image",
            screen_x=50,
            screen_y=50,
            screen_width=400,
            screen_height=800,
            frame_path="nonexistent.png",
        )
        manager.register_frame(config)

        screenshot = Image.new("RGB", (400, 800), (255, 255, 255))

        with pytest.raises(ValueError, match="Frame image not found"):
            manager.apply_frame(screenshot, "missing-image")

    def test_frame_cache(self):
        """Test that frames are cached after first load."""
        manager = FrameManager()

        # First load
        frame1 = manager.get_frame("iphone-15-pro-max")
        assert "iphone-15-pro-max" in manager._frame_cache

        # Second load should use cache (returns a copy)
        frame2 = manager.get_frame("iphone-15-pro-max")

        # Images should be identical in content but different objects
        assert frame1 is not frame2
        assert frame1.size == frame2.size


class TestFrameManagerIntegration:
    """Integration tests for FrameManager."""

    def test_multiple_device_frames(self):
        """Test applying frames to multiple devices."""
        manager = FrameManager()
        devices = manager.list_available_frames()

        assert len(devices) >= 4, "Should have at least 4 device frames"

        for device in devices:
            config = manager.get_frame_config(device)
            screenshot = Image.new("RGB", (config.screen_width, config.screen_height), (100, 100, 100))

            result = manager.apply_frame(screenshot, device, shadow=False)
            assert result is not None, f"Failed to apply frame for {device}"

    def test_screenshot_resizing(self):
        """Test that screenshots are resized to fit frame screen area."""
        manager = FrameManager()

        # Create a screenshot that's larger than the screen area
        large_screenshot = Image.new("RGB", (1000, 2000), (255, 0, 0))

        result = manager.apply_frame(large_screenshot, "iphone-15-pro-max", shadow=False)

        # Should still produce a valid output
        assert result is not None
        config = manager.get_frame_config("iphone-15-pro-max")
        # Result dimensions should match frame size
        assert result.width > config.screen_width
        assert result.height > config.screen_height


class TestFrameSingleLayout:
    """Tests for FrameSingleLayout."""

    def test_layout_creation(self):
        """Test creating a frame single layout."""
        from appscreen.layouts import FrameSingleLayout

        layout = FrameSingleLayout(
            width=1200,
            height=1600,
            device_name="iphone-15-pro-max",
        )
        assert layout.width == 1200
        assert layout.height == 1600
        assert layout.device_name == "iphone-15-pro-max"

    def test_layout_render(self):
        """Test rendering a screenshot with frame layout."""
        from appscreen.layouts import FrameSingleLayout

        layout = FrameSingleLayout(
            width=1200,
            height=1600,
            device_name="iphone-15-pro-max",
            shadow=True,
        )

        screenshot = Image.new("RGB", (430, 932), (0, 128, 255))
        result = layout.render([screenshot])

        assert result is not None
        assert result.size == (1200, 1600)
        assert result.mode == "RGB"

    def test_layout_render_override_device(self):
        """Test overriding device name in render."""
        from appscreen.layouts import FrameSingleLayout

        layout = FrameSingleLayout(
            width=1500,
            height=2000,
            device_name="iphone-15-pro-max",
        )

        screenshot = Image.new("RGB", (393, 852), (255, 0, 0))
        # Override to use iPhone 14 Pro
        result = layout.render([screenshot], device_name="iphone-14-pro")

        assert result is not None
        assert result.size == (1500, 2000)

    def test_layout_no_screenshot_raises(self):
        """Test that empty screenshot list raises ValueError."""
        from appscreen.layouts import FrameSingleLayout

        layout = FrameSingleLayout(
            width=1200,
            height=1600,
        )

        with pytest.raises(ValueError, match="requires at least one screenshot"):
            layout.render([])

    def test_layout_unknown_device_raises(self):
        """Test that unknown device raises ValueError."""
        from appscreen.layouts import FrameSingleLayout

        layout = FrameSingleLayout(
            width=1200,
            height=1600,
            device_name="unknown-device",
        )

        screenshot = Image.new("RGB", (400, 800), (255, 255, 255))

        with pytest.raises(ValueError):
            layout.render([screenshot])


class TestLayoutIntegration:
    """Test frame layout integration with layout factory."""

    def test_get_layout_factory(self):
        """Test getting frame-single layout from factory."""
        from appscreen.layouts import get_layout, FrameSingleLayout

        layout = get_layout(
            "frame-single",
            width=1200,
            height=1600,
            device_name="iphone-15-pro-max",
        )

        assert isinstance(layout, FrameSingleLayout)
        assert layout.width == 1200
        assert layout.height == 1600

    def test_layout_factory_unknown_raises(self):
        """Test factory raises for unknown layout."""
        from appscreen.layouts import get_layout

        with pytest.raises(ValueError, match="Unknown layout"):
            get_layout("unknown-layout", width=1200, height=1600)
