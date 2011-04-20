# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008-2009, Gustavo Narea <me@gustavonarea.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

"""
SQLAlchemy plugin for repoze.who.

TODO: Write a function that configures the three plugins in one go.

"""

from zope.interface import implements
from repoze.who.interfaces import IAuthenticator, IMetadataProvider
from repoze.who.utils import resolveDotted
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


__all__ = ("SQLAlchemyAuthenticatorPlugin", "SQLAlchemyUserMDPlugin",
           "SQLAlchemyUserChecker", "make_sa_authenticator",
           "make_sa_user_mdprovider")


class _BaseSQLAlchemyPlugin(object):
    
    default_translations = {'user_name': "user_name"}
    
    def __init__(self, user_class, dbsession):
        """
        Setup the plugin.
    
        :param user_class: The SQLAlchemy/Elixir class for the users.
        :param session: The SQLAlchemy/Elixir session.
        
        """
        self.user_class = user_class
        self.dbsession = dbsession
        self.translations = self.default_translations.copy()
    
    def get_user(self, username):
        # A fresh transaction must be used to avoid using an invalid one. It's
        # therefore assumed that at this point it must've been successfully
        # committed or rolled back.
        self.dbsession.remove()
        
        # Getting a translation:
        username_attr = getattr(self.user_class,
                                self.translations['user_name'])
        
        query = self.dbsession.query(self.user_class)
        query = query.filter(username_attr==username)
        
        try:
            return query.one()
        except (NoResultFound, MultipleResultsFound):
            # As recommended in the docs for repoze.who, it's important to
            # verify that there's only _one_ matching userid.
            return None


class SQLAlchemyUserChecker(_BaseSQLAlchemyPlugin):
    """
    User existence checker for
    :class:`repoze.who.plugins.auth_tkt.AuthTktCookiePlugin`.
    
    Example::
    
        from repoze.who.plugins.sa import SQLAlchemyUserChecker
        from yourcoolproject.model import User, DBSession
        
        checker = SQLAlchemyUserChecker(User, DBSession)
    
    This plugin assumes that the user name is kept in the ``user_name``
    attribute of the users' class. If you don't want to call it that way, then
    you have to "translate" it as in the sample below::
    
        # You have User.username instead of User.user_name:
        checker.translations['user_name'] = 'username'
    
    """
    
    def __call__(self, username):
        """
        Check whether a user account identified by ``username`` exists.
        
        :param username: The user account's id to be verified.
        :type username: basestring
        :return: Whether it exists or not.
        :rtype: bool
        
        """
        if self.get_user(username):
            return True
        return False


#{ repoze.who plugins


class SQLAlchemyAuthenticatorPlugin(_BaseSQLAlchemyPlugin):
    """
    :mod:`repoze.who` authenticator for SQLAlchemy models.
    
    Example::
    
        from repoze.who.plugins.sa import SQLAlchemyAuthenticatorPlugin
        from yourcoolproject.model import User, DBSession
        
        authenticator = SQLAlchemyAuthenticatorPlugin(User, DBSession)
    
    This plugin assumes that the user name is kept in the ``user_name``
    attribute of the users' class, as well as that such a class has a method
    that verifies the user's password against the password provided through the
    login form (it receives the password to be verified as the only argument
    and such method is assumed to be called ``validate_password``).
    
    If you don't want to call the attributes above as ``user_name`` and/or
    ``validate_password``, respectively, then you have to "translate" them as
    in the sample below::
    
        # You have User.username instead of User.user_name:
        authenticator.translations['user_name'] = 'username'
        
        # You have User.verify_password instead of User.validate_password:
        authenticator.translations['validate_password'] = 'verify_password'
    
    .. note::
    
        If you want to configure this authenticator from an ``ini`` file, use
        :func:`make_sa_authenticator`.
    
    """
    
    implements(IAuthenticator)
    
    default_translations = _BaseSQLAlchemyPlugin.default_translations.copy()
    default_translations['validate_password'] = "validate_password"

    # IAuthenticator
    def authenticate(self, environ, identity):
        if not ("login" in identity and "password" in identity):
            return None
        
        user = self.get_user(identity['login'])
        
        if user:
            validator = getattr(user, self.translations['validate_password'])
            if validator(identity['password']):
                return identity['login']


