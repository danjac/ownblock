from django.db.models import Q

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.storage.models import Item
from apps.parking.models import Vehicle
from apps.messaging.models import Message
from apps.notices.models import Notice
from apps.amenities.models import Booking

from .models import User

from .serializers import (
    UserSerializer,
    RestrictedUserSerializer,
    AuthUserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):

    model = User

    def get_serializer_class(self):
        if self.request.user.role == 'manager':
            return RestrictedUserSerializer
        return UserSerializer

    def retrieve(self, request, *args, **kwargs):
        self.object = self.get_object()

        data = self.get_serializer(self.object).data

        notices = Notice.objects.filter(author=self.object)

        data['notices'] = []

        for notice in notices.iterator():
            data['notices'].append({
                'id': notice.id,
                'title': notice.title,
                'details': notice.details,
                'created': notice.created,
            })

        if self.object != self.request.user:

            messages = Message.objects.filter(
                Q(sender=self.object) | Q(recipient=self.object)).filter(
                Q(sender=self.request.user) | Q(recipient=self.request.user)
            ).order_by('-created')

            data['sent_messages'] = []
            data['received_messages'] = []

            for message in messages.iterator():
                message_data = {
                    'id': message.id,
                    'header': message.header,
                    'details': message.details,
                    'created': message.created,
                }
                if message.sender_id == self.object.id:
                    data['sent_messages'].append(message_data)
                else:
                    data['received_messages'].append(message_data)

        if self.object.role == 'resident':
            items = Item.objects.filter(
                resident=self.object
            ).select_related('place')

            data['items'] = []

            for item in items.iterator():
                data['items'].append({
                    'id': item.id,
                    'place_id': item.place_id,
                    'place_name': item.place.name,
                    'description': item.description,
                })

            vehicles = Vehicle.objects.filter(
                resident=self.object
            )

            data['vehicles'] = []

            for vehicle in vehicles.iterator():
                data['vehicles'].append({
                    'id': vehicle.id,
                    'description': vehicle.description,
                    'registration_number': vehicle.registration_number,
                })

            bookings = Booking.objects.filter(
                resident=self.object
            ).select_related('amenity')

            data['bookings'] = []
            for booking in bookings:
                data['bookings'].append({
                                        'id': booking.id,
                                        'amenity': {
                                            'id': booking.amenity.id,
                                            'name': booking.amenity.name,
                                        },

                                        'reserved_from': booking.reserved_from,
                                        'reserved_to': booking.reserved_to,
                                        })

        return Response(data)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).select_related(
            'apartment'
        ).filter(is_active=True).order_by('last_name', 'first_name')

        if self.request.GET.get('residents'):
            return qs.filter(apartment__building=self.request.building)

        return qs.filter(
            Q(
                Q(apartment__building=self.request.building) |
                Q(organization=self.request.building.organization)
            ),
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
