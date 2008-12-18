# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008, Gustavo Narea <me@gustavonarea.net>
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

"""SQLAlchemy plugin for repoze.who."""

from zope.interface import implements
from repoze.who.interfaces import IAuthenticator
from repoze.who.utils import resolveDotted
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


__all__ = ['SQLAlchemyAuthenticatorPlugin', 'make_sa_authenticator']


class SQLAlchemyAuthenticatorPlugin(object):
    """
    repoze.who authenticator for SQLAlchemy models.
    
    Example::
    
        from repoze.who.plugins.sa import SQLAlchemyAuthenticatorPlugin
        from yourcoolproject.model import User, DBSession
        
        authenticator = SQLAlchemyAuthenticatorPlugin(User, DBSession)
    
    This plugin assumes that the user name is kept in the ``user_name``
    attribute of the users' class, as well as that such a class has a method
    that verifies the user's password against the password provided through the
    login form (it receives the password to be verified as the only argument
    and such method is assumed to be called ``validate_password``).
    
    If you don't want to call the attributes below as ``user_name`` and/or
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
    
    def __init__(self, user_class, dbsession):
        """
        Setup the authenticator.
    
        :param user_class: The SQLAlchemy/Elixir class for the users.
        :param session: The SQLAlchemy/Elixir session.
        
        """
        self.user_class = user_class
        self.dbsession = dbsession
        self.translations = {
            'user_name': 'user_name',
            'validate_password': 'validate_password'
        }

    # IAuthenticator
    def authenticate(self, environ, identity):
        if not ('login' in identity and 'password' in identity):
            return None
        
        # Getting a translation:
        username = getattr(self.user_class, self.translations['user_name'])
        
        query = self.dbsession.query(self.user_class)
        query = query.filter(username==identity['login'])
        try:
            user = query.one()
            # Getting the other translation:
            validator = getattr(user, self.translations['validate_password'])
            if validator(identity['password']):
                return user.user_name
        except (NoResultFound, MultipleResultsFound):
            # As recommended in the docs for repoze.who, it's important to
            # verify that there's only _one_ matching userid.
            return None


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
    :param validate_password_translation: The translation for ``validate_password``, if any.
    :type validate_password_translation: str
    
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
    
    if user_class is None:
        raise ValueError('user_class must not be None')
    if dbsession is None:
        raise ValueError('user_class must not be None')
    user_model = resolveDotted(user_class)
    dbsession_object = resolveDotted(dbsession)
    
    authenticator = SQLAlchemyAuthenticatorPlugin(user_model, dbsession_object)
    
    if user_name_translation:
        authenticator.translations['user_name'] = user_name_translation
    if validate_password_translation:
        authenticator.translations['validate_password'] = \
            validate_password_translation
    
    return authenticator
