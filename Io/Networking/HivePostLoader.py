import sys

from beem.comment import Comment
from Io.Networking.PostEntity import PostEntity
from beem.discussions import Query, Discussions_by_created
from beem.exceptions import OfflineHasNoRPCException, AccountDoesNotExistsException
from Config import Config

"""
    Author: quantumg
    Description: Objects of this class can load LIL tagged hive posts and translate it to objects of the PostEntity class.
"""


class HivePostLoader:
    LMAC_CATEGORY = "hive-174695"
    LIL_PREFIXES = ['LIL:', 'LIL-', 'LIL -', 'LIL :', 'LIL.', 'lil:', 'lil-', 'lil -', 'lil :', 'lil.', '#lil', '#LIL', 'LIL ', 'lil ']

    def __init__(self, hivePostLinksToReload=None):

        self.postEntities = []
        self.error = ""
        self.current = None
        self.hivePostLinksToReload = hivePostLinksToReload

    def _hasPostRequiredCurator(self, post):
        try:
            return post.get_vote_with_curation(Config.requiredCurator, True) is not None
        except AccountDoesNotExistsException:
            return False

    def _hasPostRequiredTitlePrefix(self, post):
        for prefix in self.LIL_PREFIXES:
            if post.title.startswith(prefix):
                return True

        return False

    """
        Fetches all available active hive posts tagged with #LIL and adds them to the internal iteration queue.
        Returns: True on success
    """

    def fetch(self):

        self.fetchPostsToReload()

        q = Query(limit=100, tag=Config.indicatorTag)

        try:

            for post in Discussions_by_created(q):

                if post.category != self.LMAC_CATEGORY:
                    continue
                if not self._hasPostRequiredTitlePrefix(post):
                    continue
                if not self._hasPostRequiredCurator(post):
                    continue

                self.postEntities.append(PostEntity.createFromDictionary(post))

            return True
        except OfflineHasNoRPCException as e:
            self.error = "Offline. " + getattr(e, 'message', repr(e))
        except Exception as e:
            self.error = "Can't fetch posts. " + getattr(e, 'message', repr(e))
            return False

    """
        Looks if there are still posts in the iteration queue.
        Returns: True on success
    """

    def isPostAvailable(self):
        return self.postEntities is not None and len(self.postEntities) > 0

    """
        Retrieves the next hive post from the iteration queue, if available.
        Returns: An object of the PostEntity class on success. Otherwise None.
    """

    def next(self):

        if not self.isPostAvailable():
            return None

        current = self.postEntities[0]

        del self.postEntities[0]

        return current

    """
    Retrieves the amount of available posts in the iteration queue.
    Returns: A number.
    """

    def countPosts(self):
        return len(self.postEntities)

    """
    Loads all posts that should be reload for indexing again.
    """

    def fetchPostsToReload(self):

        for link in self.hivePostLinksToReload:
            post = Comment(link)
            self.postEntities.append(PostEntity.createFromDictionary(post))

    """
    Loads a single posts that should be added to the index.
    """
    def fetchSinglePost(self, permlink):
        try:
            post = Comment(permlink)
        except OfflineHasNoRPCException as e:
            print('OFFLINE')
            return None
        except Exception as e:
            print(e)
            return None

        return PostEntity.createFromDictionary(post)
