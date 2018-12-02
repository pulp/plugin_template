"""
Check `Plugin Writer's Guide`_ for more details.

.. _Plugin Writer's Guide:
    http://docs.pulpproject.org/en/3.0/nightly/plugins/plugin-writer/index.html
"""

from drf_yasg.utils import swagger_auto_schema

from pulpcore.plugin import viewsets as core
from pulpcore.plugin.serializers import (
    AsyncOperationResponseSerializer,
    RepositoryPublishURLSerializer,
    RepositorySyncURLSerializer,
)
from pulpcore.plugin.tasking import enqueue_with_reservation
from rest_framework.decorators import detail_route

from . import models, serializers, tasks


class PluginTemplateContentFilter(core.ContentFilter):
    """
    FilterSet for FileContent.
    """

    class Meta:
        model = models.PluginTemplateContent
        fields = [
            # ...
        ]


class PluginTemplateContentViewSet(core.ContentViewSet):
    """
    A ViewSet for PluginTemplateContent.

    Define endpoint name which will appear in the API endpoint for this content type.
    For example::
        http://pulp.example.com/pulp/api/v3/content/plugin-template/

    Also specify queryset and serializer for PluginTemplateContent.
    """

    endpoint_name = 'plugin-template'
    queryset = models.PluginTemplateContent.objects.all()
    serializer_class = serializers.PluginTemplateContentSerializer
    filterset_class = PluginTemplateContentFilter


class PluginTemplateRemoteViewSet(core.RemoteViewSet):
    """
    A ViewSet for PluginTemplateRemote.

    Similar to the PluginTemplateContentViewSet above, define endpoint_name,
    queryset and serializer, at a minimum.
    """

    endpoint_name = 'plugin-template'
    queryset = models.PluginTemplateRemote.objects.all()
    serializer_class = serializers.PluginTemplateRemoteSerializer

    # This decorator is necessary since a sync operation is asyncrounous and returns
    # the id and href of the sync task.
    @swagger_auto_schema(
        operation_description="Trigger an asynchronous task to sync content",
        responses={202: AsyncOperationResponseSerializer}
    )
    @detail_route(methods=('post',), serializer_class=RepositorySyncURLSerializer)
    def sync(self, request, pk):
        """
        Synchronizes a repository. The ``repository`` field has to be provided.
        """
        remote = self.get_object()
        serializer = RepositorySyncURLSerializer(data=request.data, context={'request': request})

        # Validate synchronously to return 400 errors.
        serializer.is_valid(raise_exception=True)
        repository = serializer.validated_data.get('repository')
        mirror = serializer.validated_data.get('mirror', True)
        result = enqueue_with_reservation(
            tasks.synchronize,
            [repository, remote],
            kwargs={
                'remote_pk': remote.pk,
                'repository_pk': repository.pk,
                'mirror': mirror
            }
        )
        return core.OperationPostponedResponse(result, request)


class PluginTemplatePublisherViewSet(core.PublisherViewSet):
    """
    A ViewSet for PluginTemplatePublisher.

    Similar to the PluginTemplateContentViewSet above, define endpoint_name,
    queryset and serializer, at a minimum.
    """

    endpoint_name = 'plugin-template'
    queryset = models.PluginTemplatePublisher.objects.all()
    serializer_class = serializers.PluginTemplatePublisherSerializer

    # This decorator is necessary since a publish operation is asyncrounous and returns
    # the id and href of the publish task.
    @swagger_auto_schema(
        operation_description="Trigger an asynchronous task to publish content",
        responses={202: AsyncOperationResponseSerializer}
    )
    @detail_route(methods=('post',), serializer_class=RepositoryPublishURLSerializer)
    def publish(self, request, pk):
        """
        Publishes a repository.

        Either the ``repository`` or the ``repository_version`` fields can
        be provided but not both at the same time.
        """
        publisher = self.get_object()
        serializer = RepositoryPublishURLSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        repository_version = serializer.validated_data.get('repository_version')

        result = enqueue_with_reservation(
            tasks.publish,
            [repository_version.repository, publisher],
            kwargs={
                'publisher_pk': str(publisher.pk),
                'repository_version_pk': str(repository_version.pk)
            }
        )
        return core.OperationPostponedResponse(result, request)
