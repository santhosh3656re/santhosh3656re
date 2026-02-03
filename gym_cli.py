#!/usr/bin/env python3
"""
Command-line interface for the Gym Management System
"""

import sys
from datetime import datetime
from gym_management.gym_system import GymManagementSystem
from gym_management.models import MembershipType


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_menu():
    """Print the main menu"""
    print_header("GYM MANAGEMENT SYSTEM")
    print("\n1. Member Management")
    print("   1.1. Register New Member")
    print("   1.2. View All Members")
    print("   1.3. View Member Details")
    print("   1.4. Deactivate Member")
    print("\n2. Membership Management")
    print("   2.1. Create Membership")
    print("   2.2. Check Membership Status")
    print("\n3. Attendance Management")
    print("   3.1. Check In")
    print("   3.2. Check Out")
    print("   3.3. View Attendance History")
    print("\n4. Payment Management")
    print("   4.1. Process Payment")
    print("   4.2. View Member Payments")
    print("   4.3. View Pending Payments")
    print("\n5. Reports")
    print("   5.1. Dashboard Summary")
    print("   5.2. Membership Distribution")
    print("\n0. Exit")
    print("\n" + "-" * 60)


def register_member(gym):
    """Register a new member"""
    print_header("Register New Member")
    name = input("Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    address = input("Address: ")
    dob_str = input("Date of Birth (YYYY-MM-DD): ")
    
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        member = gym.register_member(name, email, phone, address, dob)
        print(f"\n✓ Member registered successfully!")
        print(f"  Member ID: {member.member_id}")
        print(f"  Name: {member.name}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def view_all_members(gym):
    """View all members"""
    print_header("All Members")
    members = gym.get_all_members()
    
    if not members:
        print("\nNo members found.")
        return
    
    print(f"\nTotal Members: {len(members)}\n")
    print(f"{'ID':<15} {'Name':<25} {'Email':<30} {'Status':<10}")
    print("-" * 80)
    
    for member in members:
        status = "Active" if member.is_active else "Inactive"
        print(f"{member.member_id:<15} {member.name:<25} {member.email:<30} {status:<10}")


def view_member_details(gym):
    """View member details"""
    print_header("View Member Details")
    member_id = input("Member ID: ")
    
    member = gym.get_member(member_id)
    if not member:
        print("\n✗ Member not found.")
        return
    
    print(f"\nMember Details:")
    print(f"  ID: {member.member_id}")
    print(f"  Name: {member.name}")
    print(f"  Email: {member.email}")
    print(f"  Phone: {member.phone}")
    print(f"  Address: {member.address}")
    print(f"  Date of Birth: {member.date_of_birth.strftime('%Y-%m-%d')}")
    print(f"  Join Date: {member.join_date.strftime('%Y-%m-%d')}")
    print(f"  Status: {'Active' if member.is_active else 'Inactive'}")
    
    if member.membership:
        print(f"\n  Membership:")
        print(f"    Type: {member.membership.membership_type.value}")
        print(f"    Status: {'Expired' if member.membership.is_expired() else 'Active'}")
        print(f"    Days Remaining: {member.membership.days_remaining()}")


def create_membership(gym):
    """Create a membership"""
    print_header("Create Membership")
    member_id = input("Member ID: ")
    
    member = gym.get_member(member_id)
    if not member:
        print("\n✗ Member not found.")
        return
    
    print("\nMembership Types:")
    print("  1. Basic - $29.99/month")
    print("  2. Premium - $49.99/month")
    print("  3. VIP - $99.99/month")
    
    type_choice = input("\nSelect membership type (1-3): ")
    duration = int(input("Duration (months): "))
    
    membership_types = {
        "1": MembershipType.BASIC,
        "2": MembershipType.PREMIUM,
        "3": MembershipType.VIP
    }
    
    if type_choice not in membership_types:
        print("\n✗ Invalid membership type.")
        return
    
    try:
        membership = gym.create_membership(
            member_id,
            membership_types[type_choice],
            duration
        )
        print(f"\n✓ Membership created successfully!")
        print(f"  Membership ID: {membership.membership_id}")
        print(f"  Type: {membership.membership_type.value}")
        print(f"  Monthly Fee: ${membership.monthly_fee}")
        print(f"  Duration: {duration} months")
        print(f"  Total: ${membership.monthly_fee * duration}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def check_in(gym):
    """Check in a member"""
    print_header("Check In")
    member_id = input("Member ID: ")
    
    try:
        attendance = gym.check_in(member_id)
        print(f"\n✓ Check-in successful!")
        print(f"  Member ID: {member_id}")
        print(f"  Check-in Time: {attendance.check_in_time.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def check_out(gym):
    """Check out a member"""
    print_header("Check Out")
    member_id = input("Member ID: ")
    
    attendance = gym.check_out(member_id)
    if attendance:
        print(f"\n✓ Check-out successful!")
        print(f"  Member ID: {member_id}")
        print(f"  Check-out Time: {attendance.check_out_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Duration: {attendance.duration_minutes()} minutes")
    else:
        print("\n✗ No active check-in found for this member.")


def dashboard_summary(gym):
    """Display dashboard summary"""
    print_header("Dashboard Summary")
    
    total_members = gym.get_total_members()
    active_members = gym.get_active_members()
    total_revenue = gym.get_total_revenue()
    pending_revenue = gym.get_pending_revenue()
    
    print(f"\n  Total Members: {total_members}")
    print(f"  Active Members: {active_members}")
    print(f"  Total Revenue: ${total_revenue:.2f}")
    print(f"  Pending Revenue: ${pending_revenue:.2f}")


def membership_distribution(gym):
    """Display membership distribution"""
    print_header("Membership Distribution")
    
    distribution = gym.get_membership_distribution()
    
    print(f"\n  Basic: {distribution['Basic']}")
    print(f"  Premium: {distribution['Premium']}")
    print(f"  VIP: {distribution['VIP']}")


def main():
    """Main function"""
    gym = GymManagementSystem()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1.1":
            register_member(gym)
        elif choice == "1.2":
            view_all_members(gym)
        elif choice == "1.3":
            view_member_details(gym)
        elif choice == "2.1":
            create_membership(gym)
        elif choice == "3.1":
            check_in(gym)
        elif choice == "3.2":
            check_out(gym)
        elif choice == "5.1":
            dashboard_summary(gym)
        elif choice == "5.2":
            membership_distribution(gym)
        elif choice == "0":
            print("\nThank you for using Gym Management System!")
            sys.exit(0)
        else:
            print("\n✗ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
