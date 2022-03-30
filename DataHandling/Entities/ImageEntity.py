"""
Author: QuantumG
Description: Objects of this class are data entities of image data.
"""
class ImageEntity:
    """
    CTor.
    Parameters (title): The title of the image.
    Parameters (tags): Comma seperated tags of the image.
    Parameters (url): The URL that leads to the image.
    """
    def __init__(self, title, tags, url):
        self.title = title
        self.tags = tags
        self.url = url
        self.imageId = 0       
        self.permlink = "" 

    def __str__(self):
        return "Permlink: {permlink}\nImageId: {imageid}\nUrl: {url}\nTags:{tags}\nTitle:\n{title}\n\n".format(permlink=self.permlink, imageid=self.imageId, tags=self.tags, url=self.url, title=self.title)

        