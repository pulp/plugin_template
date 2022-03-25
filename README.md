This is the ``plugin_template`` repository to help plugin writers get started and write their own
plugin for [Pulp Project 3.0+](https://pypi.python.org/pypi/pulpcore/).


# Plugin Writing Walkthrough

If you are planning on writing a new Pulp plugin, but have no idea what you're doing you've come to the right place.
The purpose of this guide is to walk you through, step by step, the Pulp plugin creation process.

This guide specifically details *how* you write a new content plugin.

[*Why* would you want to write a plugin?](https://docs.pulpproject.org/pulpcore/plugins/index.html)

[*What* exactly is this Pulp thing?](https://docs.pulpproject.org/pulpcore/components.html)

It's recommend that you develop on a system that already has
[Pulp installed](https://docs.pulpproject.org/pulpcore/installation/instructions.html).
This allows you to test your plugin at every step.

It's also recommended that you go through the [planning guide](meta_docs/planning-guide.md) before starting to develop your plugin.

# Generate a plugin template config for a new Pulp plugin

The first step is to create a `template_config.yml` for your new plugin. This file contains
settings used by the `./plugin-template` command when generating new plugins and for future updates.

1. Clone this repository

   ``$ git clone https://github.com/pulp/plugin_template.git``

   ``$ cd plugin_template``

2. Run the provided ``./plugin-template --generate-config ``

   ``$ ./plugin-template --generate-config --plugin-app-label <label> PLUGIN_NAME``

   **NOTE** : The `plugin-app-label` should identify the content type which you would like to
   support, e.g. `rubygem` or `maven`. The `PLUGIN_NAME` is usually `pulp_` or `pulp-` prepended
   to the `--plugin-app-label`, e.g. `pulp_maven`.

The first time this command is run, a new directory by the name of PLUGIN_NAME is created inside
the parent directory of the `plugin_template' directory. The `template_config.yml` is written to
the root of this new directory.
It is filled with default values for various aspects of the plugin scaffolding.
You can edit them according to your needs to control subsequent calls to `plugin-template`.

The following settings are stored in `template_config.yml`.

```bash
  additional_repos    A list with additional repos to be installed on Github Actions.
                        Each item in the list is a dict with the following fields:
                        name: the name of the plugin
                        bindings (optional): boolean whether or not generate bindings
                        org (optional): github organization
                        revision (optional): the git commit hash to install.
                                             "Required PR" in a commit message will override this.
                        pytest_args (optional): string to by passed to a pytest call.
                        branch: the git branch of the plugin. applies to non-tagged GHA jobs, such as PRs & cron jobs.
                        pip_version_specifier: A pip version specifier for when the gets installed from PyPI.
                                               Applies to TAGGED (release) jobs.
                                               See pulpcore_pip_version_specifier, but defaults to undefined, the latest.

  upgrade_range       A list with plugin branches to be installed on Github Actions.
                        Each item in the list is a dict with the following fields:
                        {{ plugin_name }}_branch: the branch of the plugin
                        Example:
                            upgrade_range:
                                - pulp_file_branch: 1.6
                                  pulpcore_branch: 3.11
                                - pulp_file_branch: 1.5
                                  pulpcore_branch: 3.10

  black                 Boolean, whether to use black to format python source files.

  flake8                Boolean, whether to use flake8 to lint python source files.

  check_commit_message  Include inspection of commit message for a reference to an issue in
                        pulp.plan.io.

  check_gettext         Check for problems with gettext such as mixing f-strings with gettext.

  check_manifest        Runs check-manifest to see if any files that were unintentionally left out
                        of MANIFEST.in. For more info, see https://pypi.org/project/check-manifest/.

  check_stray_pulpcore_imports
                        Check that plugins are importing from pulpcore.plugin and not pulpcore directly.

  core_import_allowed   A list of string patterns to be allowed to import from pulpcore explicitly.

  coverage              Include collection of coverage and reporting to coveralls.io

  deploy_client_to_pypi Include a Github Actions job that publishes a client library to PyPI.

                        This job only executes when a tag is associated with the commit being
                        built. When enabling this job, the user is expected to provide a
                        secure environment variable called PYPI_PASSWORD. The variable can
                        be added in the Github secrets settings page for the repository[0]. The PYPI
                        username is specified using --pypi-username option.

                        This job uses the OpenAPI schema for the plugin to generate a Python
                        client library using openapi-generator-cli.

  deploy_client_to_rubygems
                        Include a Github Actions job that publishes a client library to RubyGems.org.

                        This job only executes when a tag is associated with the commit being
                        built. When enabling this job, the user is expected to provide a
                        secure environment variable called RUBYGEMS_API_KEY. The variable can
                        be added in the Github secrets settings page for the repository.

  deploy_daily_client_to_pypi
                        Include a Github Actions job that publishes a client library to PyPI.

                        This job only executes when a tag is associated with the commit being
                        built. When enabling this job, the user is expected to provide a
                        secure environment variable called PYPI_PASSWORD. The variable can
                        be added in the Github secrets settings page for the repository[0]. The PYPI
                        username is specified using --pypi-username option.

                        This job uses the OpenAPI schema for the plugin to generate a Python
                        client library using openapi-generator-cli.

                        [0] https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets

  deploy_daily_client_to_rubygems
                        Include a Github Actions job that publishes a client library to RubyGems.org
                        with each CRON build.

                        This job only executes on builds trigerred by CRON. When enabling
                        this job, the user is expected to provide a secure environment
                        variable called RUBYGEMS_API_KEY. The variable can be added in the
                        Github secrets settings page for the repository.

  deploy_to_pypi        Include a Github Actions job that publishes builds to PyPI

                        This job only executes when a tag is associated with the commit being
                        built. When enabling this job, the user is expected to provide a
                        secure environment variable called PYPI_PASSWORD. The variable can
                        be added in the Github secrets settings page for the repository[0]. The PYPI
                        username is specified using --pypi-username option.

  docker_fixtures       In Github Actions, use the pulp-fixtures docker container to serve up
                        fixtures instead of using fedorapeople.org.

  aiohttp_fixtures_origin
                        Identifies the network origin of the aiohttp fixtures.

  github_org            The Github organization to use for the plugin.

  issue_tracker         Which issue tracker the project will use. Valid values are 'redmine' and
                        'github'. To switch from Redmine to GitHub use the --migrate-github-issues
                        option.

  keep_ci_update_for_latest_branches
                        Total of X.Y branches for which CI updates are kept. The default is 5.

  docs_test             Include a CI build for testing the 'make html' command for sphinx docs.

  parallel_test_workers Run tests in parallel using `pytest-xdist` with N parallel runners. This
                        settings specifies N. By default it is 8. Setting to 0 will disable parallel
                        test running.

  plugin_app_label      Suppose our plugin is named 'pulp_test', then this is 'test'

  plugin_camel          Suppose our plugin is named 'pulp_test', then this is 'PulpTest'

  plugin_camel_short    Suppose our plugin is named 'pulp_test', then this is 'Test'

  plugin_caps           Suppose our plugin is named 'pulp_test', then this is 'PULP_TEST'

  plugin_caps_short     Suppose our plugin is named 'pulp_test', then this is 'TEST'

  plugin_dash           Suppose our plugin is named 'pulp_test', then this is 'pulp-test'

  plugin_dash_short     Suppose our plugin is named 'pulp_test', then this is 'test'

  plugin_default_branch The default branch in your plugin repo, defaults to 'main'.

  plugin_name           Suppose our plugin is named 'pulp_test', then this is 'pulp_test'

  plugin_snake          Suppose our plugin is named 'pulp_test', then this is 'pulp_test'

  publish_docs_to_pulpprojectdotorg
                        Include a job for publishing documentation to
                        docs.pulpproject.org/<plugin_name>/. This job requires the project-specific
                        authorized ssh key to be set as a secret named `PULP_DOCS_KEY`.

  pulp_settings         A dictionary of settings that the plugin tests require to be set.

  pulpcore_revision     The git commit hash to check out and install in Github Actions.
                        "Required PR" in a commit message will override this.
  pulpcore_branch       The branch of pulpcore to check out and install in Github Actions.
                        This only applies to non-tagged jobs, such as PRs & cron jobs.
                        "Required PR" in a commit message will override this.
                        Your requirements in "setup.py" may inadvertently override this as well.

  pulpcore_pip_version_specifier
                        A pip version specifier for when pulpcore gets installed from PyPI.
                        This is only for Github Actions, and only applies to TAGGED (release) jobs.
                        An example is "~=3.0.0", which installs the latest 3.0.z,
                        and is equivalent to `pip install pulpcore~=3.0.0`.
                        Defaults to null, which installs the latest release from PyPI.
                        Your requirements in "setup.py" may inadvertently override this as well.

  pydocstyle            Boolean, whether to have flake8 use pydocstyle to check for compliance with
                        Python docstring conventions.

  pypi_username         The username that should be used when uploading packages to PyPI. It
                        is required unless deploy_client_to_pypi and deploy_daily_client_to_pypi
                        and deploy_to_pypi are specified.

  python_version        Python version to use in the CI. Currently only 3.6 and 3.8 are supported.

  redmine_project       A string that corresponds to the redmine identifier for the repo's project.
                        This is used during commit validation to make sure the commit is attached to
                        an issue in the correct project.

  release_user          The GitHub user that is associated with the RELEASE_TOKEN secret on GitHub.
                        The username and token are used to push the Changelog and version bump commits
                        created by the release workflow. The default is 'pulpbot'.

  release_email         The email address associated with the release_user.

  noissue_marker        A string that is used to mark a commit as not attached to an issue.

  single_commit_check   Runs a job to check whether a PR contains a single commit or not.

  sync_ci               Enables a nightly workflow to update the CI files.

  test_bindings         Include a job that runs a script to test generated client
                        library.

                        This job requires the plugin author to include a 'test_bindings.rb'
                        script in the ./.ci/assets/bindings directory of the plugin repository. This
                        script is supposed to exercise the generated client library.

  test_cli              Run the pulp-cli tests as part of the CI tests

  test_performance      Include a nightly job that runs a script to test performance. If using a
                        list, a separate job will run a specific performance test file for each
                        entry in the list. Otherwise, all performance tests will be run together.

  test_released_plugin_with_next_pulpcore_release
                        Include a cron job that tests the latest released version of the plugin to
                        see if it is compatible with pulpcore's main branch. This helps ensure
                        that pulpcore is following the deprecation policy for the plugin API.

  disabled_redis_runners
                        A list of test runners that should have the Redis service disabled. By
                        default, all runners execute tests with the Redis service enabled. The list
                        can be adjusted by specifying the names of runners (e.g., [s3, azure]).

  test_azure            Include azure job for running tests using [azurite](https://github.com/Azure/Azurite)
                        to emulate Azure.

  test_s3               Include s3 job for running tests using [minio](https://github.com/minio/minio)
                        to emulate S3.

  update_redmine        The CI will automatically change the state of tickets when PRs are opened,
                        or merged, and when the changes are released.

  update_github         The CI will automatically change the state of tickets when changes are released.

  ci_trigger            Value for the `on` clause on workflow/ci.yml (push, pull_request, etc...)
  ci_env                Environment variables to set for the CI build.
  pre_job_template      holds name and a path for a template to be included to run before jobs.
  post_job_template     holds name and a path for a template to be included to run after jobs.
```

# Bootstrap a new Pulp plugin

The next step is to bootstrap the plugin. This will create a functional but useless plugin, with
minimal code and tests.

1. Run the `plugin-template --bootstrap` command. This will create a skeleton for your plugin. It
   will contain a ``setup.py``, expected plugin layout and stubs for necessary classes, methods,
   and tests.

   ``$ ./plugin-template --bootstrap PLUGIN_NAME``

In addition to the basic plugin boilerplate, this template also provides a basic set of
functional tests using the [pulp_smash](https://pulp-smash.readthedocs.io/en/latest/) framework.

In order to use these tests, you will need to address the "FIXME" messages left in places where
plugin-writer intervention is required.

At this point, you have a one-off opportunity to use the --all option, which generates everything
included in the --bootstrap option, as well as documentation, functional and unit test, and Github
Actions configuration file templates that you require to support a plugin.

  **Note** : Regenerating the *bootstrap* section at a later time will reset all files to their
  original state, which is almost always not intended.

# Add CI configuration to a Pulp plugin

The next step is to add Github Actions workflows and scripts for continuous integration. These
are highly recommended, as they will make continuous verification of your plugin's functionality
much easier.

1. Run the `./plugin-template --github` command to generate the CI config based on the settings in
   `template_config.yml`.

   ``$ ./plugin-template --github PLUGIN_NAME``

Running the command again will update the plugin with the latest Github Actions CI configuration
provided by the plugin-template.

# Add Documentation to a Pulp plugin

The next step is to add documentation that can be hosted on
[Read the Docs](https://readthedocs.org/).

1. Run the `./plugin-template --docs` command to generate the docs.

   ``$ ./plugin-template --docs PLUGIN_NAME``

## Discoverability

After bootstrapping, your plugin should be installable and discoverable by Pulp.

1. Install your bootstrapped plugin

    `pip install -e your_plugin_name`

2. Start/restart the Pulp Server

    `django-admin runserver 24817`

3. Check that everything worked and you have a remote endpoint

    `$ http GET http://localhost:24817/pulp/api/v3/remotes/{{ plugin_app_label }}/{{ plugin_dash_short }}/`


The plugin specific `/pulp/api/v3/content/{{ plugin_dash_short }}/` endpoints
should now also be available, and you can validate this by checking the hosted docs
http://localhost:24817/pulp/api/v3/docs

Your plugin is discoverable by Pulp because it is [a Django application that subclasses
pulpcore.plugin.PulpPluginAppConfig]({{ plugin_snake }}/app/__init__.py)

For more information about plugin discoverability, including how it works and plugin
entrypoints see [the discoverability documentation](meta_docs/discoverability.md)


# Customizing Plugin Behavior

First, look at the [overview](https://docs.pulpproject.org/pulpcore/plugins/plugin-writer/concepts/index.html) of Pulp Models to understand how Pulp fits these pieces together.

Bootstrapping created various new endpoints (e.g. remote, repository and content).
Additional information should be added to these to tell Pulp how to handle your content.

For each of these endpoints, the bootstrap has created a `model`, a `serializer` and a `viewset`.
The [model](https://docs.djangoproject.com/en/2.1/topics/db/models/) is how the data is stored in the database.
The [serializer](http://www.django-rest-framework.org/api-guide/serializers/) converts complex data to easily parsable types (XML, JSON).
The [viewset](http://www.django-rest-framework.org/api-guide/viewsets/) provides the handlers to serve/receive the serialized data.

## Subclassing Content, Remote

Always subclass the relevant model, serializer, and viewset from the `pulpcore.plugin`
namespace. Pulp provides custom behavior for these, and although implementation details
are located in `pulpcore.app`, plugins should always use `pulpcore.plugin` instead,
since `pulpcore.plugin` gurantees the plugin API semantic versioning

Models:
 * model(s) for the specific content type(s) used in plugin, should be subclassed from [pulpcore.plugin.models.Content](https://github.com/pulp/pulpcore/blob/main/pulpcore/pulpcore/app/models/content.py) model
 * model(s) for the plugin specific repository(ies), should be subclassed from [pulpcore.plugin.models.Repository](https://github.com/pulp/pulpcore/blob/main/pulpcore/pulpcore/app/models/repository.py) model
 * model(s) for the plugin specific remote(s), should be subclassed from [pulpcore.plugin.models.Remote](https://github.com/pulp/pulpcore/blob/main/pulpcore/pulpcore/app/models/repository.py) model

Serializers:
 * serializer(s) for plugin specific content type(s), should be subclassed from [pulpcore.plugin.serializers.ContentSerializer](https://github.com/pulp/pulpcore/blob/main/pulpcore/pulpcore/app/serializers/content.py)
 * serializer(s) for plugin specific remote(s), should be subclassed from [pulpcore.plugin.serializers.RemoteSerializer](https://github.com/pulp/pulpcore/blob/main/pulpcore/pulpcore/app/serializers/repository.py)
 * serializer(s) for plugin specific repository(ies), should be subclassed from [pulpcore.plugin.serializers.RepositorySerializer](https://github.com/pulp/pulpcore/blob/main/pulpcore/pulpcore/app/serializers/repository.py)

Viewsets:
 * viewset(s) for plugin specific content type(s), should be subclassed from [pulpcore.plugin.viewsets.ContentViewSet](https://github.com/pulp/pulpcore/blob/main/pulpcore/pulpcore/app/viewsets/content.py)
 * viewset(s) for plugin specific repository(ies), should be subclassed from [pulpcore.plugin.viewsets.RepositoryViewset](https://github.com/pulp/pulpcore/blob/main/pulpcore/pulpcore/app/viewsets/repository.py)
 * viewset(s) for plugin specific remote(s), should be subclassed from [pulpcore.plugin.viewsets.RemoteViewset](https://github.com/pulp/pulpcore/blob/main/pulpcore/pulpcore/app/viewsets/repository.py)

Keep [namespacing](meta_docs/subclassing/namespacing.md) in mind when writing your viewsets.

## Content

### Model

First model your content type. This file is located at [{{ plugin_snake }}/app/models.py]({{ plugin_snake }}/app/models.py).
Add any fields that correspond to the metadata of your content, the could be the project name, the author name, or any other type of metadata.

The ``TYPE`` class attribute is used for filtering purposes.
If a uniqueness constraint is needed, add a ``Meta`` class to the model like so:

```
class {{ plugin_camel_short }}Content(Content):
    TYPE = '{{ plugin_dash_short }}'
    filename = models.TextField(unique=True, db_index=True, blank=False)

    class Meta:
        unique_together = ('filename',)
```

After adding the model, you can run the migration with

`pulp-manager makemigrations {{ plugin_app_label }}`

And make sure all your fields are on the {{ plugin_app_label }} database table.

### Serializer

Next, add a corresponding serializer field on the in [{{ plugin_snake }}/app/serializers.py]({{ plugin_snake }}/app/serializers.py).
See the [DRF documentation on serializer fields to see what's available](http://www.django-rest-framework.org/api-guide/fields/)


### Viewset

Last, add any additional routes to your [{{ plugin_snake }}/app/viewsets.py]({{ plugin_snake }}/app/viewsets.py).
The content viewset usually doesn't require any additional routes, so you can leave this alone for now.


## Remote

Remotes provide metadata about how content should be downloaded into Pulp, such as the URL of the remote source, the download policy, and some authentication settings. The base ``Remote`` class provided by Pulp Platform provides support for concurrent downloading of remote content.

### Model

First model your remote. This file is located at [{{ plugin_snake }}/app/models.py]({{ plugin_snake }}/app/models.py).
Add any fields that correspond to the remote source.

Remember to define the ``TYPE`` class attribute which is used for filtering purposes.

### Serializer

Next, add a corresponding serializer field on the in [{{ plugin_snake }}/app/serializers.py]({{ plugin_snake }}/app/serializers.py).

### Viewset

Last, add any additional routes to your [{{ plugin_snake }}/app/viewsets.py]({{ plugin_snake }}/app/viewsets.py).
The remote viewset usually doesn't require any additinal routes, so you can leave this alone for now.

## Repository

A Repository knows the specifics of which Content it supports and defines how to create new RepositoryVersions.
It is also responsible for validating that those RepositoryVersions are valid.

### Model

First model your repository. This file is located at [{{ plugin_snake }}/app/models.py]({{ plugin_snake }}/app/models.py). Add any fields as necessary for your specific content type.

Remember to define the ``TYPE`` class attribute which is used for filtering purposes, and ``CONTENT_TYPES`` which
defines which types of content are supported by the Repository. This is a list of classes such as
{{ plugin_camel_short }}Content representing the various content types your plugin supports (that you want
this repository type to support, if there is more than one repository type in your plugin).

Also, if you want to provide validation that the whole collection of the content in your RepositoryVersion makes sense
together, you do that by defining ``finalize_new_version`` on your repository model.

### Serializer

Next, add a corresponding serializer field on the in [{{ plugin_snake }}/app/serializers.py]({{ plugin_snake }}/app/serializers.py).

### Viewset

Last, add any additional routes to your [{{ plugin_snake }}/app/viewsets.py]({{ plugin_snake }}/app/viewsets.py).
Note the sync route is predefined for you. This route kicks off a task [{{ plugin_snake }}.app.tasks.synchronizing.py]({{ plugin_snake }}.app.tasks.synchronizing.py).

If you have more than one Repository type in your plugin, or you change the name of your existing one, you will also
need to have a RepositoryVersionViewSet defined for it (just a viewset, no other objects needed). This hasfield, ``parent_viewset``, which should be set to the accompanying Repository class defined in your plugin.


# Exporter

TODO

# Tasks

[Tasks](meta_docs/tasks/index.md) such as sync and publish are needed to tell Pulp how to perform certain actions.

[More about Sync task](meta_docs/tasks/add-remove.md)

[More about Publish task](meta_docs/tasks/publish.md)

[More about Export task](meta_docs/tasks/export.md)

# Tests

TODO

# Documentation

Your bootstrap template comes with a set of [prepopulated docs](docs/). You can host these on
readthedocs when you are ready.

Pulp also comes with a set of [auto API docs](meta_docs/reference/documentation.md). When your
plugin is installed endpoints in the live api docs will be automatically populate.

When you run 'make html' command to build the docs, you must have the pulp-api running on
localhost. The 'make html' command first downloads the OpenAPI schema for the plugin and saves it
in ``docs/_static/api.json``. This file will then provide data needed to display the restapi.html
page in the root of the built docs.

# Github Actions configuration

The script for generating a CI/CD configuration provided in this repository can be used to change
and update said configuration.
It should be run with the following command.

```
$ ./plugin-template --github PLUGIN_NAME
```

The default behavior enables two build jobs that generate client libraries using the OpenAPI
schema. One publishes to PyPI using ``pypi-username`` setting and the secret environment
variable called $PYPI_PASSWORD. The other job publishes the client to rubygems.org and requires
the $RUBYGEMS_API_KEY secret to be set. Both environment variables can be set in the Github secrets
settings page for the plugin repository. The job that publishes tagged builds to PyPI uses the same
configs as the client publishing job.

The before_install.sh, install.sh, before_script.sh, and script.sh can be augmented by plugin
writers by creating specially named scripts in their `.github/workflows/scripts/` directory. The
scripts are executed in the following order, with optional plugin provided scripts in bold:

1. **pre_before_install.sh**
1. before_install.sh
1. **post_before_install.sh**
1. install.sh
1. **pre_before_script.sh**
1. before_script.sh
1. **post_before_script.sh**
1. script.sh
1. **post_docs_test.sh**
1. **post_script.sh**

# Additional Topics

* [CLI](metadocs/reference/cli.md)
* [Community Development](metadocs/reference/community-development.md)
* [Live API](metadocs/reference/live-api.md)
* [Error Handling](metadocs/reference/error_handling.md)
* [Releasing](metadocs/reference/releasing.md)

# A Plugin Completeness Checklist

- [ ] Plugin django app is defined using PulpAppConfig as a parent
- [ ] Plugin entry point is defined
- [ ] Necessary models/serializers/viewsets are defined. At a minimum:
    - [ ] models for plugin content type, repository, remote
    - [ ] serializers for plugin content type, repository, remote
    - [ ] viewset for plugin content type, repository, remote
- [ ] Database migrations are generated and committed
- [ ] Errors are handled according to Pulp conventions
- [ ] Docs for plugin are available (any location and format preferred and provided by plugin writer)


# Tagging plugin_template

plugin_template uses towncrier to manage a changelog for plugin writers to view. Whenever there is a
major change to plugin_template, we recommend generating the changelog and tagging it.

The versions is the day in the format YYYY.MM.DD (eg "2020.08.11"). If there is more than one
release on a day, you can append a number to end after a hyphen (eg "2020.08.11-1").

1. First, generate the changelog with your version (`towncrier --yes --version 2020.08.11`)
2. Check in the new changelog, push, and open your PR.
3. After the PR is merged, create a tag pointing to the changelog commit (`git tag 2020.08.11 9fceb02`)
4. Push your tag (`git push origin 2020.08.11`)


# Contributing

### Pull Request Checklist

1. Unless a change is small or doesn't affect plugin writers, create an issue on
https://pulp.plan.io/projects/pulp. Add the tag "Plugin Template".
2. Add [a changelog update.](https://docs.pulpproject.org/contributing/git.html#changelog-update)
3. Write an excellent [Commit Message.](https://docs.pulpproject.org/contributing/git.html#commit-message)
Make sure you reference and link to the issue.
4. Push your branch to your fork and open a [Pull request across forks.](https://help.github.com/articles/creating-a-pull-request-from-a-fork/)
