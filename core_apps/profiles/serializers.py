from .models import Profile
from rest_framework import serializers
from django_countries.serializer_fields import CountryField

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    username = serializers.ReadOnlyField(source="user.username")
    full_name = serializers.ReadOnlyField(source="user.get_full_name")
    country_of_origin = CountryField(name_only=True)
    # SerializerMethodField. Do avatar chi lay url, ne dung method la get_avatar
    avatar = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)
    class Meta:
        model = Profile
        fields = [
            "id","slug","first_name","last_name","username","full_name","gender","occupation","avatar","bio",
            "phone_number","country_of_origin","city_of_origin","report_count",
            "reputation","date_joined"
        ]
    
    def get_avatar(self, obj):
        try:
            return obj.avatar.url
        except AttributeError:
            return None

class UpdateProfileSerializer(serializers.ModelSerializer):
    # ReadOnlyField chi dung voi GET
    # De thuc hien PUT, PATCH phai doi thanh CharField
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    username = serializers.CharField(source="user.username")
    country_of_origin = CountryField(name_only=True)
    class Meta:
        model = Profile
        fields = [
            "first_name","last_name","username",
            "gender","occupation","bio","phone_number",
            "country_of_origin","city_of_origin"
        ]

class AvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]