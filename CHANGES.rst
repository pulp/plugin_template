=========
Changelog
=========

..
    You should *NOT* be adding new change log entries to this file, this
    file is managed by towncrier. You *may* edit previous change logs to
    fix problems like typo corrections or such.
    To add a new change log entry, please see
    https://docs.pulpproject.org/pulpcore/contributing/git.html#changelog-update

    WARNING: Don't drop the next directive!

.. towncrier release notes start

2021.08.04 (2021-08-04)
=======================


Features
--------

- Enable https functional tests
  `#403 <https://github.com/pulp/plugin_template/issues/403>`_
- Added a new nightly workflow to update CI files.
  `#420 <https://github.com/pulp/plugin_template/issues/420>`_
- Added an optional 'before_script' parameter to the release workflow.
  `#433 <https://github.com/pulp/plugin_template/issues/433>`_
- Added check to ensure the cherrypick script runs from project root.
  `#438 <https://github.com/pulp/plugin_template/issues/438>`_
- Added python_version option.
  `#457 <https://github.com/pulp/plugin_template/issues/457>`_


Bugfixes
--------

- Handle conflicts when cherry-picking changelog to the main branch.
  `#439 <https://github.com/pulp/plugin_template/issues/439>`_
- Updated CLI test code to use cli.toml instead of settings.toml.
  `#448 <https://github.com/pulp/plugin_template/issues/448>`_
- Update the Python version to 3.8 in CI files.
  `#453 <https://github.com/pulp/plugin_template/issues/453>`_


----


2021.07.01 (2021-07-01)

Features
--------

- Release workflow opens PR against master with the latest changelog.
  `#416 <https://github.com/pulp/plugin_template/issues/416>`_
- Added a new workflow for creating release branches.
  `#417 <https://github.com/pulp/plugin_template/issues/417>`_


Bugfixes
--------

- Fixed hardcoded reference to plugin default branch.
  `#421 <https://github.com/pulp/plugin_template/issues/421>`_


----


2021.06.18 (2021-06-18)
=======================


Features
--------

- Made the release workflow idempotent.
  `#7868 <https://pulp.plan.io/issues/7868>`_
- Automated the pre-release steps for the release workflow

  The release workflow for plugins now expects a release branch to exist with the correct 
  .dev version and correct pulpcore requirements. The release workflow needs to be run
  against the release branch being released. It takes one parameter: release tag (a.k.a
  version string).
  `#8119 <https://pulp.plan.io/issues/8119>`_


Misc
----

- `#8226 <https://pulp.plan.io/issues/8226>`_


----


2021.05.25 (2021-05-25)
=======================


Features
--------

- Adding upgrade tests
  `#8776 <https://pulp.plan.io/issues/8776>`_


----


2021.05.18 (2021-05-18)
=======================


Features
--------

- Added retry when installing amazon.aws collection in CI.
  `#8529 <https://pulp.plan.io/issues/8529>`_
- Updated the bootstrap code to use the new ``Distribution`` model.
  `#8569 <https://pulp.plan.io/issues/8569>`_
- Added cherrypick.sh script to perform cherry-picks.
  `#8601 <https://pulp.plan.io/issues/8601>`_


Misc
----

- `#8532 <https://pulp.plan.io/issues/8532>`_


----


2021.04.08 (2021-04-08)
=======================


Features
--------

- Created a manual trigger for our release process so the process could be rerun in case of failures.
  `#8404 <https://pulp.plan.io/issues/8404>`_
- Enable PR checkout from repos outside pulp org
  `#8510 <https://pulp.plan.io/issues/8510>`_


Deprecations and Removals
-------------------------

- Removed FIPS tests
  `#8455 <https://pulp.plan.io/issues/8455>`_


----


2021.03.15 (2021-03-15)
=======================


Features
--------

- Adding nightly FIPS tests
  `#3800 <https://pulp.plan.io/issues/3800>`_
- Add a ``test_cli`` option to test against pulp-cli.
  `#8184 <https://pulp.plan.io/issues/8184>`_
