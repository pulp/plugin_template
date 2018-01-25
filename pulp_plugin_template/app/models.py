"""
Check `Plugin Writer's Guide`_ and `pulp_example`_ plugin
implementation for more details.

.. _Plugin Writer's Guide:
    http://docs.pulpproject.org/en/3.0/nightly/plugins/plugin-writer/index.html

.. _pulp_example:
    https://github.com/pulp/pulp_example/
"""

from gettext import gettext as _
from logging import getLogger

from django.db import models

from pulpcore.plugin.models import (Artifact, Content, ContentArtifact, RemoteArtifact, Importer,
                                    ProgressBar, Publisher, RepositoryVersion, PublishedArtifact,
                                    PublishedMetadata)
from pulpcore.plugin.tasking import Task


log = getLogger(__name__)


class PluginTemplateContent(Content):
    """
    The "plugin-template" content type.

    Define fields you need for your new content type and
    specify uniqueness constraint to identify unit of this type.

    For example::

        field1 = models.TextField()
        field2 = models.IntegerField()
        field3 = models.CharField()

        class Meta:
            unique_together = (field1, field2)
    """

    TYPE = 'plugin-template'


class PluginTemplatePublisher(Publisher):
    """
    A Publisher for PluginTemplateContent.

    Define any additional fields for your new publisher if needed.
   """

    TYPE = 'plugin-template'


class PluginTemplateImporter(Importer):
    """
    An Importer for PluginTemplateContent.

    Define any additional fields for your new importer if needed.
   """

    TYPE = 'plugin-template'

