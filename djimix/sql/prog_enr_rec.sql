select
id,
TRIM(NVL(major1,"")) as mj1,
TRIM(NVL(major2,"")) as mj2,
TRIM(NVL(major3,"")) as mj3,
TRIM(NVL(minor1,"")) as mi1,
TRIM(NVL(minor2,"")) as mi2,
TRIM(NVL(minor3,"")) as mi3,
conc1,
conc2,
conc3
from prog_enr_rec where
major1 <> ''
and
major2 <> ''
and
minor1 <> ''
and
minor2 <> ''
