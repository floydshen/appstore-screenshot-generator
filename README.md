# AppStore Screenshot Generator

Generate App Store marketing screenshots with multiple layouts, themes, and locales.

## Features

- **22 Layout Types**: Single, duo, grid, fan, perspective, device frames, etc.
- **10 Preset Themes**: Gradient, solid, texture backgrounds
- **Multi-language Support**: Generate screenshots for all locales
- **Fastlane Compatible**: Direct output to `fastlane/metadata/{locale}/`
- **Web UI**: Real-time preview with Gradio
- **CLI**: Command-line tools for automation

## Installation

```bash
pip install appstore-screenshot-generator
```

## Quick Start

```bash
# Initialize project
appscreen init --app-name "MyApp" --bundle-id "com.example.myapp"

# Generate all screenshots
appscreen generate-all --config config.yaml --output ./fastlane/metadata/
```

## License

MIT
