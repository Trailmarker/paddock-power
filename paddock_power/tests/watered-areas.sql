with NearWateredAreas as (
    select
        st_union(geometry) as geometry,
        Paddock,
        "Paddock Name",
        Timeframe
    from
        "Waterpoint Buffers"
    where
        "Grazing Radius Type" = 'Near'
    group by
        Paddock,
        "Paddock Name",
        Timeframe
),
FarWateredAreas as (
    select
        st_union(geometry) as geometry,
        Paddock,
        "Paddock Name",
        Timeframe
    from
        "Waterpoint Buffers"
    where
        "Grazing Radius Type" = 'Far'
    group by
        Paddock,
        "Paddock Name",
        Timeframe
),
UnwateredPaddocks as (
    select
        st_multi("Analytic Paddocks".geometry) as geometry,
        0 as fid,
        "Analytic Paddocks".Paddock as Paddock,
        "Analytic Paddocks".Name as "Paddock Name",
        'Unwatered' as Watered,
        'Current' as Timeframe
    from
        "Analytic Paddocks"
        left join "Waterpoint Buffers"
    where
        not exists (
            select
                1
            from
                "Waterpoint Buffers"
            where
                "Waterpoint Buffers".Paddock = "Analytic Paddocks".Paddock
                and ("Waterpoint Buffers".Timeframe = 'Current')
                and (
                    "Analytic Paddocks".Status in (
                        'Built',
                        'BuiltSuperseded',
                        'PlannedSuperseded',
                        'BuiltArchived',
                        'PlannedArchived'
                    )
                )
        )
    union
    select
        st_multi("Analytic Paddocks".geometry) as geometry,
        0 as fid,
        "Analytic Paddocks".Paddock as Paddock,
        "Analytic Paddocks".Name as "Paddock Name",
        'Unwatered' as Watered,
        'Future' as Timeframe
    from
        "Analytic Paddocks"
        left join "Waterpoint Buffers"
    where
        not exists (
            select
                1
            from
                "Waterpoint Buffers"
            where
                "Waterpoint Buffers".Paddock = "Analytic Paddocks".Paddock
                and ("Waterpoint Buffers".Timeframe = 'Future')
                and (
                    "Analytic Paddocks".Status in ('Drafted', 'Built', 'Planned')
                )
        )
)
select
    st_multi(geometry) as geometry,
    0 as fid,
    NearWateredAreas.Paddock,
    NearWateredAreas."Paddock Name",
    'Near' as Watered,
    NearWateredAreas.Timeframe
from
    NearWateredAreas
union
select
    st_multi(
        st_difference(
            FarWateredAreas.geometry,
            NearWateredAreas.geometry
        )
    ) as geometry,
    0 as fid,
    FarWateredAreas.Paddock,
    FarWateredAreas."Paddock Name",
    'Far' as Watered,
    FarWateredAreas.Timeframe
from
    FarWateredAreas
    inner join NearWateredAreas on FarWateredAreas.Paddock = NearWateredAreas.Paddock
    and FarWateredAreas.Timeframe = NearWateredAreas.Timeframe
    and st_difference(
        FarWateredAreas.geometry,
        NearWateredAreas.geometry
    ) is not null
    and st_area(
        st_difference(
            FarWateredAreas.geometry,
            NearWateredAreas.geometry
        )
    ) >= 10.0
union
select
    st_multi(
        st_difference(
            "Analytic Paddocks".geometry,
            FarWateredAreas.geometry
        )
    ) as geometry,
    0 as fid,
    FarWateredAreas.Paddock,
    FarWateredAreas."Paddock Name",
    'Unwatered' as Watered,
    FarWateredAreas.Timeframe
from
    "Analytic Paddocks"
    inner join FarWateredAreas on "Analytic Paddocks".Paddock = FarWateredAreas.Paddock
    and st_difference(
        "Analytic Paddocks".geometry,
        FarWateredAreas.geometry
    ) is not null
    and st_area(
        st_difference(
            "Analytic Paddocks".geometry,
            FarWateredAreas.geometry
        )
    ) >= 10.0
    and (
        ("FarWateredAreas"."Timeframe" = 'Current')
        and (
            "Analytic Paddocks"."Status" in (
                'Built',
                'BuiltSuperseded',
                'PlannedSuperseded',
                'BuiltArchived',
                'PlannedArchived'
            )
        )
        or ("FarWateredAreas"."Timeframe" = 'Future')
        and (
            "Analytic Paddocks"."Status" in ('Drafted', 'Built', 'Planned')
        )
        or ("FarWateredAreas"."Timeframe" = 'Undefined')
        and (
            "Analytic Paddocks"."Status" in (
                'PlannedSuperseded',
                'PlannedArchived',
                'Undefined'
            )
        )
    )
union
select
    *
from
    UnwateredPaddocks