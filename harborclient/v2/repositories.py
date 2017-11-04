from harborclient import base
from harborclient import exceptions as exp


class RepositoryManager(base.Manager):
    def get(self, id):
        """Get a Repository.

        :param id: ID of the :class:`Repository` to get.
        :rtype: :class:`User`
        """
        return self._get("/repositories/%s" % id)

    def list(self, project):
        """Get a list of repositories.

        :rtype: list of :class:`Repository`

        """
        try:
            repositories = self._list("/repositories?project_id=%s" % project)
            return repositories
        except exp.NotFound as e:
            raise exp.ProjectNotFound(e.message)

    def list_tags(self, repo_name):
        return self.api.client.get(
            "/repositories/%s/tags" % repo_name)

    def get_manifests(self, repo_name, tag):
        return self.api.client.get(
            "/repositories/%(repo_name)s/tags/%(tag)s/manifest"
            % {"repo_name": repo_name, "tag": tag})

    def get_top(self, count):
        return self._list("/repositories/top?count=%s" % count)
