from django.shortcuts import render
from .serializers import BlogSerializer,CreateBlogSerializer,AddChoiceSerializer
from rest_framework.generics import ListAPIView,CreateAPIView
from .models import Blog
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



class BlogView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    

class BlogCreateView(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = CreateBlogSerializer

class AddChoiceAPIView(APIView):
    def post(self, request):
        serializer = AddChoiceSerializer(data=request.data)
        if serializer.is_valid():
            new_choice = serializer.validated_data.get('new_choice')
            # Add the new choice dynamically
            Blog.add_b_type_choice(new_choice)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)