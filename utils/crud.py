from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from .database import async_session_maker
from models.models import Schedule, Promotion

class ScheduleCRUD:

    @staticmethod
    async def create_schedule(schedule_data: dict):
        async with async_session_maker() as session:
            new_schedule = Schedule(**schedule_data)
            session.add(new_schedule)
            await session.commit()
            await session.refresh(new_schedule)
            return new_schedule

    @staticmethod
    async def get_all_schedules():
        async with async_session_maker() as session:
            query = select(Schedule)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def check_by_section(section: str):
        async with async_session_maker() as session:
            query = select(Schedule).where(Schedule.section == section)
            result = await session.execute(query)
            schedules = result.scalars().all()
            return schedules

    @staticmethod
    async def update_schedule(schedule_id: int, schedule_data: dict):
        async with async_session_maker() as session:
            schedule = await session.get(Schedule, schedule_id)
            if schedule:
                for key, value in schedule_data.items():
                    setattr(schedule, key, value)
                await session.commit()
                await session.refresh(schedule)
            return schedule

    @staticmethod
    async def delete_schedule(schedule_id: int):
        async with async_session_maker() as session:
            schedule = await session.get(Schedule, schedule_id)
            if schedule:
                await session.delete(schedule)
                await session.commit()
            return schedule


class PromotionCRUD:
    @staticmethod
    async def create_promotion(promotion_data: dict):
        async with async_session_maker() as session:
            new_promotion = Promotion(**promotion_data)
            session.add(new_promotion)
            await session.commit()
            await session.refresh(new_promotion)
            return new_promotion

    @staticmethod
    async def get_all_promotions():
        async with async_session_maker() as session:
            query = select(Promotion)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def update_promotion(promotion_id: int, promotion_data: dict):
        async with async_session_maker() as session:
            promotion = await session.get(Schedule, promotion_id)
            if promotion:
                for key, value in promotion_data.items():
                    setattr(promotion, key, value)
                await session.commit()
                await session.refresh(promotion)
            return promotion

    @staticmethod
    async def delete_promotion(promotion_id: int):
        async with async_session_maker() as session:
            promotion = await session.get(Promotion, promotion_id)
            if promotion:
                await session.delete(promotion)
                await session.commit()
            return promotion

    @staticmethod
    async def delete_all_promotions():
        async with async_session_maker() as session:
            result = await session.execute(delete(Promotion))
            await session.commit()
            return result.rowcount