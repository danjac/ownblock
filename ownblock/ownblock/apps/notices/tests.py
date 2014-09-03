from django.test import TestCase
from django.contrib.auth import get_user_model

from ..accounts.tests import ManagerFactory
from ..buildings.tests import BuildingFactory

from .models import Notice


User = get_user_model()


class NoticeTests(TestCase):

    def test_has_permission_if_manager(self):
        building = BuildingFactory()
        manager = ManagerFactory(site=building.site)
        notice = Notice(building=building)
        self.assertTrue(notice.has_permission(manager,
                                              'notices.change_notice'))

    def test_has_permission_if_not_manager(self):
        building = BuildingFactory()
        manager = ManagerFactory()
        notice = Notice(building=building)
        self.assertFalse(notice.has_permission(manager,
                                               'notices.change_notice'))

    def test_has_permission_if_not_author(self):
        notice = Notice(author=User(role='resident'))
        self.assertFalse(notice.has_permission(User(role='resident'),
                                               'notices.change_notice'))

    def test_has_permission_if_author(self):
        notice = Notice(author=User(role='resident'))
        self.assertTrue(notice.has_permission(notice.author,
                                              'notices.change_notice'))
