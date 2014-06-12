#!/usr/bin/python

import sys, requests
from PIL import Image, ImageEnhance
from io import BytesIO

from constants import *
from instagram import client

CONFIG = {
    'client_id': FADE_CLIENT_ID,
    'client_secret': FADE_CLIENT_SECRET
}
unauthenticated_api = client.InstagramAPI(**CONFIG)

def main():

    # Get the user's Instagram ID
    try:
        username = sys.argv[1]
        user_data = unauthenticated_api.user_search(username, 1)
        user_id = user_data[0].id
    except:
        print "No ID was found for the given username."
	return

    # Get the user's recent public media
    try:
        media, next =  unauthenticated_api.user_recent_media(user_id=user_id, count=1, max_id=None)
    except:
        print "An error occurred while fetching the user media."
	return

    # Manipulate the first image and save to disk
    try:
	url = media[0].images['standard_resolution'].url
    	response = requests.get(url)
    	img = Image.open(BytesIO(response.content))

	img = fade_image(img)
	img.save('image.jpg')
    except:
	print "An error occurred while proccessing the image."

    print "Done."
    return

def fade_image(img):
    color_enhancer = ImageEnhance.Color(img)
    img = color_enhancer.enhance(0.5)

    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(0.5)

    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(1.5)

    return img

if __name__ == "__main__":
    main()
