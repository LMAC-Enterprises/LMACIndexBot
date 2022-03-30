class Config:
    mysqlDatabaseName = "test"
    mysqlHost = "localhost"
    mysqlUser = "test
    mysqlPassword = "test"
    indicatorTag = "lil"
    maximumPostsToLoad = 250
    requiredCurator = 'lmac'

    # autor/permlink based Hive post Urls
    hivePostBlacklist = []
    # Image Urls
    imageUrlBlacklist = []
    
    whitelistMode = False
    initialWhitelisterName = "-BOT-"
    initialWhitelist = ["shaka", "quantumg", "agmoore", "mballesteros", "muelli", \
    "cetb2008", "louis88", "tormenta", "jedigeiss", "m1alsan", \
    "justclickindiva", "onyechi", "dwixer"]

    """
    Checks whether a post i blacklisted from being indexed.
    Parameter (author): The author of the post.
    Parameter (permlink): The permlink of the post.
    Returns: True on success.
    """
    def isPostBlacklisted(author, permlink):
        return '@' + author + '/' + permlink in Config.hivePostBlacklist

    """
    Checks whether an Url is blacklisted from being indexed.
    Parameter (url): The url to check.
    Returns: True on success.
    """
    def isImageUrlBlacklisted(url):
        return url in Config.imageUrlBlacklist
