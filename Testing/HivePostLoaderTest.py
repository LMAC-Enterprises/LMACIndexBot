from Io.Networking.HivePostLoader import HivePostLoader
from Io.Networking.PostEntity import PostEntity
from Config import Config

print("Starting HivePostLoader test")

Config.maximumPostsToLoad = 20

hivePostLoader = HivePostLoader()


assert hivePostLoader.fetch(), "Fetch shouldn't return False. There must be an error: " + hivePostLoader.error

while (hivePostLoader.isPostAvailable()):
    postEntity = hivePostLoader.next()
    print(postEntity)

