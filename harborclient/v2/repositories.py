from harborclient import base


class RepositoryManager(base.Manager):
    def get(self, id):
        """Get a project.

        :param id: ID of the :class:`User` to get.
        :rtype: :class:`User`
        """
        return self._get("/repositories/%s" % id)

    def list(self, project_id):
        """Get a list of users.

        :rtype: list of :class:`User`

        """
        repositories = self._list("/repositories?project_id=%s" % project_id)
        return repositories

    def list_tags(self, repo_name):
        return self.api.client.get(
            "/repositories/tags?repo_name=%s" % repo_name)

    def get_manifests(self, repo_name, tag):
        return self.api.client.get(
            "/repositories/manifests?repo_name=%s&tag=%s" % (repo_name, tag))

    def create(self, username, password, email, realname=None, comment=None):
        data = {
            "username": username,
            "password": password,
            "email": email,
            "realname": realname or username,
            "comment": comment or "",
        }
        return self._create("/users", data)

    def delete(self, id):
        """Delete (i.e. shut down and delete the image) this server.

        :param server: The :class:`Server` (or its ID) to delete
        :returns: An instance of harborclient.base.TupleWithMeta
        """
        return self._delete("/users/%s" % id)

    def get_top(self, count):
        return self._list("/repositories/top?count=%d" % count)
