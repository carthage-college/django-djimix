TERM_LIST = {
    "RA": "Fall",
    "RB": "J-Term",
    "RC": "Spring",
    "RD": "Summer Pre-Session",
    "RE": "Summer",
    "AA": "Fall I",
    "AB": "Fall II ",
    "AG": "Winter",
    "AK": "Spring I",
    "AM": "Spring II",
    "AS": "Summer I",
    "AT": "Summer II",
    "GE": "Summer",
    "GA": "Fall",
    "GB": "J-Term",
    "TA": "Fall",
    "PA": "Fall",
    "YA": "Fall",
    "GC": "Spring",
    "TC": "Spring",
    "PC": "Spring",
    "YC": "Spring",
    "TE": "Summer",
    "PE": "Summer",
    "YE": "Summer"
}
# IDs must be unique pattern that does not repeat in any other
# item e.g 25 & 250 will not work.
SPORTS_MEN = (
    ("0","----Men's Sport----"),
    ("15","Baseball"),
    ("25","Basketball"),
    ("35","Cross Country"),
    ("45","Football"),
    ("55","Golf"),
    ("61","Ice Hockey"),
    ("65","Lacrosse"),
    ("75","Soccer"),
    ("85","Swimming"),
    ("95","Tennis"),
    ("105","Track &amp; Field"),
    ("120","Volleyball"),
)
SPORTS_WOMEN = (
    ("0","----Women's Sports----"),
    ("200","Basketball"),
    ("210","Cross Country"),
    ("220","Golf"),
    ("225","Ice Hockey"),
    ("230","Lacrosse"),
    ("240","Soccer"),
    ("260","Softball"),
    ("270","Swimming"),
    ("280","Tennis"),
    ("290","Track &amp; Field"),
    ("300","Volleyball"),
    ("305","Water Polo")
)

SPORTS_ALL = SPORTS_WOMEN + SPORTS_MEN
