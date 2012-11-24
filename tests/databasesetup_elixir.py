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
#from cStringIO import StringIO
from io import StringIO
from cgi import FieldStorage
import repoze.who._compat as compat
try:
    import elixir
    from .fixture.elixir_model import init_model, DBSession, metadata, User
except ImportError:
    pass
else:
    
    engine = create_engine(os.environ.get('DBURL', 'sqlite://'))
    
    def setup_database():
        init_model(engine)
        teardownDatabase()
        elixir.setup_all(True)
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
    
    
    def teardownDatabase():
        DBSession.rollback()
        metadata.drop_all(engine)
