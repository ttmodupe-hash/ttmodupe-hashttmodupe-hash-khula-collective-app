"""
Database Helper - Supports both SQLite and Supabase
Automatically switches based on environment configuration
"""

import os
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Check if running with Supabase
USE_SUPABASE = "supabase" in st.secrets and st.secrets["supabase"].get("url")

if USE_SUPABASE:
    from supabase import create_client, Client
    
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["key"]
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Using Supabase cloud database")
else:
    # Fallback to SQLite
    DATABASE_URL = "sqlite:///khula_collective.db"
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    Base = declarative_base()
    print("✅ Using SQLite local database")

class DatabaseManager:
    """Unified database manager for SQLite and Supabase"""
    
    def __init__(self):
        self.use_supabase = USE_SUPABASE
    
    def get_users(self, username=None):
        """Get users from database"""
        if self.use_supabase:
            if username:
                result = supabase.table("users").select("*").eq("username", username).execute()
            else:
                result = supabase.table("users").select("*").execute()
            return result.data
        else:
            session = SessionLocal()
            if username:
                users = session.query(User).filter_by(username=username).all()
            else:
                users = session.query(User).all()
            session.close()
            return [self._model_to_dict(u) for u in users]
    
    def get_contributions(self, user_id=None, month=None):
        """Get contributions from database"""
        if self.use_supabase:
            query = supabase.table("monthly_contributions").select("*")
            if user_id:
                query = query.eq("user_id", user_id)
            if month:
                query = query.eq("month", month)
            result = query.execute()
            return result.data
        else:
            session = SessionLocal()
            query = session.query(MonthlyContribution)
            if user_id:
                query = query.filter_by(user_id=user_id)
            if month:
                query = query.filter_by(month=month)
            contributions = query.all()
            session.close()
            return [self._model_to_dict(c) for c in contributions]
    
    def get_global_balance(self):
        """Get global account balance"""
        if self.use_supabase:
            result = supabase.table("global_account_sync").select("*").eq("id", 1).execute()
            return result.data[0] if result.data else {"total_balance": 0}
        else:
            session = SessionLocal()
            sync = session.query(GlobalAccountSync).first()
            session.close()
            return self._model_to_dict(sync) if sync else {"total_balance": 0}
    
    def get_votes(self, user_id=None, suggestion_id=None):
        """Get votes from database"""
        if self.use_supabase:
            query = supabase.table("votes").select("*")
            if user_id:
                query = query.eq("user_id", user_id)
            if suggestion_id:
                query = query.eq("suggestion_id", suggestion_id)
            result = query.execute()
            return result.data
        else:
            session = SessionLocal()
            query = session.query(Vote)
            if user_id:
                query = query.filter_by(user_id=user_id)
            if suggestion_id:
                query = query.filter_by(suggestion_id=suggestion_id)
            votes = query.all()
            session.close()
            return [self._model_to_dict(v) for v in votes]
    
    def add_vote(self, user_id, suggestion_id, vote_type):
        """Add a vote"""
        if self.use_supabase:
            vote_data = {
                "user_id": user_id,
                "suggestion_id": suggestion_id,
                "vote_type": vote_type,
                "created_at": datetime.now().isoformat()
            }
            result = supabase.table("votes").insert(vote_data).execute()
            return result.data[0] if result.data else None
        else:
            session = SessionLocal()
            vote = Vote(
                user_id=user_id,
                suggestion_id=suggestion_id,
                vote_type=vote_type
            )
            session.add(vote)
            session.commit()
            session.close()
            return self._model_to_dict(vote)
    
    def update_contribution_status(self, contribution_id, status, payment_date=None):
        """Update contribution status"""
        if self.use_supabase:
            update_data = {"status": status}
            if payment_date:
                update_data["payment_date"] = payment_date
            result = supabase.table("monthly_contributions").update(update_data).eq("id", contribution_id).execute()
            return result.data[0] if result.data else None
        else:
            session = SessionLocal()
            contribution = session.query(MonthlyContribution).filter_by(id=contribution_id).first()
            if contribution:
                contribution.status = status
                if payment_date:
                    contribution.payment_date = payment_date
                session.commit()
            session.close()
            return self._model_to_dict(contribution) if contribution else None
    
    def get_market_data(self):
        """Get latest market data"""
        if self.use_supabase:
            result = supabase.table("market_data").select("*").eq("id", 1).execute()
            return result.data[0] if result.data else None
        else:
            # Return default market data for SQLite
            return {
                "repo_rate": 8.25,
                "prime_rate": 11.75,
                "inflation_rate": 5.2,
                "last_updated": datetime.now().isoformat()
            }
    
    def _model_to_dict(self, model):
        """Convert SQLAlchemy model to dictionary"""
        if model is None:
            return None
        return {c.name: getattr(model, c.name) for c in model.__table__.columns}

# SQLite Models (for backward compatibility)
if not USE_SUPABASE:
    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String(50), unique=True, nullable=False)
        password_hash = Column(String(255), nullable=False)
        full_name = Column(String(100))
        email = Column(String(100))
        phone = Column(String(20))
        sa_id_number = Column(String(13))
        role = Column(String(20), default='member')
        is_active = Column(Boolean, default=True)
        created_at = Column(DateTime, default=datetime.now)
    
    class MonthlyContribution(Base):
        __tablename__ = 'monthly_contributions'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('users.id'))
        month = Column(String(7), nullable=False)
        amount = Column(Float, nullable=False)
        status = Column(String(20), default='Pending')
        payment_date = Column(String(10))
        transaction_reference = Column(String(100))
        created_at = Column(DateTime, default=datetime.now)
    
    class GlobalAccountSync(Base):
        __tablename__ = 'global_account_sync'
        id = Column(Integer, primary_key=True)
        total_balance = Column(Float, default=0)
        last_sync = Column(DateTime)
        fnb_account_id = Column(String(100))
    
    class Vote(Base):
        __tablename__ = 'votes'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('users.id'))
        suggestion_id = Column(Integer)
        vote_type = Column(String(20))
        created_at = Column(DateTime, default=datetime.now)
    
    # Create tables if they don't exist
    Base.metadata.create_all(engine)

# Export database manager instance
db = DatabaseManager()