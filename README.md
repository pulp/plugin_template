This is the ``plugin_template`` repository to help plugin writers get started and write their own
plugin for [Pulp Project 3.0+](https://pypi.python.org/pypi/pulpcore/).

# Plugin Writing Walkthrough

If you are planning on writing a new Pulp plugin, but have no idea what you're doing you've come to the right place.
The purpose of this guide is to walk you through, step by step, the Pulp plugin creation process.

This guide specifically details *how* you write a new content plugin.

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
the parent directory of the `plugin_template` directory. The `template_config.yml` is written to
the root of this new directory.
It is filled with default values for various aspects of the plugin scaffolding.
You can edit them according to your needs to control subsequent calls to `plugin-template`.

The following settings are stored in `template_config.yml`.

```bash
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
                        secure environment variable called PYPI_API_TOKEN. The variable can
                        be added in the Github secrets settings page for the repository[0].

                        This job uses the OpenAPI schema for the plugin to generate a Python
                        client library using openapi-generator-cli.

  deploy_client_to_rubygems
                        Include a Github Actions job that publishes a client library to RubyGems.org.

                        This job only executes when a tag is associated with the commit being
                        built. When enabling this job, the user is expected to provide a
                        secure environment variable called RUBYGEMS_API_KEY. The variable can
                        be added in the Github secrets settings page for the repository.

  deploy_to_pypi        Include a Github Actions job that publishes builds to PyPI

                        This job only executes when a tag is associated with the commit being
                        built. When enabling this job, the user is expected to provide a
                        secure environment variable called PYPI_API_TOKEN. The variable can
                        be added in the Github secrets settings page for the repository[0].

  docker_fixtures       In Github Actions, use the pulp-fixtures docker container to serve up
                        fixtures instead of using fedorapeople.org.

  github_org            The Github organization to use for the plugin.

  latest_release_branch A pointer to the currently latest release branch (this is automatically
                        updated).

  os_required_packages  A list of packages to be installed on the host OS (Ubuntu) in the build
                        step.

  parallel_test_workers Run tests in parallel using `pytest-xdist` with N parallel runners. This
                        settings specifies N. By default it is 8.

  plugin_app_label      Suppose our plugin is named 'pulp_test', then this is 'test'

  plugin_default_branch The default branch in your plugin repo, defaults to 'main'.

  plugin_name           Suppose our plugin is named 'pulp_test', then this is 'pulp_test'

  plugins               List of dictionaries with `app_label` and `name` as keys. One entry per
                        plugin resident in this repository.

  pulp_settings         A dictionary of settings that the plugin tests require to be set.

  pulp_settings_<scenario>
                        A dictionary of settings that the plugin <scenario> tests can set
                        additionally. `<scenario>` is one of "azure", "s3", "gcp".

  pulp_env              A dictionary of ENV variables used globally by all runners. The variables
                        are translated to separate ENV layers in Containerfile configuring the base
                        Pulp image.

  pulp_env_<scenario>
                        A dictionary of ENV variables that will be translated to separate ENV
                        layers in Containerfile configuring the base Pulp image. `<scenario>` is one
                        of "azure", "s3", "gcp".

  pydocstyle            Boolean, whether to have flake8 use pydocstyle to check for compliance with
                        Python docstring conventions.

  release_user          The GitHub user that is associated with the RELEASE_TOKEN secret on GitHub.
                        The username and token are used to push the Changelog and version bump commits
                        created by the release workflow. The default is 'pulpbot'.

  release_email         The email address associated with the release_user.

  run_pulpcore_tests_for_plugins
                        Pulpcore ships some functional tests that make sense for plugins to run.
                        These are pytest marked with the `from_pulpcore_for_all_plugins`. If true,
                        the CI will run an additional pytest call running pulpcore tests with that
                        mark.

  stalebot              A boolean that indicates whether to use stalebot or not.

  stalebot_days_until_stale
                        The number of days of inactivity before an Issue or Pull Request becomes stale.

  stalebot_days_until_close
                        The number of days of inactivity before an Issue or Pull Request with the stale
                        label is closed.

  supported_release_branches
                        Specify the release branches that should receive regular CI updates.

  sync_ci               Enables a weekly workflow to update the CI files.

  test_cli              Run the pulp-cli tests as part of the CI tests

  test_performance      Include a nightly job that runs a script to test performance. If using a
                        list, a separate job will run a specific performance test file for each
                        entry in the list. Otherwise, all performance tests will be run together.

  disabled_redis_runners
                        A list of test runners that should have the Redis service disabled. By
                        default, all runners execute tests with the Redis service enabled. The list
                        can be adjusted by specifying the names of runners (e.g., [s3, azure]).

  test_azure            Include azure job for running tests using [azurite](https://github.com/Azure/Azurite)
                        to emulate Azure.

  test_gcp              Include gcp job for running tests using [fake-gcs-server](https://github.com/fsouza/fake-gcs-server)
                        to emulate GCP.

  test_lowerbounds      Include lowerbounds job for running tests using lower bounds found in requirements.txt.

  test_s3               Include s3 job for running tests using [minio](https://github.com/minio/minio)
                        to emulate S3.

  ci_trigger            Value for the `on` clause on workflow/ci.yml (push, pull_request, etc...)
  ci_env                Environment variables to set for the CI build.
  pre_job_template      holds name and a path for a template to be included to run before jobs.
  post_job_template     holds name and a path for a template to be included to run after jobs.
  lint_requirements     Boolean (defaults True) to enable upper bound check on requirements.txt
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

The next step is to add documentation.
Pulp has a dedicated documentation tool that aggregates docs from subscribed plugins and handles
its publishing.

To learn more about how it works and how to include your plugin, check out
[pulp-docs documentation](https://pulpproject.org/pulp-docs/docs/dev/).

## Discoverability

After bootstrapping, your plugin should be installable and discoverable by Pulp.

1. Install your bootstrapped plugin

    `pip install -e your_plugin_name`

2. Start/restart the Pulp Server

    `django-admin runserver 24817`

3. Check that everything worked and you have a remote endpoint

    `$ http GET http://localhost:24817/pulp/api/v3/remotes/{{ plugin_app_label }}/{{ plugin_app_label | dash }}/`


The plugin specific `/pulp/api/v3/content/{{ plugin_app_label | dash }}/` endpoints
should now also be available, and you can validate this by checking the hosted docs
http://localhost:24817/pulp/api/v3/docs

Your plugin is discoverable by Pulp because it is [a Django application that subclasses
pulpcore.plugin.PulpPluginAppConfig]({{ plugin_name | snake }}/app/__init__.py)


# Customizing Plugin Behavior

First, look at the [overview](https://pulpproject.org/pulpcore/docs/dev/learn/plugin-concepts/) of Pulp Models to understand how Pulp fits these pieces together.

Bootstrapping created various new endpoints (e.g. remote, repository and content).
Additional information should be added to these to tell Pulp how to handle your content.

For each of these endpoints, the bootstrap has created a `model`, a `serializer` and a `viewset`.
The [model](https://docs.djangoproject.com/en/3.2/topics/db/models/) is how the data is stored in the database.
The [serializer](http://www.django-rest-framework.org/api-guide/serializers/) converts complex data to easily parsable types (XML, JSON).
The [viewset](http://www.django-rest-framework.org/api-guide/viewsets/) provides the handlers to serve/receive the serialized data.

## Subclassing Content, Remote

Always subclass the relevant model, serializer, and viewset from the `pulpcore.plugin`
namespace. Pulp provides custom behavior for these, and although implementation details
are located in `pulpcore.app`, plugins should always use `pulpcore.plugin` instead,
since `pulpcore.plugin` gurantees the plugin API semantic versioning

Models:
 * model(s) for the specific content type(s) used in plugin, should be subclassed from [pulpcore.plugin.models.Content](https://github.com/pulp/pulpcore/blob/main/pulpcore/app/models/content.py) model
 * model(s) for the plugin specific repository(ies), should be subclassed from [pulpcore.plugin.models.Repository](https://github.com/pulp/pulpcore/blob/main/pulpcore/app/models/repository.py) model
 * model(s) for the plugin specific remote(s), should be subclassed from [pulpcore.plugin.models.Remote](https://github.com/pulp/pulpcore/blob/main/pulpcore/app/models/repository.py) model

Serializers:
 * serializer(s) for plugin specific content type(s), should be subclassed from [pulpcore.plugin.serializers.ContentSerializer](https://github.com/pulp/pulpcore/blob/main/pulpcore/app/serializers/content.py)
 * serializer(s) for plugin specific remote(s), should be subclassed from [pulpcore.plugin.serializers.RemoteSerializer](https://github.com/pulp/pulpcore/blob/main/pulpcore/app/serializers/repository.py)
 * serializer(s) for plugin specific repository(ies), should be subclassed from [pulpcore.plugin.serializers.RepositorySerializer](https://github.com/pulp/pulpcore/blob/main/pulpcore/app/serializers/repository.py)

Viewsets:
 * viewset(s) for plugin specific content type(s), should be subclassed from [pulpcore.plugin.viewsets.ContentViewSet](https://github.com/pulp/pulpcore/blob/main/pulpcore/app/viewsets/content.py)
 * viewset(s) for plugin specific repository(ies), should be subclassed from [pulpcore.plugin.viewsets.RepositoryViewset](https://github.com/pulp/pulpcore/blob/main/pulpcore/app/viewsets/repository.py)
 * viewset(s) for plugin specific remote(s), should be subclassed from [pulpcore.plugin.viewsets.RemoteViewset](https://github.com/pulp/pulpcore/blob/main/pulpcore/app/viewsets/repository.py)

## Content

### Model

First model your content type. This file is located at [{{ plugin_name | snake }}/app/models.py]({{ plugin_name | snake }}/app/models.py).
Add any fields that correspond to the metadata of your content, the could be the project name, the author name, or any other type of metadata.

The ``TYPE`` class attribute is used for filtering purposes.
If a uniqueness constraint is needed, add a ``Meta`` class to the model like so:

```
class {{ plugin_app_label | camel }}Content(Content):
    TYPE = '{{ plugin_app_label | dash }}'
    filename = models.TextField(unique=True, db_index=True, blank=False)

    class Meta:
        unique_together = ('filename',)
```

After adding the model, you can run the migration with

`pulp-manager makemigrations {{ plugin_app_label }}`

And make sure all your fields are on the {{ plugin_app_label }} database table.

### Serializer

Next, add a corresponding serializer field on the in [{{ plugin_name | snake }}/app/serializers.py]({{ plugin_name | snake }}/app/serializers.py).
See the [DRF documentation on serializer fields to see what's available](http://www.django-rest-framework.org/api-guide/fields/)


### Viewset

Last, add any additional routes to your [{{ plugin_name | snake }}/app/viewsets.py]({{ plugin_name | snake }}/app/viewsets.py).
The content viewset usually doesn't require any additional routes, so you can leave this alone for now.


## Remote

Remotes provide metadata about how content should be downloaded into Pulp, such as the URL of the remote source, the download policy, and some authentication settings. The base ``Remote`` class provided by Pulp Platform provides support for concurrent downloading of remote content.

### Model

First model your remote. This file is located at [{{ plugin_name | snake }}/app/models.py]({{ plugin_name | snake }}/app/models.py).
Add any fields that correspond to the remote source.

Remember to define the ``TYPE`` class attribute which is used for filtering purposes.

### Serializer

Next, add a corresponding serializer field on the in [{{ plugin_name | snake }}/app/serializers.py]({{ plugin_name | snake }}/app/serializers.py).

### Viewset

Last, add any additional routes to your [{{ plugin_name | snake }}/app/viewsets.py]({{ plugin_name | snake }}/app/viewsets.py).
The remote viewset usually doesn't require any additinal routes, so you can leave this alone for now.

## Repository

A Repository knows the specifics of which Content it supports and defines how to create new RepositoryVersions.
It is also responsible for validating that those RepositoryVersions are valid.

### Model

First model your repository. This file is located at [{{ plugin_name | snake }}/app/models.py]({{ plugin_name | snake }}/app/models.py). Add any fields as necessary for your specific content type.

Remember to define the ``TYPE`` class attribute which is used for filtering purposes, and ``CONTENT_TYPES`` which
defines which types of content are supported by the Repository. This is a list of classes such as
{{ plugin_app_label | camel }}Content representing the various content types your plugin supports (that you want
this repository type to support, if there is more than one repository type in your plugin).

Also, if you want to provide validation that the whole collection of the content in your RepositoryVersion makes sense
together, you do that by defining ``finalize_new_version`` on your repository model.

### Serializer

Next, add a corresponding serializer field on the in [{{ plugin_name | snake }}/app/serializers.py]({{ plugin_name | snake }}/app/serializers.py).

### Viewset

Last, add any additional routes to your [{{ plugin_name | snake }}/app/viewsets.py]({{ plugin_name | snake }}/app/viewsets.py).
Note the sync route is predefined for you. This route kicks off a task [{{ plugin_name | snake }}.app.tasks.synchronizing.py]({{ plugin_name | snake }}.app.tasks.synchronizing.py).

If you have more than one Repository type in your plugin, or you change the name of your existing one, you will also
need to have a RepositoryVersionViewSet defined for it (just a viewset, no other objects needed). This hasfield, ``parent_viewset``, which should be set to the accompanying Repository class defined in your plugin.

# Github Actions configuration

The script for generating a CI/CD configuration provided in this repository can be used to change
and update said configuration.
It should be run with the following command.

```
$ ./plugin-template --github PLUGIN_NAME
```

The default behavior enables two build jobs that generate client libraries using the OpenAPI
schema. One publishes to PyPI using the secret environment variable called $PYPI_API_TOKEN.
The other job publishes the client to rubygems.org and requires the $RUBYGEMS_API_KEY secret
to be set. Both environment variables can be set in the Github secrets settings page for the
plugin repository. The job that publishes tagged builds to PyPI uses the same configs as the
client publishing job.

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
1. **post_script.sh**

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
