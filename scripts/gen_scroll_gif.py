"""Generate diagonal elliptical scrolling-text GIF for GitHub profile README."""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H = 900, 260
BG = (255, 255, 255)
FRAMES = 240
FRAME_MS = 45
OUT = ROOT / "assets" / "scroll-bg.gif"

LINES = [
    {
        "text": "SUIYUAN APPRECIATION ZONE ZERO JUSTICE WILL PREVAIL NEVER FORGET YOUR DREAM   ",
        "base_y": 24,
        "size": 22,
        "color": (161, 161, 170),
        "angle": -7,
        "ellipse_a": 14,
        "ellipse_b": 6,
        "phase": 0.0,
    },
    {
        "text": "BELIEVE IN YOURSELF LIGHT BEATS DARKNESS SHINZO SASAGEYO HERO KNIGHT   ",
        "base_y": 68,
        "size": 18,
        "color": (100, 116, 139),
        "angle": 5,
        "ellipse_a": 10,
        "ellipse_b": 5,
        "phase": 1.2,
    },
    {
        "text": "ZENLESS ZONE ZERO CHUANSHI RISHI MENG   ",
        "base_y": 112,
        "size": 26,
        "color": (113, 113, 122),
        "angle": -3,
        "ellipse_a": 12,
        "ellipse_b": 7,
        "phase": 2.4,
    },
    {
        "text": "SUIYUAN KNIGHT DREAM SURMON CODE INSIGHT NEVER GIVE UP   ",
        "base_y": 156,
        "size": 17,
        "color": (148, 163, 184),
        "angle": -5,
        "ellipse_a": 11,
        "ellipse_b": 5,
        "phase": 0.8,
    },
    {
        "text": "KIDS HERO JUSTICE ZZZ EMPTY CALIBER SHINZO SASAGEYO   ",
        "base_y": 198,
        "size": 20,
        "color": (168, 162, 158),
        "angle": 6,
        "ellipse_a": 13,
        "ellipse_b": 6,
        "phase": 1.8,
    },
]


def get_font(size: int):
    for name in ("arialbd.ttf", "Arial Bold.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def measure_text(text: str, font) -> tuple[int, int]:
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    box = probe.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def build_strip(text: str, font, color, repeat: int = 4, pad: int = 16) -> tuple[Image.Image, int]:
    tw, th = measure_text(text, font)
    strip = Image.new("RGBA", (tw * repeat, th + pad * 2), (255, 255, 255, 0))
    draw = ImageDraw.Draw(strip)
    draw.text((0, pad), text * repeat, fill=(*color, 255), font=font)
    return strip, tw


def paste_scrolling_line(
    canvas: Image.Image,
    strip: Image.Image,
    text_width: int,
    angle: float,
    base_y: int,
    progress: float,
    ellipse_a: float,
    ellipse_b: float,
    phase: float,
) -> None:
    rotated = strip.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    scroll = progress * text_width
    theta = progress * 2 * math.pi + phase
    ellipse_x = ellipse_a * math.cos(theta)
    ellipse_y = ellipse_b * math.sin(theta)

    x = (W - rotated.width) // 2 - scroll * cos_a + ellipse_x
    y = base_y - scroll * sin_a + ellipse_y
    canvas.paste(rotated, (int(x), int(y)), rotated)


def main() -> None:
    prepared = []
    for line in LINES:
        font = get_font(line["size"])
        strip, text_width = build_strip(line["text"], font, line["color"])
        prepared.append({**line, "font": font, "strip": strip, "text_width": text_width})

    frames = []
    for frame_idx in range(FRAMES):
        progress = frame_idx / FRAMES
        img = Image.new("RGB", (W, H), BG)
        for line in prepared:
            paste_scrolling_line(
                img,
                line["strip"],
                line["text_width"],
                line["angle"],
                line["base_y"],
                progress,
                line["ellipse_a"],
                line["ellipse_b"],
                line["phase"],
            )
        frames.append(img)

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
    print(f"Saved {OUT} ({FRAMES} frames @ {FRAME_MS}ms, loop {duration_sec:.1f}s, seamless)")


if __name__ == "__main__":
    main()
