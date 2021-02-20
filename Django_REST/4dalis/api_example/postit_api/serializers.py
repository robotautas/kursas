from rest_framework import serializers
from .models import Post, Comment, CommentLike, PostLike
from django.contrib.auth.models import User

# class PostSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
#     user_id = serializers.ReadOnlyField(source='user.id')
#     comments = CommentSerializer(many=True)

#     class Meta:
#         model = Post
#         fields = ['id', 'user', 'user_id', 'title', 'body', 'created']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_id', 'post', 'body', 'created']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    comment_count = serializers.SerializerMethodField()
    comments = serializers.StringRelatedField(many=True, default=[])
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'user_id', 'title', 'body', 'likes', 'comment_count', 'comments', 'created']

    def get_comment_count(self, post):
        return Comment.objects.filter(post=post).count()

    def get_likes(self, post):
        return PostLike.objects.filter(post=post).count()


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['id']

class CommentLikeSerilizer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['id']  



