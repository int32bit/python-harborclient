from harborclient import base


class LogManager(base.Manager):
    def list(self):
        """Get statistics data.

        :rtype: list of :class:`Log`

        """
        return self._list("/logs")
