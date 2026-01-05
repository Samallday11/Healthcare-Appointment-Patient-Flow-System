from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from uuid import UUID

from app.db.models import Provider, ProviderSchedule
from app.schemas.provider import (
    ProviderCreate,
    ProviderUpdate,
    ProviderScheduleCreate
)
from app.utils.exceptions import NotFoundError


class ProviderService:
    """Business logic for provider management."""
    
    @staticmethod
    async def create_provider(
        db: AsyncSession,
        provider_data: ProviderCreate
    ) -> Provider:
        """Create a new provider."""
        provider = Provider(**provider_data.model_dump())
        db.add(provider)
        await db.commit()
        await db.refresh(provider)
        return provider
    
    @staticmethod
    async def get_provider(
        db: AsyncSession,
        provider_id: UUID
    ) -> Optional[Provider]:
        """Get provider by ID."""
        result = await db.execute(
            select(Provider).where(Provider.provider_id == provider_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def list_providers(
        db: AsyncSession,
        specialty: Optional[str] = None,
        is_active: Optional[bool] = True,
        skip: int = 0,
        limit: int = 100
    ) -> List[Provider]:
        """List providers with filters."""
        query = select(Provider)
        
        if specialty:
            query = query.where(Provider.specialty.ilike(f"%{specialty}%"))
        
        if is_active is not None:
            query = query.where(Provider.is_active == is_active)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def update_provider(
        db: AsyncSession,
        provider_id: UUID,
        provider_data: ProviderUpdate
    ) -> Provider:
        """Update provider information."""
        provider = await ProviderService.get_provider(db, provider_id)
        
        if not provider:
            raise NotFoundError("Provider not found")
        
        update_data = provider_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(provider, field, value)
        
        await db.commit()
        await db.refresh(provider)
        return provider
    
    @staticmethod
    async def add_schedule(
        db: AsyncSession,
        schedule_data: ProviderScheduleCreate
    ) -> ProviderSchedule:
        """Add availability schedule for a provider."""
        # Verify provider exists
        provider = await ProviderService.get_provider(db, schedule_data.provider_id)
        if not provider:
            raise NotFoundError("Provider not found")
        
        schedule = ProviderSchedule(**schedule_data.model_dump())
        db.add(schedule)
        await db.commit()
        await db.refresh(schedule)
        return schedule
    
    @staticmethod
    async def get_provider_schedules(
        db: AsyncSession,
        provider_id: UUID
    ) -> List[ProviderSchedule]:
        """Get all schedules for a provider."""
        result = await db.execute(
            select(ProviderSchedule)
            .where(ProviderSchedule.provider_id == provider_id)
            .order_by(ProviderSchedule.day_of_week, ProviderSchedule.start_time)
        )
        return result.scalars().all()
    
    
