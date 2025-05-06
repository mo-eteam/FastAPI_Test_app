import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.future import select
from .models import User, Company, UserRole
from .security import get_password_hash
import os

# Create base for declarative models
Base = declarative_base()

# Create async engine
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://testuser:testpassword@db:5432/testdb")
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,  # Set to False in production
    future=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

async def init_db(db: AsyncSession):
    """
    Initialize database with default data
    - Create default companies
    - Create admin and test users
    """
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Check if companies exist
    company_query = select(Company).where(Company.id == 'default_company')
    existing_company = await db.execute(company_query)
    
    if not existing_company.scalar_one_or_none():
        # Create default company
        default_company = Company(
            id='default_company', 
            name='Default Company'
        )
        db.add(default_company)
        
        # Create users
        admin_user = User(
            username='admin',
            email='admin@example.com',
            hashed_password=get_password_hash('adminpassword'),
            role=UserRole.ADMIN,
            company_id='default_company'
        )
        
        test_user = User(
            username='testuser',
            email='testuser@example.com',
            hashed_password=get_password_hash('userpassword'),
            role=UserRole.USER,
            company_id='default_company'
        )
        
        db.add(admin_user)
        db.add(test_user)
        
        await db.commit()

async def async_init_db():
    """Async database initialization"""
    async with AsyncSessionLocal() as session:
        await init_db(session)

def run_init_db():
    """Synchronous wrapper to run async initialization"""
    import asyncio
    asyncio.run(async_init_db())
