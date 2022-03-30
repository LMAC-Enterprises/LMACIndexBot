import re
from DataHandling.Entities.ImageEntity import ImageEntity
from urllib.parse import urlparse
from DataHandling.Interpreting.Processors.ProcessorBase import ProcessorBase

class LILTableProcessor(ProcessorBase):

    # IMAGE_DATA_BLOCK_REGEX = r'<table class=\"lil\">[\n]+.*?</table>'  # Origin regex!
    # IMAGE_DATA_ROW_REGEX = r'<tr>[\n]+.*?<\/tr>'  # Origin regex!
    # IMAGE_TITLE_REGEX = r'<td class=\"lil-title\">(.+?)</td>'  # Origin regex!
    # IMAGE_URL_REGEX = r'<td class=\"lil-image\"><img src=\"(.+?)\" width=\"[0-9]+\"/></td>'  # Origin regex!
    IMAGE_DATA_BLOCK_REGEX = r'<table class=\"lil\">\s+.*</table>'
    IMAGE_DATA_ROW_REGEX = r'<tr>\s*.*?<\/tr>'
    IMAGE_TITLE_REGEX = r'<td class=\"lil-title\">(.+?)</td>'
    IMAGE_TAGS_REGEX = r'<td class=\"lil-tags\">(.+?)</td>'
    IMAGE_URL_REGEX = r'<td class\s*=\s*\"lil-image\"\s*>\s*<img src\s*=\s*\"(.+?)\"\s*width\s*=\s*\"[' \
                      r'0-9]+\"\s*/>\s*</td> '

    """
    Ctor
    """
    def __init__(self):
        
        self.cleanr = re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    def parse(self, post):
        if (len(post.body) == 0): return None

        dataBlocks = self.findImageDataBlock(post.body)
        if (len(dataBlocks) == 0): 
            return None
 
        images = []

        for dataBlock in dataBlocks:
            dataRows = self.findImageDataRows(dataBlock)
            if (len(dataRows) == 0):                
                continue                      
            
            for dataRow in dataRows:
                
                title = self.cleanHtml(self.extractTitleFromDataRow(dataRow))
                tags = self.cleanHtml(self.extractTagsFromDataRow(dataRow))
                url = self.extractURLFromDataRow(dataRow)
                
                if (self.isURLValid(url) == False): 
                    continue
                if (title == None or tags == None): 
                    continue
            
                imageEntity = ImageEntity(title.strip(), tags.strip().lower(), url.strip())
                imageEntity.permlink = post.permlink
                imageEntity.author = post.author
                
                images.append(imageEntity)             
        
        return images

    

    """
    Finds and extracts the data block that identifies the image donation in a Hive post body.
    Parameters (data): Text.
    Returns: an array of datablocks on success. Otherwise an empty array.
    """
    def findImageDataBlock(self, data):
    
        return re.findall(self.IMAGE_DATA_BLOCK_REGEX, data, re.IGNORECASE | re.DOTALL)

    """
    Finds and extracts all data rows that identifies the descriptive fields of a string that was extracted by findImageDataBlock (Title, tags, etc...).
    Parameters (data): Text.
    Returns: An array of strings that contains single image-data rows.
    """
    def findImageDataRows(self, dataBlock):
        
        return re.findall(self.IMAGE_DATA_ROW_REGEX, dataBlock, re.IGNORECASE | re.DOTALL)

    """

    """
    def extractTitleFromDataRow(self, dataRow):
        found = re.search(self.IMAGE_TITLE_REGEX, dataRow, re.IGNORECASE | re.DOTALL)
        if (not found):
            return None
 
        return str(found.groups(1)[0])

    """

    """
    def extractTagsFromDataRow(self, dataRow):
        found = re.search(self.IMAGE_TAGS_REGEX, dataRow, re.IGNORECASE | re.DOTALL)
        if (not found):
            return None

        return str(found.groups(1)[0])

    """

    """
    def extractURLFromDataRow(self, dataRow):
        found = re.search(self.IMAGE_URL_REGEX, dataRow, re.IGNORECASE | re.DOTALL)
        if (not found):
            return None

        return str(found.groups(1)[0])

    """
    Removes all HTML code from a text.
    Parameter (text): Text.
    Returns: Returns the cleaned text on success. None if the input string was None.
    """
    def cleanHtml(self, text):
        if (text  is None): return None
 
        return re.sub(self.cleanr, '', text)

    """
    Checks wether an URL is valid.
    Parameter (url): The URL string.
    Returns: True on success. Otherwise False.
    """
    def isURLValid(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc, result.path])
        except:
            return False
