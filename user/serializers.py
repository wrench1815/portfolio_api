from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'last_login',
            'is_superuser',
            'username',
            'email',
            'first_name',
            'last_name',
            'date_created',
            'avatar',
            'gender',
            'is_active',
            'is_staff',
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8,
        max_length=16,
    )
    confirm_password = serializers.CharField(
        min_length=8,
        max_length=16,
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'gender',
            'password',
            'confirm_password',
        ]

    def validate_password(self, value):
        # check if password is minimum 8 digit long
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long")

        # check if password contains atleast 1 number
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one number")

        # check if password contains atleast 1 capital letter
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one capital letter")

        # check if password contains atleast 1 small letter
        if not any(char.islower() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one small letter")

        # check if password contains atleast 1 special character
        if not any(char in '!@#$%^&*()_+' for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one special character")

        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'error': 'Confirm Password does not match Password'})

        return attrs
