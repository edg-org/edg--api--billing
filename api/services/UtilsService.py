import uuid

class UtilsService:
    POSTPAID = "postpaid"
    PREPAID = "prepaid"
    VAT = 0.18
    MONTHLY = 30

    def __init__(self):
        pass

    @classmethod
    def generate_uuid(cls) -> str:
        return str(uuid.uuid4())

