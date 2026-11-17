"""Draw the app icons and splash screens from the heart in the favicon.

Dev-only: needs Pillow (`pip install pillow`), which the app itself doesn't use.
Run from the project root:  python scripts/make_icons.py

Writes:
  static/icons/       icons for the installable web app (manifest + Apple touch icon)
  mobile/assets/      sources that `npx @capacitor/assets generate` turns into every
                      iOS and Android icon and splash size
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
WINE = (59, 10, 36)  # --wine, also the theme color
PLUM = (42, 15, 61)  # --plum
ROSE = (225, 29, 72)  # --rose
BLUSH = (251, 113, 133)  # --rose-soft
SS = 4  # supersampling factor for smooth edges

# The favicon heart, in a -16..16 box: M0 9 C-6 4 -14 -1 -10 -8 C-7 -13 -1 -11 0 -6 C1 -11 7 -13 10 -8 C14 -1 6 4 0 9 Z
HEART = [
    ((0, 9), (-6, 4), (-14, -1), (-10, -8)),
    ((-10, -8), (-7, -13), (-1, -11), (0, -6)),
    ((0, -6), (1, -11), (7, -13), (10, -8)),
    ((10, -8), (14, -1), (6, 4), (0, 9)),
]


def bezier(p0, p1, p2, p3, steps=64):
    for i in range(steps):
        t = i / steps
        u = 1 - t
        yield (
            u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],
        )


def heart_polygon(cx, cy, width):
    # The heart spans x -12..12 and y -11.5..9; centre it optically.
    scale = width / 24
    return [(cx + x * scale, cy + (y + 1.25) * scale) for segment in HEART for x, y in bezier(*segment)]


def gradient(size, top, bottom):
    w, h = size
    column = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        column.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    return column.resize((w, h))


def draw_heart(image, cx, cy, width, glow=True):
    w, h = image.size
    big = (w * SS, h * SS)
    if glow:
        halo = Image.new("L", big, 0)
        ImageDraw.Draw(halo).polygon(heart_polygon(cx * SS, cy * SS, width * 1.08 * SS), fill=150)
        halo = halo.filter(ImageFilter.GaussianBlur(width * 0.09 * SS)).resize((w, h), Image.LANCZOS)
        image.paste(Image.new("RGB", (w, h), BLUSH), (0, 0), halo)
    mask = Image.new("L", big, 0)
    ImageDraw.Draw(mask).polygon(heart_polygon(cx * SS, cy * SS, width * SS), fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    fill = gradient((w, h), BLUSH, ROSE)
    image.paste(fill, (0, 0), mask)
    return image


def icon(size, heart_ratio, transparent=False):
    if transparent:
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        mask = Image.new("L", (size * SS, size * SS), 0)
        ImageDraw.Draw(mask).polygon(heart_polygon(size / 2 * SS, size / 2 * SS, size * heart_ratio * SS), fill=255)
        image.paste(gradient((size, size), BLUSH, ROSE), (0, 0), mask.resize((size, size), Image.LANCZOS))
        return image
    return draw_heart(gradient((size, size), WINE, PLUM), size / 2, size / 2, size * heart_ratio)


def main():
    web = ROOT / "static" / "icons"
    mobile = ROOT / "mobile" / "assets"
    web.mkdir(parents=True, exist_ok=True)
    mobile.mkdir(parents=True, exist_ok=True)

    # Web app. "any" icons can fill the square; "maskable" ones keep the heart inside the 80% safe zone.
    icon(192, 0.62).save(web / "icon-192.png")
    icon(512, 0.62).save(web / "icon-512.png")
    icon(512, 0.48).save(web / "maskable-512.png")
    icon(180, 0.62).save(web / "apple-touch-icon.png")

    # Capacitor sources. App Store icons must be opaque, so icon-only has a full background.
    icon(1024, 0.6).save(mobile / "icon-only.png")
    icon(1024, 0.42, transparent=True).save(mobile / "icon-foreground.png")
    gradient((1024, 1024), WINE, PLUM).save(mobile / "icon-background.png")
    splash = draw_heart(gradient((2732, 2732), WINE, PLUM), 1366, 1366, 520)
    splash.save(mobile / "splash.png")
    splash.save(mobile / "splash-dark.png")
    print(f"Wrote icons to {web.relative_to(ROOT)} and {mobile.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
