from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Dict
from datetime import date, datetime, timedelta


class AnalyticsService:
    """Business logic for analytics and reporting."""
    
    @staticmethod
    async def get_provider_utilization(
        db: AsyncSession,
        days: int = 30
    ) -> List[Dict]:
        """Get provider utilization statistics."""
        query = text("""
            SELECT * FROM provider_utilization
        """)
        
        result = await db.execute(query)
        rows = result.mappings().all()
        return [dict(row) for row in rows]
    
    @staticmethod
    async def get_daily_load(
        db: AsyncSession,
        start_date: date = None,
        end_date: date = None
    ) -> List[Dict]:
        """Get daily appointment load."""
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today() + timedelta(days=30)
        
        query = text("""
            SELECT * FROM daily_appointment_load
            WHERE appointment_date BETWEEN :start_date AND :end_date
            ORDER BY appointment_date DESC
        """)
        
        result = await db.execute(
            query,
            {"start_date": start_date, "end_date": end_date}
        )
        rows = result.mappings().all()
        return [dict(row) for row in rows]
    
    @staticmethod
    async def get_no_show_analysis(
        db: AsyncSession
    ) -> List[Dict]:
        """Get no-show analysis by month."""
        query = text("""
            SELECT * FROM no_show_analysis
        """)
        
        result = await db.execute(query)
        rows = result.mappings().all()
        return [dict(row) for row in rows]
    
    @staticmethod
    async def get_wait_time_analysis(
        db: AsyncSession
    ) -> List[Dict]:
        """Calculate average wait times per provider."""
        query = text("""
            SELECT 
                pr.provider_id,
                pr.first_name || ' ' || pr.last_name AS provider_name,
                pr.specialty,
                COUNT(a.appointment_id) AS total_appointments,
                AVG(EXTRACT(EPOCH FROM (a.start_time - a.created_at::time)) / 60) AS avg_wait_minutes
            FROM providers pr
            LEFT JOIN appointments a ON pr.provider_id = a.provider_id
            WHERE a.status IN ('completed', 'no_show')
            AND a.appointment_date >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY pr.provider_id, pr.first_name, pr.last_name, pr.specialty
            HAVING COUNT(a.appointment_id) > 0
            ORDER BY avg_wait_minutes DESC
        """)
        
        result = await db.execute(query)
        rows = result.mappings().all()
        return [dict(row) for row in rows]
    
    
