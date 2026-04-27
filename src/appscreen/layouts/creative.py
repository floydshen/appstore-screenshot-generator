"""Creative layouts for screenshots with visual effects."""

import math
from typing import Tuple

from PIL import Image, ImageDraw, ImageFilter

from .base import BaseLayout


class FanLayout(BaseLayout):
    """Layout for screenshots arranged in a fan pattern.

    Screenshots are spread out in a fan shape, like cards being dealt.
    """

    def __init__(
        self,
        width: int,
        height: int,
        background_color: tuple[int, int, int] = (255, 255, 255),
        angle: float = 30.0,
        radius: int = 200,
        direction: str = "up",
        padding: int = 40,
    ):
        """Initialize fan layout.

        Args:
            width: Canvas width
            height: Canvas height
            background_color: Background color as RGB tuple
            angle: Total spread angle in degrees (default: 30)
            radius: Distance from center for screenshots (default: 200)
            direction: Fan direction - "up", "down", "left", or "right" (default: "up")
            padding: Padding around screenshots (default: 40px)
        """
        super().__init__(width, height, background_color)
        self.angle = angle
        self.radius = radius
        self.direction = direction
        self.padding = padding

    def render(self, screenshots: list[Image.Image], **kwargs) -> Image.Image:
        """Render screenshots in a fan pattern.

        Args:
            screenshots: List of screenshots to arrange
            **kwargs: Ignored

        Returns:
            Rendered image

        Raises:
            ValueError: If screenshots list is empty
        """
        if not screenshots:
            raise ValueError("FanLayout requires at least one screenshot")

        canvas = self.create_canvas()
        n = len(screenshots)

        # Calculate available space
        available_width = self.width - 2 * self.padding
        available_height = self.height - 2 * self.padding

        # Scale all screenshots to the same size
        scaled = [self._scale_to_fit(s, available_width, available_height) for s in screenshots]

        # Determine center and rotation direction based on direction
        if self.direction == "up":
            center_x = self.width // 2
            center_y = self.height - self.padding
            base_rotation = 0
        elif self.direction == "down":
            center_x = self.width // 2
            center_y = self.padding
            base_rotation = 180
        elif self.direction == "left":
            center_x = self.width - self.padding
            center_y = self.height // 2
            base_rotation = 90
        elif self.direction == "right":
            center_x = self.padding
            center_y = self.height // 2
            base_rotation = -90
        else:
            center_x = self.width // 2
            center_y = self.height - self.padding
            base_rotation = 0

        # Calculate angles for each screenshot
        if n == 1:
            angles = [base_rotation]
        else:
            # Spread from -angle/2 to +angle/2
            angle_step = self.angle / (n - 1)
            start_angle = -self.angle / 2
            angles = [start_angle + i * angle_step + base_rotation for i in range(n)]

        # Place each screenshot
        for i, (img, angle) in enumerate(zip(scaled, angles)):
            # Rotate the screenshot
            rotated = img.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)

            # Calculate position based on direction and radius
            rad = math.radians(angle - base_rotation)
            if self.direction in ["up", "down"]:
                offset_x = int(self.radius * math.sin(rad))
                offset_y = int(self.radius * math.cos(rad)) if self.direction == "up" else -int(self.radius * math.cos(rad))
            else:
                offset_x = int(self.radius * math.cos(rad)) if self.direction == "left" else -int(self.radius * math.cos(rad))
                offset_y = int(self.radius * math.sin(rad))

            # Center the rotated image at the calculated position
            x = center_x + offset_x - rotated.width // 2
            y = center_y + offset_y - rotated.height // 2

            # Paste with transparency support
            if rotated.mode == 'RGBA':
                canvas.paste(rotated, (x, y), rotated)
            else:
                canvas.paste(rotated, (x, y))

        return canvas


