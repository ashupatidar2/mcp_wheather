"""
Authentication API routes (Signup, Login, User Profile)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from backend.database import get_db
from backend.auth_models import User
from backend.auth import hash_password, verify_password, create_access_token, get_current_user

# Create router
router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# ===== Pydantic Models for Request/Response =====

class SignupRequest(BaseModel):
    """Request model for signup"""
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "password123"
            }
        }


class LoginRequest(BaseModel):
    """Request model for login"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "password123"
            }
        }


class TokenResponse(BaseModel):
    """Response model for login"""
    access_token: str
    token_type: str = "bearer"
    email: str
    message: str


class UserResponse(BaseModel):
    """Response model for user profile"""
    id: int
    email: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response"""
    success: bool
    message: str


# ===== API Endpoints =====

@router.post("/signup", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    User Signup Endpoint
    
    Creates a new user account with email and password.
    Password is hashed using bcrypt before storing.
    
    Args:
        request: Signup request with email and password
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException 400: If email already exists
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please login instead."
        )
    
    # Hash password (NEVER store plaintext password!)
    hashed_password = hash_password(request.password)
    
    # Create new user
    new_user = User(
        email=request.email,
        hashed_password=hashed_password,
        is_active=True
    )
    
    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return MessageResponse(
        success=True,
        message=f"Account created successfully! Please login with {request.email}"
    )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    User Login Endpoint
    
    Authenticates user and returns JWT access token.
    Token expires in 1 day.
    
    Args:
        request: Login request with email and password
        db: Database session
        
    Returns:
        JWT access token
        
    Raises:
        HTTPException 401: If credentials are invalid
    """
    # Check if user exists
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please signup first"
        )
    
    # Verify password
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is inactive. Please contact support."
        )
    
    # Create JWT access token (expires in 1 day)
    access_token = create_access_token(data={"sub": user.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        email=user.email,
        message="Login successful!"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get Current User Profile (Protected Route)
    
    Returns profile of currently logged-in user.
    Requires valid JWT token in Authorization header.
    
    Args:
        current_user: Current user from JWT token
        
    Returns:
        User profile
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat()
    )


@router.post("/logout", response_model=MessageResponse)
async def logout():
    """
    Logout Endpoint
    
    Note: JWT tokens are stateless, so logout is handled on frontend
    by removing the token from localStorage.
    This endpoint is just for consistency.
    
    Returns:
        Success message
    """
    return MessageResponse(
        success=True,
        message="Logout successful! Please remove token from client."
    )
