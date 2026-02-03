# Gym Management System - Quick Start Guide

## Get Started in 3 Steps

### Step 1: Run the Example Demo
```bash
python3 example_usage.py
```

This will:
- Register 3 sample members
- Create different membership types (Basic, Premium, VIP)
- Demonstrate check-in/check-out
- Process a payment
- Show dashboard statistics

### Step 2: Run the Interactive CLI
```bash
python3 gym_cli.py
```

This provides a menu-driven interface to:
- Register new members
- Create memberships
- Track attendance
- Manage payments
- View reports

### Step 3: Run the Tests
```bash
python3 -m unittest test_gym_system.py -v
```

This verifies all functionality is working correctly.

## Quick Code Example

```python
from datetime import datetime
from gym_management.gym_system import GymManagementSystem
from gym_management.models import MembershipType

# Initialize
gym = GymManagementSystem()

# Register a member
member = gym.register_member(
    name="John Doe",
    email="john@example.com",
    phone="555-0101",
    address="123 Main St",
    date_of_birth=datetime(1990, 5, 15)
)

# Create membership
membership = gym.create_membership(
    member_id=member.member_id,
    membership_type=MembershipType.PREMIUM,
    duration_months=6
)

# Check in
attendance = gym.check_in(member.member_id)
print(f"Checked in at {attendance.check_in_time}")

# Check out
checkout = gym.check_out(member.member_id)
print(f"Session duration: {checkout.duration_minutes()} minutes")
```

## Next Steps

- Read the full documentation in `GYM_SYSTEM_DOCS.md`
- Explore the code in `gym_management/` directory
- Customize the system for your needs
- Build a web interface (optional)

## Need Help?

- Check `GYM_SYSTEM_DOCS.md` for detailed documentation
- Review `example_usage.py` for code examples
- Look at `test_gym_system.py` for usage patterns
- Contact: santhoshsaravanan846@gmail.com
