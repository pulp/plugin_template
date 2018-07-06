Plugin Writing Walkthrough
==========================

TODO(asmacdo)
    Purpose of the guide
    what you will have when done
    discuss other plugin uses (standard is a new content type, but could just add exporter, for
    example)



Bootstrap a Plugin
------------------

With a firm understanding of the basics, follow the TODO(link, bootstrapping instructions)
The initial result will be a functional but useless plugin. From here use the TODO(link,
walkthrough) which provides narrative documentation alongside the comments in the Python modules
themselves.

.. toctree::
   :maxdepth: 2

   planning-guide
   checklist
   first-plugin
   basics
   releasing
   cli

The Pulp :doc:`../plugin-api/overview` is versioned separately from the Pulp Core and consists
of everything importable within the :mod:`pulpcore.plugin` namespace. When writing plugins, care should
be taken to only import Pulp Core components exposed in this namespace; importing from elsewhere
within the Pulp Core (e.g. importing directly from ``pulpcore.app``, ``pulpcore.exceptions``, etc.)
is unsupported, and not protected by the Pulp Plugin API's semantic versioning guarantees.

.. warning::

    Exactly what is versioned in the Plugin API, and how, still has yet to be determined.
    This documentation will be updated to clearly identify what guarantees come with the
    semantic versioning of the Plugin API in the future. As our initial plugins are under
    development prior to the release of Pulp 3.0, the Plugin API can be assumed to have
    semantic major version 0, indicating it is unstable and still being developed.

Discoverability
---------------

After bootstrapping, your plugin should be installable and discoverable by pulp.

STUB
    extract the tldr from discoverability page
    link to discoverability reference page
    demonstrate how to sanity check new plugin

Customizing
-----------
Linkto (or move here) subclassing/overview


STUB
    Your new plugin now has base functionality, it is time to add custom functionality.
    Discuss:
        content
        remote
            also implement sync(add and remove content link)
        publisher
            also implement publish (publish link)
        exporter
            just a stub

A Plugin Completeness Checklist
===============================

 * :ref:`Plugin django app is defined using PulpAppConfig as a parent <plugin-django-application>`
 * :ref:`Plugin entry point is defined <plugin-entry-point>`
 * `pulpcore-plugin is specified as a requirement <https://github.com/pulp/pulp_file/blob/master/setup.py#L6>`_
 * Necessary models/serializers/viewsets are :ref:`defined <subclassing-platform-models>` and :ref:`discoverable <model-serializer-viewset-discovery>`. At a minimum:

   * models for plugin content type, remote, publisher
   * serializers for plugin content type, remote, publisher
   * viewset for plugin content type, remote, publisher

 * :ref:`Errors are handled according to Pulp conventions <error-handling-basics>`
 * Docs for plugin are available (any location and format preferred and provided by plugin writer)


