from django.contrib.auth import login, logout, authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class AuthView(APIView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return Response(UserSerializer(request.user).data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        try:
            user = authenticate(email=request.DATA['email'],
                                password=request.DATA['password'])
        except KeyError:
            user = None

        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response()
