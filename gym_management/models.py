"""
Data models for the gym management system.
"""

from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum


class MembershipType(Enum):
    """Membership plan types"""
    BASIC = "Basic"
    PREMIUM = "Premium"
    VIP = "VIP"


class PaymentStatus(Enum):
    """Payment status types"""
    PENDING = "Pending"
    PAID = "Paid"
    OVERDUE = "Overdue"


class Member:
    """Represents a gym member"""
    
    def __init__(self, member_id: str, name: str, email: str, phone: str, 
                 address: str, date_of_birth: datetime, join_date: datetime = None):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.date_of_birth = date_of_birth
        self.join_date = join_date or datetime.now()
        self.is_active = True
        self.membership = None
    
    def __str__(self):
        return f"Member({self.member_id}, {self.name}, {self.email})"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        """Convert member to dictionary"""
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "date_of_birth": self.date_of_birth.isoformat(),
            "join_date": self.join_date.isoformat(),
            "is_active": self.is_active,
            "membership": self.membership.to_dict() if self.membership else None
        }


class Membership:
    """Represents a membership plan"""
    
    def __init__(self, membership_id: str, member_id: str, 
                 membership_type: MembershipType, start_date: datetime,
                 duration_months: int, monthly_fee: float):
        self.membership_id = membership_id
        self.member_id = member_id
        self.membership_type = membership_type
        self.start_date = start_date
        self.duration_months = duration_months
        self.monthly_fee = monthly_fee
        self.end_date = start_date + timedelta(days=duration_months * 30)
        self.is_active = True
    
    def is_expired(self) -> bool:
        """Check if membership has expired"""
        return datetime.now() > self.end_date
    
    def days_remaining(self) -> int:
        """Get number of days remaining in membership"""
        if self.is_expired():
            return 0
        return (self.end_date - datetime.now()).days
    
    def __str__(self):
        return f"Membership({self.membership_id}, {self.membership_type.value}, {self.member_id})"
    
    def to_dict(self):
        """Convert membership to dictionary"""
        return {
            "membership_id": self.membership_id,
            "member_id": self.member_id,
            "membership_type": self.membership_type.value,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "duration_months": self.duration_months,
            "monthly_fee": self.monthly_fee,
            "is_active": self.is_active,
            "is_expired": self.is_expired(),
            "days_remaining": self.days_remaining()
        }


class Attendance:
    """Represents member attendance record"""
    
    def __init__(self, attendance_id: str, member_id: str, 
                 check_in_time: datetime, check_out_time: Optional[datetime] = None):
        self.attendance_id = attendance_id
        self.member_id = member_id
        self.check_in_time = check_in_time
        self.check_out_time = check_out_time
    
    def check_out(self, check_out_time: datetime = None):
        """Record check-out time"""
        self.check_out_time = check_out_time or datetime.now()
    
    def duration_minutes(self) -> int:
        """Calculate duration of gym session in minutes"""
        if not self.check_out_time:
            return 0
        delta = self.check_out_time - self.check_in_time
        return int(delta.total_seconds() / 60)
    
    def __str__(self):
        return f"Attendance({self.attendance_id}, {self.member_id}, {self.check_in_time})"
    
    def to_dict(self):
        """Convert attendance to dictionary"""
        return {
            "attendance_id": self.attendance_id,
            "member_id": self.member_id,
            "check_in_time": self.check_in_time.isoformat(),
            "check_out_time": self.check_out_time.isoformat() if self.check_out_time else None,
            "duration_minutes": self.duration_minutes()
        }


class Payment:
    """Represents a payment record"""
    
    def __init__(self, payment_id: str, member_id: str, membership_id: str,
                 amount: float, payment_date: datetime, 
                 status: PaymentStatus = PaymentStatus.PENDING):
        self.payment_id = payment_id
        self.member_id = member_id
        self.membership_id = membership_id
        self.amount = amount
        self.payment_date = payment_date
        self.status = status
        self.transaction_id = None
    
    def mark_paid(self, transaction_id: str):
        """Mark payment as paid"""
        self.status = PaymentStatus.PAID
        self.transaction_id = transaction_id
    
    def mark_overdue(self):
        """Mark payment as overdue"""
        self.status = PaymentStatus.OVERDUE
    
    def __str__(self):
        return f"Payment({self.payment_id}, {self.member_id}, ${self.amount}, {self.status.value})"
    
    def to_dict(self):
        """Convert payment to dictionary"""
        return {
            "payment_id": self.payment_id,
            "member_id": self.member_id,
            "membership_id": self.membership_id,
            "amount": self.amount,
            "payment_date": self.payment_date.isoformat(),
            "status": self.status.value,
            "transaction_id": self.transaction_id
        }
