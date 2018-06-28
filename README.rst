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

Check `Plugin Writer's Guide <http://docs.pulpproject.org/en/3.0/nightly/plugins/plugin-writer/index.html>`__
for more details and suggestions on plugin implementaion.

Below are some ideas for how to document your plugin.


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
        "_href": "http://localhost:8000/pulp/api/v3/repositories/8d7cd67a-9421-461f-9106-2df8e4854f5f/",
        ...
    }

``$ export REPO_HREF=$(http :8000/pulp/pulp/api/v3/repositories/ | jq -r '.results[] | select(.name == "foo") | ._href')``

Create a new remote ``bar``
---------------------------

``$ http POST http://localhost:8000/pulp/pulp/api/v3/remotes/plugin-template/ name='bar' url='http://some.url/somewhere/'``

.. code:: json

    {
        "_href": "http://localhost:8000/pulp/pulp/api/v3/remotes/plugin-template/13ac2d63-7b7b-401d-b71b-9a5af05aab3c/",
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
        "_added_href": "http://localhost:8000/pulp/api/v3/repositories/b787e6ad-d6b6-4e3d-ab12-73eba19b42fb/versions/1/added_content/",
        "_content_href": "http://localhost:8000/pulp/api/v3/repositories/b787e6ad-d6b6-4e3d-ab12-73eba19b42fb/versions/1/content/",
        "_href": "http://localhost:8000/pulp/api/v3/repositories/b787e6ad-d6b6-4e3d-ab12-73eba19b42fb/versions/1/",
        "_removed_href": "http://localhost:8000/pulp/api/v3/repositories/b787e6ad-d6b6-4e3d-ab12-73eba19b42fb/versions/1/removed_content/",
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
        "_href": "http://localhost:8000/pulp/api/v3/artifacts/7d39e3f6-535a-4b6e-81e9-c83aa56aa19e/",
        ...
    }

Create ``plugin-template`` content from an Artifact
-----------------------------------------

Create a content unit and point it to your artifact

``$ http POST http://localhost:8000/pulp/api/v3/content/plugin-template/plugin-templates/ relative_path=$CONTENT_NAME artifact="http://localhost:8000/pulp/api/v3/artifacts/7d39e3f6-535a-4b6e-81e9-c83aa56aa19e/"``

.. code:: json

    {
        "_href": "http://localhost:8000/pulp/api/v3/content/plugin-template/plugin-templates/a9578a5f-c59f-4920-9497-8d1699c112ff/",
        "artifact": "http://localhost:8000/pulp/api/v3/artifacts/7d39e3f6-535a-4b6e-81e9-c83aa56aa19e/",
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
        "_href": "http://localhost:8000/pulp/pulp/api/v3/publishers/plugin-template/fd4cbecd-6c6a-4197-9cbe-4e45b0516309/",
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
        "_href": "http://localhost:8000/pulp/api/v3/distributions/9b29f1b2-6726-40a2-988a-273d3f009a41/",
       ...
    }

Check status of a task
----------------------

``$ http GET http://localhost:8000/pulp/pulp/api/v3/tasks/82e64412-47f8-4dd4-aa55-9de89a6c549b/``

Download ``$CONTENT_NAME`` from Pulp
------------------------------------------------------------------

``$ http GET http://localhost:8000/pulp/content/foo/$CONTENT_NAME``
