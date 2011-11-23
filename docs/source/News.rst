*************************************
:mod:`repoze.who.plugins.sa` releases
*************************************

This document describes the releases of :mod:`repoze.who.plugins.sa`.


.. _version-1.0.1:

Version 1.0.1 (2011-11-23)
==========================

* Added ability to prevent from `timing attacks
  <http://en.wikipedia.org/wiki/Timing_attack>`_. Thanks to `Arturo Sevilla
  <https://github.com/repoze/repoze.who-sqlalchemy/pull/3>`_!



.. _version-1.0:

Version 1.0 Final (2011-05-02)
==============================

* Queries issued by this plugin now use a fresh transaction, to avoid using
  an invalid one (`which happens sometimes when repoze.who-friendlyform is used
  <https://groups.google.com/forum/#!topic/pylons-discuss/DA8f4VyEEwM/discussion>`_).
  Thanks to Rick Harding for `testing the fix in production before its release
  <https://github.com/repoze/repoze.what-sql/issues/1>`_!


.. _version-1.0rc2:

Version 1.0rc2 (2009-06-27)
===========================

* Added :class:`repoze.who.plugins.sa.SQLAlchemyUserChecker`, a user checker
  for :class:`repoze.who.plugins.auth_tkt.AuthTktCookiePlugin`.


.. _version-1.0rc1:

Version 1.0rc1 (2009-01-26)
===========================
* Introduced the :class:`repoze.who.plugins.sa.SQLAlchemyUserMDPlugin` metadata
  provider.
* Minor docstring fixes.


.. _version-1.0b3:

Version 1.0b3 (2009-01-08)
==========================

Fixed `Bug #56 <http://bugs.repoze.org/issue56>`_ (``User.user_name`` was
not translatable).


.. _version-1.0b2:

Version 1.0b2 (2008-12-18)
==========================

Renamed :mod:`repoze.who.plugins.sqlalchemy` to :mod:`repoze.who.plugins.sa`
due to problems with the namespace.


.. _repoze.who.plugins.sqlalchemy-1.0b1:

:mod:`repoze.who.plugins.sqlalchemy` 1.0b1 (2008-12-18)
=======================================================

Initial release.
