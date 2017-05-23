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
        _, projects = self.list()
        for p in projects:
            if p['name'] == name:
                return p['project_id']
        raise exp.ProjectNotFound("Project '%s' not Found." % name)

    def get_name_by_id(self, id):
        _, projects = self.list()
        for p in projects:
            if p['project_id'] == id:
                return p['name']
        raise exp.ProjectNotFound("Project '%s' not Found." % id)

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
        return self._delete("/projects/%s" % id)
