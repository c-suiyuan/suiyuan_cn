"""Generate scrolling-text GIF for GitHub profile README (left-to-right)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W, H = 900, 220
BG = (255, 255, 255)
FRAMES = 48
FRAME_MS = 60
OUT = ROOT / "assets" / "scroll-bg.gif"

LINES = [
    {
        "text": "SUIYUAN APPRECIATION ZONE ZERO JUSTICE WILL PREVAIL NEVER FORGET YOUR DREAM   ",
        "y": 28,
        "size": 22,
        "color": (161, 161, 170),
        "speed": 3,
    },
    {
        "text": "BELIEVE IN YOURSELF LIGHT BEATS DARKNESS SHINZO SASAGEYO HERO KNIGHT   ",
        "y": 68,
        "size": 18,
        "color": (100, 116, 139),
        "speed": 2,
    },
    {
        "text": "ZENLESS ZONE ZERO CHUANSHI RISHI MENG   ",
        "y": 108,
        "size": 26,
        "color": (113, 113, 122),
        "speed": 4,
    },
    {
        "text": "SUIYUAN KNIGHT DREAM SURMON CODE INSIGHT NEVER GIVE UP   ",
        "y": 148,
        "size": 17,
        "color": (148, 163, 184),
        "speed": 2,
    },
    {
        "text": "KIDS HERO JUSTICE ZZZ EMPTY CALIBER SHINZO SASAGEYO   ",
        "y": 188,
        "size": 20,
        "color": (168, 162, 158),
        "speed": 3,
    },
]


def get_font(size: int):
    for name in ("arialbd.ttf", "Arial Bold.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def measure(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def main():
    probe = Image.new("RGB", (1, 1), BG)
    probe_draw = ImageDraw.Draw(probe)
    for line in LINES:
        line["font"] = get_font(line["size"])
        line["width"] = measure(probe_draw, line["text"], line["font"])

    frames = []
    for f in range(FRAMES):
        img = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(img)
        for line in LINES:
            tw = line["width"]
            offset = (f * line["speed"]) % tw
            x = offset - tw
            draw.text((x, line["y"]), line["text"] * 2, fill=line["color"], font=line["font"])
        frames.append(img)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
    )
    print(f"Saved {OUT} ({FRAMES} frames @ {FRAME_MS}ms)")


if __name__ == "__main__":
    main()
