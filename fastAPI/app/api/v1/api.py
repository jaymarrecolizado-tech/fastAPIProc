"""API v1 Router - aggregates all API routes"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Additional routers will be added as we create them:
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(purchase_requests.router, prefix="/purchase-requests", tags=["Purchase Requests"])
# api_router.include_router(rfqs.router, prefix="/rfqs", tags=["RFQs"])
# api_router.include_router(canvasses.router, prefix="/canvasses", tags=["Canvassing"])
# api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Suppliers"])
# api_router.include_router(bac_documents.router, prefix="/bac-documents", tags=["BAC Documents"])
# api_router.include_router(purchase_orders.router, prefix="/purchase-orders", tags=["Purchase Orders"])
# api_router.include_router(approvals.router, prefix="/approvals", tags=["Approvals"])
# api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
# api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
# api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
