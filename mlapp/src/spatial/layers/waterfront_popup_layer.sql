with
  "Near" as
	(select
	 st_union(geometry) as "geometry", "Waterpoint", "Name", "Waterpoint Buffer Type", "Buffer Distance (m)", "Status" from "{{0}}"
	 where "Waterpoint Buffer Type" = 'Near'
	 and "Waterpoint" = {waterpointId}
	 group by "Status")
, "Far" as
	(select
	 st_union(geometry) as "geometry", "Waterpoint", "Name", "Waterpoint Buffer Type", "Buffer Distance (m)", "Status" from "{{0}}"
	 where "Waterpoint Buffer Type" = 'Far'
	 and "Waterpoint" = {waterpointId}
	 group by "Status")
select * 
from "Near"
union
select st_difference("Far".geometry, "Near".geometry), "Far"."Waterpoint", "Far"."Name", "Far"."Waterpoint Buffer Type", "Far"."Buffer Distance (m)", "Far"."Status"
from "Far"
inner join "Near"
on "Far"."Status" = "Near"."Status"