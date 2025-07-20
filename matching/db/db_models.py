from sqlalchemy import (
    Column, BigInteger, Integer, String, Text, DateTime, Boolean,
    ForeignKey, func, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Users
class Users(Base):
    __tablename__ = "Users"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    provider_id = Column(String(100), nullable=False, unique=True)
    nickname = Column(String(200), nullable=False)
    provider_name = Column(String(100))
    profile_image_url = Column(Text)
    status = Column(String(40), default="active")
    has_completed_survey = Column(Boolean, default=False)

    # 관계 설정
    groups = relationship("UserGroups", back_populates="user")
    hobbies = relationship("SurveyHobby", back_populates="user", cascade="all, delete-orphan")
    missions = relationship("UserMissions", back_populates="user", cascade="all, delete-orphan")
    mbti_records = relationship("SurveyMBTI", back_populates="user", cascade="all, delete-orphan")
    mbti_updates = relationship("MBTIUpdates", back_populates="user", cascade="all, delete-orphan")


# Groups
class Groups(Base):
    __tablename__ = "Groups"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    invite_code = Column(String(6), unique=True, nullable=False)
    image_url = Column(Text)

    # 관계 설정
    users = relationship("UserGroups", back_populates="group")
    missions = relationship("GroupMissions", back_populates="group", cascade="all, delete-orphan")


# UserGroups
class UserGroups(Base):
    __tablename__ = "UserGroups"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    group_id = Column(BigInteger, ForeignKey("Groups.id", ondelete="CASCADE"), nullable=False)

    # 관계 매핑
    user = relationship("Users", back_populates="groups")
    group = relationship("Groups", back_populates="users")

    __table_args__ = (
        UniqueConstraint("user_id", "group_id", name="uq_user_group"),
    )


# Manittos
class Manittos(Base):
    __tablename__ = "Manittos"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    group_id = Column(BigInteger, ForeignKey("Groups.id", ondelete="CASCADE"), index=True, nullable=False)
    manittee_id = Column(BigInteger, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    manitto_id = Column(BigInteger, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    week = Column(Integer, nullable=False)


# SurVeyHobby
class SurveyHobby(Base):
    __tablename__ = "SurveyHobby"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)       
    user_id = Column(BigInteger, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False) 
    hobby_name = Column(String(100), nullable=False)                                      
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)  
    updated_at = Column(DateTime, server_default=func.current_timestamp(),
                        onupdate=func.current_timestamp(), nullable=False) 
    
    
    # 관계 매핑
    user = relationship("Users", back_populates = "hobbies")

    __table_args__ = (
        UniqueConstraint("user_id", "hobby_name", name = "uq_user_hobby"),
    )


# SurveyMBTI
class SurveyMBTI(Base):
    __tablename__ = "SurveyMBTI"
    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    # MBTI 축별 점수 (0~100 사이, 5단위로 저장되는 것으로 가정)
    ei_score = Column(Integer, nullable=False)
    sn_score = Column(Integer, nullable=False)
    tf_score = Column(Integer, nullable=False)
    jp_score = Column(Integer, nullable=False)

    mbti = Column(String(4), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, server_default=func.current_timestamp(),
                        onupdate=func.current_timestamp(), nullable=False)

    # 관계 매핑
    user = relationship("Users", back_populates="mbti_records")



# Missions
class Missions(Base):
    __tablename__ = "Missions"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    difficulty = Column(String(20))

    # 관계 매핑
    group_missions = relationship("GroupMissions", back_populates="mission", cascade="all, delete-orphan")
    user_missions = relationship("UserMissions", back_populates="missions", cascade="all, delete-orphan")



# UserMissions
class UserMissions(Base):
    __tablename__ = "UserMissions"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    group_id = Column(BigInteger, ForeignKey("Groups.id", ondelete="CASCADE"), nullable=False)
    mission_id = Column(BigInteger, ForeignKey("Missions.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), nullable=False, default="ing") 
    week = Column(Integer, nullable=False)
    assigned_date = Column(DateTime, server_default=func.current_timestamp(), nullable=False)

    # 관계 매핑
    user = relationship("Users", back_populates="missions")
    group = relationship("Groups")      
    missions = relationship("Missions", back_populates="user_missions")


    __table_args__ = (
        UniqueConstraint("user_id", "group_id", "mission_id", "week", name="uq_user_mission_week"),
    )


class GroupMissions(Base):
    __tablename__ = "GroupMissions"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    group_id = Column(BigInteger, ForeignKey("Groups.id", ondelete="CASCADE"), nullable=False)
    mission_id = Column(BigInteger, ForeignKey("Missions.id", ondelete="CASCADE"), nullable=False)
    week = Column(Integer, nullable=False)  

    # 관계 매핑
    group = relationship("Groups", back_populates="missions")
    mission = relationship("Missions", back_populates="group_missions")

    __table_args__ = (
        UniqueConstraint("group_id", "mission_id", "week", name="uq_group_mission_week"),
    )


class MBTIUpdates(Base):
    __tablename__ = "MBTIUpdates"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(BigInteger, nullable=True)  

    ei_score = Column(Integer, nullable=False)
    sn_score = Column(Integer, nullable=False)
    tf_score = Column(Integer, nullable=False)
    jp_score = Column(Integer, nullable=False)

    previous_score = Column(String(4), nullable=False)
    changed_mbti_type = Column(String(4), nullable=False)
    change_reason = Column(Text, nullable=True)
    current_score = Column(String(4), nullable=False)

    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)

    user = relationship("Users")