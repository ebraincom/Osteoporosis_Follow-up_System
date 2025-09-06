# 导入所有模型以确保它们被正确初始化
from .user import User, UserType, Gender
from .patient import Patient, RiskLevel
from .followup import FollowupRecord
from .report import Report

__all__ = [
    "User", "UserType", "Gender",
    "Patient", "RiskLevel", 
    "FollowupRecord",
    "Report"
] 