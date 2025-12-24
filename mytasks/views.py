from json import loads as json_loads
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import ApiTaskSerializer

# Create your views here.
class TasksView(TemplateView):
    """ TasksView: Tasks view of app mytasks
    """
    template_name = "mytasks/mytasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# API VIEWS
@api_view(["POST"])
def add_task(request):
    """ API endpoint to add a task
    """
    if request.method == "POST":
        serializer = ApiTaskSerializer(data=json_loads(list(dict(request.data).keys())[0]))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_tasks(request):
    """ API endpoint to add a task
    """
    if request.method == "GET":
        tasks = Task.objects.all()
        serializer = ApiTaskSerializer(tasks, many=True)
        return Response(serializer.data)
    

@api_view(["POST"])
def remove_task(request):
    """ API endpoint to remove a task
    """
    if request.method == "POST":
        task = get_object_or_404(Task, id=json_loads(list(dict(request.data).keys())[0])["id"])
        serializer = ApiTaskSerializer(task)
        task.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)