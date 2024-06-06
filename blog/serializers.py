from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = "__all__"
#ADMIN
class CreateBlogSerializer(serializers.ModelSerializer):
    BlogImage = serializers.ImageField(required=False)

    class Meta:
        model = Blog
        fields = ["BlogTitle","BlogDescription","BlogType","BlogImage", "SeoTitle","SeoDescription","SeoKeywords","SeoIndexpage","SeoCanonical","SeoSchema"]

class DeleteBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ('id', 'title')





class AddChoiceSerializer(serializers.Serializer):
    new_choice = serializers.CharField(max_length=100)