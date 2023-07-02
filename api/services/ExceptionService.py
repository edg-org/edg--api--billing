from fastapi import HTTPException

class ExceptionService:
    def __init__(self):
        pass


    @classmethod
    def tracking_not_found(cls):
        raise HTTPException(status_code = 404, detail = "Tracking not found")


    @classmethod
    def invoice_not_found(cls):
        raise HTTPException(status_code = 404, detail = "Invoice not found")


    @classmethod
    def internal_server_error(cls):
        raise HTTPException(status_code = 500, detail = "Internal Server Error")

