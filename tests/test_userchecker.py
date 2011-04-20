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

from repoze.who.plugins.sa import SQLAlchemyUserChecker

import databasesetup_sa
from fixture import sa_model


class TestUserChecker(unittest.TestCase):
    """Tests for the user checker"""
    
    def setUp(self):
        databasesetup_sa.setup_database()
        self.plugin = SQLAlchemyUserChecker(sa_model.User, sa_model.DBSession)
    
    def tearDown(self):
        databasesetup_sa.teardownDatabase()
    
    def test_existing_user(self):
        self.assertTrue(self.plugin(u"guido"))
    
    def test_non_existing_user(self):
        self.assertFalse(self.plugin(u"gustavo"))

