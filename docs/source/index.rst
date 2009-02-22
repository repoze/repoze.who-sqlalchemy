:mod:`repoze.who` SQLAlchemy plugin
===================================

.. module:: repoze.who.plugins.sa
    :synopsis: SQLAlchemy/Elixir-based plugins for repoze.who
.. moduleauthor:: Gustavo Narea <me@gustavonarea.net>

:Author: Gustavo Narea.
:Latest version: |release|

.. topic:: Overview

    The :mod:`repoze.who` SQLAlchemy plugin provides an authenticator and
    a metadata provider plugins for SQLAlchemy or Elixir-based models. 


How to install
==============

The minimum requirements :mod:`repoze.who` and SQLAlchemy and you can
install it all by running::

    easy_install repoze.who.plugins.sa

The development mainline is available at the following Subversion repository::

    http://svn.repoze.org/whoplugins/whoalchemy/trunk/


Authenticator
=============

.. autoclass:: SQLAlchemyAuthenticatorPlugin

.. autofunction:: make_sa_authenticator


Metadata providers
==================

.. autoclass:: SQLAlchemyUserMDPlugin

.. autoclass:: SQLAlchemyStrictUserMDPlugin

.. autofunction:: make_sa_user_mdprovider


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
