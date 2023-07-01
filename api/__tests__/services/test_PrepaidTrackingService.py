from faker import Faker
from typing import List
from unittest import TestCase
from unittest.mock import Mock, create_autospec, patch
from api.repositories.TrackingRepository import TrackingRepository
from api.services.PrepaidTrackingService import PrepaidTrackingService

class TestPrepaidTrackingService(TestCase):
    trackingRepository: TrackingRepository
    prepaidTrackingService: PrepaidTrackingService

    def setUp(self):
        super().setUp()
        self.trackingRepository = create_autospec(TrackingRepository)
        self.prepaidTrackingService = PrepaidTrackingService(self.trackingRepository)

    @patch("api.schemas.TrackingSchema.PrepaidCreateSchema", autospec=True)
    async def test_create(self, PrepaidCreateSchema):
        fake = Faker()
        prepaid_list = [PrepaidCreateSchema(
                 contract_number = fake,
                 power_recharged = fake,
                 power_recharged_date= fake,
        )]
        self.prepaidTrackingService.create_prepaid_tracking = Mock()
        self.prepaidTrackingService.create_prepaid_tracking(prepaid_list)
        self.prepaidTrackingService.create_prepaid_tracking.assert_called_once_with(prepaid_list)
