:mod:`repoze.who` SQLAlchemy plugin
===================================

.. module:: repoze.who.plugins.sqlalchemy
    :synopsis: SQLAlchemy/Elixir-based authenticator for repoze.who
.. moduleauthor:: Gustavo Narea <me@gustavonarea.net>

:Author: Gustavo Narea.
:Latest version: |release|

.. topic:: Overview

    The :mod:`repoze.who` SQLAlchemy plugin provides an authenticator plugin
    for SQLAlchemy or Elixir-based models. 


How to install
==============

The minimum requirements :mod:`repoze.who` and SQLAlchemy and you can
install it all by running::

    easy_install repoze.who.plugins.sqlalchemy

The development mainline is available at the following Subversion repository::

    http://svn.repoze.org/whoplugins/whoalchemy/trunk/


Authenticator
=============

.. class:: SQLAlchemyAuthenticatorPlugin

    repoze.who authenticator for SQLAlchemy models.
    
    :param user_class: The SQLAlchemy/Elixir class for the users.
    :param session: The SQLAlchemy/Elixir session.
    
    Example::
    
        from repoze.who.plugins.sqlalchemy import SQLAlchemyAuthenticatorPlugin
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


.. function:: make_sa_authenticator(user_class=None, dbsession=None, user_name_translation=None, validate_password_translation=None)

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
        use = repoze.who.plugins.sqlalchemy:make_sa_authenticator
        user_class = yourcoolproject.model:User
        dbsession = yourcoolproject.model:DBSession
        # ...
    
    Or, if you need translations::
    
        # ...
        [plugin:sa_auth]
        use = repoze.who.plugins.sqlalchemy:make_sa_authenticator
        user_class = yourcoolproject.model:User
        dbsession = yourcoolproject.model:DBSession
        user_name_translation = username
        validate_password_translation = verify_password
        # ...

How to get help?
================

The prefered place to ask questions is the `Repoze mailing list 
<http://lists.repoze.org/listinfo/repoze-dev>`_ or the `#repoze 
<irc://irc.freenode.net/#repoze>`_ IRC channel. Bugs reports and feature 
requests should be sent to `the issue tracker of the Repoze project 
<http://bugs.repoze.org/>`_.


Contents
========

.. toctree::
    :maxdepth: 2

    News


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
