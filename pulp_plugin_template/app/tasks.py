from celery import shared_task
from pulpcore.plugin import changeset
from pulpcore.plugin.tasking import WorkingDirectory, UserFacingTask
from pulpcore.plugin.wrappers import Publication, RepositoryVersion


@shared_task(base=UserFacingTask)
def sync(importer_pk):
    """
    Task to synchronize a Repository with an external source, generates a new RepositoryVersion.

    This task is deployed by the PluginTemplateImporterViewset. Plugin writers can add additional
    parameters if necessary.

    Sync typically follows this workflow:
        1. Download metadata from external source
        2. Parse metadata and create new units and fetch units to be removed
        3. Use a ChangeSet to safely add/remove to the created_version

    Args:
        importer_pk (str): The importer PK.

    """
    # # Settings needed to fetch content from a remote source should be stored on a
    # # PluginTemplateImporter.
    # importer = PluginTemplateImporter.objects.get(pk=importer_pk)
    #
    #
    # # Use the RepositoryVersion context manager to safely create a new version. This new version
    # # will be mutable within the context, and will be made immutable when the context exits. If
    # # there is a failure, the version is safely cleaned up.
    # with RepositoryVersion.create(repository) as created_version:
    #     # Use the WorkingDirectory context manager to set the CWD before writing any files.
    #     with WorkingDirectory():
    #         download_and_write_metadata()
    #         changeset = ChangeSet(importer, created_version, additions=additions, removals=removals)
    #         changeset.apply_and_drain()
    raise NotImplementedError


@shared_task(base=UserFacingTask)
def publish(publisher_pk):
    """
    Task to create a Publication based on a RepositoryVersion.

    Publish typically follows this workflow:
        1. Write metadata files
        2. Add metadata to database

    Args:
        publisher_pk (str): Use the publish settings provided by this publisher.
        repository_pk (str): Create a Publication from the latest version of this Repository.

    """
    # # Settings needed to publish content should be stored on a PluginTemplatePublisher.
    # publisher = PluginTemplatePublisher.objects.get(pk=publisher_pk)
    # #
    # # Use the RepositoryVersion wrapper to retrieve a version.
    # latest_version = RepositoryVersion.latest(repository)
    # #
    # # Use the Publication wrapper as a context manager to safely create a new Publication
    # # The new Publication  will be mutable within the context, and will be made immutable when the
    # # context exits. If there is a failure, the Publication is safely cleaned up.
    # with Publication.create(latest_version) as publication:
    #
    #     # Use the WorkingDirectory context manager to set the CWD before writing any files.
    #     with WorkingDirectory():
    #         write_metadata(publication, path)
    #
    #         # Create a PublishedMetadata unit and save to the database.
    #         metadata = models.PublishedMetadata(
    #             relative_path=os.path.basename(path),
    #             publication=publication,
    #             file=File(open(path, 'rb')))
    #         metadata.save()
    #
    # log.info(
    #     _('Publishing: repository=%(repository)s, version=%(version)d, publisher=%(publisher)s'),
    #     {
    #         'repository': repository.name,
    #         'publisher': publisher.name,
    #         'version': latest_version,
    #     })
    raise NotImplementedError
