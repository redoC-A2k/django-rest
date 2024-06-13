from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        # return super().validate(data):
        if data["username"]:
            if User.objects.filter(username=data["username"]).exists():
                raise serializers.ValidationError("Username already exists")

        if data["email"]:
            if User.objects.filter(email=data["email"]).exists():
                raise serializers.ValidationError("Email already exists")
            
        return data

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(username = validated_data["username"], email = validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["color_name"]


class peopleSerializer(serializers.ModelSerializer):
    # color = ColorSerializer()
    # country = serializers.SerializerMethodField()

    def get_country(self, obj):
        color_obj = Color.objects.get(id=obj.color.id)
        return {"color_name": color_obj.color_name, "hex_code": "#000000"}

    class Meta:
        model = Person
        fields = "__all__"
        # depth = 1

    def validate(self, data):
        special_characters = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"
        if "name" in data:
            if any(char in special_characters for char in data["name"]):
                raise serializers.ValidationError(
                    "Name should not contain special characters"
                )

        if "age" in data:
            if data["age"] < 18:
                raise serializers.ValidationError("Age should be greater than 18")

        return data
