"""
================================================================================
             AUTO-SKETCHING COLORFUL GANESH CHATURTHI ANIMATION
================================================================================
A devotional, visually stunning, and high-performance digital art experience
created with Python and Pygame.

Features:
- Dynamic Auto-Sketching Engine: Lord Ganesha is drawn stroke-by-stroke on screen
  with a glowing, sparkling magic brush tip and trailing light embers.
- Vibrant Sacred Colors: Glowing lines in divine gold, sacred saffron, lotus pink,
  and temple vermillion.
- Watercolor Bloom: Rich vibrant color washes smoothly bloom inside the sketch
  upon completion.
- Harmonious Breathing Pulse: Once drawn, the entire colorful sketch breathes
  peacefully with a gentle harmonic zoom effect.
- Radiant Golden Divine Aura (Prabhavali) with pulsating glow & sunburst rays.
- Authentic bottom brass Diyas with multi-tiered flickering flames & floor light.
- 3D tumbling falling flower petals (marigold and red rose).
- Floating golden sparkles and sacred particles.
- Traditional hanging Toran garland and swaying brass temple bells.
- Subtly rotating sacred Mandala in the deep temple background.
- Full keyboard controls including Re-sketching ([R]) and Pause ([SPACE]).

Controls:
- SPACE : Pause / Resume animation
- R     : Re-sketch from beginning (restart auto-drawing)
- S     : Skip directly to completed colorful sketch
- F     : Toggle Fullscreen
- ESC   : Exit application
================================================================================
"""

import json
import math
import os
import random
import sys
import pygame

# ------------------------------------------------------------------------------
# 1. CONFIGURATION & CONSTANTS
# ------------------------------------------------------------------------------
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Ganesh Chaturthi Auto-Sketching Celebration | ॥ श्री गणेशाय नमः ॥"

# Devotional Color Palette
COLOR_BG_DARK = (22, 6, 14)          # Deep spiritual maroon / midnight temple
COLOR_BG_MID = (48, 12, 26)          # Temple vermillion / deep crimson
COLOR_BG_LIGHT = (72, 20, 36)        # Warm devotional ambient glow
COLOR_GOLD_BRIGHT = (255, 242, 175)  # Bright golden highlight
COLOR_GOLD_CORE = (255, 215, 65)     # Divine rich gold
COLOR_GOLD_WARM = (235, 165, 25)     # Warm brass amber
COLOR_GOLD_DARK = (175, 105, 12)     # Deep antique gold
COLOR_WHITE = (255, 255, 255)
COLOR_TEXT_SHADOW = (15, 3, 8)

# ------------------------------------------------------------------------------
# 2. HELPER UTILITIES & PATH RESOLUTION
# ------------------------------------------------------------------------------
def find_asset_path(filename="ganesh.png"):
    """
    Intelligently searches for the asset file across multiple common directories
    so that running from any working directory works reliably.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cwd = os.getcwd()

    candidates = [
        os.path.join(script_dir, "assets", filename),
        os.path.join(script_dir, filename),
        os.path.join(cwd, "assets", filename),
        os.path.join(cwd, filename),
        os.path.join(script_dir, "..", "assets", filename),
        os.path.join(cwd, "..", "assets", filename),
    ]

    for path in candidates:
        if os.path.exists(path):
            return os.path.abspath(path)

    return os.path.join(script_dir, "assets", filename)


def create_radial_glow_surface(radius, inner_color):
    """
    Generates an ultra-smooth, continuous radial glow surface with premultiplied
    alpha for zero-artifact additive and normal blending.
    """
    size = radius * 2
    r_c, g_c, b_c, a_c = inner_color

    try:
        import numpy as np
        y, x = np.ogrid[-radius:radius, -radius:radius]
        dist = np.sqrt(x * x + y * y)
        factor = np.clip(1.0 - (dist / radius), 0.0, 1.0)
        smooth = factor * factor * (3.0 - 2.0 * factor)
        intensity = smooth * (a_c / 255.0)

        rgba = np.zeros((size, size, 4), dtype=np.uint8)
        rgba[..., 0] = (r_c * intensity).astype(np.uint8)
        rgba[..., 1] = (g_c * intensity).astype(np.uint8)
        rgba[..., 2] = (b_c * intensity).astype(np.uint8)
        rgba[..., 3] = (smooth * a_c).astype(np.uint8)

        return pygame.image.frombuffer(rgba.tobytes(), (size, size), "RGBA")
    except Exception:
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        for r in range(radius, 0, -2):
            factor = r / radius
            smooth = (1.0 - factor) ** 2.0
            alpha = int(a_c * smooth)
            intensity = smooth * (a_c / 255.0)
            if alpha > 0:
                col = (int(r_c * intensity), int(g_c * intensity), int(b_c * intensity), min(255, alpha))
                pygame.draw.circle(surf, col, (radius, radius), r, 2)
        return surf


# ------------------------------------------------------------------------------
# 3. AUTO-SKETCHING COLORFUL ENGINE
# ------------------------------------------------------------------------------
class BrushSpark:
    """Sparkle particle emitted by the moving drawing pen."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1.2, 3.8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 0.6  # Slight upward spiritual drift
        self.color = color
        self.life = random.uniform(0.3, 0.6)
        self.age = 0.0
        self.size = random.uniform(2.0, 4.5)

    def update(self, dt):
        self.x += self.vx * (60.0 * dt)
        self.y += self.vy * (60.0 * dt)
        self.age += dt
        return self.age < self.life

    def draw(self, surface):
        progress = self.age / self.life
        alpha = int(255 * (1.0 - progress))
        if alpha <= 0:
            return

        r = max(1, int(self.size * (1.0 - progress * 0.6)))
        s = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
        c = r + 1
        col = (self.color[0], self.color[1], self.color[2], alpha)
        pygame.draw.circle(s, col, (c, c), r)
        surface.blit(s, (int(self.x - c), int(self.y - c)))


