"""
Author: quantumg
Description: Objects of this class are data entities which contains manual inspection datasets.
"""
class ManualInspectionEntity:
    
    def __init__(self, link, noticed, status):
        self.link = link
        self.noticed = noticed
        self.status = status
