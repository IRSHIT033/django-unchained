# api/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from .models import Project
from .serializers import ProjectSerializer
from rest_framework import status

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(contributors=user).prefetch_related('contributors', 'tasks').select_related('owner')

    def create(self, request, *args, **kwargs):
        data = request.data
        data['owner'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user != project.owner and request.user not in project.contributors.all():
            raise PermissionDenied("You do not have access to this project.")
        serializer = self.get_serializer(project)
        return Response(serializer.data)

