<!-- TEMPLATE_REMOVE_START -->

This is the ``plugin_template`` repository to help plugin writers get started and write their own
plugin for [Pulp Project 3.0+](https://pypi.python.org/pypi/pulpcore/).


# Plugin Writing Walkthrough

If you are planning on writing a new Pulp plugin, but have no idea what you're doing you've come to the right place.
The purpose of this guide is to walk you through, step by step, the Pulp plugin creation process.

This guide specifically details *how* you write a new content plugin.

[*Why* would you want to write a plugin?](https://docs.pulpproject.org/en/3.0/nightly/plugins/index.html)

[*What* exactly is this Pulp thing?](https://docs.pulpproject.org/en/3.0/nightly/overview/concepts.html)

It's recommend that you develop on a system that already has
[Pulp installed](https://docs.pulpproject.org/en/3.0/nightly/installation/instructions.html).
This allows you to test your plugin at every step.

It's also recommended that you go through the [planning guide](meta_docs/planning-guide.md) before starting to develop your plugin.

# Bootstrap a new Pulp plugin

The first step is to bootstrap this template. This will create a functional but useless plugin,
with minimal code, docs, and tests. Later on we'll discuss exactly what each part of this template does and what to
change to create a 'real' plugin.

1. Clone this repository

   ``$ git clone https://github.com/pulp/plugin_template.git``

   ``$ cd plugin_template``

2. Run the provided ``bootstrap.py`` script to create a skeleton for your plugin with the name of your choice.
   It will contain a ``setup.py``, expected plugin layout and stubs for necessary classes and methods, minimal docs,
   and tests.

   ``$ ./bootstrap.py --bootsrap your_plugin_name``

   **NOTE** : Whatever you choose for `your_plugin_name` will be prefixed with `pulp_`.
   Therefore, for this argument it is best to just provide the content type
   which you would like to support, e.g. `rubygem` or `maven`.


In addition to the basic plugin boilerplate, this template also provides a basic set of
functional tests using the [pulp_smash](https://pulp-smash.readthedocs.io/en/latest/) framework,
and a Travis configuration file / scripts for continuous integration. These are highly recommended,
as they will make continuous verification of your plugin's functionality much easier.

In order to use these tests, you will need to address the "FIXME" messages left in places where
plugin-writer intervention is required.


## Discoverability

After bootstrapping, your plugin should be installable and discoverable by Pulp.

1. Install your bootstrapped plugin

    `pip install -e your_plugin_name`

2. Start/restart the Pulp Server

    `django-admin runserver 24817`

3. Check that everything worked and you have a remote endpoint

    `$ http GET http://localhost:24817/pulp/api/v3/remotes/{{ plugin_snake_short }}/{{ plugin_dash_short }}/`


The plugin specific `/pulp/api/v3/publishers/{{ plugin_dash_short }}/` and `/pulp/api/v3/content/{{ plugin_dash_short }}/` endpoints
should now also be available, and you can validate this by checking the hosted docs
http://localhost:24817/pulp/api/v3/docs

Your plugin is discoverable by Pulp because it is [a Django application that subclasses
pulpcore.plugin.PulpPluginAppConfig]({{ plugin_snake }}/app/__init__.py)

For more information about plugin discoverability, including how it works and plugin
entrypoints see [the discoverability documentation](meta_docs/discoverability.md)


# Customizing Plugin Behavior

First, look at the [overview](https://docs.pulpproject.org/en/3.0/nightly/plugins/plugin-writer/first-plugin.html#understanding-models) of Pulp Models to understand how Pulp fits these pieces together.

Bootstrapping created three new endpoints (remote, publisher, and content). Additional information should be added to these
to tell Pulp how to handle your content.

For each of these three endpoints, the bootstrap has created a `model`, a `serializer` and a `viewset`.
The [model](https://docs.djangoproject.com/en/2.1/topics/db/models/) is how the data is stored in the database.
The [serializer](http://www.django-rest-framework.org/api-guide/serializers/) converts complex data to easily parsable types (XML, JSON).
The [viewset](http://www.django-rest-framework.org/api-guide/viewsets/) provides the handlers to serve/receive the serialized data.

## Subclassing Content, Remote, Publisher

Always subclass the relevant model, serializer, and viewset from the `pulpcore.plugin`
namespace. Pulp provides custom behavior for these, and although implementation details
are located in `pulpcore.app`, plugins should always use `pulpcore.plugin` instead,
since `pulpcore.plugin` gurantees the plugin API semantic versioning

Models:
 * model(s) for the specific content type(s) used in plugin, should be subclassed from [pulpcore.plugin.models.Content](https://github.com/pulp/pulpcore/blob/master/pulpcore/pulpcore/app/models/content.py) model
 * model(s) for the plugin specific remote(s), should be subclassed from [pulpcore.plugin.models.Remote](https://github.com/pulp/pulpcore/blob/master/pulpcore/pulpcore/app/models/repository.py) model
 * model(s) for the plugin specific publisher(s), should be subclassed from [pulpcore.plugin.models.Publisher](https://github.com/pulp/pulpcore/blob/master/pulpcore/pulpcore/app/models/repository.py) model

Serializers:
 * serializer(s) for plugin specific content type(s), should be subclassed from [pulpcore.plugin.serializers.ContentSerializer](https://github.com/pulp/pulpcore/blob/master/pulpcore/pulpcore/app/serializers/content.py)
 * serializer(s) for plugin specific remote(s), should be subclassed from [pulpcore.plugin.serializers.RemoteSerializer](https://github.com/pulp/pulpcore/blob/master/pulpcore/pulpcore/app/serializers/repository.py)
 * serializer(s) for plugin specific publisher(s), should be subclassed from [pulpcore.plugin.serializers.PublisherSerializer](https://github.com/pulp/pulpcore/blob/master/pulpcore/pulpcore/app/serializers/repository.py)

Viewsets:
 * viewset(s) for plugin specific content type(s), should be subclassed from [pulpcore.plugin.viewsets.ContentViewSet](https://github.com/pulp/pulpcore/blob/master/pulpcore/pulpcore/app/viewsets/content.py)
 * viewset(s) for plugin specific remote(s), should be subclassed from [pulpcore.plugin.viewsets.RemoteViewset](https://github.com/pulp/pulpcore/blob/master/pulpcore/pulpcore/app/viewsets/repository.py)
 * viewset(s) for plugin specific publisher(s), should be subclassed from [pulpcore.plugin.viewsets.PublisherViewset](https://github.com/pulp/pulpcore/blob/master/pulpcore/pulpcore/app/viewsets/repository.py)

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

`pulp-manager makemigrations {{ plugin_snake_short }}`

And make sure all your fields are on the {{ plugin_snake_short }} database table.

### Serializer

Next, add a corresponding serializer field on the in [{{ plugin_snake }}/app/serializers.py]({{ plugin_snake }}/app/serializers.py).
See the [DRF documentation on serializer fields to see what's available](http://www.django-rest-framework.org/api-guide/fields/)


### Viewset

Last, add any additional routes to your [{{ plugin_snake }}/app/viewsets.py]({{ plugin_snake }}/app/viewsets.py).
The content viewset usually doesn't require any additinal routes, so you can leave this alone for now.


## Remote

A remote knows specifics of the plugin Content to put it into Pulp. Remote defines how to synchronize remote content.
Pulp Platform provides support for concurrent downloading of remote content. Plugin writer is encouraged to use one of
them but is not required to.

### Model

First model your remote. This file is located at [{{ plugin_snake }}/app/models.py]({{ plugin_snake }}/app/models.py).
Add any fields that correspond to the remote source.

Remember to define the ``TYPE`` class attribute which is used for filtering purposes,

### Serializer

Next, add a corresponding serializer field on the in [{{ plugin_snake }}/app/serializers.py]({{ plugin_snake }}/app/serializers.py).

### Viewset

Last, add any additional routes to your [{{ plugin_snake }}/app/viewsets.py]({{ plugin_snake }}/app/viewsets.py).
Note the sync route is predefined for you. This route kicks off a task [{{ plugin_snake }}.app.tasks.synchronizing.py]({{ plugin_snake }}.app.tasks.synchronizing.py).

## Publisher

### Model
e. This file is located at [{{ plugin_snake }}/app/models.py]({{ plugin_snake }}/app/models.py).
Add any additional fields.

Make sure you define the ``TYPE`` class attribute which is used for filtering purposes,

### Serializer
Next, add a corresponding serializer field on the in [{{ plugin_snake }}/app/serializers.py]({{ plugin_snake }}/app/serializers.py).

### Viewset

Last, add any additional routes to your [{{ plugin_snake }}/app/viewsets.py]({{ plugin_snake }}/app/viewsets.py).
Note the publish route is predefined for you. This route kicks off a task [{{ plugin_snake }}.app.tasks.publishing.py]({{ plugin_snake }}.app.tasks.publishing.py).

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
in ``docs/_static/api.json``. You should add this file to git. This file will then provide data
needed to display the restapi.html page in the root of the built docs.

# Travis configuration

This repository also provides a script for generating a Travis configuration. The script should be
run with the following command.

   ``$ ./bootstrap.py --travis --pypi-username your_pypi_username plugin_name``

The default behavior enables two build stages that generate client libraries using the OpenAPI
schema. One publishes to PyPI using ``--pypi-username`` setting and the secret environment
variable called $PYPI_PASSWORD. The other stage publishes the client to rubygems.org and requires
the $RUBYGEMS_API_KEY environment variable to be set. Both environment variables can be created on
the travis-ci.com settings page for the plugin[0]. The stage that publishes tagged builds to PyPI
uses the same configs as the client publishing stage. The default pipeline can be created using the
following commands:

```
$ git clone git@github.com/pulp/{{ plugin_snake_short }}
$ cd {{ plugin_snake_short }}
$ # copying the requirements file is only needed if plugin was created before this file was added
$ # to the plugin template
$ cp doc_requirements.txt ../pulp_<plugin_name>/
$ touch ../pulp_<plugin_name>/.travis/test_bindings.py
$ ./bootstrap.py --travis --pypi-username your_pypi_username plugin_name
```

The before_install.sh, install.sh, before_script.sh, and script.sh can be augmented by plugin
writers by creating specially named scripts in their .travis directories. The scripts are executed
in the following order, with optional plugin provided scripts in bold:

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

The pipeline can be modified, see the help text for available options.

```
$ ./bootstrap.py --help
usage: bootstrap.py [-h] [--bootstrap] [--test] [--travis] [--docs] [--all]
                    [--verbose] [--pypi-username PYPI_USERNAME]
                    [--exclude-docs-test] [--exclude-mariadb-test]
                    [--exclude-deploy-to-pypi] [--exclude-test-bindings]
                    [--exclude-deploy-client-to-pypi]
                    [--exclude-deploy-client-to-rubygems]
                    [--exclude-deploy-daily-client-to-pypi]
                    [--exclude-deploy-daily-client-to-rubygems]
                    [--exclude-check-commit-message] [--exclude-coverage]
                    plugin_name

Generate a .travis.yml and .travis directoryfor a specified plugin

positional arguments:
  plugin_name           Create or update this plugin.


optional arguments:
  -h, --help            show this help message and exit
  --bootstrap           Create a new plugin and template boilerplate code.

  --test                Generate or update functional and unit tests.

  --travis              Generate or update travis configuration files.

  --docs                Generate or update plugin documentation.

  --all                 Create a new plugin and template all non-excluded files.

  --verbose             Include more output.

  --pypi-username PYPI_USERNAME
                        The username that should be used when uploading packages to PyPI. It
                        is required unless --exclude-deploy-client-to-pypi and
                        --exclude-deploy-daily-client-to-pypi and --exclude-deploy-to-pypi are
                        specified.

  --exclude-docs-test   Exclude a Travis build for testing the 'make html' command for sphinx
                        docs

  --exclude-mariadb-test
                        Exclude a Travis build for testing against MariaDB.

  --exclude-deploy-to-pypi
                        Exclude a Travis stage that publishes builds to PyPI

                        This stage only executes when a tag is associated with the commit being
                        built. When enabling this stage, the user is expected to provide a
                        secure environment variable called PYPI_PASSWORD. The variable can
                        be added in the travis-ci.com settings page for the project[0]. The PYPI
                        username is specified using --pypi-username option.

  --exclude-test-bindings
                        Exclude a Travis stage that runs a script to test generated client
                        library.

                        This stage requires the plugin author to include a 'test_bindings.py'
                        script in the .travis directory of the plugin repository. This script
                        is supposed to exercise the generated client library.

  --exclude-deploy-client-to-pypi
                        Exclude a Travis stage that publishes a client library to PyPI.

                        This stage only executes when a tag is associated with the commit being
                        built. When enabling this stage, the user is expected to provide a
                        secure environment variable called PYPI_PASSWORD. The variable can
                        be added in the travis-ci.com settings page for the project[0]. The PYPI
                        username is specified using --pypi-username option.

                        This stage uses the OpenAPI schema for the plugin to generate a Python
                        client library using openapi-generator-cli.

  --exclude-deploy-client-to-rubygems
                        Exclude a Travis stage that publishes a client library to RubyGems.org.

                        This stage only executes when a tag is associated with the commit being
                        built. When enabling this stage, the user is expected to provide a
                        secure environment variable called RUBYGEMS_API_KEY. The variable can
                        be added in the travis-ci.com settings page for the project.

  --exclude-deploy-daily-client-to-pypi
                        Exclude a Travis stage that publishes a client library to PyPI.

                        This stage only executes when a tag is associated with the commit being
                        built. When enabling this stage, the user is expected to provide a
                        secure environment variable called PYPI_PASSWORD. The variable can
                        be added in the travis-ci.com settings page for the project[0]. The PYPI
                        username is specified using --pypi-username option.

                        This stage uses the OpenAPI schema for the plugin to generate a Python
                        client library using openapi-generator-cli.

                        [0] https://docs.travis-ci.com/user/environment-variables/
                        #defining-variables-in-repository-settings

  --exclude-deploy-daily-client-to-rubygems
                        Exclude a Travis stage that publishes a client library to RubyGems.org
                        with each CRON build.

                        This stage only executes on builds trigerred by CRON. When enabling
                        this stage, the user is expected to provide a secure environment
                        variable called RUBYGEMS_API_KEY. The variable can be added in the
                        travis-ci.com settings page for the project.

  --exclude-check-commit-message
                        Exclude inspection of commit message for a reference to an issue in
                        pulp.plan.io.

  --exclude-coverage    Exclude collection of coverage and reporting to coveralls.io
                        pulp.plan.io.

```

# Additional Topics

* [CLI](metadocs/reference/cli.md)
* [Community Development](metadocs/reference/community-development.md)
* [Live API](metadocs/reference/live-api.md)
* [Error Handling](metadocs/reference/error_handling.md)
* [Releasing](metadocs/reference/releasing.md)

# A Plugin Completeness Checklist

- [ ] Plugin django app is defined using PulpAppConfig as a parent
- [ ] Plugin entry point is defined
- [ ] pulpcore-plugin is specified as a requirement in setup.py
- [ ] Necessary models/serializers/viewsets are defined. At a minimum:
    - [ ] models for plugin content type, remote, publisher
    - [ ] serializers for plugin content type, remote, publisher
    - [ ] viewset for plugin content type, remote, publisher

- [ ] Errors are handled according to Pulp conventions
- [ ] Docs for plugin are available (any location and format preferred and provided by plugin writer)


<!-- TEMPLATE_REMOVE_END -->
# {{ plugin_dash }}

A Pulp plugin to support hosting your own {{ plugin_dash_short }}.

For more information, please see the [documentation](docs/index.rst) or the [Pulp project page](https://pulpproject.org/).
