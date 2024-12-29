# Copyright Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import os

import ulid

PHOTO_URL = "https://photos.pbarker.dev"
if os.path.exists(".photo_url"):
    with open(".photo_url", "r") as f:
        PHOTO_URL = f.read().strip()


def write_image(line, f):
    id_raw = None
    flickr_url = None
    pixelfed_url = None
    while line.startswith("$$"):
        tag, arg, line = line.split(maxsplit=2)
        if tag == "$$IMAGE":
            id_raw = arg
        elif tag == "$$FLICKR":
            flickr_url = arg
        elif tag == "$$PIXELFED":
            pixelfed_url = arg
        else:
            print(f"Unrecognized tag: {tag}")
            return
    alt_text = line

    if not id_raw:
        print("Missing $$IMAGE tag")
        return

    id = ulid.ULID.from_str(id_raw.upper())
    shard = id.hex[-4:]
    id = str(id).lower()
    url = f"{PHOTO_URL}/{shard}/{id}/{id}"

    f.write(".. raw:: html\n")
    f.write("\n")
    f.write("    <div class=\"figure\">\n")
    f.write("      <picture>\n")
    f.write(f"        <source srcset=\"{url}_960.webp, {url}_1920.webp 2x\" type=\"image/webp\" />\n")
    f.write(f"        <source srcset=\"{url}_960.jpg, {url}_1920.jpg 2x\" type=\"image/jpeg\" />\n")
    f.write(f"        <img src=\"{url}_960.jpg\" alt=\"{alt_text.strip()}\" style=\"width:100%\" />\n")
    f.write("      </picture>\n")
    f.write("      <p class=\"text-sm text-right download-links\">\n")
    f.write("        Download WebP:\n")
    f.write(f"        <a href=\"{url}_960.webp\">960px</a>,\n")
    f.write(f"        <a href=\"{url}_1920.webp\">1920px</a>,\n")
    f.write(f"        <a href=\"{url}_3840.webp\">3840px</a>,\n")
    f.write(f"        <a href=\"{url}.webp\">Lossless</a>\n")
    f.write("        <br />\n")
    f.write("        Download JPEG:\n")
    f.write(f"        <a href=\"{url}_960.jpg\">960px</a>,\n")
    f.write(f"        <a href=\"{url}_1920.jpg\">1920px</a>,\n")
    f.write(f"        <a href=\"{url}_3840.jpg\">3840px</a>\n")
    if flickr_url or pixelfed_url:
        f.write("        <br />\n")
        f.write("        Also available on:\n")
        if flickr_url:
            sep = "," if pixelfed_url else ""
            f.write(f"        <a href=\"{flickr_url}\">Flickr</a>{sep}\n")
        if pixelfed_url:
            f.write(f"        <a href=\"{pixelfed_url}\">Pixelfed</a>\n")
    f.write("      </p>\n")
    f.write("    </div>\n")


def main():
    photography_dir = os.path.dirname(__file__)
    top_dir = os.path.dirname(photography_dir)
    output_dir = f"{top_dir}/content/photography"

    os.makedirs(output_dir, exist_ok=True)

    for fname in os.listdir(photography_dir):
        if not fname.endswith(".rst"):
            continue

        input_path = f"{photography_dir}/{fname}"
        output_path = f"{output_dir}/{fname}"
        with open(input_path, "r") as f_in, open(output_path, "w") as f_out:
            for line in f_in:
                if line.startswith("..$$"):
                    write_image(line[2:], f_out)
                else:
                    f_out.write(line)


main()
