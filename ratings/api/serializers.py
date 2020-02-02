from rest_framework import serializers
from ratings.models import Rating
from profiles.models import Profile
from books.models import Book

class RatingCreateSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField
    class Meta:
        model=Rating
        fields=['book','user','star']
        read_only_fields=['user']

    def get_user(self,obj):
        return obj.user.user.username
    
    def validate(self,data):
        user=data.get('user')
        star=data.get('star')
        book=data.get('book')
        qs=Rating.objects.filter(book=book,user=user)
        if qs.exists():
            raise serializers.ValidationError('You have already rated this book')
        return data

    def create(self,validated_data):
        user=validated_data.get('user')
        print(user)
        star=validated_data.get('star')
        book=validated_data.get('book')
        profile=Profile.objects.get(user=user)
        Rating.objects.create(user=user,book=book,star=star)
        profile.book_list.add(book)

        return validated_data
        

            
