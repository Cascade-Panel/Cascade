""" The User model. """

import datetime
import uuid
import pyotp
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy_utils import EncryptedType, StringEncryptedType, UUIDType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from core.database import Base

def fetch_encryption_key() -> str:
    pass

def gen_uuid() -> uuid:
    return uuid.uuid4()

class User(Base):
    """
        The User model.

        Attributes:
            uuid (UUID): The UUID of the user.
            username (String): The username of the user.
            email (Encrypted[String]): The email of the user.
            password (String): The password of the user.
            first_name (Encrypted[String]): The first name of the user.
            last_name (Encrypted[String]): The last name of the user.
            address (Encrypted[String]): The address of the user.
            postcode (Encrypted[String]): The postcode of the user.
            avatar (Encrypted[String]): The avatar of the user.
            staff_level (Integer): The staff level of the user.
            email_verification_code (Encrypted[UUID]): The email verification code of the user.
            mfa_secret (Encrypted[String]): The MFA secret of the user.
            created_at (Encrypted[DateTime]): The date the users account was created.
            last_login (Encrypted[DateTime]): The date the user last logged in.
            last_failed_login (Encrypted[DateTime]): The date the user last failed to login.
            failed_login_attempts (Encrypted[Integer]): The number of failed login attempts.
            signup_ip (Encrypted[String]): The IP the user signed up with.
            last_login_ip (Encrypted[String]): The IP the user last logged in with.
            last_failed_login_ip (Encrypted[String]): The IP the user last failed to login with.
            max_sessions (Integer): The maximum number of sessions the user can have.
            is_root_admin (Boolean): True if the user is a root admin, False otherwise.
            is_mfa_enabled (Boolean): True if the user has MFA enabled, False otherwise.
            is_email_verified (Boolean): True if the user has verified their email, False otherwise.
    """
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUIDType(binary=False), nullable=False, default=gen_uuid())
    username = Column(String, nullable=False) # Value not required to be unique - just for UI purposes

    email = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False, unique=True)
    
    password = Column(String, nullable=False)

    ## Personal Information
    first_name = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False)
    last_name = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False)

    address = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False)

    postcode = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False)

    avatar = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False)
    ## End Personal Information

    # Staff Level: The level of staff privileges the user has
    staff_level = Column(Integer, nullable=True, default=False)

    # Email verification code: The code used to verify the email
    email_verification_code = Column(EncryptedType(
        UUIDType(binary=False), fetch_encryption_key(), AesEngine
    ), nullable=False, default=gen_uuid())

    # OTP Secret: The secret used to generate the OTP
    mfa_secret = Column(EncryptedType(
        String, fetch_encryption_key(), AesEngine
    ), nullable=False, default=pyotp.random_base32())

    # Login information: The login information of the user
    created_at = Column(
        EncryptedType(DateTime(timezone=True), fetch_encryption_key(), AesEngine
    ), nullable=False, default=datetime.datetime.now())

    last_login = Column(
        EncryptedType(DateTime(timezone=True), fetch_encryption_key(), AesEngine
    ), nullable=False, default=datetime.datetime.now())

    last_failed_login = Column(
        StringEncryptedType(DateTime(timezone=True), fetch_encryption_key(), AesEngine
    ), nullable=True, default=None)

    failed_login_attempts = Column(
        EncryptedType(Integer, fetch_encryption_key(), AesEngine
    ), nullable=False, default=0)

    # IP information: The information of the user
    signup_ip = Column(
        EncryptedType(String(225), fetch_encryption_key(), AesEngine
    ), nullable=False)

    last_login_ip = Column(
        EncryptedType(String(225), fetch_encryption_key(), AesEngine
    ), nullable=False)

    last_failed_login_ip = Column(
        EncryptedType(String(225), fetch_encryption_key(), AesEngine
    ), nullable=True, default=None)

    # Sessions: The sessions of the user
    max_sessions = Column(Integer, nullable=False, default=5)

    # User Config: True if the user has enabled, False
    is_root_admin = Column(Boolean, nullable=False, default=False)
    is_mfa_enabled = Column(Boolean, nullable=False, default=False)
    is_email_verified = Column(Boolean, nullable=False, default=True)
