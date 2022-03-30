import mysql.connector
from Config import Config
from DataHandling.Entities.ImageEntity import ImageEntity
from DataHandling.Entities.WhitelistEntity import WhitelistEntity
from DataHandling.Entities.ManualInspectionEntity import ManualInspectionEntity
from random import shuffle
import time

"""
Author: QuantumG
Description: Objects of this class are used to read data from and write data to the database.
"""


class DataHandler:
    IMAGE_TABLE_COL_ID = 0
    IMAGE_TABLE_COL_TITLE = 1
    IMAGE_TABLE_COL_TAGS = 2
    IMAGE_TABLE_COL_URL = 3
    IMAGE_TABLE_COL_PERMLINK = 4
    IMAGE_TABLE_COL_AUTHOR = 5

    WHITELIST_TABLE_COL_AUTHOR = 0
    WHITELIST_TABLE_COL_WHITELISTER = 1
    WHITELIST_TABLE_COL_ADDED = 2

    MANUALINSPECTION_TABLE_COL_LINK = 0
    MANUALINSPECTION_TABLE_COL_NOTICED = 1
    MANUALINSPECTION_TABLE_COL_STATUS = 2

    """
    CTor.
    """

    def __init__(self):

        self.whitelist = {}
        self.manualInspectionEntries = {}
        self.manualInspectionLookup = {}
        self.imageURLLookUpDict = {}
        self.error = ""

        try:
            self.mysqlDb = mysql.connector.connect(
                host=Config.mysqlHost,
                user=Config.mysqlUser,
                password=Config.mysqlPassword
            )
        except(Exception) as e:
            self.error = getattr(e, 'message', repr(e))
            return

        self.mysqlDb = mysql.connector.connect(
            host=Config.mysqlHost,
            user=Config.mysqlUser,
            password=Config.mysqlPassword,
            database=Config.mysqlDatabaseName
        )

        self.loadImageIndex()
        self.loadManualInspections()

    """
    Checks whether an error message currently exist.
    Returns: True on success.
    """

    def hasError(self):
        return len(self.error) > 0;

    """
    Adds initial data from Config.py to the whitelist table in the database.
    """

    def createInitialWhitelist(self):
        cursor = self.mysqlDb.cursor()

        for author in Config.initialWhitelist:
            cursor.execute("INSERT INTO whitelist (author, whitelister, added) VALUES(%s, %s, %s)",
                           (author, Config.initialWhitelisterName, time.time()))
            self.whitelist[author] = WhitelistEntity(author, Config.initialWhitelisterName, time.time())

        self.mysqlDb.commit()

    """
    Checks whether an image URL already exists in the image index.
    Parameter (imageURL): The url of the image.
    Returns: True on success.
    """

    def isImageAlreadyIndexed(self, imageURL):
        return imageURL in self.imageURLLookUpDict

    """
    Loads the entire images table into the runtime image index.
    Returns: Nothing.
    """

    def loadImageIndex(self):
        cursor = self.mysqlDb.cursor()

        cursor.execute("SELECT * FROM images ORDER BY imageid DESC LIMIT 1000")

        qresult = cursor.fetchall()

        for imageRow in qresult:
            imageEntity = ImageEntity(imageRow[self.IMAGE_TABLE_COL_TITLE], imageRow[self.IMAGE_TABLE_COL_TAGS],
                                      imageRow[self.IMAGE_TABLE_COL_URL])
            imageEntity.permlink = imageRow[self.IMAGE_TABLE_COL_PERMLINK]
            imageEntity.author = imageRow[self.IMAGE_TABLE_COL_AUTHOR]
            imageEntity.imageId = int(imageRow[self.IMAGE_TABLE_COL_ID])
            self.imageURLLookUpDict[imageEntity.url] = imageEntity

    """
    Loads the entire whitelist table into the runtime whitelist.
    Returns: Nothing.
    """

    def loadWhitelist(self):
        cursor = self.mysqlDb.cursor()

        cursor.execute("SELECT * FROM whitelist")

        qresult = cursor.fetchall()
        for whitelistRow in qresult:
            self.whitelist[whitelistRow[self.WHITELIST_TABLE_COL_AUTHOR]] = WhitelistEntity(
                whitelistRow[self.WHITELIST_TABLE_COL_AUTHOR], whitelistRow[self.WHITELIST_TABLE_COL_WHITELISTER],
                whitelistRow[self.WHITELIST_TABLE_COL_ADDED])

    def loadManualInspections(self):
        cursor = self.mysqlDb.cursor()

        cursor.execute("SELECT * FROM manual_inspection")

        qresult = cursor.fetchall()
        for manualInspectionRow in qresult:
            self.manualInspectionLookup[
                manualInspectionRow[self.MANUALINSPECTION_TABLE_COL_LINK]] = ManualInspectionEntity(
                manualInspectionRow[self.MANUALINSPECTION_TABLE_COL_LINK],
                manualInspectionRow[self.MANUALINSPECTION_TABLE_COL_NOTICED],
                manualInspectionRow[self.MANUALINSPECTION_TABLE_COL_STATUS])

    """
    Adds or updates an entity in the image index.
    Parameter (imageEntity): The imageEntity to update.
    Returns: Nothing.
    """

    def updateImageIndex(self, imageEntity):

        if (imageEntity.url in self.imageURLLookUpDict):
            imageEntity.imageId = self.imageURLLookUpDict[imageEntity.url].imageId

        self.imageURLLookUpDict.update({imageEntity.url: imageEntity})

    """
    Saves all the changes made on the image index.
    Returns: Nothing.
    """

    def commitAllChanges(self):

        cursor = self.mysqlDb.cursor()

        for imageEntity in self.imageURLLookUpDict.values():

            if (imageEntity.imageId == 0):
                cursor.execute("INSERT INTO images (title, tags, url, permlink, author) VALUES (%s, %s, %s, %s, %s)", (
                imageEntity.title, imageEntity.tags, imageEntity.url, imageEntity.permlink, imageEntity.author))
                imageEntity.imageId = cursor.rowcount
            else:
                cursor.execute(
                    "UPDATE images Set title=%(title)s, tags=%(tags)s, url=%(url)s, permlink=%(permlink)s WHERE imageid=%(imageid)s AND (title<>%(title)s OR tags<>%(tags)s OR url<>%(url)s)",
                    {"title": imageEntity.title, "tags": imageEntity.tags, "url": imageEntity.url,
                     "permlink": imageEntity.permlink, "imageid": imageEntity.imageId})

        for manualInspectionEntity in self.manualInspectionEntries.values():
            cursor.execute("INSERT INTO manual_inspection (link, noticed, status) VALUES(%s, %s, %s)",
                           (manualInspectionEntity.link, manualInspectionEntity.noticed, manualInspectionEntity.status))

        self.mysqlDb.commit()

    """
    Adds a permlink to the "manual inspection" table.
    Parameter (permlink): A string that contains a Hive post link.
    """

    def addToManualInspection(self, link):
        if (link in self.manualInspectionLookup.keys()):
            return

        entry = ManualInspectionEntity(link, time.time(), 0)

        self.manualInspectionEntries[link] = entry
        self.manualInspectionLookup[link] = entry

    """
    Checks whether an author is whitelisted.
    Parameter (permlink): A string that contains an author name (with leading @).
    Returns: True on success.
    """

    def isAuthorWhitelisted(self, author):
        return author in self.whitelist.keys()

    """
    Retrieves the amount of indexed images.
    Returns: An integer number that represents the number of indexed images.
    """

    def getAmountOfIndexedImages(self):
        return len(self.imageURLLookUpDict)

    """
    Performs a cleanup on the existing image data regarding blacklisted posts.
    """

    def cleanupBlacklistedPosts(self):

        toDelete = []
        cursor = self.mysqlDb.cursor()

        for imageEntity in self.imageURLLookUpDict.values():
            if not (Config.isPostBlacklisted(imageEntity.author, imageEntity.permlink) or Config.isImageUrlBlacklisted(
                    imageEntity.url)):
                continue

            cursor.execute('DELETE FROM images WHERE author=%s AND permlink=%s',
                           (imageEntity.author, imageEntity.permlink))
            toDelete.append(imageEntity.url)

        for url in toDelete:
            del self.imageURLLookUpDict[url]

    """
    Retrieves all post links with solved status from manual inspection table.
    Returns: An array of Hive Post links.
    """

    def getManualInspectionLinksWithSolvedStatus(self):
        links = []

        for manualInspectionEntity in self.manualInspectionLookup.values():
            if manualInspectionEntity.status == 3:
                links.append(manualInspectionEntity.link)

        for link in links:
            del self.manualInspectionLookup[link]

        cursor = self.mysqlDb.cursor()
        cursor.execute("DELETE FROM manual_inspection WHERE status=3")
        self.mysqlDb.commit()

        return links


    """
    Retrieves a specific amount post links from manual inspection table.
    Returns: An array of Hive Post links.
    """
    def getManualInspectionLinks(self, maxLinks: int):
        links = list(self.manualInspectionLookup.values())
        shuffle(links)
        links = links[:maxLinks]

        return links

    def removeManualInspectionEntryByLink(self, solvedLink: ManualInspectionEntity):
        cursor = self.mysqlDb.cursor()
        cursor.execute("DELETE FROM manual_inspection WHERE link=%(link)s", {'link': solvedLink})
        self.mysqlDb.commit()
