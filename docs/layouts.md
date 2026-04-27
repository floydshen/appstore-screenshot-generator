# Layouts

AppStore Screenshot Generator supports 9 layout types for arranging your screenshots. Each layout has specific parameters for customization.

## Layout Overview

| Layout | Best For | Screenshot Count |
|--------|----------|------------------|
| `single` | Hero shot, main feature | 1 |
| `frame-single` | Device showcase | 1 |
| `duo-horizontal` | Feature comparison | 2 |
| `duo-vertical` | Before/after, flow | 2 |
| `grid-2x2` | Feature overview | 4 |
| `fan` | Dynamic showcase | 2-5 |
| `perspective` | Modern, 3D look | 1 |
| `stack-3d` | Depth effect | 2-5 |
| `triple-row` | Feature highlight | 3 |

---

## Single Layout

A single screenshot centered on the canvas.

```
┌─────────────────────────┐
│                         │
│                         │
│      ┌───────────┐      │
│      │           │      │
│      │ Screenshot│      │
│      │           │      │
│      └───────────┘      │
│                         │
│                         │
└─────────────────────────┘
```

### Configuration

```yaml
layout:
  type: "single"
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `spacing` | int | 20 | Padding around screenshot |
| `align` | string | "center" | Alignment: left, center, right |

---

## Frame Single Layout

Single screenshot with a device frame overlay.

```
┌─────────────────────────┐
│                         │
│      ╔═══════════╗      │
│      ║ ┌───────┐ ║      │
│      ║ │Screen │ ║      │
│      ║ └───────┘ ║      │
│      ╚═══════════╝      │
│                         │
└─────────────────────────┘
```

### Configuration

```yaml
layout:
  type: "frame-single"

frame:
  show: true
  device: "iphone-15-pro"
  color: "natural"
  scale: 1.0
```

### Frame Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `show` | bool | true | Show device frame |
| `device` | string | "iphone-15-pro" | Device frame type |
| `color` | string | "natural" | Frame color option |
| `scale` | float | 1.0 | Frame scale factor |

---

## Duo Horizontal Layout

Two screenshots arranged side by side.

```
┌─────────────────────────────────────┐
│                                     │
│    ┌──────────┐    ┌──────────┐    │
│    │          │    │          │    │
│    │ Screen 1 │    │ Screen 2 │    │
│    │          │    │          │    │
│    └──────────┘    └──────────┘    │
│                                     │
└─────────────────────────────────────┘
```

### Configuration

```yaml
screenshots:
  - files:
      - "screenshots/screen1.png"
      - "screenshots/screen2.png"
    layout:
      type: "duo-horizontal"
      spacing: 30
      align: "center"
      shadow:
        enabled: true
        blur: 10
        opacity: 0.3
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `spacing` | int | 20 | Space between screenshots (px) |
| `align` | string | "center" | Vertical alignment: top, center, bottom |
| `shadow.enabled` | bool | false | Add shadow effect |
| `shadow.blur` | int | 10 | Shadow blur radius |
| `shadow.opacity` | float | 0.3 | Shadow opacity (0-1) |

---

## Duo Vertical Layout

Two screenshots stacked vertically.

```
┌─────────────────────────┐
│      ┌──────────┐       │
│      │ Screen 1 │       │
│      └──────────┘       │
│                         │
│      ┌──────────┐       │
│      │ Screen 2 │       │
│      └──────────┘       │
│                         │
└─────────────────────────┘
```

### Configuration

```yaml
screenshots:
  - files:
      - "screenshots/before.png"
      - "screenshots/after.png"
    layout:
      type: "duo-vertical"
      spacing: 40
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `spacing` | int | 20 | Space between screenshots (px) |
| `align` | string | "center" | Horizontal alignment: left, center, right |

---

## Grid 2x2 Layout

Four screenshots in a 2×2 grid.

```
┌───────────────────────────────────┐
│    ┌──────────┐  ┌──────────┐    │
│    │ Screen 1 │  │ Screen 2 │    │
│    └──────────┘  └──────────┘    │
│                                   │
│    ┌──────────┐  ┌──────────┐    │
│    │ Screen 3 │  │ Screen 4 │    │
│    └──────────┘  └──────────┘    │
│                                   │
└───────────────────────────────────┘
```

### Configuration

```yaml
screenshots:
  - files:
      - "screenshots/feature1.png"
      - "screenshots/feature2.png"
      - "screenshots/feature3.png"
      - "screenshots/feature4.png"
    layout:
      type: "grid-2x2"
      spacing: 20
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `spacing` | int | 20 | Space between screenshots (px) |

---

## Fan Layout

