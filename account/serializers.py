from rest_framework import serializers
from account.models import MyUser
from .utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = MyUser
        fields = ['email', 'date_of_birth', 'name', 'nationality', 'password','password2']
        extra_kwargs ={
            'password':{'write_only':True}
        }
    
    # Validating password and password2 while registeration
    # the data we are geting is assed by attrs 
    def validate(self, attrs):
        print('attrs .....',attrs)
        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password do not match')
        else:
            attrs.pop('password2')
            return attrs
    
    def create(self,validated_data):
        return MyUser.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = MyUser
        fields = ('email','password')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id','email', 'date_of_birth', 'name', 'nationality')
        
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 =serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    
    class Meta:
        fields = ('password','password2')
        
    def validate(self,attrs):
        password = attrs['password']
        password2 = attrs['password2']
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password do not match')
        else:
            user.set_password(password)
            user.save()
            return attrs

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self,attrs):
        email = attrs['email']
        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID..',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset TOken ',token)
            link = 'http://localhost:3000/api/user/reset/'+uid+ '/' +token
            print('Password Reset Link...',link)

            ## send email 
            body = 'Click Following LInk To Reset Your Password ' + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email,
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not registered')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 =serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    
    class Meta:
        fields = ('password','password2')
        
    def validate(self,attrs):
        try:
            password = attrs['password']
            password2 = attrs['password2']
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('Password and Confirm Password do not match')
            else:
                id = smart_str(urlsafe_base64_decode(uid))
                user = MyUser.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user,token):
                    raise serializers.ValidationError('Token is not valid or expired')
                user.set_password(password)
                user.save()
                return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError('Token is not valid or expired')
