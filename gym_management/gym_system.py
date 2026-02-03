"""
Gym Management System - Main application class
"""

from datetime import datetime
from typing import List, Optional
import uuid

from .models import Member, Membership, Attendance, Payment, MembershipType, PaymentStatus
from .database import GymDatabase


class GymManagementSystem:
    """Main gym management system class"""
    
    def __init__(self, data_dir: str = "gym_data"):
        self.db = GymDatabase(data_dir)
    
    # Member Management
    def register_member(self, name: str, email: str, phone: str, 
                       address: str, date_of_birth: datetime) -> Member:
        """Register a new gym member"""
        member_id = f"MEM{str(uuid.uuid4())[:8].upper()}"
        member = Member(
            member_id=member_id,
            name=name,
            email=email,
            phone=phone,
            address=address,
            date_of_birth=date_of_birth
        )
        
        if self.db.add_member(member):
            return member
        else:
            raise ValueError("Failed to register member")
    
    def get_member(self, member_id: str) -> Optional[Member]:
        """Get member details"""
        return self.db.get_member(member_id)
    
    def get_all_members(self) -> List[Member]:
        """Get all members"""
        return self.db.get_all_members()
    
    def update_member_info(self, member_id: str, **kwargs) -> bool:
        """Update member information"""
        member = self.db.get_member(member_id)
        if not member:
            return False
        
        for key, value in kwargs.items():
            if hasattr(member, key):
                setattr(member, key, value)
        
        return self.db.update_member(member)
    
    def deactivate_member(self, member_id: str) -> bool:
        """Deactivate a member"""
        return self.db.deactivate_member(member_id)
    
    # Membership Management
    def create_membership(self, member_id: str, membership_type: MembershipType,
                         duration_months: int) -> Membership:
        """Create a new membership for a member"""
        member = self.db.get_member(member_id)
        if not member:
            raise ValueError("Member not found")
        
        # Define pricing based on membership type
        pricing = {
            MembershipType.BASIC: 29.99,
            MembershipType.PREMIUM: 49.99,
            MembershipType.VIP: 99.99
        }
        
        monthly_fee = pricing.get(membership_type, 29.99)
        membership_id = f"MBS{str(uuid.uuid4())[:8].upper()}"
        
        membership = Membership(
            membership_id=membership_id,
            member_id=member_id,
            membership_type=membership_type,
            start_date=datetime.now(),
            duration_months=duration_months,
            monthly_fee=monthly_fee
        )
        
        if self.db.add_membership(membership):
            # Create initial payment
            self.create_payment(member_id, membership_id, monthly_fee * duration_months)
            return membership
        else:
            raise ValueError("Failed to create membership")
    
    def get_member_membership(self, member_id: str) -> Optional[Membership]:
        """Get active membership for a member"""
        return self.db.get_member_membership(member_id)
    
    def check_membership_status(self, member_id: str) -> dict:
        """Check membership status for a member"""
        membership = self.db.get_member_membership(member_id)
        if not membership:
            return {
                "has_membership": False,
                "is_active": False,
                "is_expired": True
            }
        
        return {
            "has_membership": True,
            "is_active": membership.is_active,
            "is_expired": membership.is_expired(),
            "days_remaining": membership.days_remaining(),
            "membership_type": membership.membership_type.value,
            "end_date": membership.end_date.isoformat()
        }
    
    # Attendance Management
    def check_in(self, member_id: str) -> Attendance:
        """Check in a member"""
        member = self.db.get_member(member_id)
        if not member:
            raise ValueError("Member not found")
        
        if not member.is_active:
            raise ValueError("Member is not active")
        
        membership = self.db.get_member_membership(member_id)
        if not membership or membership.is_expired():
            raise ValueError("Member does not have an active membership")
        
        attendance_id = f"ATT{str(uuid.uuid4())[:8].upper()}"
        attendance = Attendance(
            attendance_id=attendance_id,
            member_id=member_id,
            check_in_time=datetime.now()
        )
        
        self.db.add_attendance(attendance)
        return attendance
    
    def check_out(self, member_id: str) -> Optional[Attendance]:
        """Check out a member"""
        attendances = self.db.get_member_attendances(member_id, limit=1)
        if not attendances:
            return None
        
        latest_attendance = attendances[0]
        if latest_attendance.check_out_time:
            return None
        
        latest_attendance.check_out()
        self.db.save_data()
        return latest_attendance
    
    def get_attendance_history(self, member_id: str, limit: int = None) -> List[Attendance]:
        """Get attendance history for a member"""
        return self.db.get_member_attendances(member_id, limit)
    
    # Payment Management
    def create_payment(self, member_id: str, membership_id: str, 
                      amount: float) -> Payment:
        """Create a payment record"""
        payment_id = f"PAY{str(uuid.uuid4())[:8].upper()}"
        payment = Payment(
            payment_id=payment_id,
            member_id=member_id,
            membership_id=membership_id,
            amount=amount,
            payment_date=datetime.now(),
            status=PaymentStatus.PENDING
        )
        
        self.db.add_payment(payment)
        return payment
    
    def process_payment(self, payment_id: str, transaction_id: str) -> bool:
        """Process a payment"""
        payment = self.db.get_payment(payment_id)
        if not payment:
            return False
        
        payment.mark_paid(transaction_id)
        self.db.save_data()
        return True
    
    def get_member_payments(self, member_id: str) -> List[Payment]:
        """Get all payments for a member"""
        return self.db.get_member_payments(member_id)
    
    def get_pending_payments(self) -> List[Payment]:
        """Get all pending payments"""
        return self.db.get_pending_payments()
    
    # Reports and Analytics
    def get_total_members(self) -> int:
        """Get total number of members"""
        return len(self.db.get_all_members())
    
    def get_active_members(self) -> int:
        """Get number of active members"""
        return len([m for m in self.db.get_all_members() if m.is_active])
    
    def get_total_revenue(self) -> float:
        """Calculate total revenue from paid payments"""
        paid_payments = [p for p in self.db.payments.values() 
                        if p.status == PaymentStatus.PAID]
        return sum(p.amount for p in paid_payments)
    
    def get_pending_revenue(self) -> float:
        """Calculate pending revenue"""
        pending_payments = [p for p in self.db.payments.values() 
                           if p.status == PaymentStatus.PENDING]
        return sum(p.amount for p in pending_payments)
    
    def get_membership_distribution(self) -> dict:
        """Get distribution of membership types"""
        distribution = {
            MembershipType.BASIC.value: 0,
            MembershipType.PREMIUM.value: 0,
            MembershipType.VIP.value: 0
        }
        
        for membership in self.db.memberships.values():
            if membership.is_active:
                distribution[membership.membership_type.value] += 1
        
        return distribution
