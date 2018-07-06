Adding and Removing Content
===========================

TODO: RepositoryVersion
https://pulp.plan.io/issues/3220

Synchronizing
-------------

A typical task to add and remove content to/from a repository is to synchronize with an external
source.

One of the ways to perform synchronization:

* Download and analyze repository metadata from a remote source.
* Decide what needs to be added to repository or removed from it.
* Associate already existing content to a repository by creating an instance of
  :class:`~pulpcore.plugin.models.RepositoryContent` and saving it.
* Remove :class:`~pulpcore.plugin.models.RepositoryContent` objects which were identified for
  removal.
* For every content which should be added to Pulp create but do not save yet:

  * instance of ``ExampleContent`` which will be later associated to a repository.
  * instance of :class:`~pulpcore.plugin.models.ContentArtifact` to be able to create relations with
    the artifact models.
  * instance of :class:`~pulpcore.plugin.models.RemoteArtifact` to store information about artifact
    from remote source and to make a relation with :class:`~pulpcore.plugin.models.ContentArtifact`
    created before.

* If a remote content should be downloaded right away (aka ``immediate`` download policy), use
  the suggested  :ref:`downloading <download-docs>` solution. If content should be downloaded
  later (aka ``on_demand`` or ``background`` download policy), feel free to skip this step.
* Save all artifact and content data in one transaction:

  * in case of downloaded content, create an instance of
    :class:`~pulpcore.plugin.models .Artifact`. Set the `file` field to the
    absolute path of the downloaded file. Pulp will move the file into place
    when the Artifact is saved. The Artifact refers to a downloaded file on a
    filesystem and contains calculated checksums for it.
  * in case of downloaded content, update the :class:`~pulpcore.plugin.models.ContentArtifact` with
    a reference to the created :class:`~pulpcore.plugin.models.Artifact`.
  * create and save an instance of the :class:`~pulpcore.plugin.models.RepositoryContent` to
    associate the content to a repository.
  * save all created artifacts and content: ``ExampleContent``,
    :class:`~pulpcore.plugin.models.ContentArtifact`,
    :class:`~pulpcore.plugin.models.RemoteArtifact`.

* Use :class:`~pulpcore.plugin.models.ProgressBar` to report the progress of some steps if needed.
