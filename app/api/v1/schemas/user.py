from datetime import datetime

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserDetailOut(BaseModel):
    first_name: str = Field(title="First Name", description="User first name", max_length=50)
    last_name: str = Field(title="Last Name", description="User last name", max_length=50)
    email: EmailStr = Field(title="E-Mail", description="User e-mail")
    email_verification: bool = Field(title="User e-mail verification status")
    email_verification_date: Optional[datetime] = Field(title="E-Mail Verification Date", description="Date of verification of the user's current email address")

