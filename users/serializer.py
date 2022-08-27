from email.policy import default
from rest_framework.serializers import Serializer, ModelSerializer, CharField, EmailField
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from django.contrib.auth.password_validation import validate_password


class ProfileSerializer(Serializer):
    email = EmailField(required=True)
    username = CharField(required=True)
    first_name = CharField(required=False, default="")
    last_name = CharField(required=False, default="")


class ProfileModelSerializer(ProfileSerializer, ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "username", "first_name", "last_name"]
        extra_kwargs = {
            "email": {"read_only": True},
            "username": {"read_only": True},
        }


class RegisterSerializer(ProfileSerializer):
    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise ValidationError({"password2": "Incorrect password"})
        return super().validate(attrs)


class UpdatePasswordSerializer(Serializer):
    old_password = CharField(write_only=True, required=True)
    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    def validate_old_password(self, data):
        if not self.context.request.user.check_password(data):
            raise ValidationError("Wrong old password")

    def validate(self, attrs):
        if attrs["password"] != attrs["old_password"]:
            raise ValidationError({"password": "New password similar to old one."})
        if attrs["password"] != attrs["password2"]:
            raise ValidationError({"password2": "Incorrect password"})
        return super().validate(attrs)
