Publish
=======


TODO Publication
https://pulp.plan.io/issues/3298

One of the ways to perform publishing:

* Find :class:`~pulpcore.plugin.models.ContentArtifact` objects which should be published
* For each of them create and save instance of :class:`~pulpcore.plugin.models.PublishedArtifact`
  which refers to :class:`~pulpcore.plugin.models.ContentArtifact` and
  :class:`~pulpcore.app.models.Publication` to which this artifact belongs.
* Generate and write to a disk repository metadata
* For each of the metadata objects create and save  instance of
  :class:`~pulpcore.plugin.models.PublishedMetadata` which refers to a corresponding file and
  :class:`~pulpcore.app.models.Publication` to which this metadata belongs.
* Use :class:`~pulpcore.plugin.models.ProgressBar` to report progress of some steps if needed.
