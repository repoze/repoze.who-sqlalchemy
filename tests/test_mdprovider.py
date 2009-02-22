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
Tests for the repoze.who SQLAlchemy MD provider.

"""

import unittest

from zope.interface.verify import verifyClass
from paste.httpexceptions import HTTPUnauthorized
from repoze.who.interfaces import IMetadataProvider

from repoze.who.plugins.sa import SQLAlchemyUserMDPlugin, \
                                  SQLAlchemyStrictUserMDPlugin, \
                                  make_sa_user_mdprovider

import databasesetup_sa
from fixture import sa_model


class BaseDMTester(unittest.TestCase):
    """Base Test Case for the User MD provider's tests"""
    
    def setUp(self):
        databasesetup_sa.setup_database()
    
    def tearDown(self):
        databasesetup_sa.teardownDatabase()


class TestMDProvider(BaseDMTester):
    """Tests for the MD provider"""

    def test_implements(self):
        verifyClass(IMetadataProvider, SQLAlchemyUserMDPlugin, tentative=True)
        
    def test_it(self):
        user = sa_model.DBSession.query(sa_model.User).\
               filter(sa_model.User.user_name==u'rms').one()
        identity = {'repoze.who.userid': user.user_name}
        expected_identity = {
            'repoze.who.userid': user.user_name,
            'user': user}
        plugin = SQLAlchemyUserMDPlugin(sa_model.User, sa_model.DBSession)
        plugin.add_metadata(None, identity)
        self.assertEqual(identity, expected_identity)


class TestStrictMDProvider(BaseDMTester):
    """Tests for the Strict MD provider"""

    def test_implements(self):
        verifyClass(IMetadataProvider, SQLAlchemyStrictUserMDPlugin,
                    tentative=True)
        
    def test_existing_user(self):
        user = sa_model.DBSession.query(sa_model.User).\
               filter(sa_model.User.user_name==u'rms').one()
        identity = {'repoze.who.userid': user.user_name}
        expected_identity = {
            'repoze.who.userid': user.user_name,
            'user': user}
        plugin = SQLAlchemyStrictUserMDPlugin(sa_model.User,
                                              sa_model.DBSession)
        plugin.add_metadata(None, identity)
        self.assertEqual(identity, expected_identity)
        
    def test_non_existing_user(self):
        identity = {'repoze.who.userid': u'i-dont-exist'}
        plugin = SQLAlchemyStrictUserMDPlugin(sa_model.User,
                                              sa_model.DBSession)
        self.assertRaises(HTTPUnauthorized, plugin.add_metadata, None,
                          identity)


class TestMDProviderWithTranslations(BaseDMTester):
    """Tests for the translation functionality"""
    
    def setUp(self):
        databasesetup_sa.setup_database_with_translations()
    
    def test_it(self):
        self.plugin = SQLAlchemyUserMDPlugin(sa_model.Member,
                                             sa_model.DBSession)
        # Updating the translations...
        self.plugin.translations['user_name'] = 'member_name'
        # Testing it...
        member = sa_model.DBSession.query(sa_model.Member).\
                 filter(sa_model.Member.member_name==u'rms').one()
        identity = {'repoze.who.userid': member.member_name}
        expected_identity = {
            'repoze.who.userid': member.member_name,
            'user': member}
        self.plugin.add_metadata(None, identity)
        self.assertEqual(expected_identity, identity)


class TestMDProviderMaker(BaseDMTester):
    
    def test_simple_call(self):
        user_class = 'tests.fixture.sa_model:User'
        dbsession = 'tests.fixture.sa_model:DBSession'
        mdprovider = make_sa_user_mdprovider(user_class, dbsession)
        self.assertTrue(isinstance(mdprovider, SQLAlchemyUserMDPlugin))
    
    def test_no_user_class(self):
        dbsession = 'tests.fixture.sa_model:DBSession'
        self.assertRaises(ValueError, make_sa_user_mdprovider, None, dbsession)
    
    def test_no_dbsession(self):
        user_class = 'tests.fixture.sa_model:User'
        self.assertRaises(ValueError, make_sa_user_mdprovider, user_class)
    
    def test_username_translation(self):
        user_class = 'tests.fixture.sa_model:User'
        dbsession = 'tests.fixture.sa_model:DBSession'
        username_translation = 'username'
        mdprovider = make_sa_user_mdprovider(user_class, dbsession,
                                             username_translation)
        self.assertTrue(isinstance(mdprovider, SQLAlchemyUserMDPlugin))
        self.assertEqual(username_translation,
                         mdprovider.translations['user_name'])
    
    def test_strict_user_md(self):
        user_class = 'tests.fixture.sa_model:User'
        dbsession = 'tests.fixture.sa_model:DBSession'
        mdprovider = make_sa_user_mdprovider(user_class, dbsession,
                                             strict=True)
        self.assertTrue(isinstance(mdprovider, SQLAlchemyStrictUserMDPlugin))
    
    def test_strict_is_string(self):
        user_class = 'tests.fixture.sa_model:User'
        dbsession = 'tests.fixture.sa_model:DBSession'
        # Strict == True
        strict = 'True'
        mdprovider = make_sa_user_mdprovider(user_class, dbsession,
                                             strict=strict)
        self.assertTrue(isinstance(mdprovider, SQLAlchemyStrictUserMDPlugin))
        # Strict == False
        strict = 'False'
        mdprovider = make_sa_user_mdprovider(user_class, dbsession,
                                             strict=strict)
        self.assertTrue(isinstance(mdprovider, SQLAlchemyUserMDPlugin))
