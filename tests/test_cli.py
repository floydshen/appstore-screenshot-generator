"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner

from appscreen.cli import main
from appscreen.config import Config, AppConfig


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


class TestDevicesCommand:
    """Tests for the devices command."""

    def test_devices_lists_all_devices(self, runner):
        """Test that devices command lists all available devices."""
        result = runner.invoke(main, ["devices"])

        assert result.exit_code == 0
        assert "iPhone Devices:" in result.output
        assert "iPad Devices:" in result.output
        assert "iphone-6.7" in result.output
        assert "ipad-13" in result.output
        assert "Total:" in result.output

    def test_devices_shows_dimensions(self, runner):
        """Test that devices command shows display dimensions."""
        result = runner.invoke(main, ["devices"])

        assert result.exit_code == 0
        assert "1290x2796" in result.output  # iPhone 6.7
        assert "2048x2732" in result.output  # iPad 13


class TestThemesCommand:
    """Tests for the themes command."""

    def test_themes_lists_all_themes(self, runner):
        """Test that themes command lists all preset themes."""
        result = runner.invoke(main, ["themes"])

        assert result.exit_code == 0
        assert "gradient-blue" in result.output
        assert "gradient-purple" in result.output
        assert "solid-white" in result.output
        assert "Total:" in result.output

    def test_themes_shows_colors(self, runner):
        """Test that themes command shows theme colors."""
        result = runner.invoke(main, ["themes"])

        assert result.exit_code == 0
        assert "#667eea" in result.output
        assert "#764ba2" in result.output


class TestInitCommand:
    """Tests for the init command."""

    def test_init_creates_config_file(self, runner, tmp_path):
        """Test that init creates a config.yaml file."""
        result = runner.invoke(
            main,
            [
                "init",
                "--app-name",
                "TestApp",
                "--bundle-id",
                "com.test.app",
                "--output",
                str(tmp_path),
            ],
        )

        assert result.exit_code == 0
        assert (tmp_path / "config.yaml").exists()

    def test_init_creates_screenshots_dir(self, runner, tmp_path):
        """Test that init creates a screenshots directory."""
        result = runner.invoke(
            main,
            [
                "init",
                "--app-name",
                "TestApp",
                "--bundle-id",
                "com.test.app",
                "--output",
                str(tmp_path),
            ],
        )

        assert result.exit_code == 0
        assert (tmp_path / "screenshots").exists()
        assert (tmp_path / "screenshots").is_dir()

    def test_init_config_contains_app_info(self, runner, tmp_path):
        """Test that generated config contains app information."""
        result = runner.invoke(
            main,
            [
                "init",
                "--app-name",
                "TestApp",
                "--bundle-id",
                "com.test.app",
                "--output",
                str(tmp_path),
            ],
        )

        assert result.exit_code == 0

        config = Config.from_yaml(tmp_path / "config.yaml")
        assert config.app.name == "TestApp"
        assert config.app.bundle_id == "com.test.app"

    def test_init_success_message(self, runner, tmp_path):
        """Test that init shows success message."""
        result = runner.invoke(
            main,
            [
                "init",
                "--app-name",
                "TestApp",
                "--bundle-id",
                "com.test.app",
                "--output",
                str(tmp_path),
            ],
        )

        assert result.exit_code == 0
        assert "Created" in result.output
        assert "config.yaml" in result.output


class TestValidateCommand:
    """Tests for the validate command."""

    def test_validate_valid_config(self, runner, tmp_path):
        """Test validation of a valid config file."""
        # Create a valid config
        config = Config(
            app=AppConfig(name="TestApp", bundle_id="com.test.app"),
            screenshots=[],
        )
        config_path = tmp_path / "config.yaml"
        config.to_yaml(config_path)

        result = runner.invoke(main, ["validate", "--config", str(config_path)])

        assert result.exit_code == 0
        assert "valid" in result.output.lower()
        assert "TestApp" in result.output

    def test_validate_missing_file(self, runner):
        """Test validation of a missing file."""
        result = runner.invoke(main, ["validate", "--config", "nonexistent.yaml"])

        assert result.exit_code != 0

    def test_validate_invalid_config(self, runner, tmp_path):
        """Test validation of an invalid config file."""
        # Create an invalid config
        config_path = tmp_path / "config.yaml"
        config_path.write_text("invalid: yaml: content:")

        result = runner.invoke(main, ["validate", "--config", str(config_path)])

        assert result.exit_code != 0

    def test_validate_shows_device_count(self, runner, tmp_path):
        """Test that validate shows number of devices."""
        # Create a valid config
        config = Config(
            app=AppConfig(name="TestApp", bundle_id="com.test.app"),
            devices=["iphone-6.7", "ipad-13"],
        )
        config_path = tmp_path / "config.yaml"
        config.to_yaml(config_path)

        result = runner.invoke(main, ["validate", "--config", str(config_path)])

        assert result.exit_code == 0
        assert "Devices:" in result.output
        assert "iphone-6.7" in result.output


class TestGenerateAllCommand:
    """Tests for the generate-all command."""

    def test_generate_all_placeholder(self, runner, tmp_path):
        """Test that generate-all shows placeholder message."""
        # Create a valid config
        config = Config(
            app=AppConfig(name="TestApp", bundle_id="com.test.app"),
        )
        config_path = tmp_path / "config.yaml"
        config.to_yaml(config_path)

        result = runner.invoke(
            main,
            ["generate-all", "--config", str(config_path), "--output", str(tmp_path / "output")],
        )

        assert result.exit_code == 0
        assert "not yet implemented" in result.output.lower()

    def test_generate_all_with_screenshots_count(self, runner, tmp_path):
        """Test that generate-all shows screenshot count."""
        from appscreen.config import ScreenshotConfig

        # Create a config with screenshots
        config = Config(
            app=AppConfig(name="TestApp", bundle_id="com.test.app"),
            screenshots=[
                ScreenshotConfig(file="screenshot1.png"),
                ScreenshotConfig(file="screenshot2.png"),
            ],
        )
        config_path = tmp_path / "config.yaml"
        config.to_yaml(config_path)

        result = runner.invoke(
            main,
            ["generate-all", "--config", str(config_path), "--output", str(tmp_path / "output")],
        )

        assert result.exit_code == 0
        assert "2 screenshots" in result.output


class TestVersionOption:
    """Tests for the version option."""

    def test_version(self, runner):
        """Test that version option works."""
        result = runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert "0.1.0" in result.output
