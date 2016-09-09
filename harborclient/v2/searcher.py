"""
User interface.
"""

import base64

from oslo_utils import encodeutils
import six
from six.moves.urllib import parse

from harborclient import api_versions
from harborclient import base
from harborclient import exceptions
from harborclient.i18n import _


class SearchManager(base.Manager):
    def list(self):
        pass

    def search(self, query):
        """ Search for projects and repositories. """
        return self.api.client.get("/search?q=%s" % query)
