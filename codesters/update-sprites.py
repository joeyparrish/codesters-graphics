#!/usr/bin/env python3

import json
import os
import urllib.request


IMAGE_API = "https://www.codesters.com/api/SpriteImage/"

BASE_URL = "https://d2ctfgu73hw6a8.cloudfront.net/prod_media/"

TYPE_SPRITE = "sprite"
TYPE_BACKGROUND = "background"
TYPE_SOUND = "sound"

SPRITE_METADATA_PATH = "sprites.json"
BACKGROUND_METADATA_PATH = "backgrounds.json"


def fetch(url):
    request = urllib.request.Request(url)
    # The API rejects requests from urllib, but allows curl...
    request.add_header("User-Agent", "curl/7.88.1")
    return urllib.request.urlopen(request).read()


def fetch_api(url):
    json_data = fetch(url)
    return json.loads(json_data)["results"]


print("Fetching image data from API...")
images = fetch_api(IMAGE_API)
print("Done.")

sprites = {}
backgrounds = {}

for image in images:
    # Ex: {"name": "zombie3", "url": "sprite_images_default/zombie3.png", "type": "sprite"}
    name = image["name"]
    url = image["url"]
    image_type = image["type"]

    if image_type == TYPE_SOUND:
      continue

    filename = url.split("/")[-1]
    path = "sprites/{}".format(filename)

    if image_type == TYPE_SPRITE:
        sprites[name] = path
    elif image_type == TYPE_BACKGROUND:
        backgrounds[name] = path
    else:
        # Unrecognized, skip it
        print("Unrecognized type: {}".format(image_type))
        continue

    if not os.path.exists(path):
        print("Downloading \"{}\" ({})".format(name, filename))
        with open(path, "wb") as f:
            f.write(fetch(BASE_URL + url))

print("Writing metadata...")
with open(SPRITE_METADATA_PATH, "w") as f:
  f.write(json.dumps(sprites, indent=2))
with open(BACKGROUND_METADATA_PATH, "w") as f:
  f.write(json.dumps(backgrounds, indent=2))
print("Done.")
