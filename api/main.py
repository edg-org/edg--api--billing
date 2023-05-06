from fastapi import FastAPI

from api.configs.Environment import get_environment_variables
from api.metadata.Tags import Tags
from api.models.BaseModel import init
from api.routers.v1.PrepaidConsumptionTrackingRouter import PrepaidConsumptionTrackingRouter
from api.routers.v1.PostpaidConsumptionTrackingRouter import PostpaidConsumptionTrackingRouter
from api.routers.v1.PrepaidInvoiceRouter import PrepaidInvoiceRouter
from api.routers.v1.PostpaidInvoiceRouter import PostpaidInvoiceRouter

# Application Environment Configuration
env = get_environment_variables()

# Core Application Instance
app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
)

# Add Routers
app.include_router(PostpaidConsumptionTrackingRouter)
app.include_router(PostpaidInvoiceRouter)
app.include_router(PrepaidConsumptionTrackingRouter)
app.include_router(PrepaidInvoiceRouter)


# Initialise Data Model Attributes
init()
