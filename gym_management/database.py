"""
Database manager for the gym management system.
Handles storage and retrieval of gym data.
"""

import json
import os
from typing import List, Optional, Dict
from datetime import datetime
from .models import Member, Membership, Attendance, Payment, MembershipType, PaymentStatus


class GymDatabase:
    """Manages all gym data operations"""
    
    def __init__(self, data_dir: str = "gym_data"):
        self.data_dir = data_dir
        self._ensure_data_directory()
        
        # In-memory storage
        self.members: Dict[str, Member] = {}
        self.memberships: Dict[str, Membership] = {}
        self.attendances: List[Attendance] = []
        self.payments: Dict[str, Payment] = {}
        
        # Load existing data
        self.load_data()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_data(self):
        """Save all data to JSON files"""
        # Save members
        members_data = {mid: m.to_dict() for mid, m in self.members.items()}
        with open(os.path.join(self.data_dir, "members.json"), "w") as f:
            json.dump(members_data, f, indent=2)
        
        # Save memberships
        memberships_data = {mid: m.to_dict() for mid, m in self.memberships.items()}
        with open(os.path.join(self.data_dir, "memberships.json"), "w") as f:
            json.dump(memberships_data, f, indent=2)
        
        # Save attendances
        attendances_data = [a.to_dict() for a in self.attendances]
        with open(os.path.join(self.data_dir, "attendances.json"), "w") as f:
            json.dump(attendances_data, f, indent=2)
        
        # Save payments
        payments_data = {pid: p.to_dict() for pid, p in self.payments.items()}
        with open(os.path.join(self.data_dir, "payments.json"), "w") as f:
            json.dump(payments_data, f, indent=2)
    
    def load_data(self):
        """Load all data from JSON files"""
        try:
            # Load members
            members_file = os.path.join(self.data_dir, "members.json")
            if os.path.exists(members_file):
                with open(members_file, "r") as f:
                    members_data = json.load(f)
                    for mid, data in members_data.items():
                        member = Member(
                            member_id=data["member_id"],
                            name=data["name"],
                            email=data["email"],
                            phone=data["phone"],
                            address=data["address"],
                            date_of_birth=datetime.fromisoformat(data["date_of_birth"]),
                            join_date=datetime.fromisoformat(data["join_date"])
                        )
                        member.is_active = data["is_active"]
                        self.members[mid] = member
            
            # Load memberships
            memberships_file = os.path.join(self.data_dir, "memberships.json")
            if os.path.exists(memberships_file):
                with open(memberships_file, "r") as f:
                    memberships_data = json.load(f)
                    for mid, data in memberships_data.items():
                        membership = Membership(
                            membership_id=data["membership_id"],
                            member_id=data["member_id"],
                            membership_type=MembershipType(data["membership_type"]),
                            start_date=datetime.fromisoformat(data["start_date"]),
                            duration_months=data["duration_months"],
                            monthly_fee=data["monthly_fee"]
                        )
                        membership.is_active = data["is_active"]
                        self.memberships[mid] = membership
                        
                        # Link to member
                        if membership.member_id in self.members:
                            self.members[membership.member_id].membership = membership
            
            # Load payments
            payments_file = os.path.join(self.data_dir, "payments.json")
            if os.path.exists(payments_file):
                with open(payments_file, "r") as f:
                    payments_data = json.load(f)
                    for pid, data in payments_data.items():
                        payment = Payment(
                            payment_id=data["payment_id"],
                            member_id=data["member_id"],
                            membership_id=data["membership_id"],
                            amount=data["amount"],
                            payment_date=datetime.fromisoformat(data["payment_date"]),
                            status=PaymentStatus(data["status"])
                        )
                        payment.transaction_id = data.get("transaction_id")
                        self.payments[pid] = payment
            
            # Load attendances
            attendances_file = os.path.join(self.data_dir, "attendances.json")
            if os.path.exists(attendances_file):
                with open(attendances_file, "r") as f:
                    attendances_data = json.load(f)
                    for data in attendances_data:
                        attendance = Attendance(
                            attendance_id=data["attendance_id"],
                            member_id=data["member_id"],
                            check_in_time=datetime.fromisoformat(data["check_in_time"]),
                            check_out_time=datetime.fromisoformat(data["check_out_time"]) if data["check_out_time"] else None
                        )
                        self.attendances.append(attendance)
        
        except Exception as e:
            print(f"Error loading data: {e}")
    
    # Member operations
    def add_member(self, member: Member) -> bool:
        """Add a new member"""
        if member.member_id in self.members:
            return False
        self.members[member.member_id] = member
        self.save_data()
        return True
    
    def get_member(self, member_id: str) -> Optional[Member]:
        """Get member by ID"""
        return self.members.get(member_id)
    
    def get_all_members(self) -> List[Member]:
        """Get all members"""
        return list(self.members.values())
    
    def update_member(self, member: Member) -> bool:
        """Update existing member"""
        if member.member_id not in self.members:
            return False
        self.members[member.member_id] = member
        self.save_data()
        return True
    
    def deactivate_member(self, member_id: str) -> bool:
        """Deactivate a member"""
        member = self.get_member(member_id)
        if not member:
            return False
        member.is_active = False
        self.save_data()
        return True
    
    # Membership operations
    def add_membership(self, membership: Membership) -> bool:
        """Add a new membership"""
        if membership.membership_id in self.memberships:
            return False
        self.memberships[membership.membership_id] = membership
        
        # Link to member
        if membership.member_id in self.members:
            self.members[membership.member_id].membership = membership
        
        self.save_data()
        return True
    
    def get_membership(self, membership_id: str) -> Optional[Membership]:
        """Get membership by ID"""
        return self.memberships.get(membership_id)
    
    def get_member_membership(self, member_id: str) -> Optional[Membership]:
        """Get active membership for a member"""
        for membership in self.memberships.values():
            if membership.member_id == member_id and membership.is_active:
                return membership
        return None
    
    # Attendance operations
    def add_attendance(self, attendance: Attendance) -> bool:
        """Add attendance record"""
        self.attendances.append(attendance)
        self.save_data()
        return True
    
    def get_member_attendances(self, member_id: str, limit: int = None) -> List[Attendance]:
        """Get attendance records for a member"""
        member_attendances = [a for a in self.attendances if a.member_id == member_id]
        member_attendances.sort(key=lambda x: x.check_in_time, reverse=True)
        if limit:
            return member_attendances[:limit]
        return member_attendances
    
    # Payment operations
    def add_payment(self, payment: Payment) -> bool:
        """Add payment record"""
        if payment.payment_id in self.payments:
            return False
        self.payments[payment.payment_id] = payment
        self.save_data()
        return True
    
    def get_payment(self, payment_id: str) -> Optional[Payment]:
        """Get payment by ID"""
        return self.payments.get(payment_id)
    
    def get_member_payments(self, member_id: str) -> List[Payment]:
        """Get all payments for a member"""
        return [p for p in self.payments.values() if p.member_id == member_id]
    
    def get_pending_payments(self) -> List[Payment]:
        """Get all pending payments"""
        return [p for p in self.payments.values() if p.status == PaymentStatus.PENDING]