class PerspectiveLayout(BaseLayout):
    """Layout with perspective/skew effect on screenshots.

    Applies a 3D-like skew transformation to screenshots.
    """

    def __init__(
        self,
        width: int,
        height: int,
        background_color: tuple[int, int, int] = (255, 255, 255),
        skew_x: float = 0.0,
        skew_y: float = 0.15,
        shadow: bool = True,
        padding: int = 40,
    ):
        """Initialize perspective layout.

        Args:
            width: Canvas width
            height: Canvas height
            background_color: Background color as RGB tuple
            skew_x: Horizontal skew factor (default: 0.0)
            skew_y: Vertical skew factor (default: 0.15)
            shadow: Whether to add shadow effect (default: True)
            padding: Padding around screenshots (default: 40px)
        """
        super().__init__(width, height, background_color)
        self.skew_x = skew_x
        self.skew_y = skew_y
        self.shadow = shadow
        self.padding = padding

    def _apply_perspective(self, image: Image.Image) -> Image.Image:
        """Apply perspective transformation to an image.

        Args:
            image: Source image

        Returns:
            Transformed image
        """
        w, h = image.size

        # Calculate perspective transform
        # Top corners shift by skew_y percentage of width
        # Side corners shift by skew_x percentage of height
        skew_x_offset = int(h * self.skew_x)
        skew_y_offset = int(w * self.skew_y)

        # Source points (original corners)
        src_points = [(0, 0), (w, 0), (w, h), (0, h)]

        # Destination points (skewed corners)
        dst_points = [
            (skew_y_offset, 0),  # Top-left
            (w - skew_y_offset, 0),  # Top-right
            (w + skew_y_offset, h),  # Bottom-right
            (-skew_y_offset, h),  # Bottom-left
        ]

        # Create new image with extra space for the skew
        new_w = w + abs(skew_y_offset) * 2
        new_h = h
        result = Image.new('RGBA', (new_w, new_h), (0, 0, 0, 0))

        # Apply simple perspective using PIL's transform
        # For a more accurate perspective, we'd need to use OpenCV or similar
        # Here we use a simple affine-like transformation
        transformed = image.transform(
            (new_w, new_h),
            Image.Transform.QUAD,
            data=[dst_points[0][0], dst_points[0][1],
                   dst_points[1][0], dst_points[1][1],
                   dst_points[2][0], dst_points[2][1],
                   dst_points[3][0], dst_points[3][1]],
            resample=Image.Resampling.BICUBIC,
        )

        return transformed

    def _add_shadow(self, image: Image.Image, offset: int = 10, blur: int = 5) -> Image.Image:
        """Add a shadow effect to an image.

        Args:
            image: Source image (RGBA mode)
            offset: Shadow offset in pixels
            blur: Shadow blur radius

        Returns:
            Image with shadow
        """
        # Create shadow layer
        shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))

        # Extract alpha channel and create shadow
        if image.mode == 'RGBA':
            alpha = image.split()[-1]
            shadow = Image.new('RGBA', image.size, (0, 0, 0, 100))
            shadow.putalpha(alpha)

        # Offset and blur the shadow
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur))

        # Composite shadow under the image
        result = Image.new('RGBA', image.size, (0, 0, 0, 0))
        result.paste(shadow, (offset, offset))
        result.paste(image, (0, 0), image if image.mode == 'RGBA' else None)

        return result

    def render(self, screenshots: list[Image.Image], **kwargs) -> Image.Image:
        """Render screenshots with perspective effect.

        Args:
            screenshots: List containing one or more screenshots
            **kwargs: Ignored

        Returns:
            Rendered image

        Raises:
            ValueError: If screenshots list is empty
        """
        if not screenshots:
            raise ValueError("PerspectiveLayout requires at least one screenshot")

        canvas = self.create_canvas()

        # Calculate available space
        available_width = self.width - 2 * self.padding
        available_height = self.height - 2 * self.padding

        # Take the first screenshot
        screenshot = screenshots[0]

        # Scale to fit
        scaled = self._scale_to_fit(screenshot, available_width, available_height)

        # Convert to RGBA for transparency support
        if scaled.mode != 'RGBA':
            scaled = scaled.convert('RGBA')

        # Apply perspective
        transformed = self._apply_perspective(scaled)

        # Add shadow if enabled
        if self.shadow:
            transformed = self._add_shadow(transformed)

        # Center on canvas
        x = (self.width - transformed.width) // 2
        y = (self.height - transformed.height) // 2

        # Paste with transparency
        canvas.paste(transformed, (x, y), transformed)

        return canvas


