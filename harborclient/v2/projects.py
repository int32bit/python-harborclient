from harborclient import base
from harborclient import exceptions as exp


class ProjectManager(base.Manager):
    def is_id(self, key):
        return key.isdigit()

    def get(self, id):
        """Get a project.

        :param id: ID of the :class:`User` to get.
        :rtype: :class:`User`
        """
        return self._get("/projects/%s" % id)

    def list(self):
        """Get a list of projects.

        :rtype: list of :class:`Project`

        """
        return self._list("/projects")

    def get_id_by_name(self, name):
        projects = self.list()
        for p in projects:
            if p['name'] == name:
                return p['project_id']
        raise exp.NotFound("Project '%s' not Found." % name)

    def get_name_by_id(self, id):
        projects = self.list()
        for p in projects:
            if p['project_id'] == id:
                return p['name']
        raise exp.ProjectNotFound("Project '%s' not Found." % id)

    def create(self, name, public=True):
        project = {"project_name": name, "public": 1 if public else 0}
        return self._create("/projects", project)

    def delete(self, id):
        """Delete (i.e. shut down and delete the image) this server.

        :param server: The :class:`Server` (or its ID) to delete
        :returns: An instance of harborclient.base.TupleWithMeta
        """
        return self._delete("/projects/%s" % id)

    def get_members(self, id):
        return self._list("/projects/%s/members/" % id)
