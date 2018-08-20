<!-- TEMPLATE_REMOVE_START -->

Bootstrap a new Pulp plugin
===========================

This is the ``plugin_template`` repository to help plugin writers
get started and write their own plugin for `Pulp Project
3.0+ <https://pypi.python.org/pypi/pulpcore/>`__.

Clone this repository and run the provided ``bootstrap.py`` script to create
a skeleton for your plugin with the name of your choice. It will contain
``setup.py``, expected plugin layout and stubs for necessary classes and methods.

``$ git clone https://github.com/pulp/plugin_template.git``

``$ cd plugin_template``

``$ ./bootstrap.py your_plugin_name``

.. note::

   Whatever you choose for "your_plugin_name" will be prefixed with "pulp_".
   Therefore, for this argument it is best to just provide the content type
   which you would like to support, e.g. "rubygem" or "maven".

In addition to the basic plugin boilerplate, this template also provides a basic set of
functional tests using the `pulp_smash <https://pulp-smash.readthedocs.io/en/latest/>`_ framework,
and a Travis configuration file / scripts for continuous integration. These are highly recommended,
as they will make continuous verification of your plugin's functionality much easier.

In order to use these tests, you will need to address the "FIXME" messages left in places where
plugin-writer intervention is required.

Check `Plugin Writer's Guide <http://docs.pulpproject.org/en/3.0/nightly/plugins/plugin-writer/index.html>`__
for more details and suggestions on plugin implementation.

Below are some ideas for how to document your plugin.

<!-- TEMPLATE_REMOVE_END -->
``pulp_plugin_template`` Plugin
===============================

All REST API examples below use `httpie <https://httpie.org/doc>`__ to
perform the requests.

.. code-block::

    machine localhost
    login admin
    password admin

If you configured the ``admin`` user with a different password, adjust the configuration
accordingly. If you prefer to specify the username and password with each request, please see
``httpie`` documentation on how to do that.

This documentation makes use of the `jq library <https://stedolan.github.io/jq/>`_
to parse the json received from requests, in order to get the unique urls generated
when objects are created. To follow this documentation as-is please install the jq
library with:

``$ sudo dnf install jq``

Install ``pulpcore``
--------------------

Follow the `installation
instructions <docs.pulpproject.org/en/3.0/nightly/installation/instructions.html>`__
provided with pulpcore.

Install plugin
--------------

This document assumes that you have
`installed pulpcore <https://docs.pulpproject.org/en/3.0/nightly/installation/instructions.html>`_
into a the virtual environment ``pulpvenv``.

Users should install from **either** PyPI or source.


Install ``pulp_plugin_template`` from source
--------------------------------------------

.. code-block:: bash

   sudo -u pulp -i
   source ~/pulpvenv/bin/activate
   cd pulp_plugin_template
   pip install -e .
   django-admin runserver


Install ``pulp_plugin_template`` From PyPI
------------------------------------------

.. code-block:: bash

   sudo -u pulp -i
   source ~/pulpvenv/bin/activate
   pip install pulp-file
   django-admin runserver


Make and Run Migrations
-----------------------

.. code-block:: bash

   pulp-manager makemigrations pulp_plugin_template
   pulp-manager migrate pulp_plugin_template

Run Services
------------

.. code-block:: bash

   pulp-manager runserver
   sudo systemctl restart pulp_resource_manager
   sudo systemctl restart pulp_worker@1
   sudo systemctl restart pulp_worker@2


Create a repository ``foo``
---------------------------

``$ http POST http://localhost:8000/pulp/pulp/api/v3/repositories/ name=foo``

.. code:: json

    {
        "_href": "http://localhost:8000/pulp/api/v3/repositories/1/",
        ...
    }

``$ export REPO_HREF=$(http :8000/pulp/pulp/api/v3/repositories/ | jq -r '.results[] | select(.name == "foo") | ._href')``

Create a new remote ``bar``
---------------------------

``$ http POST http://localhost:8000/pulp/pulp/api/v3/remotes/plugin-template/ name='bar' url='http://some.url/somewhere/'``

.. code:: json

    {
        "_href": "http://localhost:8000/pulp/pulp/api/v3/remotes/plugin-template/1/",
        ...
    }

