import uuid
import json
from api.services.ExceptionService import ExceptionService

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


    @classmethod
    def get_json_data(cls, file_name: str):
        try:
            with open('../data/' + file_name, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("File not found!")
            ExceptionService.internal_server_error()
        except json.JSONDecodeError:
            print("Invalid JSON format!")
            ExceptionService.internal_server_error()
            
