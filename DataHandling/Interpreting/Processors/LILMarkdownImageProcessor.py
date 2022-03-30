import re
from DataHandling.Interpreting.Processors.ProcessorBase import ProcessorBase
from DataHandling.Entities.ImageEntity import ImageEntity

class LILMarkdownImageProcessor(ProcessorBase):
    
    MARKDOWN_IMAGE_REGEX = r'!\[LIL\:(.+?)\]\((.+?)\)'
    MARKDOWN_IMAGE_TAGS = r'#(\w+)'

    def parse(self, post):

        images = []

        dataBlocks = self.findImageDataBlocks(post.body)
        if (len(dataBlocks) == 0): return None

        for dataBlock in dataBlocks:
            tagList = self.findImageTagsFields(dataBlock[0])            
            if (len(tagList) == 0): continue
  
            try:
                title = re.sub(self.MARKDOWN_IMAGE_TAGS, '', dataBlock[0])
                url = dataBlock[1]
                tags = ', '.join(tagList)
            except:
                continue
 
            imageEntity = ImageEntity(title.strip(), tags.strip(), url.strip())
            imageEntity.permlink = post.permlink
            imageEntity.author = post.author
            images.append(imageEntity)

        return images

    def findImageDataBlocks(self, data):

        return re.findall(self.MARKDOWN_IMAGE_REGEX, data, re.IGNORECASE | re.DOTALL)

    def findImageTagsFields(self, data):
        found = re.findall(self.MARKDOWN_IMAGE_TAGS, data, re.IGNORECASE | re.DOTALL)
        if (len(found) == 0):
            return []

        return found



