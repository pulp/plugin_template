.. _define-content-type:

Define your plugin Content type
-------------------------------

To define a new content type(s), e.g. ``ExampleContent``:

* :class:`pulpcore.plugin.models.Content` should be subclassed and extended with additional
  attributes to the plugin needs,
* define ``TYPE`` class attribute which is used for filtering purposes,
* uniqueness should be specified in ``Meta`` class of newly defined ``ExampleContent`` model,
* ``unique_together`` should be specified for the ``Meta`` class of ``ExampleContent`` model,
* create a serializer for your new Content type as a subclass of
  :class:`pulpcore.plugin.serializers.ContentSerializer`,
* create a viewset for your new Content type as a subclass of
  :class:`pulpcore.plugin.viewsets.ContentViewSet`

:class:`~pulpcore.plugin.models.Content` model should not be used directly anywhere in plugin code.
Only plugin-defined Content classes are expected to be used.

Check ``pulp_file`` implementation of `the FileContent
<https://github.com/pulp/pulp_file/blob/master/pulp_file/app/models.py>`_ and its
`serializer <https://github.com/pulp/pulp_file/blob/master/pulp_file/app/serializers.py>`_
and `viewset <https://github.com/pulp/pulp_file/blob/master/pulp_file/app/viewsets.py>`_.
For a general reference for serializers and viewsets, check `DRF documentation
<http://www.django-rest-framework.org/api-guide/viewsets/>`_.


.. _define-remote:


