"""Status enums for procurement workflow entities"""

from enum import Enum


class PurchaseRequestStatus(str, Enum):
    """Purchase Request workflow statuses"""
    
    PR_UNDER_REVIEW = "PR_UNDER_REVIEW"
    RFQ_READY = "RFQ_READY"
    RFQ_DISSEMINATED = "RFQ_DISSEMINATED"
    CANVASS_COMPLETE = "CANVASS_COMPLETE"
    BAC_DOCS_READY = "BAC_DOCS_READY"
    BAC_APPROVED = "BAC_APPROVED"
    PO_APPROVED = "PO_APPROVED"
    AWAITING_CONFORME = "AWAITING_CONFORME"
    PO_COMPLETE = "PO_COMPLETE"
    COA_STAMPED = "COA_STAMPED"
    CANCELLED = "CANCELLED"


class RFQStatus(str, Enum):
    """Request for Quotation statuses"""
    
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class CanvassStatus(str, Enum):
    """Canvass task statuses"""
    
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"


class ComplianceStatus(str, Enum):
    """Supplier quotation compliance status"""
    
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    PARTIAL = "PARTIAL"


class ProcurementMode(str, Enum):
    """Procurement modes as per RA 9184"""
    
    SHOPPING = "SHOPPING"
    SVP = "SVP"  # Small Value Procurement
    PUBLIC_BIDDING = "PUBLIC_BIDDING"
    NEGOTIATED = "NEGOTIATED"
    DIRECT_CONTRACTING = "DIRECT_CONTRACTING"


class BACDocumentType(str, Enum):
    """BAC document types"""
    
    ABSTRACT_OF_QUOTATIONS = "ABSTRACT_OF_QUOTATIONS"
    PRICE_MATRIX = "PRICE_MATRIX"
    TWG_CERT = "TWG_CERT"  # Technical Working Group Certificate
    RECOMMENDATION = "RECOMMENDATION"
    RESOLUTION = "RESOLUTION"


class BACDocumentStatus(str, Enum):
    """BAC document workflow statuses"""
    
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class PurchaseOrderStatus(str, Enum):
    """Purchase Order statuses"""
    
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DISSEMINATED = "DISSEMINATED"
    AWAITING_CONFORME = "AWAITING_CONFORME"
    CONFORME_ACCEPTED = "CONFORME_ACCEPTED"
    CONFORME_REJECTED = "CONFORME_REJECTED"
    COMPLETE = "COMPLETE"
    CANCELLED = "CANCELLED"


class ApprovalStatus(str, Enum):
    """Approval routing statuses"""
    
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


class DocumentCategory(str, Enum):
    """Document upload categories"""
    
    PR_DOCUMENT = "PR_DOCUMENT"
    RFQ_DOCUMENT = "RFQ_DOCUMENT"
    CANVASS_DOCUMENT = "CANVASS_DOCUMENT"
    BAC_DOCUMENT = "BAC_DOCUMENT"
    PO_DOCUMENT = "PO_DOCUMENT"
    QUOTATION_IMAGE = "QUOTATION_IMAGE"
    CONTRACT_DOCUMENT = "CONTRACT_DOCUMENT"
    OTHER = "OTHER"


class NotificationType(str, Enum):
    """Notification types"""
    
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    ITEM_APPROVED = "ITEM_APPROVED"
    ITEM_REJECTED = "ITEM_REJECTED"
    STATUS_UPDATED = "STATUS_UPDATED"
    PURCHASE_ORDER_DISSEMINATED = "PURCHASE_ORDER_DISSEMINATED"
    DEADLINE_APPROACHING = "DEADLINE_APPROACHING"
    OVERDUE_ALERT = "OVERDUE_ALERT"
    CANVASS_ASSIGNED = "CANVASS_ASSIGNED"
    SUPPLIER_CONFORME = "SUPPLIER_CONFORME"


class UrgencyLevel(str, Enum):
    """Urgency levels for purchase requests"""
    
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class ActivityAction(str, Enum):
    """Activity log action types"""
    
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    STATUS_CHANGED = "STATUS_CHANGED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ROUTED = "ROUTED"
    UPLOADED = "UPLOADED"
    DOWNLOADED = "DOWNLOADED"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    PASSWORD_RESET = "PASSWORD_RESET"