class Stack3DLayout(BaseLayout):
    """Layout for screenshots stacked with 3D depth effect.

    Multiple screenshots are stacked with offset and rotation for a 3D look.
    """

    def __init__(
        self,
        width: int,
        height: int,
        background_color: tuple[int, int, int] = (255, 255, 255),
        depth: int = 30,
        rotation: float = 5.0,
        padding: int = 40,
    ):
        """Initialize 3D stack layout.

        Args:
            width: Canvas width
            height: Canvas height
            background_color: Background color as RGB tuple
            depth: Offset depth between stacked screenshots (default: 30)
            rotation: Rotation angle for each layer (default: 5.0 degrees)
            padding: Padding around screenshots (default: 40px)
        """
        super().__init__(width, height, background_color)
        self.depth = depth
        self.rotation = rotation
        self.padding = padding

    def render(self, screenshots: list[Image.Image], **kwargs) -> Image.Image:
        """Render screenshots stacked with 3D effect.

        Args:
            screenshots: List of screenshots to stack
            **kwargs: Ignored

        Returns:
            Rendered image

        Raises:
            ValueError: If screenshots list is empty
        """
        if not screenshots:
            raise ValueError("Stack3DLayout requires at least one screenshot")

        canvas = self.create_canvas()
        n = len(screenshots)

        # Calculate available space (need extra space for 3D effect)
        extra_space = self.depth * (n - 1)
        available_width = self.width - 2 * self.padding - extra_space
        available_height = self.height - 2 * self.padding - extra_space

        # Scale all screenshots to the same size
        scaled = [self._scale_to_fit(s, available_width, available_height) for s in screenshots]

        # Calculate base position (centered)
        base_x = self.width // 2
        base_y = self.height // 2

        # Render from back to front
        for i in range(n - 1, -1, -1):
            img = scaled[i]

            # Calculate offset for this layer (front layers have positive offset)
            layer_offset = (n - 1 - i) * self.depth

            # Rotate alternately for visual interest
            angle = self.rotation * (n - 1 - i) * (1 if i % 2 == 0 else -1)

            # Rotate the image
            if angle != 0:
                # Convert to RGBA for transparency
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                rotated = img.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
            else:
                rotated = img

            # Add subtle shadow for depth
            if rotated.mode != 'RGBA':
                rotated = rotated.convert('RGBA')

            # Position the layer
            x = base_x - rotated.width // 2 + layer_offset
            y = base_y - rotated.height // 2 + layer_offset

            # Paste with transparency
            canvas.paste(rotated, (x, y), rotated)

        return canvas


class TripleRowLayout(BaseLayout):
    """Layout for three screenshots arranged horizontally.

    Three screenshots are placed side by side with equal spacing.
    """

    def __init__(
        self,
        width: int,
        height: int,
        background_color: tuple[int, int, int] = (255, 255, 255),
        spacing: int = 20,
        padding: int = 40,
    ):
        """Initialize triple row layout.

        Args:
            width: Canvas width
            height: Canvas height
            background_color: Background color as RGB tuple
            spacing: Space between screenshots (default: 20px)
            padding: Padding around screenshots (default: 40px)
        """
        super().__init__(width, height, background_color)
        self.spacing = spacing
        self.padding = padding

    def render(self, screenshots: list[Image.Image], **kwargs) -> Image.Image:
        """Render three screenshots in a horizontal row.

        Args:
            screenshots: List containing three screenshots
            **kwargs: Ignored

        Returns:
            Rendered image

        Raises:
            ValueError: If screenshots list doesn't contain exactly three images
        """
        if len(screenshots) != 3:
            raise ValueError(f"TripleRowLayout requires exactly 3 screenshots, got {len(screenshots)}")

        canvas = self.create_canvas()

        # Calculate available space for each screenshot
        available_width = (self.width - 2 * self.padding - 2 * self.spacing) // 3
        available_height = self.height - 2 * self.padding

        # Scale all screenshots to the same size
        scaled = [self._scale_to_fit(s, available_width, available_height) for s in screenshots]

        # Calculate positions (centered vertically)
        y_positions = [(self.height - s.height) // 2 for s in scaled]
        x_positions = []

        # Calculate x positions with center alignment
        current_x = self.padding
        for i, img in enumerate(scaled):
            # Center the image in its allocated space
            offset = (available_width - img.width) // 2
            x_positions.append(current_x + offset)
            current_x += available_width + self.spacing

        # Paste screenshots
        for i, (img, x, y) in enumerate(zip(scaled, x_positions, y_positions)):
            canvas.paste(img, (x, y))

        return canvas
