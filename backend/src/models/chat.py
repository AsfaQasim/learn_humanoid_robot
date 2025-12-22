from sqlalchemy import create_engine, Column, String, DateTime, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

DATABASE_URL = "postgresql://user:password@host:port/database"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)

class UserQuery(Base):
    __tablename__ = "user_queries"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String)
    query_text = Column(String)
    selected_text = Column(String, nullable=True)
    timestamp = Column(DateTime)

class ChatbotResponse(Base):
    __tablename__ = "chatbot_responses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query_id = Column(String)
    response_text = Column(String)
    sources = Column(JSON)
    timestamp = Column(DateTime)
    user_feedback = Column(Integer, nullable=True)
