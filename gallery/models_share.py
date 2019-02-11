"""
This module aims to create a model having the filesystem as backend, since
if someone don't want to add extra metadata more than the metadata given
by the file informations is useless to use a database.

TODO: traverse directory.
"""
from flask import current_app
from werkzeug.utils import secure_filename

import os


class FilesystemObjectDoesNotExist(Exception):
    pass

class FilesystemObject_share(object):
    def __init__(self, filename, post=None, root=None):
        """Create an object from the information of the given filename or from a
        uploaded file.

        Example of usage:

            if request.method == 'POST' and 'photo' in request.POST:
                f = FilesystemObject('cats.png', request.POST['photo'])

        """

        self.root_dir = current_app.config['GALLERY_ROOT_SHARE_DIR']
        self.filename = filename if not post else secure_filename(post.filename)
        self.abspath  = os.path.join(self.root_dir, filename)

        if post:
            self.upload(post)

        try:
            stats = os.stat(self.abspath)
        except IOError as e:
            raise FilesystemObjectDoesNotExist(e.message)

        self.timestamp = stats.st_mtime



    @classmethod
    def all(cls, root):
        """Return a list of files contained in the directory pointed by settings.GALLERY_ROOT_DIR.
        """
        return [cls(x) for x in os.listdir(root)]

class Images_share(FilesystemObject_share):
    pass

