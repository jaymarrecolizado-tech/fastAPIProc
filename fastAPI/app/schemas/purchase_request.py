"""Pydantic schemas for Purchase Request model"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

from app.core.status import PurchaseRequestStatus, UrgencyLevel


class PRItemBase(BaseModel):
    """Base PR item schema"""
    item_code: str = Field(..., max_length=100)
    item_name: str = Field(..., max_length=500)
    quantity: Decimal = Field(..., gt=0, decimal_places=2, max_digits=10)
    unit_of_measure: str = Field(..., max_length=50)
    estimated_price: Decimal = Field(..., gt=0, decimal_places=2, max_digits=15)


class PRItemCreate(PRItemBase):
    """Schema for creating PR item"""
    pass


class PRItemResponse(PRItemBase):
    """Schema for PR item response"""
    id: int
    total_estimated_cost: Decimal
    
    model_config = ConfigDict(from_attributes=True)


class PurchaseRequestBase(BaseModel):
    """Base Purchase Request schema"""
    project_title: str = Field(..., min_length=10, max_length=500)
    project_description: str = Field(..., min_length=20)
    purpose: str = Field(..., min_length=10)
    end_user_department: str = Field(..., max_length=255)
    office_name: Optional[str] = Field(None, max_length=255)
    office_address: Optional[str] = None
    responsibility_center: Optional[str] = Field(None, max_length=100)
    fund_source: str = Field(..., max_length=255)
    estimated_budget: Decimal = Field(..., gt=0, decimal_places=2, max_digits=15)
    urgency_level: UrgencyLevel
    urgency_timeline: Optional[str] = None
    has_signatures: bool = False
    has_specs: bool = False
    has_quantity: bool = False
    has_market_survey: bool = False
    requested_by_name: str = Field(..., max_length=255)
    requested_by_designation: str = Field(..., max_length=255)
    approved_by_name: Optional[str] = Field(None, max_length=255)
    approved_by_designation: Optional[str] = Field(None, max_length=255)
    budget_officer_name: str = Field(..., max_length=255)
    budget_officer_designation: str = Field(..., max_length=255)
    deficiency_notes: Optional[str] = None


class PurchaseRequestCreate(PurchaseRequestBase):
    """Schema for creating Purchase Request"""
    pr_items: List[PRItemCreate] = Field(..., min_length=1, max_length=100)


class PurchaseRequestUpdate(BaseModel):
    """Schema for updating Purchase Request"""
    project_title: Optional[str] = Field(None, min_length=10, max_length=500)
    project_description: Optional[str] = Field(None, min_length=20)
    purpose: Optional[str] = Field(None, min_length=10)
    estimated_budget: Optional[Decimal] = Field(None, gt=0, decimal_places=2, max_digits=15)
    urgency_level: Optional[UrgencyLevel] = None
    urgency_timeline: Optional[str] = None
    deficiency_notes: Optional[str] = None


class PurchaseRequestResponse(PurchaseRequestBase):
    """Schema for Purchase Request response"""
    id: int
    pr_number: str
    end_user_id: int
    status: PurchaseRequestStatus
    approval_date: Optional[datetime] = None
    pr_items: List[PRItemResponse] = []
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PurchaseRequestList(BaseModel):
    """Schema for Purchase Request list response"""
    items: List[PurchaseRequestResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ApprovalRoutingCreate(BaseModel):
    """Schema for creating approval routing"""
    approver_ids: List[int] = Field(..., min_length=1, max_length=10)
    comments: Optional[str] = None


class ApprovalAction(BaseModel):
    """Schema for approval/rejection action"""
    comments: Optional[str] = None
    rejection_reason: Optional[str] = Field(None, max_length=1000)


class PRStatusUpdate(BaseModel):
    """Schema for manual PR status update"""
    status: PurchaseRequestStatus
    notes: Optional[str] = None
