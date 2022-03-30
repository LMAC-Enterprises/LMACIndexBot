#!/usr/bin/python

import sys
import logging
import time

from DataHandling.DataHandler import DataHandler
from DataHandling.Interpreting.BodyParser import BodyParser
from Io.Networking.HivePostLoader import HivePostLoader
from Config import Config

"""
    Author: quantumg
    Description: Contains the bootstrap logic.
"""


class Bot:

    def __init__(self):
        parameters = sys.argv

        self.debugMode = False

        if len(parameters) > 1 and parameters[1] == "debug":
            self.debugMode = True

        loglevel = logging.DEBUG if self.debugMode else logging.INFO
        logging.basicConfig(filename="LMACIndexBot.log", format='%(levelname)s (%(asctime)s): %(message)s',
                            datefmt='%d-%m-%Y %H:%M:%S', level=loglevel)
        self.logger = logging.getLogger('LMACIndexBot_Log')

        self.dataHandler = DataHandler()

    """
    Logs messages. But only when the debug mode is activated.
    Parameter (message): The message to be logged.
    """

    def debug(self, message):
        self.logger.info(message)
        if not self.debugMode: return
        print(message)

    """
    Main function. Runs the bootstrap.
    """

    def execute(self):

        if self.dataHandler.hasError():
            self.logger.error(self.dataHandler.error)
            return

        # Cleanup blacklisted image posts
        self.dataHandler.cleanupBlacklistedPosts()

        # Loading Hive Posts

        self.debug("Loading Hive posts...")
        hivePostLoader = HivePostLoader(self.dataHandler.getManualInspectionLinksWithSolvedStatus())
        if not hivePostLoader.fetch():
            self.logger.error("Couldn't load Hive posts: " + hivePostLoader.error)
            return;
        self.debug("Loaded posts: " + str(hivePostLoader.countPosts()))

        # Parsing Hive post bodies

        bodyParser = BodyParser()

        self.debug("Parsing Hive Posts...")

        amountOfImages = 0

        while hivePostLoader.isPostAvailable():
            post = hivePostLoader.next()

            if Config.whitelistMode and self.dataHandler.isAuthorWhitelisted(post.author) == False:
                self.dataHandler.addToManualInspection(post.link)
                continue

            images = bodyParser.parse(post)

            if images is None:
                self.dataHandler.addToManualInspection(post.link)
                continue

                # Adding image data to the database

            for imageEntity in images:

                if Config.isPostBlacklisted(imageEntity.author, imageEntity.permlink) or Config.isImageUrlBlacklisted(
                        imageEntity.url):
                    self.logger.info('Blacklisted image {permlink} skipped.'.format(permlink=imageEntity.permlink))
                    continue

                self.dataHandler.updateImageIndex(imageEntity)
                amountOfImages += 1

        self.debug("Added images: " + str(amountOfImages))
        self.debug("Images in database: " + str(self.dataHandler.getAmountOfIndexedImages()))

        self.dataHandler.commitAllChanges()

        self.debug("Finished!")

    def executeSpecificPostMode(self, permlink, returnSuccess: bool = False):
        print('Start processing post.')
        bodyParser = BodyParser()

        print('Loading database.')
        if self.dataHandler.hasError():
            self.logger.error(self.dataHandler.error)
            if returnSuccess:
                return False
            return
        hivePostLoader = HivePostLoader()
        print('Loading post.')
        post = hivePostLoader.fetchSinglePost(permlink)
        if not post:
            print('Error. Can\'t load post.')
            if returnSuccess:
                return False
            return

        print('Parsing post.')
        images = bodyParser.parse(post)

        if images is None:
            print('Error. No images found.')
            if returnSuccess:
                return False
            return

        for imageEntity in images:
            self.dataHandler.updateImageIndex(imageEntity)
        print('Saving images.')
        self.dataHandler.commitAllChanges()
        print('Finished. Added {imageCount}'.format(imageCount=len(images)))

        if returnSuccess:
            return True

    def executeReprocessWastedPostsMode(self, maxPosts: int):
        solvedLinks = 0
        print('Start processing posts.')

        inspectionEntries = self.dataHandler.getManualInspectionLinks(maxPosts)

        for inspectionEntry in inspectionEntries:
            print('Trying to solve {link}'.format(link=inspectionEntry.link))
            if self.executeSpecificPostMode(inspectionEntry.link.replace('hive-174695/', ''), True):
                self.dataHandler.removeManualInspectionEntryByLink(inspectionEntry.link)
                solvedLinks += 1
            print('')
            time.sleep(1)

        print('Solved {amount} posts.'.format(amount=solvedLinks))



# PROGRAM START
bot = Bot()
if len(sys.argv) > 2 and sys.argv[1] == "sp":
    bot.executeSpecificPostMode(sys.argv[2])
elif len(sys.argv) > 2 and sys.argv[1] == "r":
    bot.executeReprocessWastedPostsMode(int(sys.argv[2]))
else:
    bot.execute()
