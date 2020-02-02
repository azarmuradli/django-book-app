from rest_framework import serializers
from likes.models import Like

class LikeCreateSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField
    class Meta:
        model=Like
        fields=['comment','user']

    def get_user(self,obj):
        return obj.user.user.username
    
    def validate(self,data):
        user=data.get('user')
        comment=data.get('comment')
        qs=Like.objects.filter(comment=comment,user=user).distinct()
        if qs.exists():
            raise serializers.ValidationError('You have already liked this book')
        return data
            
