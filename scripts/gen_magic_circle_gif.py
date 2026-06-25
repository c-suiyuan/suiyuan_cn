"""Generate magic-circle orbital text GIF for GitHub profile README."""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
W, H = 900, 300
BG = (255, 255, 255)
FRAMES = 180
FRAME_MS = 55
OUT = ROOT / "assets" / "scroll-bg.gif"

CENTER_TEXT = "SUIYUAN"
CENTER_SUB = "PROLOGUE"

RINGS = [
    {
        "a": 390,
        "b": 88,
        "cx": 450,
        "cy": 205,
        "tilt": -8,
        "text": "ZENLESS ZONE ZERO · JUSTICE WILL PREVAIL · NEVER FORGET YOUR DREAM · BELIEVE IN YOURSELF · ",
        "size": 13,
        "color": (170, 170, 182),
        "ring": (215, 215, 225),
        "speed": 1.0,
    },
    {
        "a": 300,
        "b": 68,
        "cx": 450,
        "cy": 165,
        "tilt": 12,
        "text": "SHINZO SASAGEYO · HERO KNIGHT · LIGHT BEATS DARKNESS · CODE INSIGHT · ",
        "size": 11,
        "color": (150, 158, 172),
        "ring": (205, 210, 220),
        "speed": -1.35,
    },
    {
        "a": 210,
        "b": 52,
        "cx": 450,
        "cy": 138,
        "tilt": -18,
        "text": "SUIYUAN KNIGHT · DREAM SURMON · CHUANSHI RISHI MENG · NEVER GIVE UP · ",
        "size": 10,
        "color": (140, 148, 162),
        "ring": (200, 205, 215),
        "speed": 1.6,
    },
    {
        "a": 125,
        "b": 34,
        "cx": 450,
        "cy": 118,
        "tilt": 22,
        "text": "KIDS HERO JUSTICE ZZZ EMPTY CALIBER · ",
        "size": 9,
        "color": (130, 138, 152),
        "ring": (195, 200, 210),
        "speed": -2.0,
    },
]


def get_font(size: int, bold: bool = True):
    names = ("arialbd.ttf", "Arial Bold.ttf") if bold else ("arial.ttf", "Arial.ttf")
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def ellipse_point(cx: float, cy: float, a: float, b: float, tilt: float, t: float) -> tuple[float, float]:
    x_local = a * math.cos(t)
    y_local = b * math.sin(t)
    x = cx + x_local * math.cos(tilt) - y_local * math.sin(tilt)
    y = cy + x_local * math.sin(tilt) + y_local * math.cos(tilt)
    return x, y


def tangent_angle(t: float, tilt: float) -> float:
    return math.degrees(t + tilt) + 90


def draw_rotated_text(
    canvas: Image.Image,
    text: str,
    x: float,
    y: float,
    angle: float,
    font,
    fill,
) -> None:
    pad = 4
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    box = probe.textbbox((0, 0), text, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    layer = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (255, 255, 255, 0))
    ImageDraw.Draw(layer).text((pad, pad), text, font=font, fill=fill)
    rotated = layer.rotate(-angle, expand=True, resample=Image.Resampling.BICUBIC)
    canvas.paste(
        rotated,
        (int(x - rotated.width / 2), int(y - rotated.height / 2)),
        rotated,
    )


def draw_rotated_char(
    canvas: Image.Image,
    char: str,
    x: float,
    y: float,
    angle: float,
    font,
    fill,
) -> None:
    size = max(font.size * 2, 24)
    layer = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    ImageDraw.Draw(layer).text((size // 4, size // 4), char, font=font, fill=fill)
    rotated = layer.rotate(-angle, expand=True, resample=Image.Resampling.BICUBIC)
    canvas.paste(
        rotated,
        (int(x - rotated.width / 2), int(y - rotated.height / 2)),
        rotated,
    )


def draw_ring_glow(base: Image.Image, ring: dict) -> None:
    glow = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    draw = ImageDraw.Draw(glow)
    cx, cy = ring["cx"], ring["cy"]
    a, b = ring["a"], ring["b"]
    tilt = math.radians(ring["tilt"])
    points = []
    for i in range(121):
        t = 2 * math.pi * i / 120
        points.append(ellipse_point(cx, cy, a, b, tilt, t))
    draw.line(points + [points[0]], fill=(*ring["ring"], 120), width=2)
    blurred = glow.filter(ImageFilter.GaussianBlur(radius=2))
    base.alpha_composite(blurred)


def draw_orbital_text(
    canvas: Image.Image,
    ring: dict,
    angle_offset: float,
) -> None:
    font = get_font(ring["size"])
    text = ring["text"]
    chars = [c for c in text if c.strip()]
    if not chars:
        return
    tilt = math.radians(ring["tilt"])
    n = len(chars)
    for i, char in enumerate(chars):
        t = angle_offset + (2 * math.pi * i / n)
        x, y = ellipse_point(ring["cx"], ring["cy"], ring["a"], ring["b"], tilt, t)
        draw_rotated_char(canvas, char, x, y, tangent_angle(t, tilt), font, (*ring["color"], 210))


def draw_center_glow(base: Image.Image, pulse: float) -> None:
    glow = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    draw = ImageDraw.Draw(glow)
    cx, cy = 450, 145
    radius = int(70 + pulse * 12)
    draw.ellipse(
        [cx - radius, cy - radius // 2, cx + radius, cy + radius // 2],
        fill=(245, 245, 250, 90),
    )
    for i in range(16):
        angle = pulse * 0.4 + i * math.pi / 8
        x2 = cx + math.cos(angle) * 360
        y2 = cy + math.sin(angle) * 110
        draw.line([(cx, cy), (x2, y2)], fill=(238, 238, 245, 55), width=1)
    blurred = glow.filter(ImageFilter.GaussianBlur(radius=6))
    base.alpha_composite(blurred)


def draw_center_text(canvas: Image.Image) -> None:
    main_font = get_font(28)
    sub_font = get_font(14, bold=False)
    draw_rotated_text(canvas, CENTER_TEXT, 450, 132, -6, main_font, (120, 120, 132, 230))
    draw_rotated_text(canvas, CENTER_SUB, 450, 162, -4, sub_font, (160, 160, 172, 180))


def render_frame(progress: float) -> Image.Image:
    frame = Image.new("RGBA", (W, H), (*BG, 255))
    pulse = math.sin(progress * 2 * math.pi)

    for ring in RINGS:
        draw_ring_glow(frame, ring)

    draw_center_glow(frame, pulse)

    for ring in RINGS:
        angle_offset = progress * 2 * math.pi * ring["speed"]
        draw_orbital_text(frame, ring, angle_offset)

    draw_center_text(frame)

    flat = Image.new("RGB", (W, H), BG)
    flat.paste(frame, mask=frame.split()[3])
    return flat


def main() -> None:
    frames = [render_frame(i / FRAMES) for i in range(FRAMES)]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    duration_sec = FRAMES * FRAME_MS / 1000
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
    )
    print(f"Saved {OUT} ({FRAMES} frames @ {FRAME_MS}ms, loop {duration_sec:.1f}s)")


if __name__ == "__main__":
    main()
