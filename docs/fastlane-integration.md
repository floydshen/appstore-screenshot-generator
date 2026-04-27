# Fastlane Integration

This guide explains how to integrate AppStore Screenshot Generator with [Fastlane](https://fastlane.tools/) for automated screenshot uploads to App Store Connect.

## Output Format

AppStore Screenshot Generator outputs files in a Fastlane-compatible directory structure:

```
fastlane/metadata/
├── en-US/
│   └── screenshots/
│       ├── iPhone67_01.png
│       ├── iPhone67_02.png
│       ├── iPhone67_03.png
│       iPadPro129_01.png
│       └── iPadPro129_02.png
├── zh-Hans/
│   └── screenshots/
│       ├── iPhone67_01.png
│       └── ...
├── ja/
│   └── screenshots/
│       └── ...
└── ...
```

### Device Naming Convention

| Device | Fastlane Name | Filename Prefix |
|--------|---------------|-----------------|
| `iphone-6.9` | iPhone69 | iPhone69_ |
| `iphone-6.7` | iPhone67 | iPhone67_ |
| `iphone-6.5` | iPhone65 | iPhone65_ |
| `iphone-6.1` | iPhone61 | iPhone61_ |
| `iphone-5.5` | iPhone55 | iPhone55_ |
| `ipad-13` | iPadPro129 | iPadPro129_ |
| `ipad-11` | iPadPro11 | iPadPro11_ |
| `ipad-10.5` | iPad105 | iPad105_ |

## Configuration for Fastlane

### Basic Configuration

```yaml
app:
  name: "MyApp"
  bundle_id: "com.example.myapp"

screenshots:
  - file: "screenshots/home.png"
    caption: "Welcome"
  - file: "screenshots/features.png"
    caption: "Features"

devices:
  - "iphone-6.7"
  - "iphone-6.5"
  - "ipad-13"

output:
  fastlane_compatible: true
  output_dir: "./fastlane/metadata"
  filename_template: "{device}_{index}.{ext}"
```

### Multi-locale Configuration

```yaml
output:
  fastlane_compatible: true
  output_dir: "./fastlane/metadata"
  locale_mapping:
    "en-US": "en-US"
    "zh-Hans": "zh-Hans"
    "zh-Hant": "zh-Hant"
    "ja": "ja"
    "ko": "ko"
```

## Using with Fastlane Deliver

### Step 1: Generate Screenshots

```bash
# Generate for all locales
appscreen generate-all --config config.yaml --output ./fastlane/metadata/
```

### Step 2: Upload with Deliver

Create a `Fastfile`:

```ruby
# fastlane/Fastfile
default_platform(:ios)

platform :ios do
  desc "Upload screenshots to App Store Connect"
  lane :upload_screenshots do
    deliver(
      skip_binary_upload: true,
      skip_metadata: false,
      skip_screenshots: false,
      screenshots_path: "./fastlane/metadata",
      force: true
    )
  end
end
```

Run the upload:

```bash
fastlane upload_screenshots
```

### Alternative: Upload Only Screenshots

```ruby
lane :upload_screenshots_only do
  deliver(
    skip_binary_upload: true,
    skip_metadata: true,
    skip_screenshots: false,
    screenshots_path: "./fastlane/metadata"
  )
end
```

## Automation Scripts

### GitHub Actions

Create `.github/workflows/screenshots.yml`:

```yaml
name: Generate and Upload Screenshots

on:
  push:
    branches: [main]
    paths:
      - 'screenshots/**'
      - 'config.yaml'

jobs:
  screenshots:
    runs-on: macos-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install appstore-screenshot-generator
          bundle install
      
      - name: Generate screenshots
        run: |
          appscreen validate --config config.yaml
          appscreen generate-all --config config.yaml --output ./fastlane/metadata/
      
      - name: Upload to App Store Connect
        env:
          APP_STORE_CONNECT_API_KEY_ID: ${{ secrets.APP_STORE_CONNECT_API_KEY_ID }}
          APP_STORE_CONNECT_ISSUER_ID: ${{ secrets.APP_STORE_CONNECT_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_BASE64: ${{ secrets.APP_STORE_CONNECT_API_KEY_BASE64 }}
        run: |
          fastlane upload_screenshots
```

### Shell Script

Create `scripts/generate_and_upload.sh`:

```bash
#!/bin/bash
set -e

# Configuration
CONFIG_FILE="config.yaml"
OUTPUT_DIR="./fastlane/metadata"

echo "📱 Generating App Store screenshots..."

# Validate configuration
echo "✓ Validating configuration..."
appscreen validate --config $CONFIG_FILE

# Generate screenshots
echo "✓ Generating screenshots..."
appscreen generate-all --config $CONFIG_FILE --output $OUTPUT_DIR

# Count generated screenshots
SCREENSHOT_COUNT=$(find $OUTPUT_DIR -name "*.png" | wc -l)
echo "✓ Generated $SCREENSHOT_COUNT screenshots"

# Upload to App Store Connect
echo "📤 Uploading to App Store Connect..."
fastlane upload_screenshots

echo "✅ Done!"
```

Make it executable:

```bash
chmod +x scripts/generate_and_upload.sh
./scripts/generate_and_upload.sh
```

### Python Script

Create `scripts/generate_screenshots.py`:

```python
#!/usr/bin/env python3
"""
Generate App Store screenshots for all configured locales.
"""

import subprocess
import sys
from pathlib import Path

# Configuration
CONFIG_FILE = "config.yaml"
OUTPUT_BASE = Path("./fastlane/metadata")

# Locale-specific caption files
LOCALES = {
    "en-US": {
        "captions": {
            "home.png": "Welcome to MyApp",
            "features.png": "Discover Amazing Features",
        }
    },
    "zh-Hans": {
        "captions": {
            "home.png": "欢迎使用 MyApp",
            "features.png": "发现精彩功能",
        }
    },
}


def generate_for_locale(locale: str, captions: dict):
    """Generate screenshots for a specific locale."""
    print(f"Generating screenshots for {locale}...")
    
    output_dir = OUTPUT_BASE / locale / "screenshots"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run generation (simplified example)
    result = subprocess.run(
        ["appscreen", "generate-all", "--config", CONFIG_FILE, "--output", str(output_dir)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error generating {locale}: {result.stderr}")
        return False
    
    print(f"✓ Generated screenshots for {locale}")
    return True


def main():
    """Generate screenshots for all locales."""
    success = True
    
    for locale, config in LOCALES.items():
        if not generate_for_locale(locale, config["captions"]):
            success = False
    
    if success:
        print("\n✅ All screenshots generated successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some screenshots failed to generate")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Directory Structure

Maintain a clean project structure:

```
my-app/
├── fastlane/
│   ├── Fastfile
│   ├── Appfile
│   └── metadata/
│       ├── en-US/
│       ├── zh-Hans/
│       └── ...
├── screenshots/           # Raw screenshots from device
│   ├── home.png
│   └── features.png
├── config.yaml           # Screenshot generator config
└── scripts/
    └── generate_and_upload.sh
```

### 2. Version Control

Add to `.gitignore`:

```gitignore
# Generated screenshots (regenerate on CI)
fastlane/metadata/*/screenshots/

# Keep structure
!fastlane/metadata/.gitkeep
```

### 3. CI/CD Integration

- Generate screenshots in CI to ensure consistency
- Use App Store Connect API keys for authentication
- Run on schedule or when screenshots change

### 4. Testing Before Upload

```bash
# Validate configuration
appscreen validate --config config.yaml

# Check what will be generated
ls -la ./fastlane/metadata/en-US/screenshots/

# Dry run with Fastlane (use --skip_screenshots for testing)
fastlane deliver --skip_screenshots --skip_binary_upload
```

### 5. Handling Multiple Apps

For multiple apps in the same repo:

```yaml
# config-app1.yaml
app:
  name: "App1"
  bundle_id: "com.example.app1"
output:
  output_dir: "./fastlane/app1/metadata"

# config-app2.yaml
app:
  name: "App2"
  bundle_id: "com.example.app2"
output:
  output_dir: "./fastlane/app2/metadata"
```

## Troubleshooting

### Screenshots not appearing in App Store Connect

1. Check file naming matches Fastlane conventions
2. Verify screenshots are in the correct locale folder
3. Ensure screenshots meet App Store requirements:
   - PNG or JPEG format
   - Correct dimensions for device type
   - Not too similar to each other

### Authentication errors

```bash
# Use App Store Connect API key
fastlane deliver \
  --api_key_path ./AuthKey.p8 \
  --api_key_issuer_id YOUR_ISSUER_ID \
  --api_key_id YOUR_KEY_ID
```

### Locale not recognized

Add mapping in `config.yaml`:

```yaml
output:
  locale_mapping:
    "your-locale": "App Store Locale Code"
```

## Resources

- [Fastlane Documentation](https://docs.fastlane.tools/)
- [Fastlane Deliver](https://docs.fastlane.tools/actions/deliver/)
- [App Store Screenshot Requirements](https://developer.apple.com/help/app-store-connect/reference/screenshot-specifications)
- [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi)
