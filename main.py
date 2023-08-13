""" import needed Modules """
import textwrap
import random
import os
from time import sleep
from get_quotes import QUOTE
# from get_image import *
from get_image import GETIMAGE
# from edit_photo import *
from edit_photo import EDIT_IMAGE
from telegram_api import bot, channlel_name

words = ["friend", "car", "alone", "lonely", "sad", "wealth"]


def check_text(quote):
    """
    Check if text needs wrapping

    Args:
        quote (_str_): _text to be checked_

    Returns:
        _bool_: _true if need wrapping false otherwise_
    """
    lines = textwrap.wrap(quote["quote"], 56)
    if len(lines) < 4:
        return True
    return False


def start():
    """
    _Driver function_
    """
    quote = QUOTE()
    get_image = GETIMAGE()
    _quote = quote.get_quote()
    if check_text(_quote):

        file_name = get_image.search_image(random.choice(words))
        image = EDIT_IMAGE(file_name)
        file_name_edited = image.add_text(_quote["quote"], _quote["author"])
        os.remove(file_name)  # type: ignore
        return file_name_edited
    else:

        start()


def post_insta(file_name, sleep_time):
    """
    _Post given image to instagram_

    Args:
        file_name (_str_): _file name of the image_
        sleep_time (_int_): _sleept time duration_
    """
    photographer = file_name.split("b7")[1].split("_")[0]
    caption = f"📸 Photographer {photographer},\n🖼 Image from [Pexeles](https://www.pexels.com/) \n\
Quote from [themotivate365](https://api.themotivate365.com/stoic-quote)\n🕔next post in {sleep_time} sec"
    with open(file_name, 'rb') as photo:
        bot.send_photo(chat_id=channlel_name, photo=photo,
                       caption=caption, parse_mode="Markdown")
    # cl.upload_photo(
    #     file_name,
    #     caption
    # )

    os.remove(filename)  # type: ignore


times = [10, 13, 11, 6]

try:
    os.mkdir("downloads")
    os.mkdir("photos")
except FileExistsError:
    pass


while True:
    filename = start()
    sleep_time = random.choice(times)
    if filename is not None:
        post_insta(filename, sleep_time)

    else:
        continue
    print("sleeping for ", sleep_time*60)

    sleep(int(sleep_time))
