Template to create your own plugin
==================================

This is the ``plugin_template`` repository to help plugin writers
get started and write their own plugin for `Pulp Project
3.0+ <https://pypi.python.org/pypi/pulpcore/>`__.

Clone this repository and run the provided ``rename.py`` script to create
a skeleton for your plugin with the name of your choice. It will contain
``setup.py``, expected plugin layout and stubs for necessary classes and methods.

``$ git clone https://github.com/pulp/plugin_template.git``

``$ cd plugin_template``

``$ ./rename.py your_plugin_name``

Check `Plugin Writer's Guide <http://docs.pulpproject.org/en/3.0/nightly/plugins/plugin-writer/index.html>`__
for more details and suggestions on plugin implementaion.

Below are some ideas for how to document your plugin.


All REST API examples below use `httpie <https://httpie.org/doc>`__ to
perform the requests.

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

From source
~~~~~~~~~~~

Define installation steps here.

Install from PyPI
~~~~~~~~~~~~~~~~~

Define installation steps here.


Create a repository ``foo``
---------------------------

``$ http POST http://localhost:8000/api/v3/repositories/ name=foo``

``$ export REPO_HREF=$(http :8000/api/v3/repositories/ | jq -r '.results[] | select(.name == "foo") | ._href')``

Add an Importer to repository ``foo``
-------------------------------------

Add important details about your Importer and provide examples.

``$ http POST http://localhost:8000/api/v3/importers/plugin-template/ some=params repository=$REPO_HREF``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/importers/plugin-template/$UUID/",
        ...
    }

``$ export IMPORTER_HREF=$(http :8000/api/v3/importers/plugin-template/ | jq -r '.results[] | select(.name == "bar") | ._href')``


Sync repository ``foo`` using Importer ``bar``
----------------------------------------------

Use ``plugin-template`` Importer:

``$ http POST $IMPORTER_HREF'sync/'``


Add a Publisher to repository ``foo``
-------------------------------------

``$ http POST http://localhost:8000/api/v3/publishers/plugin-template/ name=bar repository=$REPO_HREF``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/publishers/plugin-template/$UUID/",
        ...
    }

``$ export PUBLISHER_HREF=$(http :8000/api/v3/publishers/file/ | jq -r '.results[] | select(.name == "bar") | ._href')``


Create a Publication using Publisher ``bar``
--------------------------------------------

``$ http POST http://localhost:8000/api/v3/publications/ publisher=$PUBLISHER_HREF``

.. code:: json

    [
        {
            "_href": "http://localhost:8000/api/v3/tasks/fd4cbecd-6c6a-4197-9cbe-4e45b0516309/",
            "task_id": "fd4cbecd-6c6a-4197-9cbe-4e45b0516309"
        }
    ]

``$ export PUBLICATION_HREF=$(http :8000/api/v3/publications/ | jq -r --arg PUBLISHER_HREF "$PUBLISHER_HREF" '.results[] | select(.publisher==$PUBLISHER_HREF) | ._href')``

Add a Distribution to Publisher ``bar``
---------------------------------------

``$ http POST http://localhost:8000/api/v3/distributions/ name='baz' publisher=$PUBLISHER_HREF publication=$PUBLICATION_HREF``


Check status of a task
----------------------

``$ http GET http://localhost:8000/api/v3/tasks/82e64412-47f8-4dd4-aa55-9de89a6c549b/``

Download ``foo.tar.gz`` from Pulp
---------------------------------

``$ http GET http://localhost:8000/content/foo/foo.tar.gz``
