from django.core import mail
from django.test import TestCase

from rest_framework.test import APIRequestFactory, force_authenticate

from ..accounts.tests import ResidentFactory, ManagerFactory

from .models import Complaint
from .views import ComplaintViewSet


class ComplaintViewSetTests(TestCase):

    def test_post(self):
        factory = APIRequestFactory(enforce_csrf_checks=False)
        data = {
            'complaint': 'the rent is too damn high',
        }
        user = ResidentFactory.create()
        ManagerFactory.create(site=user.apartment.building.site)  # for email
        req = factory.post('/complaints/complaints', data, format='json')
        req.building = user.apartment.building
        force_authenticate(req, user=user)
        # clear intro messages
        mail.outbox = []
        response = ComplaintViewSet.as_view({'post': 'create'})(req)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)

        complaint = Complaint.objects.get()
        self.assertEqual(complaint.resident, user)
        self.assertEqual(complaint.building, req.building)
