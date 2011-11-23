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
Tests for the repoze.who SQLAlchemy authenticator.

"""

import unittest

from repoze.who.interfaces import IAuthenticator
try:
    from sqlalchemy.exceptions import IntegrityError
except ImportError:
    from sqlalchemy.exc import IntegrityError
from zope.interface.verify import verifyClass

from repoze.who.plugins.sa import SQLAlchemyAuthenticatorPlugin, \
                                  make_sa_authenticator

import databasesetup_sa, databasesetup_elixir
from fixture import sa_model, elixir_model


class TestAuthenticator(unittest.TestCase):
    """Tests for the authenticator function"""
    
    def setUp(self):
        databasesetup_sa.setup_database()
        self.plugin = SQLAlchemyAuthenticatorPlugin(sa_model.User, 
                                                    sa_model.DBSession)
    
    def tearDown(self):
        databasesetup_sa.teardownDatabase()

    def test_implements(self):
        verifyClass(IAuthenticator, SQLAlchemyAuthenticatorPlugin, 
                    tentative=True)
        
    def test_no_identity(self):
        identity = {}
        self.assertEqual(None, self.plugin.authenticate(None, identity))
        
    def test_incomplete_credentials(self):
        identity = {'login': 'rms'}
        self.assertEqual(None, self.plugin.authenticate(None, identity))
        identity = {'password': 'freedom'}
        self.assertEqual(None, self.plugin.authenticate(None, identity))
        
    def test_no_match(self):
        identity = {'login': u'gustavo', 'password': u'narea'}
        self.assertEqual(None, self.plugin.authenticate(None, identity))
        
    def test_match(self):
        identity = {'login': u'rms', 'password': u'freedom'}
        self.assertEqual(u'rms', self.plugin.authenticate(None, identity))
    
    def test_rollback(self):
        """The session must be rolled back before use."""
        # Make the transaction invalid by attempting to add an existing user:
        try:
            user = sa_model.User()
            user.user_name = u"rms"
            user.password = "free software"
            sa_model.DBSession.add(user)
            sa_model.DBSession.commit()
        except IntegrityError:
            pass
        else:
            self.fail("An IntegrityError must've been raised")
        
        identity = {'login': u'rms', 'password': u'freedom'}
        self.plugin.authenticate(None, identity)


class TestAuthenticatorWithTranslations(unittest.TestCase):
    """Tests for the authenticator function"""
    
    def setUp(self):
        databasesetup_sa.setup_database_with_translations()
    
    def tearDown(self):
        databasesetup_sa.teardownDatabase()
    
    def test_it(self):
        self.plugin = SQLAlchemyAuthenticatorPlugin(sa_model.Member, 
                                                    sa_model.DBSession)
        # Updating the translations...
        self.plugin.translations['user_name'] = 'member_name'
        self.plugin.translations['validate_password'] = 'verify_pass'
        # Testing it...
        identity = {'login': u'rms', 'password': u'freedom'}
        self.assertEqual(u'rms', self.plugin.authenticate(None, identity))

    def test_dummy_validate(self):
        self.plugin = SQLAlchemyAuthenticatorPlugin(sa_model.User, 
                                                    sa_model.DBSession)
        self.plugin.translations['dummy_validate_password'] = \
            sa_model.dummy_validate
        identity = {'login': u'QWERTY', 'password': u'freedom'}
        self.assertRaises(sa_model.DummyValidateException,
                          self.plugin.authenticate, None, identity)


class TestAuthenticatorWithElixir(TestAuthenticator):
    
    def setUp(self):
        databasesetup_elixir.setup_database()
        self.plugin = SQLAlchemyAuthenticatorPlugin(elixir_model.User,
                                            elixir_model.DBSession)
    
    def tearDown(self):
        databasesetup_elixir.teardownDatabase()
    
    def test_rollback(self):
        """The session must be rolled back before use."""
        # Make the transaction invalid by attempting to add an existing user:
        try:
            user = elixir_model.User()
            user.user_name = u"rms"
            user.password = "free software"
            elixir_model.DBSession.add(user)
            elixir_model.DBSession.commit()
        except IntegrityError:
            pass
        else:
            self.fail("An IntegrityError must've been raised")
        
        identity = {'login': u'rms', 'password': u'freedom'}
        self.plugin.authenticate(None, identity)


class TestAuthenticatorMaker(unittest.TestCase):
    
    def setUp(self):
        databasesetup_sa.setup_database()
    
    def tearDown(self):
        databasesetup_sa.teardownDatabase()
    
    def test_simple_call(self):
        user_class = 'tests.fixture.sa_model:User'
        dbsession = 'tests.fixture.sa_model:DBSession'
        authenticator = make_sa_authenticator(user_class, dbsession)
        self.assertTrue(isinstance(authenticator, 
                                   SQLAlchemyAuthenticatorPlugin))
    
    def test_no_user_class(self):
        dbsession = 'tests.fixture.sa_model:DBSession'
        self.assertRaises(ValueError, make_sa_authenticator, None, dbsession)
    
    def test_no_dbsession(self):
        user_class = 'tests.fixture.sa_model:User'
        self.assertRaises(ValueError, make_sa_authenticator, user_class)
    
    def test_username_translation(self):
        user_class = 'tests.fixture.sa_model:User'
        dbsession = 'tests.fixture.sa_model:DBSession'
        username_translation = 'username'
        authenticator = make_sa_authenticator(user_class, dbsession,
                                              username_translation)
        self.assertTrue(isinstance(authenticator, 
                                   SQLAlchemyAuthenticatorPlugin))
        self.assertEqual(username_translation,
                         authenticator.translations['user_name'])
    
    def test_passwd_validator_translation(self):
        user_class = 'tests.fixture.sa_model:User'
        dbsession = 'tests.fixture.sa_model:DBSession'
        password_validator_translation = 'verify_pass'
        authenticator = make_sa_authenticator(
            user_class,
            dbsession,
            validate_password_translation=password_validator_translation)
        self.assertTrue(isinstance(authenticator, 
                                   SQLAlchemyAuthenticatorPlugin))
        self.assertEqual(password_validator_translation,
                         authenticator.translations['validate_password'])

    def test_dummy_validate_translation(self):
        user_class = 'tests.fixture.sa_model:User'
        dbsession = 'tests.fixture.sa_model:DBSession'
        dummy_val_translation = 'tests.fixture.sa_model:dummy_validate'
        authenticator = make_sa_authenticator(
            user_class,
            dbsession,
            dummy_validate_password_translation=dummy_val_translation)
        self.assertTrue(isinstance(authenticator, 
                                   SQLAlchemyAuthenticatorPlugin))
        self.assertEqual(sa_model.dummy_validate,
                         authenticator.translations['dummy_validate_password'])
