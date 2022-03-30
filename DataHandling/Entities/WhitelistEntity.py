"""
Author: quantumg
Description: Objects of this class are data entities which contains whitelist datasets.
"""
class WhitelistEntity:
    
    def __init__(self, author, whitelister, added):
        self.author = author
        self.whitelister = whitelister
        self.added = added
