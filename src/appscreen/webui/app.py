"""Gradio Web UI application for AppStore Screenshot Generator."""

import tempfile
from pathlib import Path
from typing import Optional

import gradio as gr
from PIL import Image

from ..devices import get_device, DeviceType, _ALL_DEVICES as ALL_DEVICES
from ..themes.preset import PRESET_THEMES, get_theme
from ..layouts import get_layout


def create_ui():
    """Create the Gradio UI for AppStore Screenshot Generator.

    Returns:
        Gradio Blocks application
    """
    with gr.Blocks(
        title="AppStore Screenshot Generator",
        theme=gr.themes.Soft(),
        css="""
        .preview-container {
            min-height: 600px;
        }
        .upload-box {
            min-height: 150px;
        }
        """,
    ) as app:
        gr.Markdown("# 📱 App Store Screenshot Generator")
        gr.Markdown("Create beautiful marketing screenshots for your iOS apps")

        with gr.Row():
            # Left column - Configuration Panel
            with gr.Column(scale=1, min_width=300):
                gr.Markdown("### ⚙️ Configuration")

                # Screenshot upload
                screenshots = gr.File(
                    file_count="multiple",
                    file_types=["image"],
                    label="📸 Upload Screenshots",
                    elem_classes=["upload-box"],
                )

                # Theme selection
                theme = gr.Dropdown(
                    choices=list(PRESET_THEMES.keys()),
                    value="gradient-blue",
                    label="🎨 Theme",
                    info="Select background theme",
                )

                # Layout selection
                layout = gr.Dropdown(
                    choices=list(
                        [
                            "single",
                            "frame-single",
                            "duo-horizontal",
                            "duo-vertical",
                            "grid-2x2",
                            "fan",
                            "perspective",
                            "stack-3d",
                            "triple-row",
                        ]
                    ),
                    value="single",
                    label="📐 Layout",
                    info="Select screenshot layout",
                )

                # Device selection
                device_names = list(ALL_DEVICES.keys())
                device = gr.Dropdown(
                    choices=device_names,
                    value="iphone-6.7" if "iphone-6.7" in device_names else device_names[0],
                    label="📱 Device",
                    info="Target device size",
                )

                # Device info display
                device_info = gr.Markdown("", elem_id="device-info")

                # Generate button
                generate_btn = gr.Button("🎨 Generate Preview", variant="primary", size="lg")

            # Right column - Preview Area
            with gr.Column(scale=2, min_width=500):
                gr.Markdown("### 👁️ Preview")

                preview = gr.Image(
                    label="Generated Screenshot",
                    type="filepath",
                    elem_classes=["preview-container"],
                )

                # Export options
                with gr.Row():
                    export_format = gr.Radio(
                        choices=["PNG", "JPG"], value="PNG", label="Export Format"
                    )

                export_btn = gr.Button("💾 Export", variant="secondary")
                export_status = gr.Markdown("")

        # Event handlers
        def update_device_info(device_name: str) -> str:
            """Update device info display."""
            try:
                dev = get_device(device_name)
                device_type = "iPhone" if dev.device_type == DeviceType.IPHONE else "iPad"
                return f"**{device_type}** • {dev.display_size} • {dev.width}×{dev.height} • Fastlane: `{dev.fastlane_name}`"
            except Exception as e:
                return f"Error: {e}"

        def generate_preview(
            uploaded_files,
            theme_name: str,
            layout_name: str,
            device_name: str,
        ) -> Optional[str]:
            """Generate preview image.

            Args:
                uploaded_files: List of uploaded file objects
                theme_name: Selected theme name
                layout_name: Selected layout name
                device_name: Selected device name

            Returns:
                Path to generated preview image, or None if error
            """
            if not uploaded_files or len(uploaded_files) == 0:
                return None

            try:
                # Get device specs
                device = get_device(device_name)

                # Get theme
                theme = get_theme(theme_name)

                # Load screenshots
                screenshot_images = []
                for file_info in uploaded_files:
                    if isinstance(file_info, (list, tuple)):
                        file_path = file_info[0] if len(file_info) > 0 else None
                    else:
                        file_path = file_info

                    if file_path:
                        img = Image.open(file_path)
                        # Convert to RGB if necessary
                        if img.mode == "RGBA":
                            # Create white background for RGBA images
                            bg = Image.new("RGB", img.size, (255, 255, 255))
                            bg.paste(img, mask=img.split()[3])
                            img = bg
                        elif img.mode != "RGB":
                            img = img.convert("RGB")
                        screenshot_images.append(img)

                if not screenshot_images:
                    return None

                # Create background from theme
                background = theme.render_background(device.width, device.height)

                # Get layout and render screenshots onto white canvas
                layout_instance = get_layout(
                    name=layout_name,
                    width=device.width,
                    height=device.height,
                )
                screenshot_layer = layout_instance.render(screenshots=screenshot_images)

                # Composite: paste screenshot layer onto background
                # White pixels in screenshot_layer should be transparent
                # Convert both to RGBA
                bg_rgba = background.convert("RGBA")
                fg_rgba = screenshot_layer.convert("RGBA")

                # Make white/near-white pixels transparent in foreground
                pixels = fg_rgba.load()
                for y in range(fg_rgba.height):
                    for x in range(fg_rgba.width):
                        r, g, b, a = pixels[x, y]
                        # If pixel is very white (background), make it transparent
                        if r > 250 and g > 250 and b > 250:
                            pixels[x, y] = (r, g, b, 0)

                # Composite
                result = Image.alpha_composite(bg_rgba, fg_rgba)
                result = result.convert("RGB")

                # Save to temp file
                with tempfile.NamedTemporaryFile(
                    suffix=".png",
                    delete=False,
                ) as tmp:
                    result.save(tmp.name, "PNG")
                    return tmp.name

            except Exception as e:
                print(f"Error generating preview: {e}")
                import traceback

                traceback.print_exc()
                return None

        def export_image(
            preview_path: Optional[str],
            format_name: str,
        ) -> str:
            """Export the generated image.

            Args:
                preview_path: Path to the preview image
                format_name: Export format (PNG or JPG)

            Returns:
                Status message
            """
            if not preview_path:
                return "❌ No preview to export. Generate a preview first."

            try:
                # Generate output filename
                output_dir = Path.home() / "Downloads"
                output_dir.mkdir(parents=True, exist_ok=True)

                output_path = output_dir / f"screenshot.{format_name.lower()}"

                # Load and save
                img = Image.open(preview_path)
                img.save(output_path, format_name)

                return f"✅ Exported to: `{output_path}`"
            except Exception as e:
                return f"❌ Export failed: {e}"

        # Connect event handlers
        device.change(fn=update_device_info, inputs=[device], outputs=[device_info])

        generate_btn.click(
            fn=generate_preview, inputs=[screenshots, theme, layout, device], outputs=[preview]
        )

        export_btn.click(fn=export_image, inputs=[preview, export_format], outputs=[export_status])

        # Load initial device info
        app.load(fn=update_device_info, inputs=[device], outputs=[device_info])

    return app


def launch_ui(
    server_name: str = "127.0.0.1", server_port: int = 7860, share: bool = False, **kwargs
):
    """Launch the Gradio UI.

    Args:
        server_name: Server host address
        server_port: Server port
        share: Whether to create a public share link
        **kwargs: Additional arguments passed to gradio.launch()
    """
    app = create_ui()
    app.launch(server_name=server_name, server_port=server_port, share=share, **kwargs)


if __name__ == "__main__":
    launch_ui()
