
.. _subclassing-platform-models:

Subclassing Content, Remote, Publisher
----------------------------------------

The following classes are expected to be defined by plugin.
For more details and examples see :ref:`define-content-type`, :ref:`define-remote`, :ref:`define-publisher` sections of the guide.

Models:
 * model(s) for the specific content type(s) used in plugin, should be subclassed from Content model
 * model(s) for the plugin specific remote(s), should be subclassed from Remote model
 * model(s) for the plugin specific publisher(s), should be subclassed from Publisher model

Serializers:
 * serializer(s) for plugin specific content type(s), should be subclassed from ContentSerializer
 * serializer(s) for plugin specific remote(s), should be subclassed from RemoteSerializer
 * serializer(s) for plugin specific publisher(s), should be subclassed from PublisherSerializer

Viewsets:
 * viewset(s) for plugin specific content type(s), should be subclassed from ContentViewset
 * viewset(s) for plugin specific remote(s), should be subclassed from RemoteViewset
 * viewset(s) for plugin specific publisher(s), should be subclassed from PublisherViewset

.. _understanding-models:

Understanding models
--------------------
There are models which are expected to be used in plugin implementation, so understanding what they
are designed for is useful for a plugin writer. Each model below has a link to its documentation
where its purpose, all attributes and relations are listed.

Here is a gist of how models are related to each other and what each model is responsible for.

* :class:`~pulpcore.app.models.Repository` contains :class:`~pulpcore.plugin.models.Content`.
  :class:`~pulpcore.plugin.models.RepositoryContent` is used to represent this relation.
* :class:`~pulpcore.plugin.models.Content` can have :class:`~pulpcore.plugin.models.Artifact`
  associated with it. :class:`~pulpcore.plugin.models.ContentArtifact` is used to represent this
  relation.
* :class:`~pulpcore.plugin.models.ContentArtifact` can have
  :class:`~pulpcore.plugin.models.RemoteArtifact` associated with it.
* :class:`~pulpcore.plugin.models.Artifact` is a file.
* :class:`~pulpcore.plugin.models.RemoteArtifact` contains information about
  :class:`~pulpcore.plugin.models.Artifact` from a remote source, including URL to perform
  download later at any point.
* :class:`~pulpcore.plugin.models.Remote` knows specifics of the plugin
  :class:`~pulpcore.plugin.models.Content` to put it into Pulp.
  :class:`~pulpcore.plugin.models.Remote` defines how to synchronize remote content. Pulp
  Platform provides support for concurrent  :ref:`downloading <download-docs>` of remote content.
  Plugin writer is encouraged to use one of them but is not required to.
* :class:`~pulpcore.plugin.models.PublishedArtifact` refers to
  :class:`~pulpcore.plugin.models.ContentArtifact` which is published and belongs to a certain
  :class:`~pulpcore.app.models.Publication`.
* :class:`~pulpcore.plugin.models.PublishedMetadata` is a repository metadata which is published,
  located in ``/var/lib/pulp/published`` and belongs to a certain
  :class:`~pulpcore.app.models.Publication`.
* :class:`~pulpcore.plugin.models.Publisher` knows specifics of the plugin
  :class:`~pulpcore.plugin.models.Content` to make it available outside of Pulp.
  :class:`~pulpcore.plugin.models.Publisher` defines how to publish content available in Pulp.
* :class:`~pulpcore.app.models.Publication` is a result of publish operation of a specific
  :class:`~pulpcore.plugin.models.Publisher`.
* :class:`~pulpcore.app.models.Distribution` defines how a publication is distributed for a specific
  :class:`~pulpcore.plugin.models.Publisher`.
* :class:`~pulpcore.plugin.models.ProgressBar` is used to report progress of the task.


An important feature of the current design is deduplication of
:class:`~pulpcore.plugin.models.Content` and :class:`~pulpcore.plugin.models.Artifact` data.
:class:`~pulpcore.plugin.models.Content` is shared between :class:`~pulpcore.app.models.Repository`,
:class:`~pulpcore.plugin.models.Artifact` is shared between
:class:`~pulpcore.plugin.models.Content`.
See more details on how it affects remote implementation in :ref:`define-remote` section.


Check ``pulp_file`` `implementation <https://github.com/pulp/pulp_file/>`_ to see how all
those models are used in practice.
More detailed explanation of model usage with references to ``pulp_file`` code is below.


Models, Viewsets, Serializers
=============================


STUB


