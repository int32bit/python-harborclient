from harborclient import base


class ConfigurationManager(base.Manager):
    def get(self):
        """List filters targets by name.

        :rtype: list of :class:`Target`
        """
        return self._get("/configurations")
