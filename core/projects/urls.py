
from django.urls import path
from .views import ProjectCreateView, ProjectDetailView, ProjectListView

urlpatterns = [
    path('projects', ProjectCreateView.as_view(), name='project'),
    path('projects/<uuid:project_id>', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/list', ProjectListView.as_view(), name='project-list'),
]