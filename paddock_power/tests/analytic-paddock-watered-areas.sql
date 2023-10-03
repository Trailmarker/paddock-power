select
    "Watered Areas".geometry as geometry,
    "Analytic Paddocks".Paddock as Paddock,
    "Analytic Paddocks".Name,
    "Watered Areas".Watered,
    "Watered Areas".Timeframe
from
    "Analytic Paddocks"
    inner join "Watered Areas" on "Analytic Paddocks".Paddock = "Watered Areas".Paddock
    and (
        ("Watered Areas".Timeframe = 'Current')
        and (
            "Analytic Paddocks".Status in (
                'Built',
                'BuiltSuperseded',
                'PlannedSuperseded',
                'BuiltArchived',
                'PlannedArchived'
            )
        )
        or ("Watered Areas".Timeframe = 'Future')
        and (
            "Analytic Paddocks".Status in ('Drafted', 'Built', 'Planned')
        )
        or ("Watered Areas".Timeframe = 'Undefined')
        and (
            "Analytic Paddocks".Status in (
                'PlannedSuperseded',
                'PlannedArchived',
                'Undefined'
            )
        )
    )