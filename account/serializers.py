from rest_framework import serializers
from account.models import MyUser


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