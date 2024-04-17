from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = "__all__"
#ADMIN
class CreateBlogSerializer(serializers.ModelSerializer):
    b_image = serializers.ImageField(required=False)

    class Meta:
        model = Blog
        fields = ["b_name","b_text","b_type","b_image", "SeoTitle","SeoDescription","SeoKeywords","SeoIndexpage","SeoCanonical","SeoSchema"]


class AddChoiceSerializer(serializers.Serializer):
    new_choice = serializers.CharField(max_length=100)