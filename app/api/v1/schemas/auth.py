from pydantic import BaseModel, EmailStr, Field


class LoginOut(BaseModel):
    access_token: str
    token_type: str


class RegisterIn(BaseModel):
    first_name: str = Field(title="First Name", description="User first name", max_length=50)
    last_name: str = Field(title="Last Name", description="User last name", max_length=50)
    email: EmailStr = Field(title="E-Mail", description="User e-mail")
    password: str = Field(title="Password", description="User password", min_length=6)


class PasswordResetIn(BaseModel):
    email: EmailStr = Field(title="E-Mail", description="Email address of requesting password reset")
    code: str = Field(title="Verification Code", description="Email verification code")
    password: str = Field(title="New Password", description="The new password you want to use")


class EmailVerificationIn(BaseModel):
    email: EmailStr = Field("E-Mail", description="The e-mail address to be activated")
    code: str = Field(title="Verification Code", description="Email verification code")
