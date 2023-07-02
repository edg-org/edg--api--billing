from faker import Faker
from typing import List
from unittest import TestCase
from unittest.mock import Mock, create_autospec, patch
from api.repositories.TrackingRepository import TrackingRepository
from api.services.PostpaidTrackingService import PostpaidTrackingService

class TestPostpaidTrackingService(TestCase):
    trackingRepository: TrackingRepository
    postpaidTrackingService: PostpaidTrackingService

    def setUp(self):
        super().setUp()
        self.trackingRepository = create_autospec(TrackingRepository)
        self.postpaidTrackingService = PostpaidTrackingService(self.trackingRepository)

    @patch("api.schemas.TrackingSchema.PostpaidCreateSchema", autospec=True)
    async def test_create(self, PostpaidCreateSchema):
        fake = Faker()
        postpaid_list = [PostpaidCreateSchema(
                 contract_number = fake,
                 index_value = fake,
                 index_date= fake,
        )]
        self.postpaidTrackingService.create_postpaid_tracking = Mock()
        self.postpaidTrackingService.create_postpaid_tracking(postpaid_list)
        self.postpaidTrackingService.create_postpaid_tracking.assert_called_once_with(postpaid_list)
