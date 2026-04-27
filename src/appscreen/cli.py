"""CLI commands for AppStore Screenshot Generator."""

import click
from pathlib import Path
from typing import Optional

from .config import Config, AppConfig, ThemeConfig, OutputConfig
from .devices import get_device, DeviceType, _ALL_DEVICES as ALL_DEVICES
from .themes.preset import PRESET_THEMES


@click.group()
@click.version_option(version="0.1.0")
def main():
    """AppStore Screenshot Generator - Create beautiful marketing screenshots."""
    pass


@main.command()
@click.option("--app-name", required=True, help="App name")
@click.option("--bundle-id", required=True, help="Bundle ID (e.g., com.example.myapp)")
@click.option("--output", default=".", help="Output directory (default: current directory)")
def init(app_name: str, bundle_id: str, output: str):
    """Initialize a new project with default configuration.
    
    Creates a config.yaml template and screenshots directory.
    """
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create config template
    config = Config(
        app=AppConfig(name=app_name, bundle_id=bundle_id),
        screenshots=[],
        devices=["iphone-6.7", "iphone-6.5", "ipad-13"],
        theme=ThemeConfig(),
        output=OutputConfig(output_dir=str(output_dir / "fastlane" / "metadata")),
    )
    
    config_path = output_dir / "config.yaml"
    config.to_yaml(config_path)
    
    # Create screenshots directory
    screenshots_dir = output_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    
    click.secho(f"✓ Created {config_path}", fg="green")
    click.secho(f"✓ Created {screenshots_dir}/", fg="green")
    click.secho(f"\nNext steps:", fg="cyan")
    click.echo(f"  1. Add your screenshots to {screenshots_dir}/")
    click.echo(f"  2. Edit {config_path} to configure your screenshots")
    click.echo(f"  3. Run: appscreen generate-all --config config.yaml --output ./output/")


@main.command()
@click.option("--config", required=True, type=click.Path(exists=True), help="Config file path")
def validate(config: str):
    """Validate configuration file.
    
    Checks if the configuration file is valid and reports any errors.
    """
    try:
        cfg = Config.from_yaml(config)
        click.secho("✓ Configuration is valid", fg="green")
        click.echo(f"\nApp: {cfg.app.name} ({cfg.app.bundle_id})")
        click.echo(f"Devices: {', '.join(cfg.devices)}")
        click.echo(f"Screenshots: {len(cfg.screenshots)}")
        click.echo(f"Theme: {cfg.theme.name}")
        
        # Validate devices
        for device_name in cfg.devices:
            try:
                get_device(device_name)
            except ValueError as e:
                click.secho(f"  ⚠ {e}", fg="yellow")
        
    except FileNotFoundError as e:
        click.secho(f"✗ Error: {e}", fg="red")
        raise click.Abort()
    except Exception as e:
        click.secho(f"✗ Validation error: {e}", fg="red")
        raise click.Abort()


@main.command("generate-all")
@click.option("--config", required=True, type=click.Path(exists=True), help="Config file path")
@click.option("--output", required=True, help="Output directory")
def generate_all(config: str, output: str):
    """Generate all screenshots based on configuration.
    
    This is a placeholder implementation.
    """
    click.secho("⚠ Generate command not yet implemented", fg="yellow")
    click.echo(f"\nConfig: {config}")
    click.echo(f"Output: {output}")
    
    try:
        cfg = Config.from_yaml(config)
        click.echo(f"\nWould generate {len(cfg.screenshots)} screenshots for {len(cfg.devices)} devices")
    except Exception as e:
        click.secho(f"Error loading config: {e}", fg="red")
        raise click.Abort()


@main.command()
def devices():
    """List available device types."""
    click.secho("\n📱 iPhone Devices:\n", fg="cyan", bold=True)
    for name, device in sorted(ALL_DEVICES.items()):
        if device.device_type == DeviceType.IPHONE:
            click.echo(f"  {name:<15} {device.display_size:<6} ({device.width}x{device.height}) [{device.fastlane_name}]")
    
    click.secho("\n📱 iPad Devices:\n", fg="cyan", bold=True)
    for name, device in sorted(ALL_DEVICES.items()):
        if device.device_type == DeviceType.IPAD:
            click.echo(f"  {name:<15} {device.display_size:<6} ({device.width}x{device.height}) [{device.fastlane_name}]")
    
    click.echo(f"\nTotal: {len(ALL_DEVICES)} devices")


@main.command()
def themes():
    """List available preset themes."""
    click.secho("\n🎨 Preset Themes:\n", fg="cyan", bold=True)
    
    for name, theme in sorted(PRESET_THEMES.items()):
        colors_str = " → ".join(theme.colors)
        type_str = "gradient" if theme.background_type == "gradient" else "solid   "
        click.echo(f"  {name:<20} [{type_str}] {colors_str}")
    
    click.echo(f"\nTotal: {len(PRESET_THEMES)} themes")


@main.command()
@click.option("--host", default="127.0.0.1", help="Server host address")
@click.option("--port", default=7860, help="Server port")
@click.option("--share", is_flag=True, help="Create a public share link")
def preview(host: str, port: int, share: bool):
    """Launch the Gradio Web UI for interactive preview.
    
    Opens a web browser with an interactive interface for generating
    App Store screenshots with real-time preview.
    """
    from .webui import launch_ui
    
    click.secho(f"\n🚀 Launching Web UI...", fg="cyan")
    click.echo(f"   Host: {host}")
    click.echo(f"   Port: {port}")
    if share:
        click.echo(f"   Share: enabled (public link will be generated)")
    click.echo(f"\n   Press Ctrl+C to stop\n")
    
    try:
        launch_ui(server_name=host, server_port=port, share=share)
    except KeyboardInterrupt:
        click.secho("\n\n👋 Web UI stopped", fg="yellow")


if __name__ == "__main__":
    main()
