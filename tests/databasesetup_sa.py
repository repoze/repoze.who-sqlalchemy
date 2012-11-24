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
from io import StringIO
from cgi import FieldStorage
import repoze.who._compat as compat

from .fixture.sa_model import init_model, DBSession, metadata, User, Member

engine = create_engine(os.environ.get('DBURL', 'sqlite://'))

def setup_database():
    init_model(engine)
    teardownDatabase()
    metadata.create_all(engine)
    
    # Creating users

    user = User()
    user.user_name = compat.u('rms')
    user.password = compat.u('freedom')
    DBSession.add(user)

    user = User()
    user.user_name = compat.u('linus')
    user.password = compat.u('linux')
    DBSession.add(user)

    user = User()
    user.user_name = compat.u('sballmer')
    user.password = compat.u('developers')
    DBSession.add(user)

    # Plus a couple of users without groups
    user = User()
    user.user_name = compat.u('guido')
    user.password = compat.u('phytonic')
    DBSession.add(user)

    user = User()
    user.user_name = compat.u('rasmus')
    user.password = compat.u('php')
    DBSession.add(user)

    DBSession.commit()

def setup_database_with_translations():
    init_model(engine)
    teardownDatabase()
    metadata.create_all(engine)
    
    # Creating members

    member = Member()
    member.member_name = compat.u('rms')
    member.password = compat.u('freedom')
    DBSession.add(member)

    member = Member()
    member.member_name = compat.u('linus')
    member.password = compat.u('linux')
    DBSession.add(member)

    member = Member()
    member.member_name = compat.u('sballmer')
    member.password = compat.u('developers')
    DBSession.add(member)

    # Plus a couple of members without groups
    member = Member()
    member.member_name = compat.u('guido')
    member.password = compat.u('phytonic')
    DBSession.add(member)

    member = Member()
    member.member_name = compat.u('rasmus')
    member.password = compat.u('php')
    DBSession.add(member)

    DBSession.commit()


def teardownDatabase():
    DBSession.rollback()
    metadata.drop_all(engine)

