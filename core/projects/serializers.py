from rest_framework import serializers
from .models import Project, Task, Contributor
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer()

    class Meta:
        model = Task
        fields = [ 'name', 'description', 'assignee', 'completed']

class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = [ 'user', 'project' ]

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)
    contributors = ContributorSerializer(many=True)
    owner = UserSerializer()

    class Meta:
        model = Project
        fields = [ 'name', 'description', 'owner', 'tasks', 'contributors']

    def create(self, validated_data):
        tasks_data = validated_data.pop('tasks')
        contributors_data = validated_data.pop('contributors')
        project = Project.objects.create(**validated_data)

        for task_data in tasks_data:
            Task.objects.create(project=project, **task_data)

        for contributor_data in contributors_data:
            Contributor.objects.create(project=project, **contributor_data)

        return project