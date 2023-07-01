from faker import Faker
from unittest import TestCase
from sqlalchemy.orm import Session
from unittest.mock import Mock, create_autospec, patch
from api.repositories.TrackingRepository import TrackingRepository

class TestRegionRepository(TestCase):
    session: Session
    trackingRepository: TrackingRepository


    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.trackingRepository = TrackingRepository(self.session)


    @patch("api.repositories.TrackingRepository.ConsumptionTracking", autospec=True)
    def test_create(self, MockConsumptionTracking):
        fake = Faker()
        tracking_list = [
            MockConsumptionTracking(
                tracking_number=fake.random_number(),
                tracking_date=fake.date_time(),
                infos=fake.sentence()
            )
        ]

        result = self.trackingRepository.create_tracking(tracking_list)

        self.session.add_all.assert_called_once_with(tracking_list)
        self.session.commit.assert_called_once()
        self.assertEqual(result, tracking_list)


    @patch("api.repositories.TrackingRepository.ConsumptionTracking", autospec=True)
    def test_update(self, MockConsumptionTracking):
        fake = Faker()
        data  = MockConsumptionTracking(
                tracking_number=fake.random_number(),
                tracking_date=fake.date_time(),
                infos=fake.sentence()
            )

        self.trackingRepository.update_tracking_postpaid = Mock()
        self.trackingRepository.update_tracking_postpaid(data)
        self.trackingRepository.update_tracking_postpaid.assert_called_with(data)

