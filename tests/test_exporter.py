"""Tests for the Fastlane-compatible exporter."""

import tempfile
from pathlib import Path
from unittest.mock import Mock

import pytest
from PIL import Image

from appscreen.config import AppConfig, Config, OutputConfig
from appscreen.exporter import Exporter


@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    config = Mock(spec=Config)
    config.output = OutputConfig(
        output_dir="./fastlane/metadata",
        locale_mapping={
            "en": "en-US",
            "zh": "zh-Hans",
            "zh-hant": "zh-Hant",
            "ja": "ja",
            "ko": "ko",
        },
    )
    return config


@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    # Create a simple test image (100x100 red square)
    img = Image.new("RGB", (100, 100), color="red")
    return img


class TestExporter:
    """Test suite for Exporter class."""

    def test_export_single_screenshot(self, mock_config, sample_image):
        """Test exporting a single screenshot."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_config.output.output_dir = tmpdir
            exporter = Exporter(mock_config)

            # Export a screenshot
            result = exporter.export(
                image=sample_image,
                device_name="iphone-6.9",
                index=1,
                locale="en",
            )

            # Check the file was created
            assert result.exists()
            assert result.name == "iPhone69-01.png"
            assert result.parent.name == "en-US"

    def test_locale_mapping_en_to_en_US(self, mock_config, sample_image):
        """Test locale mapping: en -> en-US."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_config.output.output_dir = tmpdir
            exporter = Exporter(mock_config)

            result = exporter.export(
                image=sample_image,
                device_name="iphone-6.7",
                index=1,
                locale="en",
            )

            assert result.parent.name == "en-US"

    def test_locale_mapping_zh_to_zh_Hans(self, mock_config, sample_image):
        """Test locale mapping: zh -> zh-Hans."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_config.output.output_dir = tmpdir
            exporter = Exporter(mock_config)

            result = exporter.export(
                image=sample_image,
                device_name="iphone-6.7",
                index=1,
                locale="zh",
            )

            assert result.parent.name == "zh-Hans"

    def test_locale_mapping_zh_hant_to_zh_Hant(self, mock_config, sample_image):
        """Test locale mapping: zh-hant -> zh-Hant."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_config.output.output_dir = tmpdir
            exporter = Exporter(mock_config)

            result = exporter.export(
                image=sample_image,
                device_name="iphone-6.7",
                index=1,
                locale="zh-hant",
            )

            assert result.parent.name == "zh-Hant"

    def test_filename_format(self, mock_config, sample_image):
        """Test filename format: {FastlaneName}-{index:02d}.png."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_config.output.output_dir = tmpdir
            exporter = Exporter(mock_config)

            # Test different indices
            for idx in [1, 5, 10]:
                result = exporter.export(
                    image=sample_image,
                    device_name="iphone-6.9",
                    index=idx,
                    locale="en",
                )
                expected_name = f"iPhone69-{idx:02d}.png"
                assert result.name == expected_name

    def test_different_devices(self, mock_config, sample_image):
        """Test filename generation for different devices."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_config.output.output_dir = tmpdir
            exporter = Exporter(mock_config)

            test_cases = [
                ("iphone-6.9", "iPhone69"),
                ("iphone-6.7", "iPhone67"),
                ("iphone-6.5", "iPhone65"),
                ("ipad-13", "iPadPro129"),
                ("ipad-11", "iPadPro11"),
            ]

            for device_name, expected_fastlane_name in test_cases:
                result = exporter.export(
                    image=sample_image,
                    device_name=device_name,
                    index=1,
                    locale="en",
                )
                expected_name = f"{expected_fastlane_name}-01.png"
                assert result.name == expected_name

    def test_auto_resize(self, mock_config):
        """Test automatic resizing of images."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_config.output.output_dir = tmpdir
            exporter = Exporter(mock_config)

            # Create an image with wrong size
            wrong_size_img = Image.new("RGB", (500, 500), color="blue")

            result = exporter.export(
                image=wrong_size_img,
                device_name="iphone-6.9",  # Expected: 1260x2736
                index=1,
                locale="en",
            )

            # Load the saved image and check dimensions
            saved_img = Image.open(result)
            assert saved_img.size == (1260, 2736)

    def test_no_resize_when_correct_size(self, mock_config):
        """Test that no resize happens when image is already correct size."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_config.output.output_dir = tmpdir
            exporter = Exporter(mock_config)

            # Create an image with correct size for iphone-6.9
            correct_size_img = Image.new("RGB", (1260, 2736), color="green")

            result = exporter.export(
                image=correct_size_img,
                device_name="iphone-6.9",
                index=1,
                locale="en",
            )

            # Load the saved image and check dimensions
            saved_img = Image.open(result)
            assert saved_img.size == (1260, 2736)

    def test_export_all(self, mock_config, sample_image):
        """Test exporting multiple screenshots at once."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_config.output.output_dir = tmpdir
            exporter = Exporter(mock_config)

            images = [
                (sample_image, "iphone-6.9", 1, "en"),
                (sample_image, "iphone-6.7", 2, "en"),
                (sample_image, "iphone-6.9", 1, "zh"),
            ]

            results = exporter.export_all(images)

            assert len(results) == 3
            assert all(path.exists() for path in results)

            # Check specific files
            assert results[0].name == "iPhone69-01.png"
            assert results[0].parent.name == "en-US"

            assert results[1].name == "iPhone67-02.png"
            assert results[1].parent.name == "en-US"

            assert results[2].name == "iPhone69-01.png"
            assert results[2].parent.name == "zh-Hans"

    def test_directory_creation(self, mock_config, sample_image):
        """Test that output directories are created automatically."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Use a nested path that doesn't exist
            nested_path = Path(tmpdir) / "fastlane" / "metadata"
            mock_config.output.output_dir = str(nested_path)
            exporter = Exporter(mock_config)

            # Directory doesn't exist yet
            assert not nested_path.exists()

            # Export should create it
            result = exporter.export(
                image=sample_image,
                device_name="iphone-6.9",
                index=1,
                locale="en",
            )

            # Now it should exist
            assert nested_path.exists()
            assert result.exists()

    def test_unknown_locale_passes_through(self, mock_config, sample_image):
        """Test that unknown locale codes pass through unchanged."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_config.output.output_dir = tmpdir
            exporter = Exporter(mock_config)

            result = exporter.export(
                image=sample_image,
                device_name="iphone-6.9",
                index=1,
                locale="fr",  # Not in mapping
            )

            # Should use "fr" as-is
            assert result.parent.name == "fr"

    def test_png_format(self, mock_config, sample_image):
        """Test that images are saved as PNG."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_config.output.output_dir = tmpdir
            exporter = Exporter(mock_config)

            result = exporter.export(
                image=sample_image,
                device_name="iphone-6.9",
                index=1,
                locale="en",
            )

            # Check file extension
            assert result.suffix == ".png"

            # Verify it's a valid PNG by loading it
            img = Image.open(result)
            assert img.format == "PNG"
