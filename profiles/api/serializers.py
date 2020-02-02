from rest_framework import serializers
from profiles.models import Profile
from rest_framework.response import Response
from django.apps import apps
from books.api.serializers import BookListSerializer
from books.models import Book
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404




User=get_user_model()

class ProfilePublicSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField()
    class Meta:
        model=Profile
        fields=['id','name','image']
    
    def get_name(self,obj):
        return obj.user.username

class ProfileListSerializer(serializers.ModelSerializer):
    is_following=serializers.SerializerMethodField()
    name=serializers.SerializerMethodField()
    class Meta:
        model=Profile
        fields=['id','name','image','followers','is_following','book_list','wish_list','currently_reading','created']

    def get_is_following(self,obj):
        return ProfilePublicSerializer(obj.isfollowing.all(),many=True).data
    
    def get_name(self,obj):
        return obj.user.username



class ProfileDetailSerializer(serializers.ModelSerializer):
    is_following=serializers.SerializerMethodField()
    name=serializers.SerializerMethodField()
    books=serializers.SerializerMethodField()
    
    class Meta:
        model=Profile
        fields=['id','books','name','image','followers','is_following','book_list','wish_list','currently_reading','created']

    def get_is_following(self,obj):
        return ProfilePublicSerializer(obj.isfollowing.all(),many=True).data
    
    def get_name(self,obj):
        return obj.user.username
    
    def get_books(self,obj):
        qs=Book.objects.filter(author=obj)
        return BookListSerializer(qs,many=True).data
    
    

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['id','image','book_list',"wish_list","currently_reading"]
    
    def validate(self, data):
        # Object-level validation
        # Custom validation logic will go here
        return data  # validated_data
    
    def alma(self,added,field,instance,*args,**kwargs):
        other=[]
        if field==instance.book_list:
            other=[instance.wish_list,instance.currently_reading]
        elif field==instance.wish_list:
            other=[instance.book_list,instance.currently_reading]
        elif field==instance.currently_reading:
            other=[instance.wish_list,instance.book_list]

        if added:
            try:
                obj=Book.objects.get(id=int(added))
                if obj in field.all():
                    field.remove(added)
                else:
                    for a in other:
                        if obj in a.all():
                            a.remove(obj)
                    field.add(added)
            except Book.DoesNotExist:
                raise serializers.ValidationError("This book does not exist")

    def update(self, instance, validated_data):

        added_book=validated_data.get('book',None)
        added_wish=validated_data.get('wish',None)
        added_currently=validated_data.get('currently',None)
        image=validated_data.get('image',None)
        follow=validated_data.get('follow',None)
        print(validated_data)
        if added_book:
            self.alma(added_book,instance.book_list,instance)
        if added_wish:
            self.alma(added_wish,instance.wish_list,instance)
        if added_currently:
            self.alma(added_currently,instance.currently_reading,instance)
        if follow:
            try:
                obj=Profile.objects.get(id=int(follow))
                if obj in instance.isfollowing.all():
                    instance.isfollowing.remove(obj)
                else:
                    instance.isfollowing.add(obj)
            except Profile.DoesNotExist:
                raise serializers.ValidationError("This profile does not exist")
        if image:
            instance.image=image
        
        
        instance.save()

        return instance
        
    