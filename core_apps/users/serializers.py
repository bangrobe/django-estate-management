#This file begin from chapter 10
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

User = get_user_model()

class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "first_name","last_name","password"]

# Custom User Serializers de tra ve user data khi call api users/me
class CustomUserSerializers(UserSerializer):
    full_name = serializers.ReadOnlyField(source="get_full_name") #get_full_name la 1 @property duoc tao ra khi viet model
    gender = serializers.ReadOnlyField(source="profile.gender")
    slug = serializers.ReadOnlyField(source="profile.slug")
    occupation = serializers.ReadOnlyField(source="profile.occupation")
    phone_number = serializers.ReadOnlyField(source="profile.phone_number")
    country = CountryField(source="profile.country_of_origin")
    city = serializers.ReadOnlyField(source="profile.city_of_origin")
    avatar = serializers.ReadOnlyField(source="profile.avatar.url")
    reputation = serializers.ReadOnlyField(source="profile.reputation")

    class Meta(UserSerializer.Meta):
        model = User
        fields = [
            "id","email","first_name","last_name","username","slug",
            "full_name","gender","occupation","phone_number","country",
            "city","avatar","reputation","date_joined"
        ]
        read_only_fields=["id","email","date_joined"]