
.. _define-publisher:

Define your plugin Publisher
----------------------------

To define a new publisher, e.g. ``ExamplePublisher``:

* :class:`pulpcore.plugin.models.Publisher` should be subclassed and extended with additional
  attributes to the plugin needs,
* define ``TYPE`` class attribute which is used for filtering purposes,
* create a serializer for your new publisher a subclass of
  :class:`pulpcore.plugin.serializers.PublisherSerializer`,
* create a viewset for your new publisher as a subclass of
  :class:`pulpcore.plugin.viewsets.PublisherViewSet`.

:class:`~pulpcore.plugin.models.Publisher` model should not be used directly anywhere in plugin
code. Only plugin-defined Publisher classes are expected to be used.

Check ``pulp_file`` implementation of `the FilePublisher
<https://github.com/pulp/pulp_file/blob/master/pulp_file/app/models.py>`_.


