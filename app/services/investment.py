from datetime import datetime
from typing import Optional, Union

from app.models import CharityProject, Donation


def investment_process(
    target: Union[CharityProject, Donation],
    sources: Optional[Union[list[CharityProject], list[Donation]]],
) -> Union[list[CharityProject], list[Donation]]:
    changed = []
    for source in sources:
        investment_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount,
        )
        changed.append(source)
        for changed_object in (source, target):
            changed_object.invested_amount += investment_amount
            if changed_object.full_amount == changed_object.invested_amount:
                changed_object.fully_invested = True
                changed_object.close_date = datetime.now()
        if target.fully_invested:
            break
    return changed
