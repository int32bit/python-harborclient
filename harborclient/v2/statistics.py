from harborclient import base


class StatisticsManager(base.Manager):
    def list(self):
        """Get statistics data.

        :rtype: list of :class:`Statistics`
        """
        return self._list("/statistics")
