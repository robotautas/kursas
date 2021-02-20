from rest_framework import serializers
from .models import Post, Comment, CommentLike, PostLike

# class PostSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
#     user_id = serializers.ReadOnlyField(source='user.id')
#     comments = CommentSerializer(many=True)

#     class Meta:
#         model = Post
#         fields = ['id', 'user', 'user_id', 'title', 'body', 'created']


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
    comments = serializers.StringRelatedField(many=True) #, default=[])
    likes = serializers.SerializerMethodField()
    # extra_kwargs = {'comments': {'read_only': True}}

    class Meta:
        model = Post
        fields = ['id', 'user', 'user_id', 'title', 'body', 'image', 'likes', 'comment_count', 'comments', 'created']

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



