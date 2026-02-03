"""
Unit tests for the Gym Management System
"""

import unittest
import os
import shutil
from datetime import datetime, timedelta

from gym_management.gym_system import GymManagementSystem
from gym_management.models import Member, Membership, MembershipType, PaymentStatus


class TestGymManagementSystem(unittest.TestCase):
    """Test cases for Gym Management System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = "test_gym_data"
        self.gym = GymManagementSystem(data_dir=self.test_data_dir)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
    
    def test_register_member(self):
        """Test member registration"""
        member = self.gym.register_member(
            name="Test User",
            email="test@example.com",
            phone="555-0100",
            address="123 Test St",
            date_of_birth=datetime(1990, 1, 1)
        )
        
        self.assertIsNotNone(member)
        self.assertEqual(member.name, "Test User")
        self.assertEqual(member.email, "test@example.com")
        self.assertTrue(member.is_active)
    
    def test_get_member(self):
        """Test getting member by ID"""
        member = self.gym.register_member(
            name="Test User",
            email="test@example.com",
            phone="555-0100",
            address="123 Test St",
            date_of_birth=datetime(1990, 1, 1)
        )
        
        retrieved_member = self.gym.get_member(member.member_id)
        self.assertIsNotNone(retrieved_member)
        self.assertEqual(retrieved_member.member_id, member.member_id)
        self.assertEqual(retrieved_member.name, "Test User")
    
    def test_create_membership(self):
        """Test membership creation"""
        member = self.gym.register_member(
            name="Test User",
            email="test@example.com",
            phone="555-0100",
            address="123 Test St",
            date_of_birth=datetime(1990, 1, 1)
        )
        
        membership = self.gym.create_membership(
            member_id=member.member_id,
            membership_type=MembershipType.PREMIUM,
            duration_months=6
        )
        
        self.assertIsNotNone(membership)
        self.assertEqual(membership.member_id, member.member_id)
        self.assertEqual(membership.membership_type, MembershipType.PREMIUM)
        self.assertEqual(membership.duration_months, 6)
    
    def test_check_membership_status(self):
        """Test membership status check"""
        member = self.gym.register_member(
            name="Test User",
            email="test@example.com",
            phone="555-0100",
            address="123 Test St",
            date_of_birth=datetime(1990, 1, 1)
        )
        
        membership = self.gym.create_membership(
            member_id=member.member_id,
            membership_type=MembershipType.BASIC,
            duration_months=3
        )
        
        status = self.gym.check_membership_status(member.member_id)
        
        self.assertTrue(status['has_membership'])
        self.assertTrue(status['is_active'])
        self.assertFalse(status['is_expired'])
        self.assertEqual(status['membership_type'], 'Basic')
    
    def test_check_in(self):
        """Test member check-in"""
        member = self.gym.register_member(
            name="Test User",
            email="test@example.com",
            phone="555-0100",
            address="123 Test St",
            date_of_birth=datetime(1990, 1, 1)
        )
        
        membership = self.gym.create_membership(
            member_id=member.member_id,
            membership_type=MembershipType.BASIC,
            duration_months=3
        )
        
        attendance = self.gym.check_in(member.member_id)
        
        self.assertIsNotNone(attendance)
        self.assertEqual(attendance.member_id, member.member_id)
        self.assertIsNotNone(attendance.check_in_time)
        self.assertIsNone(attendance.check_out_time)
    
    def test_check_out(self):
        """Test member check-out"""
        import time
        
        member = self.gym.register_member(
            name="Test User",
            email="test@example.com",
            phone="555-0100",
            address="123 Test St",
            date_of_birth=datetime(1990, 1, 1)
        )
        
        membership = self.gym.create_membership(
            member_id=member.member_id,
            membership_type=MembershipType.BASIC,
            duration_months=3
        )
        
        # Check in first
        self.gym.check_in(member.member_id)
        
        # Wait a bit to ensure duration > 0
        time.sleep(1)
        
        # Then check out
        attendance = self.gym.check_out(member.member_id)
        
        self.assertIsNotNone(attendance)
        self.assertIsNotNone(attendance.check_out_time)
        self.assertGreaterEqual(attendance.duration_minutes(), 0)
    
    def test_payment_creation(self):
        """Test payment creation"""
        member = self.gym.register_member(
            name="Test User",
            email="test@example.com",
            phone="555-0100",
            address="123 Test St",
            date_of_birth=datetime(1990, 1, 1)
        )
        
        membership = self.gym.create_membership(
            member_id=member.member_id,
            membership_type=MembershipType.PREMIUM,
            duration_months=6
        )
        
        payments = self.gym.get_member_payments(member.member_id)
        
        self.assertGreater(len(payments), 0)
        payment = payments[0]
        self.assertEqual(payment.member_id, member.member_id)
        self.assertEqual(payment.status, PaymentStatus.PENDING)
    
    def test_payment_processing(self):
        """Test payment processing"""
        member = self.gym.register_member(
            name="Test User",
            email="test@example.com",
            phone="555-0100",
            address="123 Test St",
            date_of_birth=datetime(1990, 1, 1)
        )
        
        membership = self.gym.create_membership(
            member_id=member.member_id,
            membership_type=MembershipType.BASIC,
            duration_months=3
        )
        
        payments = self.gym.get_member_payments(member.member_id)
        payment = payments[0]
        
        # Process the payment
        success = self.gym.process_payment(payment.payment_id, "TXN123456")
        
        self.assertTrue(success)
        
        # Verify payment status
        updated_payment = self.gym.db.get_payment(payment.payment_id)
        self.assertEqual(updated_payment.status, PaymentStatus.PAID)
        self.assertEqual(updated_payment.transaction_id, "TXN123456")
    
    def test_dashboard_stats(self):
        """Test dashboard statistics"""
        # Register multiple members
        for i in range(3):
            member = self.gym.register_member(
                name=f"Test User {i}",
                email=f"test{i}@example.com",
                phone=f"555-010{i}",
                address=f"{i} Test St",
                date_of_birth=datetime(1990, 1, 1)
            )
            
            self.gym.create_membership(
                member_id=member.member_id,
                membership_type=MembershipType.BASIC,
                duration_months=3
            )
        
        total_members = self.gym.get_total_members()
        active_members = self.gym.get_active_members()
        
        self.assertEqual(total_members, 3)
        self.assertEqual(active_members, 3)
    
    def test_membership_distribution(self):
        """Test membership distribution"""
        # Create members with different membership types
        member1 = self.gym.register_member(
            name="Basic User",
            email="basic@example.com",
            phone="555-0101",
            address="1 Test St",
            date_of_birth=datetime(1990, 1, 1)
        )
        self.gym.create_membership(member1.member_id, MembershipType.BASIC, 3)
        
        member2 = self.gym.register_member(
            name="Premium User",
            email="premium@example.com",
            phone="555-0102",
            address="2 Test St",
            date_of_birth=datetime(1990, 1, 1)
        )
        self.gym.create_membership(member2.member_id, MembershipType.PREMIUM, 6)
        
        member3 = self.gym.register_member(
            name="VIP User",
            email="vip@example.com",
            phone="555-0103",
            address="3 Test St",
            date_of_birth=datetime(1990, 1, 1)
        )
        self.gym.create_membership(member3.member_id, MembershipType.VIP, 12)
        
        distribution = self.gym.get_membership_distribution()
        
        self.assertEqual(distribution['Basic'], 1)
        self.assertEqual(distribution['Premium'], 1)
        self.assertEqual(distribution['VIP'], 1)


if __name__ == "__main__":
    unittest.main()
