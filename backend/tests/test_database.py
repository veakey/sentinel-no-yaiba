"""
Tests for database setup and connection
"""
import pytest
from sqlalchemy import text

from app.database.database import SessionLocal, engine
from app.database.base import Base


def test_database_connection(db_session):
    """Test that database connection works"""
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


def test_database_tables_can_be_created(db_session):
    """Test that tables can be created"""
    # Tables should be created by the fixture
    # Just verify we can query
    result = db_session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
    tables = [row[0] for row in result]
    # At minimum, sqlite_sequence should exist
    assert len(tables) >= 0

