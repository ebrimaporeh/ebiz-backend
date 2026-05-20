# apps/core/seed_data/users.py
from django.contrib.auth.hashers import make_password

USERS = [
    {
        "email": "admin@e-biz.gm",
        "password": "Admin@123",
        "first_name": "Ebrima",
        "last_name": "Barry",
        "is_staff": True,
        "is_superuser": True,
        "is_active": True,
        "tier": "premium"
    },
    {
        "email": "researcher@e-biz.gm",
        "first_name": "Fatou",
        "last_name": "Jallow",
        "is_staff": True,
        "is_active": True,
        "tier": "premium"
    },
    {
        "email": "demo@e-biz.gm",
        "first_name": "Demo",
        "last_name": "User",
        "is_active": True,
        "tier": "regular"
    },
    {
        "email": "premium@e-biz.gm",
        "first_name": "Premium",
        "last_name": "User",
        "is_active": True,
        "tier": "premium",
        "tier_expires_at": "2025-12-31"
    }
]

# Regular users for testing
REGULAR_USERS = [
    {"email": f"user{i}@example.com", "first_name": f"User{i}", "last_name": "Test"}
    for i in range(1, 11)
]

PROFILES = [
    {
        "user_email": "demo@e-biz.gm",
        "linkedin_url": "https://linkedin.com/in/demo",
        "twitter_handle": "demouser",
        "newsletter_subscribed": True
    },
    {
        "user_email": "premium@e-biz.gm",
        "linkedin_url": "https://linkedin.com/in/premium",
        "newsletter_subscribed": True
    }
]