# Gym Management System

A comprehensive Python-based gym management system for managing members, memberships, attendance tracking, and billing.

## Features

### 1. Member Management
- Register new gym members with complete profile information
- View all members or specific member details
- Update member information
- Deactivate members
- Track member join dates and status

### 2. Membership Plans
- Three membership tiers:
  - **Basic**: $29.99/month - Essential gym access
  - **Premium**: $49.99/month - Extended features and benefits
  - **VIP**: $99.99/month - Premium access with all amenities
- Flexible duration (1-12 months)
- Automatic expiration tracking
- Days remaining calculation

### 3. Attendance Tracking
- Check-in/check-out system
- Automatic timestamp recording
- Session duration calculation
- Complete attendance history
- Membership validation on check-in

### 4. Payment & Billing
- Automated payment generation on membership creation
- Payment status tracking (Pending/Paid/Overdue)
- Transaction ID management
- Revenue reporting (total and pending)
- Member payment history

### 5. Reports & Analytics
- Dashboard summary with key metrics
- Total and active member counts
- Revenue tracking
- Membership distribution by type
- Financial overview

## Installation

### Prerequisites
- Python 3.7 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/santhosh3656re/santhosh3656re.git
cd santhosh3656re
```

2. The system uses only Python standard library, so no additional packages are required.

## Usage

### Command-Line Interface

Run the interactive CLI:

```bash
python3 gym_cli.py
```

The CLI provides a menu-driven interface for all gym management operations:

```
============================================================
  GYM MANAGEMENT SYSTEM
============================================================

1. Member Management
   1.1. Register New Member
   1.2. View All Members
   1.3. View Member Details
   1.4. Deactivate Member

2. Membership Management
   2.1. Create Membership
   2.2. Check Membership Status

3. Attendance Management
   3.1. Check In
   3.2. Check Out
   3.3. View Attendance History

4. Payment Management
   4.1. Process Payment
   4.2. View Member Payments
   4.3. View Pending Payments

5. Reports
   5.1. Dashboard Summary
   5.2. Membership Distribution

0. Exit
```

### Example Usage (Programmatic)

Run the example demonstration:

```bash
python3 example_usage.py
```

Or use the system in your own code:

```python
from datetime import datetime
from gym_management.gym_system import GymManagementSystem
from gym_management.models import MembershipType

# Initialize the system
gym = GymManagementSystem()

# Register a new member
member = gym.register_member(
    name="John Doe",
    email="john.doe@example.com",
    phone="555-0101",
    address="123 Main St",
    date_of_birth=datetime(1990, 5, 15)
)

# Create a membership
membership = gym.create_membership(
    member_id=member.member_id,
    membership_type=MembershipType.PREMIUM,
    duration_months=6
)

# Check in member
attendance = gym.check_in(member.member_id)

# Check out member
checkout = gym.check_out(member.member_id)

# Process payment
payments = gym.get_member_payments(member.member_id)
gym.process_payment(payments[0].payment_id, "TXN123456")

# Get dashboard statistics
total_members = gym.get_total_members()
total_revenue = gym.get_total_revenue()
```

## Project Structure

```
santhosh3656re/
│
├── gym_management/           # Main package
│   ├── __init__.py          # Package initialization
│   ├── models.py            # Data models (Member, Membership, etc.)
│   ├── database.py          # Database operations and persistence
│   └── gym_system.py        # Main system logic
│
├── gym_cli.py               # Command-line interface
├── example_usage.py         # Example usage demonstration
├── test_gym_system.py       # Unit tests
├── GYM_SYSTEM_DOCS.md       # This documentation
└── gym_data/                # Data storage directory (auto-created)
    ├── members.json
    ├── memberships.json
    ├── attendances.json
    └── payments.json
```

## Data Models

### Member
- `member_id`: Unique identifier
- `name`: Full name
- `email`: Email address
- `phone`: Phone number
- `address`: Physical address
- `date_of_birth`: Date of birth
- `join_date`: Registration date
- `is_active`: Active status

### Membership
- `membership_id`: Unique identifier
- `member_id`: Associated member
- `membership_type`: BASIC/PREMIUM/VIP
- `start_date`: Membership start date
- `end_date`: Membership end date
- `duration_months`: Duration in months
- `monthly_fee`: Monthly fee amount
- `is_active`: Active status

### Attendance
- `attendance_id`: Unique identifier
- `member_id`: Associated member
- `check_in_time`: Check-in timestamp
- `check_out_time`: Check-out timestamp
- `duration_minutes`: Session duration

### Payment
- `payment_id`: Unique identifier
- `member_id`: Associated member
- `membership_id`: Associated membership
- `amount`: Payment amount
- `payment_date`: Payment date
- `status`: PENDING/PAID/OVERDUE
- `transaction_id`: Transaction reference

## Testing

Run the unit tests:

```bash
python3 -m unittest test_gym_system.py
```

Or run with verbose output:

```bash
python3 -m unittest test_gym_system.py -v
```

The test suite includes:
- Member registration and retrieval
- Membership creation and status
- Check-in/check-out operations
- Payment processing
- Dashboard statistics
- Membership distribution

## Data Persistence

The system automatically saves data to JSON files in the `gym_data/` directory:

- `members.json`: All member records
- `memberships.json`: All membership plans
- `attendances.json`: All attendance records
- `payments.json`: All payment records

Data is automatically loaded on system startup and saved after each operation.

## API Reference

### GymManagementSystem Class

#### Member Management
- `register_member(name, email, phone, address, date_of_birth)` - Register a new member
- `get_member(member_id)` - Get member by ID
- `get_all_members()` - Get all members
- `update_member_info(member_id, **kwargs)` - Update member information
- `deactivate_member(member_id)` - Deactivate a member

#### Membership Management
- `create_membership(member_id, membership_type, duration_months)` - Create a membership
- `get_member_membership(member_id)` - Get active membership for a member
- `check_membership_status(member_id)` - Check membership status

#### Attendance Management
- `check_in(member_id)` - Check in a member
- `check_out(member_id)` - Check out a member
- `get_attendance_history(member_id, limit)` - Get attendance history

#### Payment Management
- `create_payment(member_id, membership_id, amount)` - Create a payment record
- `process_payment(payment_id, transaction_id)` - Process a payment
- `get_member_payments(member_id)` - Get all payments for a member
- `get_pending_payments()` - Get all pending payments

#### Reports & Analytics
- `get_total_members()` - Get total member count
- `get_active_members()` - Get active member count
- `get_total_revenue()` - Get total revenue
- `get_pending_revenue()` - Get pending revenue
- `get_membership_distribution()` - Get membership distribution

## Future Enhancements

Potential features for future versions:
- Web-based dashboard
- Email notifications for membership expiry
- SMS alerts for check-in/check-out
- Trainer management
- Class scheduling
- Equipment tracking
- Inventory management
- Advanced reporting with charts
- Mobile app integration
- Biometric authentication
- Payment gateway integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

**Santhosh S**
- Email: santhoshsaravanan846@gmail.com
- GitHub: [@santhosh3656re](https://github.com/santhosh3656re)
- LinkedIn: [santhosh3656](https://linkedin.com/in/santhosh3656)

## Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the author directly.