class SQLAlchemyUserMDPlugin(_BaseSQLAlchemyPlugin):
    """
    :mod:`repoze.who` metadata provider that loads the SQLAlchemy-powered
    object for the current user.
    
    It loads the object into ``identity['user']``.
    
    Example::
    
        from repoze.who.plugins.sa import SQLAlchemyUserMDPlugin
        from yourcoolproject.model import User, DBSession
        
        mdprovider = SQLAlchemyUserMDPlugin(User, DBSession)
    
    This plugin assumes that the user name is kept in the ``user_name``
    attribute of the users' class. If you don't want to call the attribute
    above as ``user_name``, then you have to "translate" it as in the sample 
    below::
    
        # You have User.username instead of User.user_name:
        mdprovider.translations['user_name'] = 'username'
    
    .. note::
    
        If you want to configure this plugin from an ``ini`` file, use
        :func:`make_sa_user_mdprovider`.
    
    """
    
    implements(IMetadataProvider)
    
    def add_metadata(self, environ, identity):
        identity['user'] = self.get_user(identity['repoze.who.userid'])


#{ Functions to instantiate the plugins from a Paste configuration


def _base_plugin_maker(user_class=None, dbsession=None):
    """
    Turn ``userclass`` and ``dbsession`` into Python objects.
    
    """
    
    if user_class is None:
        raise ValueError("user_class must not be None")
    if dbsession is None:
        raise ValueError("dbsession must not be None")
    return resolveDotted(user_class), resolveDotted(dbsession)


def make_sa_authenticator(user_class=None, dbsession=None, 
                          user_name_translation=None, 
                          validate_password_translation=None):
    """
    Configure :class:`SQLAlchemyAuthenticatorPlugin`.
    
    :param user_class: The SQLAlchemy/Elixir class for the users.
    :type user_class: str
    :param dbsession: The SQLAlchemy/Elixir session.
    :type dbsession: str
    :param user_name_translation: The translation for ``user_name``, if any.
    :type user_name_translation: str
    :param validate_password_translation: The translation for 
        ``validate_password``, if any.
    :type validate_password_translation: str
    :return: The authenticator.
    :rtype: SQLAlchemyAuthenticatorPlugin
    
    Example from an ``*.ini`` file::
    
        # ...
        [plugin:sa_auth]
        use = repoze.who.plugins.sa:make_sa_authenticator
        user_class = yourcoolproject.model:User
        dbsession = yourcoolproject.model:DBSession
        # ...
    
    Or, if you need translations::
    
        # ...
        [plugin:sa_auth]
        use = repoze.who.plugins.sa:make_sa_authenticator
        user_class = yourcoolproject.model:User
        dbsession = yourcoolproject.model:DBSession
        user_name_translation = username
        validate_password_translation = verify_password
        # ...
    
    """
    
    user_model, dbsession_object = _base_plugin_maker(user_class, dbsession)
    
    authenticator = SQLAlchemyAuthenticatorPlugin(user_model, dbsession_object)
    
    if user_name_translation:
        authenticator.translations['user_name'] = user_name_translation
    if validate_password_translation:
        authenticator.translations['validate_password'] = \
            validate_password_translation
    
    return authenticator


def make_sa_user_mdprovider(user_class=None, dbsession=None, 
                            user_name_translation=None):
    """
    Configure :class:`SQLAlchemyUserMDPlugin`.
    
    :param user_class: The SQLAlchemy/Elixir class for the users.
    :type user_class: str
    :param dbsession: The SQLAlchemy/Elixir session.
    :type dbsession: str
    :param user_name_translation: The translation for ``user_name``, if any.
    :type user_name_translation: str
    :return: The metadata provider.
    :rtype: SQLAlchemyUserMDPlugin
    
    Example from an ``*.ini`` file::
    
        # ...
        [plugin:sa_md]
        use = repoze.who.plugins.sa:make_sa_user_mdprovider
        user_class = yourcoolproject.model:User
        dbsession = yourcoolproject.model:DBSession
        # ...
    
    Or, if you need translations::
    
        # ...
        [plugin:sa_md]
        use = repoze.who.plugins.sa:make_sa_user_mdprovider
        user_class = yourcoolproject.model:User
        dbsession = yourcoolproject.model:DBSession
        user_name_translation = username
        # ...
    
    """
    
    user_model, dbsession_object = _base_plugin_maker(user_class, dbsession)
    
    mdprovider = SQLAlchemyUserMDPlugin(user_model, dbsession_object)
    
    if user_name_translation:
        mdprovider.translations['user_name'] = user_name_translation
    
    return mdprovider


#}
