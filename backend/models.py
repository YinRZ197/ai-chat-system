from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.types import Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    create_time = Column(DateTime, default=datetime.now)

class ModelInfo(Base):
    __tablename__ = "model_info"
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    model_type = Column(String(20), nullable=False) # local / remote
    system_prompt = Column(Text, nullable=True)
    model_path = Column(String(200), nullable=True)
    create_time = Column(DateTime, default=datetime.now)

    keys = relationship("ModelKey", back_populates="model")

class ModelKey(Base):
    __tablename__ = "model_key"
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("model_info.id"), nullable=False)
    api_key = Column(String(255), nullable=False)
    is_enable = Column(Boolean, default=True)

    model = relationship("ModelInfo", back_populates="keys")

class Conversation(Base):
    __tablename__ = "conversation"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("model_info.id"), nullable=False)
    title = Column(String(100), nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    messages = relationship("ChatMessage", back_populates="conversation")

class ChatMessage(Base):
    __tablename__ = "chat_message"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversation.id"), nullable=False)
    role = Column(String(20), nullable=False) # user / assistant
    content = Column(Text, nullable=False)
    create_time = Column(DateTime, default=datetime.now)

    conversation = relationship("Conversation", back_populates="messages")
