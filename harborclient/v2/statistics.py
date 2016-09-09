"""
User interface.
"""

import base64

from oslo_utils import encodeutils
import six
from six.moves.urllib import parse

from harborclient import api_versions
from harborclient import base
from harborclient import exceptions as exp
from harborclient.i18n import _


class StatisticsManager(base.Manager):
    def list(self):
        """
        Get statistics data.

        :rtype: list of :class:`Project`

        """
        return self._list("/statistics")
