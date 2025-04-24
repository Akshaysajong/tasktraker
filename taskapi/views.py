from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JWTLoginSerializer, TaskSerializer, TaskUpdateSerializer, TaskReportSerializer
from taskapp.models import Task
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class JWTLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = JWTLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    

class TaskStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        task = get_object_or_404(Task, id=pk, assigned_to=request.user)
        serializer = TaskUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Task updated successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        task = get_object_or_404(Task, id=pk)

        # user = request.user.userprofile
        # print('type:', user.user_type)
        # # Check role
        if not request.user.is_superuser:
            if request.user.userprofile.user_type != 'admin':
                return Response({'detail': 'Access denied. Only Admins and SuperAdmins can view this.'},
                                status=status.HTTP_403_FORBIDDEN)
        
        if task.status != 'Completed':
            return Response({'detail': 'Task is not completed yet.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskReportSerializer(task)
        return Response(serializer.data)