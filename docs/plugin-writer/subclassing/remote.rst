
Define your plugin Remote
-------------------------

To define a new remote, e.g. ``ExampleRemote``:

* :class:`pulpcore.plugin.models.Remote` should be subclassed and extended with additional
  attributes to the plugin needs,
* define ``TYPE`` class attribute which is used for filtering purposes,
* create a serializer for your new remote as a subclass of
  :class:`pulpcore.plugin.serializers.RemoteSerializer`,
* create a viewset for your new remote as a subclass of
  :class:`pulpcore.plugin.viewsets.RemoteViewSet`.

:class:`~pulpcore.plugin.models.Remote` model should not be used directly anywhere in plugin code.
Only plugin-defined Remote classes are expected to be used.


There are several important aspects relevant to remote implementation which were briefly mentioned
in the :ref:`understanding-models` section:

* due to deduplication of :class:`~pulpcore.plugin.models.Content` and
  :class:`~pulpcore.plugin.models.Artifact` data, they may already exist and the remote needs to
  fetch and use them when they do.
* :class:`~pulpcore.plugin.models.ContentArtifact` associates
  :class:`~pulpcore.plugin.models.Content` and :class:`~pulpcore.plugin.models.Artifact`. If
  :class:`~pulpcore.plugin.models.Artifact` is not downloaded yet,
  :class:`~pulpcore.plugin.models.ContentArtifact` contains ``NULL`` value for
  :attr:`~pulpcore.plugin.models.ContentArtifact.artifact`. It should be updated whenever
  corresponding :class:`~pulpcore.plugin.models.Artifact` is downloaded.

The remote implementation suggestion above allows plugin writer to have an understanding and
control at a low level.
The plugin API has a higher level, more simplified, API which introduces the concept of
:class:`~pulpcore.plugin.changeset.ChangeSet`.
It allows plugin writer:

* to specify a set of changes (which :class:`~pulpcore.plugin.models.Content` to add or to remove)
  to be made to a repository
* apply those changes (add to a repository, remove from a repository, download files if needed)

Check :ref:`documentation and detailed examples <changeset-docs>` for the
:class:`~pulpcore.plugin.changeset.ChangeSet` as well as `the implementation of File plugin remote
<https://github.com/pulp/pulp_file/blob/master/pulp_file/app/models.py>`_ which uses it.


