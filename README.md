# AppStore Screenshot Generator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generate beautiful App Store marketing screenshots with multiple layouts, themes, and locales.

## ✨ Features

- **9 Layout Types** - Single, duo, grid, fan, perspective, 3D stack, and more
- **7 Preset Themes** - Gradient and solid color backgrounds
- **Multi-device Support** - iPhone (5.5" to 6.9") and iPad (10.5" to 13")
- **Multi-language** - Generate screenshots for all App Store locales
- **Fastlane Compatible** - Direct output to `fastlane/metadata/{locale}/`
- **Web UI** - Real-time preview with Gradio interface
- **CLI** - Command-line tools for CI/CD automation
- **Customizable** - Fine-tune colors, fonts, shadows, and device frames

## 📦 Installation

```bash
# Install from PyPI
pip install appstore-screenshot-generator

# Or install from source
git clone https://github.com/floydshen/appstore-screenshot-generator.git
cd appstore-screenshot-generator
pip install -e .
```

## 🚀 Quick Start

### 1. Initialize a new project

```bash
appscreen init --app-name "MyApp" --bundle-id "com.example.myapp"
```

This creates:
- `config.yaml` - Configuration template
- `screenshots/` - Directory for your raw screenshots

### 2. Add your screenshots

Place your app screenshots in the `screenshots/` directory.

### 3. Configure your screenshots

Edit `config.yaml` to define your screenshot layouts:

```yaml
app:
  name: "MyApp"
  bundle_id: "com.example.myapp"

screenshots:
  - file: "screenshots/home.png"
    caption: "Welcome to MyApp"
  - file: "screenshots/features.png"
    caption: "Discover Features"
    layout:
      type: "duo-horizontal"
      spacing: 20

devices:
  - "iphone-6.7"
  - "iphone-6.5"
  - "ipad-13"

theme:
  name: "gradient-blue"

output:
  output_dir: "./fastlane/metadata"
  fastlane_compatible: true
```

### 4. Generate screenshots

```bash
# Validate configuration first
appscreen validate --config config.yaml

# Generate all screenshots
appscreen generate-all --config config.yaml --output ./fastlane/metadata/
```

## 📖 CLI Commands

| Command | Description |
|---------|-------------|
| `appscreen init` | Initialize a new project |
| `appscreen validate` | Validate configuration file |
| `appscreen generate-all` | Generate all screenshots |
| `appscreen devices` | List available device types |
| `appscreen themes` | List available preset themes |
| `appscreen preview` | Launch web UI for interactive editing |

### CLI Options

```bash
# Initialize with custom output directory
appscreen init --app-name "MyApp" --bundle-id "com.example.myapp" --output ./my-project

# Launch web UI with public share link
appscreen preview --host 0.0.0.0 --port 7860 --share
```

## 🎨 Layout Types

| Layout | Description |
|--------|-------------|
| `single` | Single screenshot centered on canvas |
| `frame-single` | Single screenshot with device frame |
| `duo-horizontal` | Two screenshots side by side |
| `duo-vertical` | Two screenshots stacked vertically |
| `grid-2x2` | Four screenshots in a 2x2 grid |
| `fan` | Screenshots spread in a fan pattern |
| `perspective` | Single screenshot with 3D skew effect |
| `stack-3d` | Multiple screenshots stacked with 3D depth |
| `triple-row` | Three screenshots in a horizontal row |

See [docs/layouts.md](docs/layouts.md) for detailed parameters and examples.

## 🎭 Preset Themes

| Theme | Type | Colors |
|-------|------|--------|
| `gradient-blue` | Gradient | Purple → Blue |
| `gradient-purple` | Gradient | Purple → Pink |
| `gradient-sunset` | Gradient | Orange → Red |
| `gradient-green` | Gradient | Green → Teal |
| `gradient-dark` | Gradient | Dark slate gradient |
| `solid-white` | Solid | White |
| `solid-black` | Solid | Black |

See [docs/themes.md](docs/themes.md) for custom theme configuration.

## 📱 Supported Devices

### iPhone
| Device | Display | Resolution | Fastlane Name |
|--------|---------|------------|---------------|
| `iphone-6.9` | 6.9" | 1260×2736 | iPhone69 |
| `iphone-6.7` | 6.7" | 1290×2796 | iPhone67 |
| `iphone-6.5` | 6.5" | 1284×2778 | iPhone65 |
| `iphone-6.1` | 6.1" | 1170×2532 | iPhone61 |
| `iphone-5.5` | 5.5" | 1242×2208 | iPhone55 |

### iPad
| Device | Display | Resolution | Fastlane Name |
|--------|---------|------------|---------------|
| `ipad-13` | 13" | 2048×2732 | iPadPro129 |
| `ipad-11` | 11" | 1668×2388 | iPadPro11 |
| `ipad-10.5` | 10.5" | 1668×2224 | iPad105 |

## 🔧 Configuration Example

```yaml
app:
  name: "MyApp"
  bundle_id: "com.example.myapp"
  version: "1.0.0"
  icon: "assets/app-icon.png"

screenshots:
  - file: "screenshots/home.png"
    caption: "Welcome"
    layout:
      type: "single"
    icon:
      show: true
      position: "top-right"
      size: 100

  - files:
      - "screenshots/feature1.png"
      - "screenshots/feature2.png"
    caption: "Features"
    layout:
      type: "duo-horizontal"
      spacing: 30
      align: "center"
      shadow:
        enabled: true
        blur: 10

devices:
  - "iphone-6.7"
  - "ipad-13"

theme:
  name: "gradient-blue"
  background:
    type: "gradient"
    gradient: ["#667eea", "#764ba2"]
    gradient_direction: "diagonal"
  font:
    family: "SF Pro Display"
    size: 60
    color: "#FFFFFF"
    weight: "bold"
  frame:
    show: true
    device: "iphone-15-pro"
    color: "natural"

output:
  fastlane_compatible: true
  output_dir: "./fastlane/metadata"
  filename_template: "{device}_{index}.{ext}"
```

## 📚 Documentation

- [Getting Started](docs/getting-started.md) - Detailed installation and first steps
- [Layouts](docs/layouts.md) - Layout types and parameters
- [Themes](docs/themes.md) - Theme configuration and customization
- [Fastlane Integration](docs/fastlane-integration.md) - Integrate with Fastlane deliver

## 🔗 Fastlane Integration

Generated screenshots are compatible with [Fastlane](https://fastlane.tools/):

```
fastlane/metadata/
├── en-US/
│   └── screenshots/
│       ├── iPhone67_01.png
│       ├── iPhone67_02.png
│       └── ...
├── zh-Hans/
│   └── screenshots/
│       └── ...
└── ...
```

See [docs/fastlane-integration.md](docs/fastlane-integration.md) for automation scripts.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Fastlane](https://fastlane.tools/) - App automation toolkit
- [Pillow](https://python-pillow.org/) - Python Imaging Library
- [Gradio](https://gradio.app/) - Web UI framework
