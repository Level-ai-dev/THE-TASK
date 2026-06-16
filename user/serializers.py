from rest_framework import serializers
from .models import User
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode

user = get_user_model
class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'
        read_only_fields = ['user']
        
        
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        return value
    

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid      = serializers.CharField()
    token    = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            return serializers.ValidationError("Password doesnt match")\
                
        try: 
            uid = urlsafe_base64_decode(data['uid']).decode()
            user = user.objects.get(pk=uid)
        except (user.DoesNotExist, ValueError, TypeError):
            return serializers.ValidationError("Invalid reset link")
        
        
        if not default_token_generator.check_token(user, data['token']):
            return serializers.ValidationError("Invalid Token")
        
        
        data['user'] = user
        return data