- Added a gettext check for use of f-strings with gettext.
  `#8316 <https://pulp.plan.io/issues/8316>`_


Bugfixes
--------

- Fix publish job by using app label.
  `#8311 <https://pulp.plan.io/issues/8311>`_


----


2021.02.04 (2021-02-04)
=======================


Features
--------

- Added a check for deprecated files (ie files that have been moved or removed).
  `#7933 <https://pulp.plan.io/issues/7933>`_
- Moved the version definition to the ``version`` attribute of ``PulpPluginAppConfig``, and have
  ``bump2version`` maintain it. Also update the ``docs/conf.py`` to be bump2version maintained. The
  release script now parses its versions from ``setup.py`` which is needed for the removal of
  ``{plugin_name}.__init__.__version__``.
  `#7943 <https://pulp.plan.io/issues/7943>`_
- GHA workflows have been switched to run on a CentOS 8 based container.
  `#8148 <https://pulp.plan.io/issues/8148>`_


Bugfixes
--------

- Fixed bug where older version of docs would overwrite the latest docs when an older Y stream was released.
  `#7766 <https://pulp.plan.io/issues/7766>`_
- Get performance tests working on Github Actions.
  `#7896 <https://pulp.plan.io/issues/7896>`_
- Updated the port for pulp-fixtures in smash-config.json.
  `#8183 <https://pulp.plan.io/issues/8183>`_


Improved Documentation
----------------------

- Updated instructions in the README to use Github Actions instead of Travis.
  `#7861 <https://pulp.plan.io/issues/7861>`_


Deprecations and Removals
-------------------------

- Removed Travis files and references to Travis.
  `#7861 <https://pulp.plan.io/issues/7861>`_
- Cherrypick processor is no longer available. 

  Configuration options `cherry_pick_automation` and `stable_branch` are no longer in use.
  Feel free to remove them from your template_config.yml.
  `#7869 <https://pulp.plan.io/issues/7869>`_


----


2020.12.07 (2020-12-07)
=======================


Features
--------

- Added a stage for testing released plugin with master branch of pulpcore.
  `#7411 <https://pulp.plan.io/issues/7411>`_
- Added support for Github Actions.
  `#7858 <https://pulp.plan.io/issues/7858>`_
- Added a workflow to test the bootstrapping mechanism for a new plugin
  `#7860 <https://pulp.plan.io/issues/7860>`_


Bugfixes
--------

- Stopped to derive the docker tag from the branch name.
  `#7799 <https://pulp.plan.io/issues/7799>`_


Misc
----

- `#7880 <https://pulp.plan.io/issues/7880>`_


----


2020.10.20 (2020-10-20)
=======================


Features
--------

- Add diagrams to plugins docs Makefile
  `#7629 <https://pulp.plan.io/issues/7629>`_
- Added check_manifest option that runs check-manifest to check for files ommitted from MANIFEST.in.
  `#7656 <https://pulp.plan.io/issues/7656>`_


----


2020.09.23 (2020-09-23)
=======================


Misc
----

- `#7556 <https://pulp.plan.io/issues/7556>`_


----


2020.09.22 (2020-09-22)
=======================


Features
--------

- Added ability for plugins to publish docs to pulpproject.org.
  `#7229 <https://pulp.plan.io/issues/7229>`_
- Have validate_commit_message.py accept different cases (e.g. "Fixes #1234").
  `#7404 <https://pulp.plan.io/issues/7404>`_
- Adding support for deprecation towncrier type.
  `#7421 <https://pulp.plan.io/issues/7421>`_


Misc
----

- `#7452 <https://pulp.plan.io/issues/7452>`_, `#7500 <https://pulp.plan.io/issues/7500>`_


----


2020.09.01 (2020-09-01)
=======================


Features
--------

- Configured the use of token_authentication as used py pulp_container in the CI for plugins.
  `#6782 <https://pulp.plan.io/issues/6782>`_
- Introducing towncrier
  `#7273 <https://pulp.plan.io/issues/7273>`_


----
