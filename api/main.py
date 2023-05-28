from fastapi import FastAPI
from api.metadata.Tags import Tags
from api.configs.BaseModel import init
from api.configs.Environment import get_env_var
from api.routers.v1.PrepaidInvoiceRouter import prepaidinvoiceRouter
from api.routers.v1.PostpaidInvoiceRouter import postpaidinvoiceRouter
from api.routers.v1.PrepaidTrackingRouter import prepaidtrackingRouter
from api.routers.v1.PostpaidTrackingRouter import postpaidtrackingRouter

# Application Environment Configuration
env = get_env_var()

# Core Application Instance
app = FastAPI(
    title=env.app_name,
    description=env.app_desc,
    version="0.0." + env.api_version,
    openapi_tags=Tags,
)

# Add Routers
app.include_router(postpaidtrackingRouter)
app.include_router(postpaidinvoiceRouter)
app.include_router(prepaidtrackingRouter)
app.include_router(prepaidinvoiceRouter)

# Initialise Data Model Attributes
init()
