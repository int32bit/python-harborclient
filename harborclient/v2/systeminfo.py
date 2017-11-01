from harborclient import base


class SystemInfoManager(base.Manager):
    def get(self):
        """List filters targets by name.

        :rtype: list of :class:`Target`
        """
        return self._get("/systeminfo")

    def get_volumes(self):
        return self._get("/systeminfo/volumes")

    def get_cert(self):
        return self._get("/systeminfo/getcert")
