import pytest
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import verify_password
from app.models.user import User

def test_superadmin_password_consistency():
    """Ensure the password used by the tests matches the stored superadmin hash.
    This guarantees that login attempts will succeed.
    """
    # Open a session (same DB used by init_db)
    db: Session = SessionLocal()
    try:
        superadmin = db.query(User).filter(User.email == settings.FIRST_SUPERADMIN_EMAIL).first()
        assert superadmin is not None, "Superadmin user should exist"
        # Verify the password configured in Settings matches the stored hash
        assert verify_password(settings.FIRST_SUPERADMIN_PASSWORD, superadmin.password_hash)
    finally:
        db.close()
