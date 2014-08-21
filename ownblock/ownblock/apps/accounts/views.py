from django.db.models import Q

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import User
from .serializers import UserSerializer, AuthUserSerializer


class UserViewSet(viewsets.ModelViewSet):

    model = User
    serializer_class = UserSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).select_related(
            'apartment'
        ).order_by('last_name', 'first_name')

        if self.request.GET.get('residents'):
            return qs.filter(apartment__building=self.request.building)

        return qs.filter(
            Q(
                Q(apartment__building=self.request.building) |
                Q(organization=self.request.building.organization)
            ),
            is_active=True,
        )


class AuthView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_user_response(self, request):
            return Response(AuthUserSerializer(
                request.user, context={'request': request}).data)

    def get(self, request, *args, **kwargs):
        return self.get_user_response(request)

    def put(self, request, *args, **kwargs):
        serializer = AuthUserSerializer(request.user, data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save(force_update=True)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        password = request.DATA.get('password')
        if not password:
            return Response('Password is missing',
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(request.DATA['password'])
        request.user.save()
        return Response()
