# api/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer, ProjectCreateSerializer
from rest_framework import status
from django.db.models import Q
from .permissions import IsOwnerOrContributor
from django.core.cache import cache

class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        POST: Create a new project with nested contributors and tasks.
        """
        serializer = ProjectCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            project = serializer.save()  # owner is automatically set inside serializer
            return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrContributor]

    def get(self, request, project_id):
        """
        GET: Retrieve a project by ID.
        """
        # Fetch project with related contributors and tasks in a single query show 404 if not found
        try:
            project = cache.get(f'project_{project_id}')
            if not project:
                project =  Project.objects.prefetch_related('contributors',  'tasks__assigned_to').select_related('owner').get(id=project_id)
                cache.set(f'project_{project_id}', project)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # Check if the user has permission to access the project
        self.check_object_permissions(request, project)

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProjectListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET: Retrieve a list of projects where the user is either a contributor or the owner.
        """
        # Fetch projects where the user is either a contributor or the owner
        projects = Project.objects.prefetch_related('contributors',  'tasks__assigned_to').select_related('owner').filter(
            Q(contributors__user=request.user) | Q(owner=request.user)
        )
        
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