class AutoSketchGaneshEngine:
    """
    Procedural sketch engine that auto-draws Lord Ganesha stroke-by-stroke
    with a sparkling golden brush tip, vibrant sacred colors, and watercolor bloom.
    """
    def __init__(self, cx, cy, display_size=490):
        self.cx = cx
        self.cy = cy
        self.display_size = display_size
        self.ox = cx - display_size // 2
        self.oy = cy - display_size // 2

        # Drawing state
        self.strokes = []
        self.total_points = 0
        self.current_stroke_idx = 0
        self.current_pt_idx = 0
        self.brush_pos = (cx, cy)
        self.brush_sparks = []

        self.is_completed = False
        self.color_bloom_alpha = 0.0
        self.points_per_frame = 48  # Tuned for ~6 seconds of captivating sketching

        # Pre-render brush glow tip
        self.brush_glow = create_radial_glow_surface(18, (255, 230, 90, 160))

        # Persistent surfaces
        self.sketch_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.bloom_surf = None

        # Load strokes and color wash
        self.load_sketch_data()

    def load_sketch_data(self):
        """Loads precomputed stroke curves or extracts them on the fly."""
        json_path = find_asset_path("ganesh_sketch.json")
        loaded = False

        if os.path.exists(json_path):
            try:
                with open(json_path, "r") as f:
                    data = json.load(f)
                cached_size = data.get("size", self.display_size)
                scale_ratio = self.display_size / cached_size

                for s in data["strokes"]:
                    raw_pts = s["pts"]
                    scaled_pts = [
                        (self.ox + int(p[0] * scale_ratio), self.oy + int(p[1] * scale_ratio))
                        for p in raw_pts
                    ]
                    if len(scaled_pts) >= 2:
                        self.strokes.append({
                            "pts": scaled_pts,
                            "color": tuple(s["color"]),
                        })
                loaded = True
                print(f"Loaded {len(self.strokes)} sketch strokes from cache.")
            except Exception as e:
                print(f"Warning: Could not read JSON cache ({e}).")

        # Fallback to OpenCV extraction if cache was not available
        if not loaded:
            self.extract_with_opencv()

        # Compute total points for progress tracking
        self.total_points = sum(len(s["pts"]) for s in self.strokes)
        self.points_drawn = 0

        # Prepare soft color wash under-layer
        self.build_color_bloom_surface()

    def extract_with_opencv(self):
        """Extracts continuous contour strokes from ganesh.png using OpenCV."""
        asset_path = find_asset_path("ganesh.png")
        if not os.path.exists(asset_path):
            return

        try:
            import cv2
            img = cv2.imread(asset_path)
            img_small = cv2.resize(img, (self.display_size, self.display_size), interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            edges = cv2.Canny(blurred, 45, 110)
            contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

            for c in contours:
                if len(c) >= 6:
                    epsilon = 0.0022 * cv2.arcLength(c, False)
                    approx = cv2.approxPolyDP(c, epsilon, False)
                    pts = [(self.ox + int(pt[0][0]), self.oy + int(pt[0][1])) for pt in approx]
                    if len(pts) >= 2:
                        mid = approx[len(approx) // 2][0]
                        mx = min(self.display_size - 1, max(0, mid[0]))
                        my = min(self.display_size - 1, max(0, mid[1]))
                        b, g, r = img_small[my, mx]
                        r_c = min(255, int(r * 1.35 + 40))
                        g_c = min(255, int(g * 1.35 + 30))
                        b_c = min(255, int(b * 1.35 + 20))
                        self.strokes.append({
                            "pts": pts,
                            "color": (r_c, g_c, b_c),
                            "len": cv2.arcLength(c, False)
                        })

            self.strokes.sort(key=lambda s: s.get("len", 0), reverse=True)
            print(f"Extracted {len(self.strokes)} strokes on-the-fly.")
        except Exception as e:
            print(f"OpenCV extraction notice: {e}")

    def build_color_bloom_surface(self):
        """Creates a rich, soft-blurred watercolor wash to bloom under the sketch."""
        asset_path = find_asset_path("ganesh.png")
        if os.path.exists(asset_path):
            try:
                raw_img = pygame.image.load(asset_path).convert_alpha()
                scaled = pygame.transform.smoothscale(raw_img, (self.display_size, self.display_size))

                # Circular soft vignette mask so color wash blends smoothly into background
                mask = pygame.Surface((self.display_size, self.display_size), pygame.SRCALPHA)
                cr = self.display_size // 2
                for r in range(cr, 0, -3):
                    alpha = int(255 * (1.0 - (r / cr) ** 3.0))
                    pygame.draw.circle(mask, (255, 255, 255, alpha), (cr, cr), r)

                bloom = scaled.copy()
                bloom.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                self.bloom_surf = bloom
            except Exception as e:
                print(f"Color bloom creation notice: {e}")

    def reset(self):
        """Restarts the auto-sketching process from the beginning."""
        self.sketch_surf.fill((0, 0, 0, 0))
        self.current_stroke_idx = 0
        self.current_pt_idx = 0
        self.brush_sparks.clear()
        self.is_completed = False
        self.color_bloom_alpha = 0.0
        self.points_drawn = 0

    def skip_to_end(self):
        """Instantly finishes drawing all strokes."""
        if self.is_completed:
            return

        for s in self.strokes:
            pts = s["pts"]
            if len(pts) > 1:
                pygame.draw.lines(self.sketch_surf, s["color"], False, pts, 2)

        self.current_stroke_idx = len(self.strokes)
        self.is_completed = True
        self.color_bloom_alpha = 180.0
        self.points_drawn = self.total_points

    def update(self, dt):
        """Progressively advances the pen along the stroke curves."""
        # Update active brush sparks
        self.brush_sparks = [s for s in self.brush_sparks if s.update(dt)]

        if not self.is_completed:
            pts_budget = self.points_per_frame

            while pts_budget > 0 and self.current_stroke_idx < len(self.strokes):
                cur_stroke = self.strokes[self.current_stroke_idx]
                pts = cur_stroke["pts"]
                color = cur_stroke["color"]

                if self.current_pt_idx < len(pts) - 1:
                    p0 = pts[self.current_pt_idx]
                    p1 = pts[self.current_pt_idx + 1]

                    # Draw stroke line segment
                    pygame.draw.line(self.sketch_surf, color, p0, p1, 2)
                    self.brush_pos = p1
                    self.current_pt_idx += 1
                    self.points_drawn += 1
                    pts_budget -= 1

                    # Emit brush sparks
                    if random.random() < 0.65:
                        spark_col = random.choice([
                            (255, 245, 180),
                            (255, 215, 60),
                            (255, 170, 30),
                            color,
                        ])
                        self.brush_sparks.append(BrushSpark(p1[0], p1[1], spark_col))

                else:
                    # Stroke finished, advance to next stroke
                    self.current_stroke_idx += 1
                    self.current_pt_idx = 0

            # Check if all strokes are complete
            if self.current_stroke_idx >= len(self.strokes):
                self.is_completed = True
                print("Lord Ganesha sketch complete! Blooming vibrant colors.")

        else:
            # Fade in soft watercolor bloom
            if self.color_bloom_alpha < 185.0:
                self.color_bloom_alpha = min(185.0, self.color_bloom_alpha + 65.0 * dt)

    def draw(self, surface, time_sec):
        """Renders the sketch, watercolor bloom, brush sparks, and glowing pen tip."""
        pulse = 0.5 + 0.5 * math.sin(time_sec * 1.8)

        # 1. Watercolor bloom wash under the sketch
        if self.bloom_surf and self.color_bloom_alpha > 0:
            bloom_copy = self.bloom_surf.copy()
            bloom_copy.set_alpha(int(self.color_bloom_alpha))
            rect = bloom_copy.get_rect(center=(self.cx, self.cy))
            surface.blit(bloom_copy, rect)

        # 2. Main sketch lines
        if self.is_completed:
            # Gentle breathing pulse once sketch is completed
            scale = 1.0 + 0.015 * pulse
            cur_w = int(WINDOW_WIDTH * scale)
            cur_h = int(WINDOW_HEIGHT * scale)
            scaled = pygame.transform.smoothscale(self.sketch_surf, (cur_w, cur_h))
            rect = scaled.get_rect(center=(self.cx, self.cy))
            surface.blit(scaled, rect)
        else:
            surface.blit(self.sketch_surf, (0, 0))

        # 3. Active brush sparks
        for spark in self.brush_sparks:
            spark.draw(surface)

        # 4. Glowing magic pen cursor (only while sketching)
        if not self.is_completed:
            bx, by = self.brush_pos

            # Outer soft glow halo
            rect_glow = self.brush_glow.get_rect(center=(bx, by))
            surface.blit(self.brush_glow, rect_glow, special_flags=pygame.BLEND_ADD)

            # 4-point golden star sparkle
            sparkle_len = 10 + int(3 * math.sin(time_sec * 14.0))
            pygame.draw.line(surface, (255, 250, 200), (bx - sparkle_len, by), (bx + sparkle_len, by), 2)
            pygame.draw.line(surface, (255, 250, 200), (bx, by - sparkle_len), (bx, by + sparkle_len), 2)

            # Bright white-gold center core
            pygame.draw.circle(surface, (255, 255, 240), (bx, by), 4)
            pygame.draw.circle(surface, (255, 215, 60), (bx, by), 2)


# ------------------------------------------------------------------------------
# 4. VISUAL COMPONENT: FALLING FLOWER PETALS (Marigold & Sacred Rose)
# ------------------------------------------------------------------------------
class FallingPetal:
    """Simulates 3D fluttering flower petals with wind sway and flip rotation."""
    def __init__(self, width, height, start_anywhere=False):
        self.screen_width = width
        self.screen_height = height
        self.reset(start_anywhere=start_anywhere)

    def reset(self, start_anywhere=False):
        self.x_base = random.uniform(-20, self.screen_width + 20)
        self.y = random.uniform(-60, self.screen_height) if start_anywhere else random.uniform(-80, -20)
        self.speed_y = random.uniform(1.2, 2.5)

        self.sway_amplitude = random.uniform(25, 55)
        self.sway_speed = random.uniform(1.0, 2.0)
        self.sway_phase = random.uniform(0, math.pi * 2)

        self.angle = random.uniform(0, 360)
        self.rot_speed = random.uniform(-1.6, 1.6)
        self.flip_angle = random.uniform(0, math.pi * 2)
        self.flip_speed = random.uniform(1.5, 3.2)

        self.size = random.uniform(10, 18)
        self.depth_scale = random.uniform(0.75, 1.15)

        # 65% vibrant Marigold, 35% sacred Red Rose
        self.is_marigold = random.random() < 0.65
        if self.is_marigold:
            variants = [
                ((255, 160, 0), (255, 215, 40)),
                ((255, 135, 0), (255, 195, 25)),
                ((255, 190, 20), (255, 235, 110)),
            ]
            self.color_dark, self.color_light = random.choice(variants)
        else:
            variants = [
                ((185, 18, 55), (235, 65, 105)),
                ((165, 12, 45), (215, 45, 90)),
                ((205, 25, 75), (250, 95, 135)),
            ]
            self.color_dark, self.color_light = random.choice(variants)

    def update(self, dt, time_sec):
        self.y += self.speed_y * (60.0 * dt)
        self.flip_angle += self.flip_speed * dt
        self.angle += self.rot_speed * (60.0 * dt)

        if self.y > self.screen_height + 40:
            self.reset(start_anywhere=False)

    def draw(self, surface, time_sec):
        sway = math.sin(time_sec * self.sway_speed + self.sway_phase) * self.sway_amplitude
        cur_x = self.x_base + sway

        flip_factor = abs(math.cos(self.flip_angle))
        w = max(3.0, self.size * self.depth_scale * (0.3 + 0.7 * flip_factor))
        h = max(4.0, self.size * 1.5 * self.depth_scale)

        surf_dim = int(max(w, h) * 2.4)
        petal_surf = pygame.Surface((surf_dim, surf_dim), pygame.SRCALPHA)
        center = (surf_dim // 2, surf_dim // 2)

        rect = pygame.Rect(center[0] - int(w // 2), center[1] - int(h // 2), int(w), int(h))
        pygame.draw.ellipse(petal_surf, self.color_dark, rect)

        inner_rect = pygame.Rect(
            center[0] - int(w * 0.35),
            center[1] - int(h * 0.35),
            int(max(2, w * 0.7)),
            int(max(3, h * 0.7)),
        )
        pygame.draw.ellipse(petal_surf, self.color_light, inner_rect)

        rotated_surf = pygame.transform.rotate(petal_surf, self.angle)
        rot_rect = rotated_surf.get_rect(center=(int(cur_x), int(self.y)))
        surface.blit(rotated_surf, rot_rect)


# ------------------------------------------------------------------------------
# 5. VISUAL COMPONENT: FLOATING GOLDEN SPARKLES & PARTICLES
# ------------------------------------------------------------------------------
class GoldenSparkle:
    """Sacred luminous particles floating with pulsating alpha."""
    def __init__(self, width, height):
        self.screen_width = width
        self.screen_height = height
        self.reset()

    def reset(self):
        if random.random() < 0.7:
            self.x = random.uniform(self.screen_width * 0.22, self.screen_width * 0.78)
            self.y = random.uniform(self.screen_height * 0.20, self.screen_height * 0.88)
        else:
            self.x = random.uniform(0, self.screen_width)
            self.y = random.uniform(0, self.screen_height)

        self.vx = random.uniform(-0.35, 0.35)
        self.vy = random.uniform(-0.75, -0.2)
        self.radius = random.uniform(2.0, 4.0)
        self.base_alpha = random.uniform(130, 230)
        self.pulse_freq = random.uniform(1.8, 3.8)
        self.phase = random.uniform(0, math.pi * 2)
        self.life = random.uniform(3.5, 7.5)
        self.age = random.uniform(0, self.life)

    def update(self, dt):
        self.x += self.vx * (60.0 * dt)
        self.y += self.vy * (60.0 * dt)
        self.age += dt

        if self.age >= self.life or self.y < -10:
            self.reset()

    def draw(self, surface, time_sec):
        pulse = 0.5 + 0.5 * math.sin(time_sec * self.pulse_freq + self.phase)
        alpha = int(self.base_alpha * pulse)
        if alpha <= 10:
            return

        r = int(self.radius * (0.8 + 0.4 * pulse))
        size = r * 4 + 4
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        c = size // 2

        glow_alpha = max(10, alpha // 4)
        pygame.draw.circle(s, (255, 215, 90, glow_alpha), (c, c), r * 2)

        arm_len = int(r * 2.2)
        sparkle_color = (255, 245, 175, alpha)
        pygame.draw.line(s, sparkle_color, (c - arm_len, c), (c + arm_len, c), 1)
        pygame.draw.line(s, sparkle_color, (c, c - arm_len), (c, c + arm_len), 1)

        pygame.draw.circle(s, (255, 255, 235, min(255, alpha + 30)), (c, c), max(1, r - 1))
        surface.blit(s, (int(self.x - c), int(self.y - c)))


# ------------------------------------------------------------------------------
# 6. VISUAL COMPONENT: TRADITIONAL FLICKERING BRASS DIYAS
# ------------------------------------------------------------------------------
class DiyaLamp:
    """Traditional brass oil lamp with organic multi-tier flickering flame."""
    def __init__(self, x, y, scale=1.0):
        self.x = x
        self.y = y
        self.scale = scale
        self.flicker_phase = random.uniform(0, math.pi * 2)
        self.flame_height = 38 * scale
        self.flame_width = 16 * scale

        light_radius = int(120 * scale)
        self.light_surf = create_radial_glow_surface(light_radius, (255, 175, 45, 80))
        self.light_rect = self.light_surf.get_rect(center=(int(self.x), int(self.y - 8 * scale)))

    def update(self, dt):
        self.flicker_phase += 11.0 * dt

    def draw(self, surface, time_sec):
        jitter = math.sin(self.flicker_phase) * 0.12 + math.cos(self.flicker_phase * 2.3) * 0.08
        light_scale = 1.0 + jitter
        scaled_w = int(self.light_surf.get_width() * light_scale)
        scaled_h = int(self.light_surf.get_height() * light_scale)

        if scaled_w > 10 and scaled_h > 10:
            fl_light = pygame.transform.smoothscale(self.light_surf, (scaled_w, scaled_h))
            rect = fl_light.get_rect(center=self.light_rect.center)
            surface.blit(fl_light, rect, special_flags=pygame.BLEND_ADD)

        bx, by = self.x, self.y
        sc = self.scale

        pygame.draw.ellipse(surface, (110, 60, 10), (bx - 24 * sc, by + 12 * sc, 48 * sc, 12 * sc))
        pygame.draw.ellipse(surface, (185, 115, 20), (bx - 18 * sc, by + 10 * sc, 36 * sc, 8 * sc))

        bowl_poly = [
            (bx - 42 * sc, by),
            (bx - 30 * sc, by + 14 * sc),
            (bx + 30 * sc, by + 14 * sc),
            (bx + 42 * sc, by),
            (bx + 14 * sc, by + 5 * sc),
            (bx - 14 * sc, by + 5 * sc),
        ]
        pygame.draw.polygon(surface, (135, 75, 12), bowl_poly)

        pygame.draw.ellipse(surface, (215, 145, 28), (bx - 40 * sc, by - 4 * sc, 80 * sc, 13 * sc))
        pygame.draw.ellipse(surface, (165, 90, 15), (bx - 34 * sc, by - 2 * sc, 68 * sc, 9 * sc))
        pygame.draw.ellipse(surface, (95, 42, 5), (bx - 28 * sc, by - 1 * sc, 56 * sc, 6 * sc))

        flame_cx = bx
        flame_cy = by - 3 * sc

        tip_sway = math.sin(time_sec * 8.0 + self.flicker_phase) * 3.5 * sc
        tip_stretch = 1.0 + jitter * 0.85

        cur_h = self.flame_height * tip_stretch
        cur_w = self.flame_width * (1.0 - jitter * 0.25)
        flame_tip = (flame_cx + tip_sway, flame_cy - cur_h)

        outer_poly = [
            (flame_cx - cur_w * 0.8, flame_cy + 2 * sc),
            (flame_cx - cur_w * 0.95, flame_cy - cur_h * 0.35),
            flame_tip,
            (flame_cx + cur_w * 0.95, flame_cy - cur_h * 0.35),
            (flame_cx + cur_w * 0.8, flame_cy + 2 * sc),
        ]
        pygame.draw.polygon(surface, (255, 90, 15), outer_poly)

        mid_h = cur_h * 0.72
        mid_w = cur_w * 0.65
        mid_tip = (flame_cx + tip_sway * 0.7, flame_cy - mid_h)
        mid_poly = [
            (flame_cx - mid_w * 0.8, flame_cy),
            (flame_cx - mid_w, flame_cy - mid_h * 0.4),
            mid_tip,
            (flame_cx + mid_w, flame_cy - mid_h * 0.4),
            (flame_cx + mid_w * 0.8, flame_cy),
        ]
        pygame.draw.polygon(surface, (255, 215, 30), mid_poly)

        core_h = cur_h * 0.4
        core_w = cur_w * 0.35
        core_tip = (flame_cx + tip_sway * 0.4, flame_cy - core_h)
        core_poly = [
            (flame_cx - core_w, flame_cy),
            (flame_cx - core_w * 0.8, flame_cy - core_h * 0.5),
            core_tip,
            (flame_cx + core_w * 0.8, flame_cy - core_h * 0.5),
            (flame_cx + core_w, flame_cy),
        ]
        pygame.draw.polygon(surface, (255, 255, 215), core_poly)


# ------------------------------------------------------------------------------
# 7. VISUAL COMPONENT: TRADITIONAL TOP TORAN & SWAYING TEMPLE BELLS
# ------------------------------------------------------------------------------
class TempleBell:
    """Ornate golden temple bell swaying with pendulum physics."""
    def __init__(self, x, hang_length):
        self.x = x
        self.hang_length = hang_length
        self.phase = random.uniform(0, math.pi * 2)
        self.sway_speed = random.uniform(1.2, 1.8)
        self.sway_angle_max = random.uniform(0.04, 0.08)

    def draw(self, surface, time_sec):
        angle = math.sin(time_sec * self.sway_speed + self.phase) * self.sway_angle_max
        bottom_x = self.x + math.sin(angle) * self.hang_length
        bottom_y = math.cos(angle) * self.hang_length

        pygame.draw.line(surface, (185, 130, 25), (self.x, 0), (bottom_x, bottom_y), 2)

        for f in (0.35, 0.7):
            bx = self.x + (bottom_x - self.x) * f
            by = bottom_y * f
            pygame.draw.circle(surface, (255, 210, 60), (int(bx), int(by)), 3)

        bw = 13
        bh = 17
        bell_pts = [
            (bottom_x - bw * 0.5, bottom_y),
            (bottom_x - bw, bottom_y + bh),
            (bottom_x + bw, bottom_y + bh),
            (bottom_x + bw * 0.5, bottom_y),
        ]
        pygame.draw.polygon(surface, (220, 155, 28), bell_pts)
        pygame.draw.polygon(surface, (255, 215, 75), [
            (bottom_x - bw * 0.3, bottom_y + 2),
            (bottom_x - bw * 0.6, bottom_y + bh - 2),
            (bottom_x + bw * 0.6, bottom_y + bh - 2),
            (bottom_x + bw * 0.3, bottom_y + 2),
        ])

        clapper_x = bottom_x + math.sin(angle * 1.5) * 4
        pygame.draw.circle(surface, (155, 95, 15), (int(clapper_x), int(bottom_y + bh + 3)), 3)


class ToranGarland:
    """Decorative Indian Toran with mango leaves and marigold swags."""
    def __init__(self, width):
        self.width = width
        self.bells = [
            TempleBell(int(width * 0.08), 85),
            TempleBell(int(width * 0.18), 70),
            TempleBell(int(width * 0.82), 70),
            TempleBell(int(width * 0.92), 85),
        ]

    def draw(self, surface, time_sec):
        for bell in self.bells:
            bell.draw(surface, time_sec)

        num_arcs = 10
        arc_width = self.width / num_arcs

        for i in range(num_arcs):
            start_x = i * arc_width
            end_x = (i + 1) * arc_width
            mid_x = (start_x + end_x) / 2
            sag_y = 20

            leaf_poly = [
                (start_x + 5, 0),
                (end_x - 5, 0),
                (mid_x, sag_y + 12),
            ]
            pygame.draw.polygon(surface, (32, 95, 42), leaf_poly)
            pygame.draw.polygon(surface, (52, 135, 60), [
                (start_x + 12, 0),
                (end_x - 12, 0),
                (mid_x, sag_y + 8),
            ])

            pygame.draw.circle(surface, (255, 135, 0), (int(start_x), 4), 9)
            pygame.draw.circle(surface, (255, 210, 30), (int(start_x), 4), 5)

        for side_x in (25, self.width - 25):
            for y_step in range(15, 135, 18):
                col = (255, 145, 0) if (y_step // 18) % 2 == 0 else (255, 210, 30)
                pygame.draw.circle(surface, col, (side_x, y_step), 7)
                pygame.draw.circle(surface, (195, 45, 20), (side_x, y_step), 3)


# ------------------------------------------------------------------------------
# 8. VISUAL COMPONENT: SACRED ROTATING MANDALA BACKGROUND
# ------------------------------------------------------------------------------
class SacredMandala:
    def __init__(self, radius=290):
        self.radius = radius
        self.surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.render_pattern()

    def render_pattern(self):
        cx, cy = self.radius, self.radius
        gold_color = (255, 215, 100, 24)
        line_color = (255, 200, 80, 18)

        for r in (70, 120, 170, 220, 270):
            pygame.draw.circle(self.surf, line_color, (cx, cy), r, 1)

        petals = 16
        for i in range(petals):
            theta = (i * 2 * math.pi) / petals
            tip_r = 260
            tip_x = cx + math.cos(theta) * tip_r
            tip_y = cy + math.sin(theta) * tip_r

            base_theta1 = theta - (math.pi / petals)
            base_theta2 = theta + (math.pi / petals)
            base_r = 170

            p1 = (cx + math.cos(base_theta1) * base_r, cy + math.sin(base_theta1) * base_r)
            p2 = (tip_x, tip_y)
            p3 = (cx + math.cos(base_theta2) * base_r, cy + math.sin(base_theta2) * base_r)

            pygame.draw.lines(self.surf, gold_color, False, [p1, p2, p3], 1)
            pygame.draw.circle(self.surf, gold_color, (int(tip_x), int(tip_y)), 3)

    def draw(self, surface, center_pos, time_sec):
        rot_angle = (time_sec * 2.0) % 360
        rotated = pygame.transform.rotate(self.surf, rot_angle)
        rect = rotated.get_rect(center=center_pos)
        surface.blit(rotated, rect)


# ------------------------------------------------------------------------------
# 9. VISUAL COMPONENT: DIVINE AURA & PRABHAVALI
# ------------------------------------------------------------------------------
class DivineAura:
    def __init__(self, max_radius=280):
        self.max_radius = max_radius
        self.core_glow = create_radial_glow_surface(max_radius, (255, 195, 55, 85))
        self.outer_glow = create_radial_glow_surface(int(max_radius * 1.35), (240, 130, 20, 45))

    def draw(self, surface, center_pos, pulse_factor, time_sec):
        cx, cy = center_pos

        cur_scale = 0.95 + 0.10 * pulse_factor
        w = int(self.core_glow.get_width() * cur_scale)
        h = int(self.core_glow.get_height() * cur_scale)

        if w > 10 and h > 10:
            scaled_glow = pygame.transform.smoothscale(self.core_glow, (w, h))
            rect = scaled_glow.get_rect(center=(cx, cy))
            surface.blit(scaled_glow, rect, special_flags=pygame.BLEND_ADD)

        out_w = int(self.outer_glow.get_width() * (cur_scale * 0.96))
        out_h = int(self.outer_glow.get_height() * (cur_scale * 0.96))
        scaled_outer = pygame.transform.smoothscale(self.outer_glow, (out_w, out_h))
        rect_out = scaled_outer.get_rect(center=(cx, cy))
        surface.blit(scaled_outer, rect_out, special_flags=pygame.BLEND_ADD)

        num_rays = 28
        ray_base_len = 240 + pulse_factor * 22
        ray_surf = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)

        for i in range(num_rays):
            angle = (i * (math.pi * 2 / num_rays)) + (time_sec * 0.07)
            ray_len = ray_base_len + math.sin(i * 3 + time_sec * 2.8) * 16
            alpha = int(35 + 20 * math.sin(i * 2 + time_sec * 2.2))

            ex = cx + math.cos(angle) * ray_len
            ey = cy + math.sin(angle) * ray_len
            pygame.draw.line(ray_surf, (255, 225, 120, alpha), (cx, cy), (ex, ey), 2)

        surface.blit(ray_surf, (0, 0), special_flags=pygame.BLEND_ADD)


# ------------------------------------------------------------------------------
# 10. MAIN ANIMATION CONTROLLER & APPLICATION LOOP
# ------------------------------------------------------------------------------
class GaneshAnimationApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)

        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        self.is_running = True
        self.is_paused = False
        self.is_fullscreen = False
        self.total_time = 0.0

        self.init_fonts()
        self.ganesh_center = (self.width // 2, int(self.height * 0.535))

        # Auto-Sketching Engine
        self.sketch_engine = AutoSketchGaneshEngine(
            self.ganesh_center[0], self.ganesh_center[1], display_size=490
        )

        self.mandala = SacredMandala(radius=280)
        self.divine_aura = DivineAura(max_radius=270)
        self.toran = ToranGarland(self.width)

        self.diyas = [
            DiyaLamp(140, 642, scale=1.15),
            DiyaLamp(310, 658, scale=0.85),
            DiyaLamp(self.width - 310, 658, scale=0.85),
            DiyaLamp(self.width - 140, 642, scale=1.15),
        ]

        self.petals = [FallingPetal(self.width, self.height, start_anywhere=True) for _ in range(50)]
        self.sparkles = [GoldenSparkle(self.width, self.height) for _ in range(70)]
        self.bg_surface = self.create_background_gradient()

    def init_fonts(self):
        for font_name in ["georgia", "palatino", "timesnewroman", "segoeui"]:
            try:
                self.font_title = pygame.font.SysFont(font_name, 54, bold=True)
                break
            except Exception:
                continue
        else:
            self.font_title = pygame.font.Font(None, 60)

        for font_name in ["nirmalaui", "mangal", "segoeui", "arial"]:
            try:
                self.font_subtitle = pygame.font.SysFont(font_name, 25, bold=True)
                break
            except Exception:
                continue
        else:
            self.font_subtitle = pygame.font.Font(None, 30)

        self.font_ui = pygame.font.SysFont("segoeui", 17)
        self.font_banner = pygame.font.SysFont("segoeui", 21, bold=True)

    def create_background_gradient(self):
        surf = pygame.Surface((self.width, self.height))
        for y in range(self.height):
            factor_y = y / self.height
            r = int(COLOR_BG_DARK[0] + (COLOR_BG_MID[0] - COLOR_BG_DARK[0]) * math.sin(factor_y * math.pi))
            g = int(COLOR_BG_DARK[1] + (COLOR_BG_MID[1] - COLOR_BG_DARK[1]) * math.sin(factor_y * math.pi))
            b = int(COLOR_BG_DARK[2] + (COLOR_BG_MID[2] - COLOR_BG_DARK[2]) * math.sin(factor_y * math.pi))
            pygame.draw.line(surf, (r, g, b), (0, y), (self.width, y))
        return surf

    def draw_top_banner(self, surface, time_sec):
        cx = self.width // 2
        title_y = 50

        glow_pulse = 0.8 + 0.2 * math.sin(time_sec * 2.5)
        title_str = "Ganesh Chaturthi"

        shadow_surf = self.font_title.render(title_str, True, COLOR_TEXT_SHADOW)
        surface.blit(shadow_surf, shadow_surf.get_rect(center=(cx + 2, title_y + 3)))

        glow_alpha_val = int(180 * glow_pulse)
        glow_surf = self.font_title.render(title_str, True, (255, 200, 50))
        glow_surf.set_alpha(glow_alpha_val)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            surface.blit(glow_surf, glow_surf.get_rect(center=(cx + dx, title_y + dy)))

        main_title_surf = self.font_title.render(title_str, True, COLOR_GOLD_BRIGHT)
        surface.blit(main_title_surf, main_title_surf.get_rect(center=(cx, title_y)))

        sub_y = title_y + 44
        sub_str = "॥ ॐ गं गणपतये नमः ॥"

        sub_shadow = self.font_subtitle.render(sub_str, True, COLOR_TEXT_SHADOW)
        surface.blit(sub_shadow, sub_shadow.get_rect(center=(cx + 1, sub_y + 2)))

        sub_surf = self.font_subtitle.render(sub_str, True, (255, 220, 130))
        surface.blit(sub_surf, sub_surf.get_rect(center=(cx, sub_y)))

        line_y = sub_y + 20
        line_len = 280

        pygame.draw.line(surface, COLOR_GOLD_DARK, (cx - line_len, line_y), (cx - 45, line_y), 2)
        pygame.draw.line(surface, COLOR_GOLD_BRIGHT, (cx - line_len + 40, line_y), (cx - 45, line_y), 1)

        pygame.draw.line(surface, COLOR_GOLD_DARK, (cx + 45, line_y), (cx + line_len, line_y), 2)
        pygame.draw.line(surface, COLOR_GOLD_BRIGHT, (cx + 45, line_y), (cx + line_len - 40, line_y), 1)

        pygame.draw.circle(surface, COLOR_GOLD_BRIGHT, (cx, line_y), 5)
        pygame.draw.circle(surface, (220, 50, 30), (cx, line_y), 2)
        pygame.draw.circle(surface, COLOR_GOLD_CORE, (cx - 18, line_y), 3)
        pygame.draw.circle(surface, COLOR_GOLD_CORE, (cx + 18, line_y), 3)

    def draw_controls_hud(self, surface):
        info_str = "[SPACE] Pause/Play   [R] Re-sketch   [S] Skip   [F] Fullscreen   [ESC] Exit"
        info_surf = self.font_ui.render(info_str, True, (210, 175, 135))
        surface.blit(info_surf, (self.width - info_surf.get_width() - 25, self.height - 28))

        # Sketch progress indicator
        if not self.sketch_engine.is_completed and self.sketch_engine.total_points > 0:
            pct = int((self.sketch_engine.points_drawn / self.sketch_engine.total_points) * 100)
            status_str = f"Sketching Lord Ganesha: {pct}%"
            status_surf = self.font_ui.render(status_str, True, (255, 215, 120))
            surface.blit(status_surf, (25, self.height - 28))

    def draw_pause_overlay(self, surface):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((15, 3, 8, 140))
        surface.blit(overlay, (0, 0))

        cx = self.width // 2
        cy = self.height // 2

        pause_text = "ANIMATION PAUSED"
        p_surf = self.font_title.render(pause_text, True, COLOR_GOLD_BRIGHT)
        p_rect = p_surf.get_rect(center=(cx, cy - 10))

        bg_rect = p_rect.inflate(60, 24)
        pygame.draw.rect(surface, (45, 12, 22), bg_rect, border_radius=12)
        pygame.draw.rect(surface, COLOR_GOLD_CORE, bg_rect, 3, border_radius=12)
        surface.blit(p_surf, p_rect)

        resume_hint = "Press SPACE to Resume"
        r_surf = self.font_ui.render(resume_hint, True, (255, 235, 180))
        surface.blit(r_surf, r_surf.get_rect(center=(cx, cy + 40)))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

                elif event.key == pygame.K_SPACE:
                    self.is_paused = not self.is_paused

                elif event.key == pygame.K_r:
                    # Re-sketch from scratch
                    self.sketch_engine.reset()

                elif event.key == pygame.K_s:
                    # Skip to completed sketch
                    self.sketch_engine.skip_to_end()

                elif event.key == pygame.K_f:
                    self.is_fullscreen = not self.is_fullscreen
                    if self.is_fullscreen:
                        self.screen = pygame.display.set_mode(
                            (self.width, self.height), pygame.FULLSCREEN | pygame.DOUBLEBUF
                        )
                    else:
                        self.screen = pygame.display.set_mode(
                            (self.width, self.height), pygame.DOUBLEBUF
                        )

    def update(self, dt):
        if self.is_paused:
            return

        self.total_time += dt

        # Update auto-sketching engine
        self.sketch_engine.update(dt)

        for petal in self.petals:
            petal.update(dt, self.total_time)

        for sparkle in self.sparkles:
            sparkle.update(dt)

        for diya in self.diyas:
            diya.update(dt)

    def draw(self):
        self.screen.blit(self.bg_surface, (0, 0))
        self.mandala.draw(self.screen, self.ganesh_center, self.total_time)

        pulse = 0.5 + 0.5 * math.sin(self.total_time * 1.8)
        self.divine_aura.draw(self.screen, self.ganesh_center, pulse, self.total_time)

        for i in range(len(self.sparkles) // 2):
            self.sparkles[i].draw(self.screen, self.total_time)

        # Draw Lord Ganesha Auto-Sketch
        self.sketch_engine.draw(self.screen, self.total_time)

        for i in range(len(self.sparkles) // 2, len(self.sparkles)):
            self.sparkles[i].draw(self.screen, self.total_time)

        for diya in self.diyas:
            diya.draw(self.screen, self.total_time)

        self.toran.draw(self.screen, self.total_time)
        self.draw_top_banner(self.screen, self.total_time)

        for petal in self.petals:
            petal.draw(self.screen, self.total_time)

        self.draw_controls_hud(self.screen)

        if self.is_paused:
            self.draw_pause_overlay(self.screen)

        pygame.display.flip()

    def run(self):
        while self.is_running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = GaneshAnimationApp()
    app.run()
