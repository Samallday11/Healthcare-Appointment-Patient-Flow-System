from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta
from typing import Optional

from app.db.session import get_db
from app.core.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/provider-utilization")
async def get_provider_utilization(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get provider utilization statistics.
    
    Returns metrics including:
    - Total appointments
    - Completed appointments
    - No-shows and cancellations
    - Completion rate
    """
    data = await AnalyticsService.get_provider_utilization(db, days)
    return {
        "period_days": days,
        "providers": data
    }


@router.get("/daily-load")
async def get_daily_load(
    start_date: Optional[date] = Query(None, description="Start date (default: 30 days ago)"),
    end_date: Optional[date] = Query(None, description="End date (default: 30 days ahead)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get daily appointment load statistics.
    
    Shows appointment volume and status breakdown by date.
    """
    data = await AnalyticsService.get_daily_load(db, start_date, end_date)
    return {
        "start_date": start_date or (date.today() - timedelta(days=30)),
        "end_date": end_date or (date.today() + timedelta(days=30)),
        "daily_stats": data
    }


@router.get("/no-shows")
async def get_no_show_analysis(
    db: AsyncSession = Depends(get_db)
):
    """
    Get no-show rate analysis by month.
    
    Returns monthly statistics for the past year.
    """
    data = await AnalyticsService.get_no_show_analysis(db)
    return {
        "analysis_period": "last_12_months",
        "monthly_stats": data
    }


@router.get("/wait-times")
async def get_wait_time_analysis(
    db: AsyncSession = Depends(get_db)
):
    """
    Get average wait time analysis per provider.
    
    Calculates time between appointment booking and actual appointment time.
    """
    data = await AnalyticsService.get_wait_time_analysis(db)
    return {
        "wait_times": data
    }

