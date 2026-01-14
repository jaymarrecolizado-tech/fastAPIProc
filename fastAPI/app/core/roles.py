"""User roles enum for role-based access control"""

from enum import Enum


class UserRole(str, Enum):
    """User roles in the procurement system"""
    
    END_USER = "END_USER"
    PROCUREMENT_OFFICER = "PROCUREMENT_OFFICER"
    CANVASSER = "CANVASSER"
    BAC_SECRETARIAT = "BAC_SECRETARIAT"
    BAC_CHAIR = "BAC_CHAIR"
    BAC_MEMBER = "BAC_MEMBER"
    SUPPLIER = "SUPPLIER"
    ADMIN = "ADMIN"
    
    @classmethod
    def all_roles(cls) -> list[str]:
        """Get all available roles"""
        return [role.value for role in cls]
    
    def is_procurement_staff(self) -> bool:
        """Check if role is part of procurement staff"""
        return self in [
            UserRole.PROCUREMENT_OFFICER,
            UserRole.BAC_SECRETARIAT,
            UserRole.BAC_CHAIR,
            UserRole.BAC_MEMBER,
        ]
    
    def is_approver(self) -> bool:
        """Check if role can approve documents"""
        return self in [
            UserRole.PROCUREMENT_OFFICER,
            UserRole.BAC_CHAIR,
            UserRole.BAC_MEMBER,
        ]
    
    def is_bac_member(self) -> bool:
        """Check if role is BAC member or chair"""
        return self in [UserRole.BAC_CHAIR, UserRole.BAC_MEMBER]
