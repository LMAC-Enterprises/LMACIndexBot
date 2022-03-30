import sys
from DataHandling.Entities.ImageEntity import ImageEntity
from DataHandling.Interpreting.Processors.LILTableProcessor import LILTableProcessor
from DataHandling.Interpreting.Processors.LILMarkdownImageProcessor import LILMarkdownImageProcessor
from DataHandling.Interpreting.Processors.ProcessorBase import ProcessorBase

"""
    Author: quantumg
    Description: Objects of this class can hive post bodies to extract LIL image data.
"""
class BodyParser:
    
    
    """
    Parses the body field of a PostEntity object for finding LIL image data.
    Parameter (post): The PostEntity object.
    Returns: Retrieves an array of ImageEntity objects on success. Otherwise None.
    """
    def parse(self, post):

        images = []
        processors = [LILTableProcessor()] #, LILMarkdownImageProcessor()]

        for processor in processors: 
            imagesFromTable = processor.parse(post)
            if (imagesFromTable != None):                 
                images.extend(imagesFromTable)  
                
        return images if (len(images) > 0) else None


