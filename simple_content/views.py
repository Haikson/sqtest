from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response

from simple_content.models import Content
from simple_content.serializers import ContentSerializer
from rest_framework import viewsets, views, authentication, permissions


class ContentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows content to be viewed or edited.
    """
    queryset = Content.objects.all().order_by('-ctime')
    serializer_class = ContentSerializer


class NavigationView(views.APIView):

    def make_tree(self, nodes, current, ancestors_list):
        return [
            {
                'title': node.title,
                'url': node.get_absolute_url,
                'pk': node.pk,
                'children': self.make_tree(node.get_children(), current, ancestors_list)
                if (node in ancestors_list or node == current) and not node.is_leaf_node() else []
            } for node in nodes
        ]

    def get(self, request, current=None):
        """
        Return navigation tree.
        """
        contents = Content.objects.filter(parent__isnull=True)
        ancestors = []
        current_content = None
        if current is not None:
            current_content = get_object_or_404(Content, pk=current)  # type: Content
            ancestors = current_content.get_ancestors()
        data = self.make_tree(contents, current_content, ancestors)
        return Response(data)

