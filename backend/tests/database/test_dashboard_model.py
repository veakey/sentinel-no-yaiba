"""
Tests for Dashboard model
"""
import pytest
from app.database.models import Dashboard, User, UserRole
from app.auth.password import hash_password


def test_dashboard_creation(db_session):
    """Test creating a dashboard"""
    # Create user first
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.CLIENT.value
    )
    db_session.add(user)
    db_session.commit()
    
    # Create dashboard
    config = {
        "widgets": ["threats", "stats"],
        "layout": "grid"
    }
    
    dashboard = Dashboard(
        user_id=user.id,
        name="My Dashboard",
        description="Test dashboard",
        config=config,
        is_default=False
    )
    
    db_session.add(dashboard)
    db_session.commit()
    
    assert dashboard.id is not None
    assert dashboard.guid is not None
    assert dashboard.user_id == user.id
    assert dashboard.name == "My Dashboard"
    assert dashboard.description == "Test dashboard"
    assert dashboard.config == config
    assert dashboard.is_default is False
    assert dashboard.created_at is not None
    assert dashboard.updated_at is not None


def test_dashboard_default_is_default(db_session):
    """Test that is_default defaults to False"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.CLIENT.value
    )
    db_session.add(user)
    db_session.commit()
    
    dashboard = Dashboard(
        user_id=user.id,
        name="Dashboard",
        config={}
    )
    
    db_session.add(dashboard)
    db_session.commit()
    
    assert dashboard.is_default is False


def test_dashboard_relationship_user(db_session):
    """Test Dashboard relationship with User"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.CLIENT.value
    )
    db_session.add(user)
    db_session.commit()
    
    dashboard1 = Dashboard(
        user_id=user.id,
        name="Dashboard 1",
        config={"widgets": []}
    )
    
    dashboard2 = Dashboard(
        user_id=user.id,
        name="Dashboard 2",
        config={"widgets": []}
    )
    
    db_session.add_all([dashboard1, dashboard2])
    db_session.commit()
    
    # Test relationship
    assert len(user.dashboards) == 2
    assert dashboard1.user.id == user.id
    assert dashboard2.user.id == user.id
    assert dashboard1.user.username == "testuser"


def test_dashboard_with_complex_config(db_session):
    """Test dashboard with complex JSON config"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.CLIENT.value
    )
    db_session.add(user)
    db_session.commit()
    
    config = {
        "layout": {
            "type": "grid",
            "columns": 3,
            "rows": 2
        },
        "widgets": [
            {
                "id": "widget-1",
                "type": "threats",
                "position": {"x": 0, "y": 0},
                "size": {"width": 2, "height": 1}
            },
            {
                "id": "widget-2",
                "type": "stats",
                "position": {"x": 2, "y": 0},
                "size": {"width": 1, "height": 1}
            }
        ],
        "filters": {
            "severity": ["high", "critical"],
            "status": ["active"]
        }
    }
    
    dashboard = Dashboard(
        user_id=user.id,
        name="Complex Dashboard",
        config=config
    )
    
    db_session.add(dashboard)
    db_session.commit()
    
    assert dashboard.config == config
    assert len(dashboard.config["widgets"]) == 2
    assert dashboard.config["layout"]["columns"] == 3


def test_dashboard_unique_guid(db_session):
    """Test that each dashboard has a unique GUID"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.CLIENT.value
    )
    db_session.add(user)
    db_session.commit()
    
    dashboard1 = Dashboard(
        user_id=user.id,
        name="Dashboard 1",
        config={}
    )
    
    dashboard2 = Dashboard(
        user_id=user.id,
        name="Dashboard 2",
        config={}
    )
    
    db_session.add_all([dashboard1, dashboard2])
    db_session.commit()
    
    assert dashboard1.guid != dashboard2.guid
    assert len(dashboard1.guid) == 36  # UUID format


def test_dashboard_cascade_delete_on_user(db_session):
    """Test that deleting a user cascades to dashboards"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.CLIENT.value
    )
    db_session.add(user)
    db_session.commit()
    
    dashboard1 = Dashboard(
        user_id=user.id,
        name="Dashboard 1",
        config={}
    )
    
    dashboard2 = Dashboard(
        user_id=user.id,
        name="Dashboard 2",
        config={}
    )
    
    db_session.add_all([dashboard1, dashboard2])
    db_session.commit()
    
    # Delete user
    db_session.delete(user)
    db_session.commit()
    
    # Verify dashboards are deleted
    assert db_session.query(Dashboard).count() == 0


def test_dashboard_multiple_users(db_session):
    """Test that multiple users can have their own dashboards"""
    user1 = User(
        username="user1",
        email="user1@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.CLIENT.value
    )
    
    user2 = User(
        username="user2",
        email="user2@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.CLIENT.value
    )
    
    db_session.add_all([user1, user2])
    db_session.commit()
    
    dashboard1 = Dashboard(
        user_id=user1.id,
        name="User1 Dashboard",
        config={}
    )
    
    dashboard2 = Dashboard(
        user_id=user2.id,
        name="User2 Dashboard",
        config={}
    )
    
    db_session.add_all([dashboard1, dashboard2])
    db_session.commit()
    
    assert len(user1.dashboards) == 1
    assert len(user2.dashboards) == 1
    assert user1.dashboards[0].name == "User1 Dashboard"
    assert user2.dashboards[0].name == "User2 Dashboard"

