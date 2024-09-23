from rest_framework import serializers
from .models import Project, Task, Contributor
from custom_auth.models import CustomUser
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'assigned_to']

class TaskCreateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(),required=False,allow_null=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'assigned_to']

class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Contributor
        fields = [ 'user' ]

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)
    contributors = ContributorSerializer(many=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'tasks', 'contributors']


class ProjectCreateSerializer(serializers.ModelSerializer):
    contributors_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True)
    tasks = TaskCreateSerializer(many=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'contributors_ids', 'tasks']

    def create(self, validated_data):
        contributors_ids = validated_data.pop('contributors_ids')
        tasks_data = validated_data.pop('tasks')
     
        try:
            #start a transaction
            with transaction.atomic():
            # Get the owner instance from request
                owner = self.context['request'].user
                
                # Create the project
                project = Project.objects.create(owner=owner, **validated_data)

                # Add contributors to the project
                for contributor_id in contributors_ids:
                    user = CustomUser.objects.get(id=contributor_id)
                    Contributor.objects.create(user=user, project=project)

                # Add tasks to the project
                for task_data in tasks_data:
                    assigned_to = task_data.pop('assigned_to')
                    Task.objects.create(project=project, assigned_to=assigned_to, **task_data)
                
                return project
        
        except Exception as e:
            raise serializers.ValidationError(f"An error occurred: {str(e)}")
        