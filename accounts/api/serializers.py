from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
from .utils import jwt_response_payload_handler
from django.conf import settings
import datetime
from django.utils import timezone

User=get_user_model()

expire_delta=settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler=api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(style={'input_type':'password2'},write_only=True)
    token=serializers.SerializerMethodField(read_only=True)
    expires=serializers.SerializerMethodField(read_only=True)
    message=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=User
        fields=['username','password','password2','email','token','expires','message']
        extra_kwargs={'password':{'write_only':True}}

    def validate_email(self,value):
        qs=User.objects.filter(email=value)
        if qs.exists():
            raise serializers.ValidationError('User with this email already exists')
        return value
    
    def validate_username(self,value):
        qs=User.objects.filter(username=value)
        if qs.exists():
            raise serializers.ValidationError('User with this username already exists')
        return value

    def get_message(self,obj):
        return 'Thank you for registration'
    def get_expires(self,obj):

        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def get_token(self,obj):
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token


    def valdiate(self,data):
        pw=data.get('password')
        pw2=data.pop('password2')
        if pw==pw2:
            raise serializers.ValidationError('Passwords must match')
        return data
    
    def create(self,validated_data):
        username=validated_data['username']
        email=validated_data['email']
        password=validated_data['password']
        user_obj=User.objects.create(username=username,email=email)
        user_obj.set_password(password)
        user_obj.is_active=True
        user_obj.save()
        return user_obj

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']


