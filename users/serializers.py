from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import NewUser

class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},min_length=8,write_only=True)

    class Meta:
        model = NewUser
        fields = ['email','password','password2']
        extra_kwargs = {'password':{'write_only':True}}

    def save(self):
        user = NewUser(
            email = self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise ValidationError({'password':'Password must match'})
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        email_exists = NewUser.objects.filter(email=attrs['email'],email_is_verify=True).exists()

        if email_exists:
            raise ValidationError('Email has been already used') 

        return super().validate(attrs) 


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ['name','phone','birth_day','gender']

    def update(self, instance, validated_data):
        setattr(instance, "name", self.validated_data.get('name', instance.name))
        if self.validated_data.get('phone', instance.phone):
            setattr(instance, "phone", self.validated_data.get('phone', instance.phone))
        if self.validated_data.get('birth_day', instance.birth_day):    
            setattr(instance, "birth_day", self.validated_data.get('birth_day', instance.birth_day))
        if self.validated_data.get('gender', instance.gender):    
            setattr(instance, "gender", self.validated_data.get('gender', instance.gender))
        instance.save()
        return instance
