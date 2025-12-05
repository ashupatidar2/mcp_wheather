"""
User model for authentication
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    """
    User model for storing user information
    
    Fields:
    - id: Primary key
    - email: Unique email address
    - hashed_password: Bcrypt hashed password (never store plaintext!)
    - is_active: Whether user account is active
    - created_at: Timestamp when user was created
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<User {self.email}>"
