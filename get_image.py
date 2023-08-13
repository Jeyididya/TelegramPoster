""" import Modules """
import requests
from PIL import Image


class GETIMAGE:
    """
    _Download Image from pexels_
    """

    def __init__(self):
        self.header = {
            "Authorization": "563492ad6f91700001000001cdf5c4ba754b4bb1b220822ab9d8426b"}
        self.base_url = "https://api.pexels.com/v1/"

    def save_image(self, image_url, image_name, photographer, color_code):
        """
        _ save image to local_

        Args:
            image_url (_str_): _image url_
            image_name (_str_): _image name_
            photographer (_str_): _name of phototgrapher_
            color_code (_str_): _color code of image_
        """
        img = Image.open(requests.get(image_url, stream=True).raw)

        img.save(
            f'./downloads/{image_name} b7 {photographer}_{color_code}.jpg')
        return f'./downloads/{image_name} b7 {photographer}_{color_code}.jpg'

    def check_image_id(self, image_id):
        """
        _check if image is already used_

        Args:
            image_id (_str_): _descripti_

        Returns:
            _type_: _description_
        """
        file_ = open("image_id.txt", "r", encoding="utf-8").readlines()
        for file_id in file_:
            if str(image_id) == str(file_id).strip():
                return True
        open("image_id.txt", "a", encoding="utf-8").write(str(image_id)+"\n")
        print("found new image")
        return False

    def search_image(self, text, color=""):
        if color != "":
            search = self.base_url + \
                "search?query={}&color={}&orientation=square".format(
                    text, color)
        else:
            search = self.base_url + \
                "search?query={}&orientation=square".format(text)

        response = requests.get(search, headers=self.header)

        for image in response.json()['photos']:
            # print("-->",images['alt'])
            # TODO check id of picture before downloading
            if not self.check_image_id(image["id"]):
                try:
                    # print("saved file->",self.save_image(image['src']['original'],image['alt'],image["photographer"],image["avg_color"]))
                    return self.save_image(image['src']['original'], image['alt'], image["photographer"], image["avg_color"])
                except Exception as e:
                    print("Exception happend", e)
                    continue

    # def test(self):
    #     search=self.base_url
    #     response=requests.get(search,headers=self.header)
    #     print("->",response)


# getImage=GET_IMAGE()
# getImage.search_image("friends")
# getImage.test()
