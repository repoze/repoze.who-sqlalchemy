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

The development mainline is available at the following Git repository::

    git://github.com/repoze/repoze.who-sqlalchemy.git


Authenticator
=============

.. autoclass:: SQLAlchemyAuthenticatorPlugin

.. autofunction:: make_sa_authenticator


Metadata provider
=================

.. autoclass:: SQLAlchemyUserMDPlugin

.. autofunction:: make_sa_user_mdprovider


Miscellaneous
=============

.. autoclass:: SQLAlchemyUserChecker


How to get help?
================

The prefered place to ask questions and request features is the
`Repoze mailing list  <http://lists.repoze.org/listinfo/repoze-dev>`_.

To report bugs, please go to `GitHub
<https://github.com/repoze/repoze.who-sqlalchemy/issues>`_.


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