Screenshots spread in a fan pattern, like cards being dealt.

```
        ╱
       ╱
┌──────────┐
│ Screen 1 │
└──────────┘
     ╲
      ╲
       ┌──────────┐
       │ Screen 2 │
       └──────────┘
            ╲
             ╲
              ┌──────────┐
              │ Screen 3 │
              └──────────┘
```

### Configuration

```yaml
screenshots:
  - files:
      - "screenshots/screen1.png"
      - "screenshots/screen2.png"
      - "screenshots/screen3.png"
    layout:
      type: "fan"
      angle: 30.0
      radius: 200
      direction: "up"
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `angle` | float | 30.0 | Total spread angle (degrees) |
| `radius` | int | 200 | Distance from center (px) |
| `direction` | string | "up" | Fan direction: up, down, left, right |

---

## Perspective Layout

Single screenshot with 3D skew effect for a modern look.

```
        ╱╲
       ╱  ╲
      ╱    ╲
     ╱──────╲
    ╱ Screenshot ╲
   ╱              ╲
  ╱────────────────╲
```

### Configuration

```yaml
screenshots:
  - file: "screenshots/hero.png"
    layout:
      type: "perspective"
      skew_x: 0.0
      skew_y: 0.15
      shadow: true
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skew_x` | float | 0.0 | Horizontal skew factor |
| `skew_y` | float | 0.15 | Vertical skew factor |
| `shadow` | bool | true | Add shadow for depth |

---

## Stack 3D Layout

Multiple screenshots stacked with offset and rotation for 3D depth effect.

```
    ┌──────────┐
    │ Screen 3 │ (front)
    └──────────┘
   ┌──────────┐
   │ Screen 2 │ (middle)
   └──────────┘
  ┌──────────┐
  │ Screen 1 │ (back)
  └──────────┘
```

### Configuration

```yaml
screenshots:
  - files:
      - "screenshots/base.png"
      - "screenshots/overlay1.png"
      - "screenshots/overlay2.png"
    layout:
      type: "stack-3d"
      depth: 30
      rotation: 5.0
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `depth` | int | 30 | Offset between layers (px) |
| `rotation` | float | 5.0 | Rotation angle per layer (degrees) |

---

## Triple Row Layout

Three screenshots arranged horizontally with equal spacing.

```
┌───────────────────────────────────────────┐
│                                           │
│  ┌────────┐  ┌────────┐  ┌────────┐     │
│  │Screen 1│  │Screen 2│  │Screen 3│     │
│  └────────┘  └────────┘  └────────┘     │
│                                           │
└───────────────────────────────────────────┘
```

### Configuration

```yaml
screenshots:
  - files:
      - "screenshots/feature1.png"
      - "screenshots/feature2.png"
      - "screenshots/feature3.png"
    layout:
      type: "triple-row"
      spacing: 20
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `spacing` | int | 20 | Space between screenshots (px) |

**Note**: This layout requires exactly 3 screenshots.

---

## Common Layout Parameters

These parameters are available for most layouts:

### Shadow Configuration

```yaml
layout:
  type: "duo-horizontal"
  shadow:
    enabled: true
    blur: 10
    offset_x: 5
    offset_y: 5
    opacity: 0.3
    color: "#000000"
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | bool | true | Enable shadow |
| `blur` | int | 10 | Blur radius (0-100) |
| `offset_x` | int | 5 | Horizontal offset |
| `offset_y` | int | 5 | Vertical offset |
| `opacity` | float | 0.3 | Shadow opacity (0-1) |
| `color` | string | "#000000" | Shadow color (hex) |

### Device Shadow in Layouts

Some layouts support device-level shadows:

```yaml
layout:
  type: "duo-horizontal"
  shadow:
    enabled: true
    blur: 10
    offset_x: 5
    offset_y: 5
    opacity: 0.3
```

---

## Tips for Choosing Layouts

| Goal | Recommended Layout |
|------|-------------------|
| Showcase main feature | `single` or `frame-single` |
| Before/after comparison | `duo-vertical` |
| Feature comparison | `duo-horizontal` |
| Multiple features | `grid-2x2` or `triple-row` |
| Dynamic, eye-catching | `fan` or `perspective` |
| Depth and layers | `stack-3d` |

## Combining with Themes

Layouts work with themes to create complete screenshots:

```yaml
screenshots:
  - file: "screenshots/hero.png"
    caption: "Welcome"
    layout:
      type: "perspective"
      skew_y: 0.15
      shadow: true

theme:
  name: "gradient-purple"
  font:
    size: 72
    color: "#FFFFFF"
```

See [themes.md](themes.md) for theme configuration details.
