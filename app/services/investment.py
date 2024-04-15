from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


def close_fully_invested_object(obj: Union[CharityProject, Donation]) -> None:
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()


async def investment_process(session: AsyncSession):
    investments_not_closed = await donation_crud.get_not_closed_objects(
        session=session
    )
    projects_not_closed = await charity_project_crud.get_not_closed_objects(
        session=session
    )
    if not investments_not_closed or not projects_not_closed:
        return
    for investment in investments_not_closed:
        for project in projects_not_closed:
            required_amount = (
                project.full_amount - project.invested_amount)
            available_amount = (
                investment.full_amount - investment.invested_amount
            )
            difference_amounts = (
                required_amount - available_amount
            )

            if difference_amounts == 0:
                close_fully_invested_object(investment)
                close_fully_invested_object(project)

            if difference_amounts < 0:
                investment.invested_amount += difference_amounts
                close_fully_invested_object(project)

            if difference_amounts > 0:
                project.invested_amount += available_amount
                close_fully_invested_object(investment)
        await session.commit()
