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
from repoze.who.interfaces import IMetadataProvider

from repoze.who.plugins.sa import SQLAlchemyUserMDPlugin, \
                                  make_sa_user_mdprovider

import databasesetup_sa
from fixture import sa_model


class TestMDProvider(unittest.TestCase):
    """Tests for the authenticator function"""
    
    def setUp(self):
        databasesetup_sa.setup_database()
        self.plugin = SQLAlchemyUserMDPlugin(sa_model.User, sa_model.DBSession)
    
    def tearDown(self):
        databasesetup_sa.teardownDatabase()

    def test_implements(self):
        verifyClass(IMetadataProvider, SQLAlchemyUserMDPlugin, tentative=True)
        
    def test_it(self):
        user = sa_model.DBSession.query(sa_model.User).\
               filter(sa_model.User.user_name==u'rms').one()
        identity = {'repoze.who.userid': user.user_name}
        expected_identity = {
            'repoze.who.userid': user.user_name,
            'user': user}
        self.plugin.add_metadata(None, identity)
        self.assertEqual(identity, expected_identity)


class TestMDProviderWithTranslations(unittest.TestCase):
    """Tests for the translation functionality"""
    
    def setUp(self):
        databasesetup_sa.setup_database_with_translations()
    
    def tearDown(self):
        databasesetup_sa.teardownDatabase()
    
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


class TestMDProviderMaker(unittest.TestCase):
    
    def setUp(self):
        databasesetup_sa.setup_database()
    
    def tearDown(self):
        databasesetup_sa.teardownDatabase()
    
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
