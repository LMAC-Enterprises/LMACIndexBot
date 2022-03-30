"""
Author: QuantumG
Description: Objects of this class are data entities of Hive post data.
"""
class PostEntity:
    """
    CTor.
    """
    def __init__(self):
        
        self.permlink = ""
        self.author = ""
        self.created = ""
        self.body = ""
        self.link = ""
        self.title = ""

    def __str__(self):
        return "Permlink: {permlink}\nAuthor: {author}\nCreated: {created}\nBody:\n{body}\n\n".format(permlink=self.permlink, author=self.author, created=self.created, body=self.body)

    """
    Creates a PostEntity object.
    Parameter (dict): Dictionary. For each field of this entity there must be a key of the same name in the dictionary.
    Returns: An object of the PostEntity class. It is initialized with values from the dictionary.
    """
    def createFromDictionary(dict):

        postEntity = PostEntity()
        postEntity.permlink = dict["permlink"].strip()
        postEntity.author = dict["author"].strip()
        postEntity.body = dict["body"].strip()
        postEntity.title = dict["title"].strip()
        postEntity.created = dict["created"]     
        postEntity.link = dict["category"] + "/@" + dict["author"] + "/" + dict["permlink"]

        return postEntity
