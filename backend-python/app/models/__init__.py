# 导入所有模型以确保它们被注册到SQLAlchemy
from .user import User
from .patient import Patient
from .report import Report
from .followup import FollowupRecord
from .followup_response import FollowupResponse

__all__ = [
    "User",
    "Patient", 
    "Report",
    "FollowupRecord",
    "FollowupResponse"
]