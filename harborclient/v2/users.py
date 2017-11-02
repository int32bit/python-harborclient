"""
User interface.
"""

import requests

from harborclient import base
from harborclient import exceptions as exp


class UserManager(base.Manager):
    def is_id(self, key):
        return key.isdigit()

    def get(self, id):
        """Get a user.

        :param id: ID of the :class:`User` to get.
        :rtype: :class:`User`
        """
        return self._get("/users/%s" % id)

    def current(self):
        """Get current user info.

        :rtype: :class:`User`
        """
        return self._get("/users/current")

    def list(self):
        """Get a list of users.

        :rtype: list of :class:`User`
        """
        return self._list("/users")

    def get_id_by_name(self, name):
        users = self.list()
        for u in users:
            if u['username'] == name:
                return u['user_id']
        raise exp.UserNotFound("User '%s' Not Found!" % name)

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
        """Delete this user.

        :param user: The :class:`User` (or its ID) to delete
        :returns: An instance of harborclient.base.TupleWithMeta
        """
        return self._delete("/users/%s" % id)

    def login(self, username, password, baseurl):
        data = {'principal': username, 'password': password}
        resp = requests.post(baseurl + "/login", data)
        return resp
