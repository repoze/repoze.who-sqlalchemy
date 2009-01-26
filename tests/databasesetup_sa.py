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

"""Stuff required to setup the test database."""

import os

from sqlalchemy import *
from sqlalchemy.orm import *
from cStringIO import StringIO
from cgi import FieldStorage

from fixture.sa_model import init_model, DBSession, metadata, User, Member

engine = create_engine(os.environ.get('DBURL', 'sqlite://'))

def setup_database():
    init_model(engine)
    teardownDatabase()
    metadata.create_all(engine)
    
    # Creating users

    user = User()
    user.user_name = u'rms'
    user.password = u'freedom'
    DBSession.add(user)

    user = User()
    user.user_name = u'linus'
    user.password = u'linux'
    DBSession.add(user)

    user = User()
    user.user_name = u'sballmer'
    user.password = u'developers'
    DBSession.add(user)

    # Plus a couple of users without groups
    user = User()
    user.user_name = u'guido'
    user.password = u'phytonic'
    DBSession.add(user)

    user = User()
    user.user_name = u'rasmus'
    user.password = u'php'
    DBSession.add(user)

    DBSession.commit()

def setup_database_with_translations():
    init_model(engine)
    teardownDatabase()
    metadata.create_all(engine)
    
    # Creating members

    member = Member()
    member.member_name = u'rms'
    member.password = u'freedom'
    DBSession.add(member)

    member = Member()
    member.member_name = u'linus'
    member.password = u'linux'
    DBSession.add(member)

    member = Member()
    member.member_name = u'sballmer'
    member.password = u'developers'
    DBSession.add(member)

    # Plus a couple of members without groups
    member = Member()
    member.member_name = u'guido'
    member.password = u'phytonic'
    DBSession.add(member)

    member = Member()
    member.member_name = u'rasmus'
    member.password = u'php'
    DBSession.add(member)

    DBSession.commit()


def teardownDatabase():
    DBSession.rollback()
    metadata.drop_all(engine)

