from typing import Any
from rest_framework import generics,status
from rest_framework import request
from rest_framework.response import Response
from core_apps.common.renderers import GenericJsonRenderer
from core_apps.profiles.models import Profile
from core_apps.apartments.models import Apartment
from .serializers import ApartmentSerializer

class ApartmentCreateAPIView(generics.CreateAPIView):
    serializer_class = ApartmentSerializer
    renderer_classes = (GenericJsonRenderer,)
    object_label = 'apartment'

    def create(self, request: request.Request, *args: Any, **kwargs: Any) -> Response:
        user = request.user
        if user.is_superuser or (hasattr(user, "profile") and user.profile.occupation == Profile.Occupation.TENANT):
            return super().create(request, *args, **kwargs)
        else:
            return Response({"error": "You are not authorized to create an apartment"}, status=status.HTTP_403_FORBIDDEN)

class ApartmentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ApartmentSerializer
    renderer_classes = (GenericJsonRenderer,)
    object_label = 'apartment'

    def get_object(self):
        queryset = self.request.user.apartment.all()
        obj = generics.get_object_or_404(queryset)
        return obj