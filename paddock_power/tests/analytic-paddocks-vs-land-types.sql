select
    "Analytic Paddocks".Name,
    st_intersection(
        "Analytic Paddocks".geometry,
        "Land Types".geometry
    ) as geometry,
    st_area(
        st_intersection(
            "Analytic Paddocks".geometry,
            "Land Types".geometry
        )
    ) / 1000000.0 as "Area (km²)"
from
    "Analytic Paddocks"
    inner join "Land Types" on st_area(
        st_intersection(
            "Analytic Paddocks".geometry,
            "Land Types".geometry
        )
    ) >= 10.0
where
    "Analytic Paddocks".Paddock = 29