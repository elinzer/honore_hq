# Honore HQ

A private home management app for tracking repairs and tasks across household units.

## Features

- Multi-household support with role-based access (Admin/Member)
- Repair/task tracking with status workflow (Open → In Progress → Done)
- Unit-based organization (apartments, common areas, exterior)
- All members can create tasks; edit your own or (admins) anyone's

## Requirements

- Python 3.10+
- Django 6.0+

## Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/honore_hq.git
cd honore_hq

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a user and household
python manage.py createuser yourname yourpassword --household "My House" --admin

# Run the server
python manage.py runserver
```

Visit http://127.0.0.1:8000 and log in.

## Creating Users

```bash
# Create admin user with new household
python manage.py createuser admin adminpass --household "My House" --admin

# Create regular member
python manage.py createuser guest guestpass --household "My House"
```

## Project Structure

```
honore_hq/
├── households/     # Users, households, memberships, permissions
├── locations/      # Units (apartments, common areas)
├── work/           # Tasks/repairs
└── templates/      # Base templates
```

## Environment Variables

For production, set:

```bash
SECRET_KEY=your-secret-key-here
```

Generate a key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## License

MIT
