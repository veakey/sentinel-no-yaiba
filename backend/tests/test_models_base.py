"""
Tests for BaseModel with GUID generation
"""
import pytest
import uuid
from datetime import datetime
from sqlalchemy import Column, String

from app.database.base import BaseModel


class TestModel(BaseModel):
    """Test model for testing BaseModel"""
    __tablename__ = "test_models"
    
    name = Column(String(100))


def test_base_model_guid_generation(db_session):
    """Test that GUID is automatically generated"""
    # Create tables
    BaseModel.metadata.create_all(bind=db_session.bind)
    
    test_model = TestModel(name="test")
    db_session.add(test_model)
    db_session.commit()
    db_session.refresh(test_model)
    
    # GUID should be generated
    assert test_model.guid is not None
    assert len(test_model.guid) == 36  # UUID format length
    assert test_model.guid.count('-') == 4  # UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    
    # Verify it's a valid UUID
    try:
        uuid.UUID(test_model.guid)
    except ValueError:
        pytest.fail("GUID is not a valid UUID")


def test_base_model_timestamps(db_session):
    """Test that created_at and updated_at are automatically set"""
    BaseModel.metadata.create_all(bind=db_session.bind)
    
    test_model = TestModel(name="test_timestamps")
    db_session.add(test_model)
    db_session.commit()
    db_session.refresh(test_model)
    
    # Timestamps should be set
    assert test_model.created_at is not None
    assert test_model.updated_at is not None
    assert isinstance(test_model.created_at, datetime)
    assert isinstance(test_model.updated_at, datetime)


def test_base_model_unique_guid(db_session):
    """Test that each model instance gets a unique GUID"""
    BaseModel.metadata.create_all(bind=db_session.bind)
    
    model1 = TestModel(name="test1")
    model2 = TestModel(name="test2")
    
    db_session.add(model1)
    db_session.add(model2)
    db_session.commit()
    
    # Each should have a unique GUID
    assert model1.guid != model2.guid


def test_base_model_has_id_and_guid(db_session):
    """Test that model has both id (DB) and guid (external)"""
    BaseModel.metadata.create_all(bind=db_session.bind)
    
    test_model = TestModel(name="test_id_guid")
    db_session.add(test_model)
    db_session.commit()
    db_session.refresh(test_model)
    
    # Should have both id and guid
    assert test_model.id is not None
    assert test_model.guid is not None
    # ID is integer, GUID is string
    assert isinstance(test_model.id, int)
    assert isinstance(test_model.guid, str)

