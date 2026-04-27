# Themes

Themes control the visual appearance of your screenshots including backgrounds, fonts, and text styling.

## Preset Themes

### Gradient Themes

| Theme | Colors | Preview |
|-------|--------|---------|
| `gradient-blue` | #667eea → #764ba2 | Purple-blue gradient |
| `gradient-purple` | #a855f7 → #ec4899 | Purple-pink gradient |
| `gradient-sunset` | #f97316 → #ef4444 | Orange-red gradient |
| `gradient-green` | #22c55e → #14b8a6 | Green-teal gradient |
| `gradient-dark` | #1e293b → #0f172a | Dark slate gradient |

### Solid Color Themes

| Theme | Color | Preview |
|-------|-------|---------|
| `solid-white` | #ffffff | Pure white |
| `solid-black` | #000000 | Pure black |

### Using Preset Themes

```yaml
theme:
  name: "gradient-blue"
```

---

## Custom Theme Configuration

Create your own theme by configuring individual elements:

### Background Configuration

#### Solid Color Background

```yaml
theme:
  background:
    type: "solid"
    color: "#1a1a2e"
```

#### Gradient Background

```yaml
theme:
  background:
    type: "gradient"
    gradient: ["#667eea", "#764ba2"]
    gradient_direction: "diagonal"
```

**Gradient Directions:**
- `vertical` - Top to bottom
- `horizontal` - Left to right
- `diagonal` - Top-left to bottom-right

#### Multi-color Gradient

```yaml
theme:
  background:
    type: "gradient"
    gradient: ["#ff6b6b", "#feca57", "#48dbfb", "#ff9ff3"]
    gradient_direction: "diagonal"
```

#### Image Background

```yaml
theme:
  background:
    type: "image"
    image: "assets/background.jpg"
    opacity: 1.0
```

**Note**: Image backgrounds are scaled to fit the canvas. Use high-resolution images (at least 1290×2796 for iPhone 6.7").

### Background Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `type` | string | "gradient" | Background type: solid, gradient, image |
| `color` | string | - | Solid color (required for type: solid) |
| `gradient` | list | ["#667eea", "#764ba2"] | Gradient colors (2+ hex values) |
| `gradient_direction` | string | "vertical" | Direction: vertical, horizontal, diagonal |
| `image` | string | - | Image path or URL (required for type: image) |
| `opacity` | float | 1.0 | Background opacity (0-1) |

---

## Font Configuration

### Basic Font Settings

```yaml
theme:
  font:
    family: "SF Pro Display"
    size: 60
    color: "#FFFFFF"
    weight: "bold"
    style: "normal"
```

### Font Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `family` | string | "SF Pro Display" | Font family name |
| `size` | int | 60 | Font size in points (8-200) |
| `color` | string | "#FFFFFF" | Font color (hex) |
| `weight` | string | "bold" | Font weight: normal, bold, etc. |
| `style` | string | "normal" | Font style: normal, italic |

### Font Size Guidelines

| Device Type | Recommended Size |
|-------------|------------------|
| iPhone 6.9" | 60-72pt |
| iPhone 6.5" | 56-64pt |
| iPhone 5.5" | 48-56pt |
| iPad 13" | 72-96pt |

### Custom Fonts

To use custom fonts:

1. Place font files in your project directory
2. Specify the font path:

```yaml
theme:
  font:
    family: "CustomFont"
    # Font file should be: CustomFont.ttf or CustomFont.otf
```

---

## Text Position

Control where caption text appears on screenshots:

```yaml
theme:
  text_position:
    x: null          # null for auto-centering
    y: null          # null for auto-positioning
    align: "center"  # left, center, right
    vertical_align: "top"  # top, center, bottom
```

### Text Position Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | int | null | X position (null = auto) |
| `y` | int | null | Y position (null = auto) |
| `align` | string | "center" | Horizontal alignment |
| `vertical_align` | string | "top" | Vertical alignment |

### Text Padding

Control spacing around text:

```yaml
theme:
  text_padding: 40  # Padding in pixels (0-200)
```

---

## Complete Theme Example

```yaml
theme:
  name: "custom-theme"
  
  background:
    type: "gradient"
    gradient: ["#0f0c29", "#302b63", "#24243e"]
    gradient_direction: "diagonal"
  
  font:
    family: "SF Pro Display"
    size: 64
    color: "#FFFFFF"
    weight: "bold"
    style: "normal"
  
  text_position:
    align: "center"
    vertical_align: "top"
  
  text_padding: 50
  
  frame:
    show: true
    device: "iphone-15-pro"
    color: "natural"
    scale: 1.0
```

---

## Color Palette Suggestions

### Professional Business

```yaml
background:
  type: "gradient"
  gradient: ["#1e3a8a", "#1e40af"]
font:
  color: "#FFFFFF"
```

### Playful & Fun

```yaml
background:
  type: "gradient"
  gradient: ["#f472b6", "#c084fc", "#60a5fa"]
font:
  color: "#FFFFFF"
```

### Dark Mode

```yaml
background:
  type: "solid"
  color: "#0a0a0a"
font:
  color: "#FFFFFF"
```

### Light & Clean

```yaml
background:
  type: "solid"
  color: "#fafafa"
font:
  color: "#1a1a1a"
```

### Gaming

```yaml
background:
  type: "gradient"
  gradient: ["#7c3aed", "#2563eb"]
font:
  color: "#FFFFFF"
```

### Nature

```yaml
background:
  type: "gradient"
  gradient: ["#059669", "#0d9488"]
font:
  color: "#FFFFFF"
```

---

## Theme Inheritance

You can define a base theme and override specific properties per screenshot:

```yaml
# Global theme
theme:
  name: "gradient-blue"
  font:
    size: 60
    color: "#FFFFFF"

screenshots:
  - file: "screenshots/home.png"
    caption: "Welcome"
    # Uses global theme
  
  - file: "screenshots/dark-feature.png"
    caption: "Dark Mode"
    # Override background for this screenshot
    theme:
      background:
        type: "solid"
        color: "#0a0a0a"
      font:
        color: "#FFFFFF"
```

---

## Theme Best Practices

### 1. Maintain Consistency

Use the same theme across all screenshots in a locale:
```yaml
theme:
  name: "gradient-purple"  # Use one theme
```

### 2. Consider Readability

Ensure sufficient contrast between text and background:
- Light text on dark backgrounds
- Dark text on light backgrounds

### 3. Match Your App Branding

```yaml
theme:
  background:
    type: "gradient"
    gradient: ["#YOUR_BRAND_COLOR_1", "#YOUR_BRAND_COLOR_2"]
  font:
    family: "Your App's Font"
```

### 4. Test Across Devices

Different device sizes may require font size adjustments:
```yaml
theme:
  font:
    size: 60  # Test on both iPhone and iPad
```

### 5. Use Hex Colors Correctly

Always use the `#` prefix for hex colors:
```yaml
background:
  color: "#1a1a2e"  # ✓ Correct
  # color: "1a1a2e" # ✗ Incorrect
```

---

## Listing Available Themes

Use the CLI to list all preset themes:

```bash
appscreen themes
```

Output:
```
🎨 Preset Themes:

  gradient-blue     [gradient] #667eea → #764ba2
  gradient-dark     [gradient] #1e293b → #0f172a
  gradient-green    [gradient] #22c55e → #14b8a6
  gradient-purple   [gradient] #a855f7 → #ec4899
  gradient-sunset   [gradient] #f97316 → #ef4444
  solid-black       [solid   ] #000000
  solid-white       [solid   ] #ffffff

Total: 7 themes
```
