Moved the version definition to the ``version`` attribute of ``PulpPluginAppConfig``, and have
``bump2version`` maintain it. Also update the ``docs/conf.py`` to be bump2version maintained. The
release script now parses its versions from ``setup.py`` which is needed for the removal of
``{plugin_name}.__init__.__version__``.
