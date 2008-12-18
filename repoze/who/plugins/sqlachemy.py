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
    """repoze.who authenticator for SQLAlchemy models."""
    
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
    """Setup an SQLAlchemy authenticator"""
    
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
