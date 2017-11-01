from harborclient import base


class TargetManager(base.Manager):
    def list(self):
        """List filters targets by name.

        :rtype: list of :class:`Target`
        """
        return self._list("/targets")
