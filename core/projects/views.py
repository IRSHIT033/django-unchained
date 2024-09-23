# api/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from .models import Project
from .serializers import ProjectSerializer
from rest_framework import status

class ProjectView(APIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    # def get(self,request,id=None):
    #     user = request.user
    #     print(user.id)
    #     #filter project where user is contributor(contributer id=user id)
    #     return Project.objects.filter(contributors=user.id).prefetch_related('contributors', 'tasks').select_related('owner')

    def post(self, request):
        data = request.data
        data['owner'] = request.user.id
        print(request.user.id)
        # serializer = self.get_serializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        return Response(data, status=status.HTTP_201_CREATED)

    # def get(self, request,id):
    #     project = self.get_object(id)
    #     if request.user != project.owner and request.user not in project.contributors.all():
    #         raise PermissionDenied("You do not have access to this project.")
    #     serializer = self.get_serializer(project)
    #     return Response(serializer.data)

