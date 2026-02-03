#!/usr/bin/env python3
"""
Example usage of the Gym Management System
Demonstrates all major features
"""

from datetime import datetime, timedelta
from gym_management.gym_system import GymManagementSystem
from gym_management.models import MembershipType


def main():
    print("=" * 70)
    print(" " * 20 + "GYM MANAGEMENT SYSTEM DEMO")
    print("=" * 70)
    
    # Initialize the system
    gym = GymManagementSystem(data_dir="demo_gym_data")
    
    # 1. Register Members
    print("\n1. REGISTERING MEMBERS")
    print("-" * 70)
    
    member1 = gym.register_member(
        name="John Doe",
        email="john.doe@example.com",
        phone="555-0101",
        address="123 Main St, City",
        date_of_birth=datetime(1990, 5, 15)
    )
    print(f"✓ Registered: {member1.name} (ID: {member1.member_id})")
    
    member2 = gym.register_member(
        name="Jane Smith",
        email="jane.smith@example.com",
        phone="555-0102",
        address="456 Oak Ave, City",
        date_of_birth=datetime(1988, 8, 22)
    )
    print(f"✓ Registered: {member2.name} (ID: {member2.member_id})")
    
    member3 = gym.register_member(
        name="Bob Johnson",
        email="bob.johnson@example.com",
        phone="555-0103",
        address="789 Pine Rd, City",
        date_of_birth=datetime(1995, 3, 10)
    )
    print(f"✓ Registered: {member3.name} (ID: {member3.member_id})")
    
    # 2. Create Memberships
    print("\n2. CREATING MEMBERSHIPS")
    print("-" * 70)
    
    membership1 = gym.create_membership(
        member_id=member1.member_id,
        membership_type=MembershipType.PREMIUM,
        duration_months=6
    )
    print(f"✓ Created {membership1.membership_type.value} membership for {member1.name}")
    print(f"  Duration: 6 months, Total: ${membership1.monthly_fee * 6:.2f}")
    
    membership2 = gym.create_membership(
        member_id=member2.member_id,
        membership_type=MembershipType.VIP,
        duration_months=12
    )
    print(f"✓ Created {membership2.membership_type.value} membership for {member2.name}")
    print(f"  Duration: 12 months, Total: ${membership2.monthly_fee * 12:.2f}")
    
    membership3 = gym.create_membership(
        member_id=member3.member_id,
        membership_type=MembershipType.BASIC,
        duration_months=3
    )
    print(f"✓ Created {membership3.membership_type.value} membership for {member3.name}")
    print(f"  Duration: 3 months, Total: ${membership3.monthly_fee * 3:.2f}")
    
    # 3. Check Membership Status
    print("\n3. CHECKING MEMBERSHIP STATUS")
    print("-" * 70)
    
    for member_id in [member1.member_id, member2.member_id, member3.member_id]:
        status = gym.check_membership_status(member_id)
        member = gym.get_member(member_id)
        print(f"✓ {member.name}:")
        print(f"  Type: {status.get('membership_type', 'N/A')}")
        print(f"  Active: {status['is_active']}")
        print(f"  Days Remaining: {status.get('days_remaining', 0)}")
    
    # 4. Attendance Tracking
    print("\n4. ATTENDANCE TRACKING")
    print("-" * 70)
    
    # Check in members
    attendance1 = gym.check_in(member1.member_id)
    print(f"✓ {member1.name} checked in at {attendance1.check_in_time.strftime('%H:%M:%S')}")
    
    attendance2 = gym.check_in(member2.member_id)
    print(f"✓ {member2.name} checked in at {attendance2.check_in_time.strftime('%H:%M:%S')}")
    
    # Simulate some time passing and check out
    import time
    time.sleep(2)
    
    checkout1 = gym.check_out(member1.member_id)
    if checkout1:
        print(f"✓ {member1.name} checked out at {checkout1.check_out_time.strftime('%H:%M:%S')}")
        print(f"  Session duration: {checkout1.duration_minutes()} minutes")
    
    # 5. Payment Processing
    print("\n5. PAYMENT PROCESSING")
    print("-" * 70)
    
    # Get pending payments
    pending_payments = gym.get_pending_payments()
    print(f"Pending Payments: {len(pending_payments)}")
    
    # Process first payment
    if pending_payments:
        payment = pending_payments[0]
        member = gym.get_member(payment.member_id)
        print(f"\n✓ Processing payment for {member.name}")
        print(f"  Amount: ${payment.amount:.2f}")
        
        # Simulate payment processing
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}"
        gym.process_payment(payment.payment_id, transaction_id)
        print(f"  Transaction ID: {transaction_id}")
        print(f"  Status: PAID")
    
    # 6. Dashboard Summary
    print("\n6. DASHBOARD SUMMARY")
    print("-" * 70)
    
    total_members = gym.get_total_members()
    active_members = gym.get_active_members()
    total_revenue = gym.get_total_revenue()
    pending_revenue = gym.get_pending_revenue()
    
    print(f"Total Members: {total_members}")
    print(f"Active Members: {active_members}")
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Pending Revenue: ${pending_revenue:.2f}")
    
    # 7. Membership Distribution
    print("\n7. MEMBERSHIP DISTRIBUTION")
    print("-" * 70)
    
    distribution = gym.get_membership_distribution()
    print(f"Basic: {distribution['Basic']}")
    print(f"Premium: {distribution['Premium']}")
    print(f"VIP: {distribution['VIP']}")
    
    # 8. View All Members
    print("\n8. ALL MEMBERS")
    print("-" * 70)
    
    all_members = gym.get_all_members()
    for member in all_members:
        print(f"✓ {member.name} ({member.member_id})")
        print(f"  Email: {member.email}")
        print(f"  Status: {'Active' if member.is_active else 'Inactive'}")
        if member.membership:
            print(f"  Membership: {member.membership.membership_type.value}")
    
    print("\n" + "=" * 70)
    print(" " * 25 + "DEMO COMPLETED")
    print("=" * 70)
    print(f"\nData saved to: demo_gym_data/")


if __name__ == "__main__":
    main()
