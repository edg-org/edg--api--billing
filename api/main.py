from fastapi import FastAPI, Depends
from api.metadata.Tags import Tags
from api.configs.BaseModel import init
from api.configs.Environment import get_env_var
from api.routers.v1.PrepaidInvoiceRouter import prepaidInvoiceRouter
from api.routers.v1.PostpaidInvoiceRouter import postpaidInvoiceRouter
from api.routers.v1.PrepaidTrackingRouter import prepaidTrackingRouter
from api.routers.v1.PostpaidTrackingRouter import postpaidTrackingRouter
from api.tools.JWTBearer import JWTBearer

# Application Environment Configuration
env = get_env_var()

# Core Application Instance
app = FastAPI(
    title=env.app_name,
    description=env.app_desc,
    version="0.0." + env.api_version,
    openapi_tags=Tags,
    dependencies=[Depends(JWTBearer())]
)

# Add Routers
app.include_router(prepaidTrackingRouter)
app.include_router(postpaidTrackingRouter)
app.include_router(prepaidInvoiceRouter)
app.include_router(postpaidInvoiceRouter)

# Initialise Data Model Attributes
init()
