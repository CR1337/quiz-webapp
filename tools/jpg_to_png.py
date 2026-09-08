from PIL import Image
import sys
import os


if len(sys.argv) < 2:
    print("You must specify a jpg file!", file=sys.stderr)
    exit(1)

in_filename = sys.argv[1]

if not in_filename.endswith(".jpg") and not in_filename.endswith(".jpeg"):
    print("You must specify a jpg file!", file=sys.stderr)
    exit(1)

out_filename = f"{in_filename.split('.')[0]}.png"

image = Image.open(in_filename)
image.save(out_filename)

os.remove(in_filename)
