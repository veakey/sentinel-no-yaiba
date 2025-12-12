"""
Tests for encryption service
"""
import pytest
from app.auth.encryption import EncryptionService


def test_encrypt_decrypt_roundtrip():
    """Test that encryption and decryption work correctly"""
    plaintext = "my-secret-api-key-12345"
    
    encrypted = EncryptionService.encrypt(plaintext)
    assert encrypted != plaintext
    assert len(encrypted) > 0
    
    decrypted = EncryptionService.decrypt(encrypted)
    assert decrypted == plaintext


def test_encrypt_empty_string():
    """Test encryption of empty string"""
    encrypted = EncryptionService.encrypt("")
    assert encrypted == ""
    
    decrypted = EncryptionService.decrypt("")
    assert decrypted == ""


def test_encrypt_long_string():
    """Test encryption of long string"""
    plaintext = "a" * 1000
    encrypted = EncryptionService.encrypt(plaintext)
    decrypted = EncryptionService.decrypt(encrypted)
    assert decrypted == plaintext


def test_encrypt_special_characters():
    """Test encryption with special characters"""
    plaintext = "key-with-special-chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
    encrypted = EncryptionService.encrypt(plaintext)
    decrypted = EncryptionService.decrypt(encrypted)
    assert decrypted == plaintext


def test_decrypt_invalid_data():
    """Test that decrypting invalid data raises ValueError"""
    with pytest.raises(ValueError, match="Failed to decrypt"):
        EncryptionService.decrypt("invalid-encrypted-data")


def test_encrypt_different_values():
    """Test that encrypting the same value twice produces different ciphertexts"""
    plaintext = "same-key"
    encrypted1 = EncryptionService.encrypt(plaintext)
    encrypted2 = EncryptionService.encrypt(plaintext)
    
    # Different ciphertexts (due to random IV)
    assert encrypted1 != encrypted2
    
    # But both decrypt to the same value
    assert EncryptionService.decrypt(encrypted1) == plaintext
    assert EncryptionService.decrypt(encrypted2) == plaintext

