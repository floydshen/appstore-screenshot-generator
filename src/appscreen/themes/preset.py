"""Preset themes for App Store screenshots."""

from PIL import Image, ImageDraw
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Theme:
    """Theme configuration for screenshot backgrounds."""
    
    name: str
    background_type: str = "gradient"  # gradient/solid
    colors: list[str] = field(default_factory=list)
    direction: str = "diagonal"  # horizontal/vertical/diagonal
    
    def render_background(self, width: int, height: int) -> Image.Image:
        """Render background image based on theme configuration.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            
        Returns:
            PIL Image with rendered background
        """
        if self.background_type == "solid":
            return self._render_solid(width, height)
        else:
            return self._render_gradient(width, height)
    
    def _render_solid(self, width: int, height: int) -> Image.Image:
        """Render solid color background."""
        color = self._hex_to_rgb(self.colors[0])
        img = Image.new("RGB", (width, height), color)
        return img
    
    def _render_gradient(self, width: int, height: int) -> Image.Image:
        """Render gradient background."""
        img = Image.new("RGB", (width, height))
        
        if len(self.colors) < 2:
            # Fallback to solid if only one color
            return self._render_solid(width, height)
        
        start_color = self._hex_to_rgb(self.colors[0])
        end_color = self._hex_to_rgb(self.colors[1])
        
        # Create gradient based on direction
        for y in range(height):
            for x in range(width):
                # Calculate interpolation factor based on direction
                if self.direction == "horizontal":
                    factor = x / width
                elif self.direction == "vertical":
                    factor = y / height
                else:  # diagonal
                    factor = (x + y) / (width + height)
                
                # Interpolate colors
                r = int(start_color[0] + (end_color[0] - start_color[0]) * factor)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * factor)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * factor)
                
                img.putpixel((x, y), (r, g, b))
        
        return img
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        """Convert hex color to RGB tuple.
        
        Args:
            hex_color: Hex color string (e.g., "#667eea")
            
        Returns:
            RGB tuple (r, g, b)
        """
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# Preset themes
PRESET_THEMES: dict[str, Theme] = {
    "gradient-blue": Theme(
        name="gradient-blue",
        background_type="gradient",
        colors=["#667eea", "#764ba2"],
        direction="diagonal"
    ),
    "gradient-purple": Theme(
        name="gradient-purple",
        background_type="gradient",
        colors=["#a855f7", "#ec4899"],
        direction="diagonal"
    ),
    "gradient-sunset": Theme(
        name="gradient-sunset",
        background_type="gradient",
        colors=["#f97316", "#ef4444"],
        direction="diagonal"
    ),
    "gradient-green": Theme(
        name="gradient-green",
        background_type="gradient",
        colors=["#22c55e", "#14b8a6"],
        direction="diagonal"
    ),
    "gradient-dark": Theme(
        name="gradient-dark",
        background_type="gradient",
        colors=["#1e293b", "#0f172a"],
        direction="diagonal"
    ),
    "solid-white": Theme(
        name="solid-white",
        background_type="solid",
        colors=["#ffffff"],
        direction="diagonal"
    ),
    "solid-black": Theme(
        name="solid-black",
        background_type="solid",
        colors=["#000000"],
        direction="diagonal"
    ),
}


def get_theme(name: str) -> Theme:
    """Get a preset theme by name.
    
    Args:
        name: Theme name
        
    Returns:
        Theme instance
        
    Raises:
        KeyError: If theme name is not found
    """
    if name not in PRESET_THEMES:
        raise KeyError(f"Unknown theme: {name}. Available themes: {list(PRESET_THEMES.keys())}")
    return PRESET_THEMES[name]