``$ export REMOTE_HREF=$(http :8000/pulp/pulp/api/v3/remotes/plugin-template/ | jq -r '.results[] | select(.name == "bar") | ._href')``


Sync repository ``foo`` using Remote ``bar``
----------------------------------------------

``$ http POST $REMOTE_HREF'sync/' repository=$REPO_HREF``

Look at the new Repository Version created
------------------------------------------

``$ http GET $REPO_HREF'versions/1/'``

.. code:: json

    {
        "_added_href": "http://localhost:8000/pulp/api/v3/repositories/1/versions/1/added_content/",
        "_content_href": "http://localhost:8000/pulp/api/v3/repositories/1/versions/1/content/",
        "_href": "http://localhost:8000/pulp/api/v3/repositories/1/versions/1/",
        "_removed_href": "http://localhost:8000/pulp/api/v3/repositories/1/versions/1/removed_content/",
        "content_summary": {
            "plugin-template": 3
        },
        "created": "2018-02-23T20:29:54.499055Z",
        "number": 1
    }


Upload ``$CONTENT_NAME`` to Pulp
-----------------------------

Create an Artifact by uploading the plugin-template to Pulp.

``$ http --form POST http://localhost:8000/pulp/api/v3/artifacts/ file@./$CONTENT_NAME``

.. code:: json

    {
        "_href": "http://localhost:8000/pulp/api/v3/artifacts/1/",
        ...
    }

Create ``plugin-template`` content from an Artifact
-----------------------------------------

Create a content unit and point it to your artifact

``$ http POST http://localhost:8000/pulp/api/v3/content/plugin-template/plugin-templates/ relative_path=$CONTENT_NAME artifact="http://localhost:8000/pulp/api/v3/artifacts/1/"``

.. code:: json

    {
        "artifact": "http://localhost:8000/pulp/api/v3/artifacts/1/",
        "relative_path": "$CONTENT_NAME",
        "type": "plugin-template"
    }

``$ export CONTENT_HREF=$(http :8000/pulp/api/v3/content/plugin-template/plugin-templates/ | jq -r '.results[] | select(.relative_path == "$CONTENT_NAME") | ._href')``


Add content to repository ``foo``
---------------------------------

``$ http POST $REPO_HREF'versions/' add_content_units:="[\"$CONTENT_HREF\"]"``


Create a ``plugin-template`` Publisher ``baz``
----------------------------------------------

``$ http POST http://localhost:8000/pulp/pulp/api/v3/publishers/plugin-template/ name=baz repository=$REPO_HREF``

.. code:: json

    {
        "_href": "http://localhost:8000/pulp/pulp/api/v3/publishers/plugin-template/1/",
        ...
    }

``$ export PUBLISHER_HREF=$(http :8000/pulp/pulp/api/v3/publishers/plugin-template/ | jq -r '.results[] | select(.name == "baz") | ._href')``


Use the ``bar`` Publisher to create a Publication
-------------------------------------------------

``$ http POST $PUBLISHER_HREF'publish/' repository=$REPO_HREF``

.. code:: json

    [
        {
            "_href": "http://localhost:8000/pulp/api/v3/tasks/fd4cbecd-6c6a-4197-9cbe-4e45b0516309/",
            "task_id": "fd4cbecd-6c6a-4197-9cbe-4e45b0516309"
        }
    ]

``$ export PUBLICATION_HREF=$(http :8000/pulp/api/v3/publications/ | jq -r --arg PUBLISHER_HREF "$PUBLISHER_HREF" '.results[] | select(.publisher==$PUBLISHER_HREF) | ._href')``

Add a Distribution to Publisher ``bar``
---------------------------------------

``$ http POST http://localhost:8000/pulp/api/v3/distributions/ name='baz' base_path='foo' publication=$PUBLICATION_HREF``


.. code:: json

    {
        "_href": "http://localhost:8000/pulp/api/v3/distributions/1/",
       ...
    }

Check status of a task
----------------------

``$ http GET http://localhost:8000/pulp/pulp/api/v3/tasks/82e64412-47f8-4dd4-aa55-9de89a6c549b/``

Download ``$CONTENT_NAME`` from Pulp
------------------------------------------------------------------

``$ http GET http://localhost:8000/pulp/content/foo/$CONTENT_NAME``
