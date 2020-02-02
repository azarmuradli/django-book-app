from rest_framework import serializers
from comments.models import Comment
from likes.models import Like
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from profiles.models import Profile

User=get_user_model()


class CommentListSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    reply_count=serializers.SerializerMethodField()
    like=serializers.SerializerMethodField()
    uri=serializers.SerializerMethodField()
    class Meta:
        model=Comment
        fields=['id','uri','user','content','reply_count','like']
    def get_user(self,obj):
        return obj.user.user.username
    def get_reply_count(self,obj):
        return obj.children.count()
    
    def get_like(self,obj):
        qs=Like.objects.filter(comment=obj)
        return qs.count()

    def get_uri(self, obj):
        request = self.context.get('request')
        return reverse("comment-api:detail", kwargs={"pk": obj.id},request=request)

class CommentSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    like=serializers.SerializerMethodField()
    
    class Meta:
        model=Comment
        fields=['id','uri','user','content','like']
    def get_user(self,obj):
        return obj.user.user.username
    def get_like(self,obj):
        qs=Like.objects.filter(comment=obj)
        return qs.count()
    
        


class CommentDetailSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    reply_count=serializers.SerializerMethodField()
    replies=serializers.SerializerMethodField()
    like=serializers.SerializerMethodField()
    uri=serializers.SerializerMethodField()
    class Meta:
        model=Comment
        fields=['id','user','content','reply_count','replies','like']
    def get_user(self,obj):
        return obj.user.user.username

    def get_reply_count(self,obj):
        return obj.children.count()

    def get_replies(self,obj):
        return CommentSerializer(obj.children,many=True).data

    def get_like(self,obj):
        qs=Like.objects.filter(comment=obj)
        return qs.count()
    
def create_comment_serializer(model_type='book', _id=None, parent_id=None, user=None):
    class CommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content'
            ]
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self._id = _id
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() ==1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise serializers.ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=self._id)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise serializers.ValidationError("This is not a id for this content type")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user = user
            else:
                main_user = Profile.objects.all().first()
            model_type = self.model_type
            _id = self._id
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                    model_type, _id, content, main_user,
                    parent_obj=parent_obj,
                    )
            return comment

    return CommentCreateSerializer