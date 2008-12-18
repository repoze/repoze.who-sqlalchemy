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

"""Stuff required to setup the test database."""

import os

from sqlalchemy import *
from sqlalchemy.orm import *
from cStringIO import StringIO
from cgi import FieldStorage

from fixture.sa_model import init_model, DBSession, metadata, User

engine = create_engine(os.environ.get('DBURL', 'sqlite://'))

def setup_database():
    init_model(engine)
    teardownDatabase()
    metadata.create_all(engine)
    
    # Creating users

    user = User()
    user.user_name = u'rms'
    user.password = u'freedom'
    DBSession.save(user)

    user = User()
    user.user_name = u'linus'
    user.password = u'linux'
    DBSession.save(user)

    user = User()
    user.user_name = u'sballmer'
    user.password = u'developers'
    DBSession.save(user)

    # Plus a couple of users without groups
    user = User()
    user.user_name = u'guido'
    user.password = u'phytonic'
    DBSession.save(user)

    user = User()
    user.user_name = u'rasmus'
    user.password = u'php'
    DBSession.save(user)

    DBSession.commit()


def teardownDatabase():
    DBSession.rollback()
    metadata.drop_all(engine)

