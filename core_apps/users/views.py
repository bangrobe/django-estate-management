import logging
from typing import Optional
from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

logger = logging.getLogger(__name__)

def set_auth_cookies(response: Response, access_token: Optional[str], refresh_token: Optional[str]) -> Response:
    access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
    cookie_settings = {
        'path': settings.COOK_PATH,
        'secure': settings.COOK_SECURE,
        'httponly': settings.COOK_HTTPONLY,
        'samesite': settings.COOK_SAMESITE,
        'max_age': access_token_lifetime,
    }

    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=access_token,
        **cookie_settings,
    )
    # Copy cookie settings cho refresh_token
    # Vi refresh_token co thoi gian song khac voi access_token nen phai thay doi max_age
    if refresh_token is not None:
        refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
        refresh_cookie_settings =  cookie_settings.copy()
        refresh_cookie_settings['max_age'] = refresh_token_lifetime
        response.set_cookie(
            key="refresh",
            value=refresh_token,
            **refresh_cookie_settings,
        )
    # Logged In Cookie Settings
    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings['httponly'] = False
    response.set_cookie(
        key="logged_in",
        value="true",
        **logged_in_cookie_settings,
    )


class CustomObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs):
        token_response = super().post(request, *args, **kwargs)
        if token_response.status_code == status.HTTP_200_OK:
            access_token =  token_response.data.get('access')
            refresh_token = token_response.data.get('refresh')
            if access_token is not None and refresh_token is not None:
                set_auth_cookies(token_response, access_token, refresh_token)

                token_response.pop('access', None)
                token_response.pop('refresh', None)

                token_response.data["message"] = "Login Successful"
            else:
                token_response.data["message"] = "Login Failed"
                logger.error("Access or refresh token not found")
        return token_response        

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token is None:
            request.data['refresh'] = refresh_token
        
        refresh_response = super().post(request, *args, **kwargs)

        if refresh_response.status_code == status.HTTP_200_OK:
            access_token =  refresh_response.data.get('access')
            refresh_token = refresh_response.data.get('refresh')
            if access_token is not None and refresh_token is not None:
                set_auth_cookies(refresh_response, access_token, refresh_token)

                refresh_response.pop('access', None)
                refresh_response.pop('refresh', None)

                refresh_response.data["message"] = "Access Token Refreshed successfully"
            else:
                refresh_response.data["message"] = "Access or refresh tokens not found in refresh response data"
                logger.error("Access or refresh token not found in refresh response data")
        return refresh_response
    
    # Custom ProviderAuthView
class CustomProviderAuthViewView(ProviderAuthView):
    def post(self, request: Request, *args, **kwargs):
        provider_response = super().post(request, *args, **kwargs)
        if provider_response.status_code == status.HTTP_201_CREATED:
            access_token =  provider_response.data.get('access')
            refresh_token = provider_response.data.get('refresh')
            if access_token is not None and refresh_token is not None:
                set_auth_cookies(provider_response, access_token, refresh_token)

                provider_response.pop('access', None)
                provider_response.pop('refresh', None)

                provider_response.data["message"] = "Google Login Successful"
            else:
                provider_response.data["message"] = "Access or refresh tokens not found in provider response data"
                logger.error("Access or refresh token not found in provider response data")
        return provider_response    
    
# Logout API View
class LogoutAPIView(APIView):
    def post(self, request: Request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(key="access")
        response.delete_cookie(key="refresh")
        response.delete_cookie(key="logged_in")
        response.data["message"] = "Logout successful"
        return response