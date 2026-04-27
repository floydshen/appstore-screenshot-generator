# Getting Started

This guide will help you set up and generate your first App Store screenshots.

## System Requirements

- **Python**: 3.10 or higher
- **OS**: macOS, Linux, or Windows
- **RAM**: 2GB minimum (4GB recommended for batch generation)

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install appstore-screenshot-generator
```

### Option 2: Install from Source

```bash
git clone https://github.com/floydshen/appstore-screenshot-generator.git
cd appstore-screenshot-generator
pip install -e .
```

### Verify Installation

```bash
appscreen --version
# Output: appscreen, version 0.1.0
```

## Your First Screenshot

### Step 1: Initialize the Project

Create a new project directory with default configuration:

```bash
mkdir my-app-screenshots
cd my-app-screenshots
appscreen init --app-name "MyApp" --bundle-id "com.example.myapp"
```

This creates:
```
my-app-screenshots/
├── config.yaml       # Configuration file
└── screenshots/      # Directory for raw screenshots
```

### Step 2: Prepare Your Screenshots

1. Take screenshots from your iOS simulator or device
2. Save them in the `screenshots/` directory
3. Recommended naming: `home.png`, `features.png`, `settings.png`, etc.

**Screenshot Tips:**
- Use high-resolution screenshots (at least 1242×2208 for iPhone)
- Screenshots are automatically scaled to fit each device size
- Avoid including sensitive data in screenshots

### Step 3: Create Your First Configuration

Edit `config.yaml` with your screenshot settings:

```yaml
app:
  name: "MyApp"
  bundle_id: "com.example.myapp"

screenshots:
  - file: "screenshots/home.png"
    caption: "Welcome to MyApp"
  
  - file: "screenshots/dashboard.png"
    caption: "Your Dashboard"

devices:
  - "iphone-6.7"
  - "iphone-6.5"

theme:
  name: "gradient-blue"

output:
  output_dir: "./output"
```

### Step 4: Validate Configuration

Before generating, validate your configuration:

```bash
appscreen validate --config config.yaml
```

Output:
```
✓ Configuration is valid

App: MyApp (com.example.myapp)
Devices: iphone-6.7, iphone-6.5
Screenshots: 2
Theme: gradient-blue
```

### Step 5: Generate Screenshots

```bash
appscreen generate-all --config config.yaml --output ./output/
```

Your generated screenshots will be in:
```
output/
├── iphone-6.7/
│   ├── 01.png
│   └── 02.png
└── iphone-6.5/
    ├── 01.png
    └── 02.png
```

## Using the Web UI

For interactive editing and real-time preview, launch the web UI:

```bash
appscreen preview
```

This opens a Gradio interface at `http://127.0.0.1:7860` where you can:
- Upload screenshots
- Preview different layouts
- Adjust themes and colors
- Download generated images

### Web UI Options

```bash
# Change host and port
appscreen preview --host 0.0.0.0 --port 8080

# Create a public share link (useful for demos)
appscreen preview --share
```

## Next Steps

- **Customize Layouts**: See [layouts.md](layouts.md) for all layout options
- **Create Custom Themes**: See [themes.md](themes.md) for theme configuration
- **Integrate with Fastlane**: See [fastlane-integration.md](fastlane-integration.md) for CI/CD workflows

## Troubleshooting

### "Configuration file not found"

Make sure you're running commands from the correct directory:
```bash
cd my-app-screenshots
appscreen validate --config config.yaml
```

### "Unknown device"

Check available devices with:
```bash
appscreen devices
```

### "Unknown layout"

Check available layouts in [layouts.md](layouts.md) or use:
```yaml
layout:
  type: "single"  # Fallback to simple single layout
```

### Image Quality Issues

For best results:
- Use PNG format for screenshots
- Ensure screenshots are high resolution (match target device or higher)
- Avoid scaling up low-resolution images
