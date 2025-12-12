"""
Encryption service for sensitive data (API keys, etc.)
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
from app.config import settings


class EncryptionService:
    """
    Service for encrypting and decrypting sensitive data.
    
    Uses Fernet (symmetric encryption) with a key derived from ENCRYPTION_KEY
    or SECRET_KEY as fallback.
    """
    
    _fernet: Fernet = None
    
    @classmethod
    def _get_fernet(cls) -> Fernet:
        """
        Get or create Fernet instance for encryption/decryption.
        
        Returns:
            Fernet instance configured with encryption key
        """
        if cls._fernet is None:
            # Use ENCRYPTION_KEY if available, otherwise fallback to SECRET_KEY
            key_source = settings.ENCRYPTION_KEY or settings.SECRET_KEY
            
            # Derive a 32-byte key from the source key using PBKDF2
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'sentinel_salt_2024',  # Fixed salt for consistency
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(key_source.encode()))
            cls._fernet = Fernet(key)
        
        return cls._fernet
    
    @classmethod
    def encrypt(cls, plaintext: str) -> str:
        """
        Encrypt a plaintext string.
        
        Args:
            plaintext: The string to encrypt
            
        Returns:
            Encrypted string (base64 encoded)
        """
        if not plaintext:
            return ""
        
        fernet = cls._get_fernet()
        encrypted = fernet.encrypt(plaintext.encode())
        return encrypted.decode()
    
    @classmethod
    def decrypt(cls, ciphertext: str) -> str:
        """
        Decrypt an encrypted string.
        
        Args:
            ciphertext: The encrypted string (base64 encoded)
            
        Returns:
            Decrypted plaintext string
            
        Raises:
            ValueError: If decryption fails (invalid key or corrupted data)
        """
        if not ciphertext:
            return ""
        
        try:
            fernet = cls._get_fernet()
            decrypted = fernet.decrypt(ciphertext.encode())
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {str(e)}")

