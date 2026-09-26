"""SQLAlchemy models.

Import all models here so Alembic can discover them.
"""

from app.models.activity import LeadActivity
from app.models.conversation import Conversation
from app.models.customer import Customer
from app.models.follow_up import FollowUp
from app.models.lead import Lead
from app.models.message import Message
from app.models.notification import Notification
from app.models.user import User

__all__ = [
    "Customer",
    "Lead",
    "Conversation",
    "Message",
    "LeadActivity",
    "FollowUp",
    "User",
    "Notification",
]
