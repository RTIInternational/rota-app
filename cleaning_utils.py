import re
from dataclasses import dataclass
from string import punctuation
import pandas as pd

all_punctuation = punctuation + "‘’·—»"
# keep in dollar signs
all_punctuation = all_punctuation.replace("$", "")


# "regex separator"
# captures the following: 1+ spaces OR 1+ non-word characters (ex: "/", "-"),
# OR 1 word boundary
# apply the this variable using an `fr` string in the regex substituion
# (ex: `fr"\bw{sep}force\b"`)
sep = r"(?: +|\W+|\b)"


@dataclass
class RegexRemoval:
    description: str
    regex_str: str  # usually raw string: r"your string"

    def __post_init__(self):
        self.regex = re.compile(self.regex_str, re.IGNORECASE)


@dataclass
class RegexSubstitution:
    description: str
    regex_str: str  # usually raw string: r"your string"
    replacement: str
    priority: int = 10  # higher values → run later (eg: 1 runs before 20)

    def __post_init__(self):
        self.regex = re.compile(self.regex_str, re.IGNORECASE)


removals = [
    RegexRemoval("OBSCIS", r"(OBSCIS)"),
    RegexRemoval(
        "MO Suffix",
        r"\b\w\s\w\s\w\w?\s\w\s\d{2}(?: |\W)\d{2}(?: |\W)\d{4}",
    ),
    RegexRemoval(
        "Statute Prefix", r"\S{1,2}\s\d\S{0,3}\.\d\S{0,3}\.\d\S{0,3}(?:\.\d?\S{0,3}?)?"
    ),
]

substitutions = [
    # LESS THAN / GREATER THAN terms =========
    RegexSubstitution("Less Than", r"\b(?:&LT;|lt)\b", " less than "),
    RegexSubstitution("Less Than 2", r"\blt(?=\d+)\b", "less than "),
    RegexSubstitution("Less Than 3", r"\<", " less than "),
    RegexSubstitution("Greater Than", r"\b(?:&GT;|gt|\>)\b", " greater than "),
    RegexSubstitution("Greater Than 2", r"\bgt(?=\d+)\b", "greater than "),
    RegexSubstitution("Greater Than 3", r"\>", " greater than "),
    # WITH terms ===========
    RegexSubstitution("With Out", r"\bw{sep}(?:o|out)\b", "without"),
    RegexSubstitution("With Out 2", r"\bwo\b", "without"),
    RegexSubstitution("Within", rf"\bw{sep}(?:i|in)\b", "within", priority=5),
    RegexSubstitution(
        "With Intent",
        rf"\bw{sep}\s?in?t?e?n?t?\b",
        "with intent",
    ),
    RegexSubstitution(
        "with a",
        rf"\bw{sep}a\b",
        "with a",
    ),
    RegexSubstitution(
        "with health",
        rf"\bw{sep}health\b",
        "with health",
    ),
    RegexSubstitution(
        "with own",
        rf"\bw{sep}own\b",
        "with own",
    ),
    RegexSubstitution(
        "with report",
        rf"\bw{sep}report\b",
        "with report",
    ),
    RegexSubstitution(
        "with license",
        rf"\bw{sep}license\b",
        "with license",
    ),
    RegexSubstitution(
        "with murder",
        rf"\bw{sep}murder\b",
        "with murder",
    ),
    RegexSubstitution(
        "with injury",
        rf"\bw{sep}(?:injury|inj|injry)\b",
        "with injury",
    ),
    RegexSubstitution(
        "with turned",
        rf"\bw{sep}turned\b",
        "with turned",
    ),
    RegexSubstitution(
        "with altered",
        rf"\bw{sep}alt\b",
        "with altered",
    ),
    RegexSubstitution(
        "with deadly",
        rf"\bw{sep}deadly\b",
        "with deadly",
    ),
    RegexSubstitution(
        "with dangerous weapon",
        rf"\b(?:with|w){sep}(?:dangerous|d){sep}(?:weapon|wpn|weapn|weap)\b",
        "with dangerous weapon",
        priority=5,
    ),
    RegexSubstitution(
        "with child",
        rf"\b(?:with|w){sep}(?:child|chi|chld)\b",
        "with child",
    ),
    RegexSubstitution(
        "with minor",
        rf"\bw{sep}minor\b",
        "with minor",
    ),
    RegexSubstitution(
        "with kidnapping",
        rf"\bw{sep}kidnapping\b",
        "with kidnapping",
    ),
    RegexSubstitution(
        "with agency",
        rf"\bw{sep}agency\b",
        "with agency",
    ),
    RegexSubstitution(
        "with firearm",
        rf"\bw{sep}firearm\b",
        "with firearm",
    ),
    RegexSubstitution(
        "with weapon",
        rf"\bw{sep}(?:weapon|wpn|weapn|weap)\b",
        "with weapon",
    ),
    RegexSubstitution(
        "with knife",
        rf"\bw{sep}knife\b",
        "with knife",
    ),
    RegexSubstitution(
        "with force",
        rf"\bw{sep}force\b",
        "with force",
    ),
    RegexSubstitution(
        "with extenuating circumstances",
        rf"\bw{sep}ext{sep}circumstances\b",
        "with extenuating circumstances",
    ),
    RegexSubstitution(
        "with prior",
        rf"\bw{sep}prior\b",
        "with prior",
    ),
    RegexSubstitution(
        "with previous",
        rf"\bw{sep}previous\b",
        "with previous",
    ),
    RegexSubstitution(
        "with domestic violence",
        rf"\bw{sep}dv\b",
        "with domestic violence",
    ),
    RegexSubstitution(
        "with suspended",
        rf"\bw{sep}suspended\b",
        "with suspended",
    ),
    RegexSubstitution(  # doublecheck this
        "vehicle with",
        rf"\bvehicle{sep}w{sep}",
        "vehicle with",
    ),
    # TODO: is this "possession with" or "possession weapon"?
    # see concealed weapon as example
    RegexSubstitution(
        "possession with",
        rf"\b(?:possession|possess|poss){sep}w{sep}",
        "possession with",
    ),
    RegexSubstitution(
        "possession with intent",
        rf"\bp{sep}with{sep}intent",
        "possession with intent",
        priority=30,
    ),
    RegexSubstitution(
        "neglect with",
        rf"\bneglect{sep}w{sep}",
        "neglect with",
    ),
    RegexSubstitution(
        "cooperate with",
        rf"\bcooperate{sep}w{sep}",
        "cooperate with",
    ),
    RegexSubstitution(
        "interfere with",
        rf"\b(?:inter|interfere){sep}w{sep}",
        "interfere with",
    ),
    RegexSubstitution(  # TODO consolidate tamper/tampering?
        "tamper with",
        rf"\btamper{sep}w{sep}",
        "tamper with",
    ),
    RegexSubstitution(
        "tampering with",
        rf"\btampering{sep}w{sep}",
        "tampering with",
    ),
    RegexSubstitution(
        "assault with",
        rf"\bassault{sep}w{sep}",
        "assault with",
    ),
    # FIREARM TERMS
    RegexSubstitution(
        "firearm with altered identification numbers",
        rf"\bfirearm{sep}(?:with|w){sep}alter\b",
        "firearm with altered identification numbers",
    ),
    RegexSubstitution(
        "firearm",
        rf"\bf{sep}a\b",
        "firearm",
    ),
    RegexSubstitution(
        "intimidation",
        r"\b(?:intim|intimid)\b",
        "intimidation",
    ),
    # DOMESTIC VIOLENCE TERMS / PROTECTION / RESTRAINING ORDERS
    RegexSubstitution(
        "protective order",
        rf"\b(?:protective|protection|prot){sep}(?:order|ord|or)\b",
        "protective order",
    ),
    RegexSubstitution(
        "domestic violence protective order",
        r"\bdvpo\b",
        "domestic violence protective order",
    ),
    RegexSubstitution("domestic", r"\bdom\b", "domestic", priority=20),
    RegexSubstitution(
        "domestic violence",
        r"\bdv\b",
        "domestic violence",
    ),
    RegexSubstitution(
        "domestic violence 2",
        rf"\bd{sep}v\b",
        "domestic violence",
    ),
    RegexSubstitution(
        "witness testimony",
        rf"\bwit{sep}tes\b",
        "witness testimony",
    ),
    # CONVICTION TERMS ==
    RegexSubstitution(
        "misdemeanor conviction",
        rf"\b(?:misdemeanor|misd){sep}(?:convic|conv)\b",
        "misdemeanor conviction",
    ),
    RegexSubstitution(
        "prior conviction",
        rf"\b(?:prior|pr|pri){sep}(?:convic|conv)\b",
        "prior conviction",
    ),
    # ==== GENERAL TERMS =====
    # NOTE: added a negative lookbehind for 'mentally' so we won't
    # override 'mentally ill' cases
    RegexSubstitution(
        "illegal",
        r"\b(?<!mentally )(?:ill|illeg|illgl)\b",
        "illegal",
    ),
    RegexSubstitution("commercial fish", rf"\bcomm{sep}fish\b", "commercial fish"),
    RegexSubstitution("vessel", r"\bvess\b", "vessel"),
    RegexSubstitution(
        "traffic control device",
        rf"\btraff{sep}control{sep}dev\b",
        "traffic control device",
    ),
    RegexSubstitution("non-culpable", r"\bnonculp\b", "non-culpable"),
    RegexSubstitution("prohibited", r"\bprohib\b", "prohibited"),
    RegexSubstitution("nuisance", r"\bnuis\b", "nuisance"),
    RegexSubstitution("obstruction", r"\bobstr\b", "obstruction"),
    RegexSubstitution("pedestrian", r"\bped\b", "pedestrian"),
    RegexSubstitution("conduct", r"\bcond\b", "conduct", priority=20),
    RegexSubstitution(
        "subsequent",
        r"\bsubsq\b",
        "subsequent",
    ),
    RegexSubstitution(
        "disturbing the peace",
        r"\bdist{sep}peace\b",
        "disturbing the peace",
    ),
    RegexSubstitution(
        "offender accountability act",
        r"\boaa\b",
        "offender accountability act",
    ),
    RegexSubstitution(
        "against",
        r"\b(?:agnst|agin)\b",
        "against",
    ),
    RegexSubstitution(
        "child",
        r"\b(?:chil|chld)\b",
        "child",
    ),
    RegexSubstitution(
        "school",
        r"\bschl\b",
        "school",
    ),
    RegexSubstitution(
        "multiple",
        r"\bmult\b",
        "multiple",
    ),
    RegexSubstitution(
        "assailant",
        r"\bassail\b",
        "assailant",
    ),
    RegexSubstitution(
        "public disturbance",
        r"\b(?:public|pub|publ){sep}(?:disturbance|disturb|dist)\b",
        "public disturbance",
    ),
    RegexSubstitution(
        "interfere",
        r"\b(?:interf|interfer)\b",
        "interfere",
    ),
    # TODO should we leave obstructing/obstruction separate terms or lump into obstruct?
    RegexSubstitution(
        "obstructing",
        r"\bob\b",
        "obstructing",
    ),
    RegexSubstitution(
        "law enforcement officer",
        r"\bleo\b",
        "law enforcement officer",
    ),
    RegexSubstitution(
        "officer",
        r"\b(?:offcr|ofcr)\b",
        "officer",
    ),
    RegexSubstitution(
        "minor",
        r"\b(?:min|minr|mnr)\b",
        "minor",
    ),
    RegexSubstitution(
        "distance within 300 feet of park",
        rf"\bdist{sep}300{sep}park\b",
        "distance within 300 feet of park",
        priority=5,
    ),
    RegexSubstitution(
        "distance within 300",
        rf"{sep}dist{sep}w{sep}i{sep}300\b",
        "distance within 300",
        priority=5,
    ),
    RegexSubstitution(
        "major",
        r"\bmajr\b",
        "major",
    ),
    RegexSubstitution(
        "willful",
        r"\b(?:wilfl|wlfl)\b",
        "willful",
    ),
    RegexSubstitution(
        "issue worthless checks",
        rf"\b(?:issue|iss){sep}(?:worthless|wrthlss|wrtls){sep}(?:checks|cks)\b",
        "worthless",
    ),
    RegexSubstitution(
        "issue multiple worthless checks",
        rf"\b(?:issue|iss){sep}(?:multiple|mltpl){sep}(?:worthless|wrthlss|wrtls){sep}(?:checks|cks)\b",
        "worthless",
    ),
    RegexSubstitution(
        "unauthorized",
        r"\b(?:unauth|unau|unauthd)\b",
        "unauthorized",
    ),
    RegexSubstitution(
        "child support",
        r"\b(?:child|chld|chi){sep}(?:support|supp|sup)\b",
        "child support",
    ),
    RegexSubstitution(
        "unlawful",
        r"\b(?:unlawfully|unlaw|unlawfl|unlawf|unlwfl|unl)\b",
        "unlawful",
    ),
    RegexSubstitution(
        "Possession",
        r"\b(?:possess|poss?)\b",
        "possession",
    ),
    RegexSubstitution(
        "Abetting",
        r"\b(?:abett|abetted)\b",
        "Abetting",
    ),
    RegexSubstitution("emergency", r"\b(?:emerg|emer)\b", "emergency", priority=20),
    RegexSubstitution(
        "Attempted",
        r"\b(?:att|atmpt)\b",
        "attempted",
    ),
    # NOTE: added negative look ahead so we don't remap "at risk" to "attempted risk"
    RegexSubstitution(
        "Attempted 2",
        r"\bat(?! risk)\b",
        "attempted",
    ),
    RegexSubstitution(
        "Battery",
        r"\bbatt\b",
        "battery",
    ),
    RegexSubstitution(
        "Violation of Probation",
        r"\bvop\b",
        "violation of probation",
    ),
    # NOTE: removed 'con' because shows up in some DV-related text,
    # may not be a one-size fits all regex / 'consp' to conspiracy or conspire?
    RegexSubstitution(
        "Conspiracy",
        r"\b(?:consp|conspi|conspira|conspirc|consprc|consprcy|cnsprcy|conspr)\b",
        "conspiracy",
    ),
    RegexSubstitution(
        "Property",
        r"\bprop\b",
        "property",
    ),
    RegexSubstitution(
        "public disturbance",
        rf"\b(?:public|pub|publ){sep}(?:disturbance|dist)\b",
        "public disturbance",
    ),
    RegexSubstitution(
        "Criminal",
        r"\bcrim\b",
        "criminal",
    ),
    RegexSubstitution(
        "License",
        r"\blic\b",
        "license",
    ),
    RegexSubstitution(
        "Credit Card",
        r"\bcc\b",
        "credit card",
    ),
    RegexSubstitution(
        "Credit Card 2",
        r"\bcred{sep}crd\b",
        "credit card",
    ),
    RegexSubstitution(
        "exchange",
        r"\bexch\b",
        "exchange",
    ),
    RegexSubstitution(
        "electric power",
        rf"\belec{sep}pwr\b",
        "electric power",
    ),
    RegexSubstitution(
        "commit false", rf"\bcom?{sep}false\b", "commit false", priority=5
    ),
    # VEHICLE terms ===========
    RegexSubstitution(
        "Vehicle",
        r"\b(?:veh|vehi)\b",
        "vehicle",
    ),
    RegexSubstitution(
        "Vehicles",
        r"\bvehs\b",
        "vehicles",
    ),
    RegexSubstitution(
        "commercial motor vehicle",
        r"\bcmv\b",
        "commercial motor vehicle",
    ),
    RegexSubstitution(
        "motor vehicle",
        rf"\b(?:mtr|mot){sep}(?:vehicle|veh)\b",
        "motor vehicle",
    ),
    RegexSubstitution(
        "motor vehicle 2",
        rf"\bm{sep}v\b",
        "motor vehicle",
    ),
    RegexSubstitution(
        "motor vehicle 3",
        r"\b(?:mtv|mv)\b",
        "motor vehicle",
    ),
    RegexSubstitution("odometer", r"\bodom\b", "odometer"),
    RegexSubstitution(
        "red light",
        rf"\bred{sep}light\b",
        "red light",
    ),
    RegexSubstitution(
        "vehicle sound system",
        rf"\bveh{sep}snd{sep}sys\b",
        "vehicle sound system",
        priority=20,
    ),
    # =====
    RegexSubstitution(
        "Assault",
        r"\bass?lt\b",
        "assault",
    ),
    RegexSubstitution(
        "Assault 2",
        r"\bass\b",
        "assault",
    ),
    RegexSubstitution(
        "Mentally",
        r"\bment\b",
        "mentally",
    ),
    RegexSubstitution(
        "mentally ill",
        r"\bmnt{sep}ill\b",
        "mentally ill",
    ),
    RegexSubstitution(
        "Unknown",
        r"\bunk\b",
        "unknown",
    ),
    RegexSubstitution(
        "cohabitation",
        r"\b(?:coh|cohbt)\b",
        "cohabitation",
    ),
    RegexSubstitution(
        "Statement",
        r"\bstmt\b",
        "statement",
    ),
    RegexSubstitution(
        "Degree",
        r"\bdegr?e?\b",
        "degree",
    ),
    RegexSubstitution(
        "Felony",
        r"\b(?:fe|fel|felo|felny|fl|flny)\b",
        "felony",
    ),
    RegexSubstitution(
        "misdemeanor",
        r"\bmisd\b",
        "misdemeanor",
    ),
    # AGE
    RegexSubstitution(
        "years of age",
        r"\byoa\b",
        "years of age",
    ),
    RegexSubstitution(
        "year",
        r"\byr\b",
        "year",
    ),
    RegexSubstitution(
        "year 2",
        r"(?!\d+)yr\b",
        " year",
    ),
    RegexSubstitution(
        "elderly",
        r"\beldrly\b",
        "elderly",
    ),
    RegexSubstitution(
        "under",
        r"\b(?:und|undr)\b",
        "under",
    ),
    # AGE / FEMALE
    RegexSubstitution(
        "female",
        r"\bfem\b",
        "female",
    ),
    RegexSubstitution(
        "age female",
        rf"\bage{sep}f\b",
        "age female",
    ),
    RegexSubstitution(
        "old female",
        rf"\bold{sep}f\b",
        "old female",
    ),
    RegexSubstitution(
        "older female",
        rf"\bolder{sep}f\b",
        "older female",
    ),
    RegexSubstitution(
        "13 female",
        rf"\b13{sep}f\b",
        "13 female",
    ),
    RegexSubstitution(
        "15 female",
        rf"\b15{sep}f\b",
        "15 female",
    ),
    RegexSubstitution(
        "17 female",
        rf"\b17{sep}f\b",
        "17 female",
    ),
    # AGE / MALE
    RegexSubstitution(
        "age male",
        rf"\bage{sep}m\b",
        "age male",
    ),
    RegexSubstitution(
        "old male",
        rf"\bold{sep}m\b",
        "old male",
    ),
    RegexSubstitution(
        "older male",
        rf"\bolder{sep}m\b",
        "older male",
    ),
    RegexSubstitution(
        "13 male",
        rf"\b13{sep}m\b",
        "13 male",
    ),
    RegexSubstitution(
        "15 male",
        rf"\b15{sep}m\b",
        "15 male",
    ),
    RegexSubstitution(
        "17 male",
        rf"\b17{sep}m\b",
        "17 male",
    ),
    # ======
    RegexSubstitution(
        "Robbery",
        r"\brobb\b",
        "robbery",
    ),
    RegexSubstitution(
        "Attempted Robbery",
        rf"\battempted{sep}(?:rob|robb)\b",
        "attempted robbery",
    ),
    RegexSubstitution(
        "Detainer Robbery",
        rf"\bdetainer{sep}(?:rob|robb)\b",
        "detainer robbery",
    ),
    RegexSubstitution(
        "Aggravated",
        r"\b(?:agg|aggrav|aggr|aggravted)\b",
        "aggravated",
    ),
    RegexSubstitution(
        "Forced",
        r"\bfrc\b",
        "forced",
    ),
    RegexSubstitution(
        "Danger",
        r"\bdng\b",
        "danger",
    ),
    RegexSubstitution(
        "Abetting",
        r"\babet\b",
        "abetting",
    ),
    RegexSubstitution(
        "Acquaintance",
        r"\b(?:acquant|acq|acquaint|acquain)\b",
        "acquaintance",
    ),
    RegexSubstitution(
        "Breaking and Entering",
        r"\bB ?& ?E\b",
        "breaking and entering",
    ),
    RegexSubstitution("Building", r"\bbldg\b", "building"),
    RegexSubstitution(
        "Adult",
        r"\badlt\b",
        "adult",
    ),
    RegexSubstitution(
        "Deliver",
        r"\bdel\b",
        "deliver",
    ),
    RegexSubstitution(
        "Family",
        r"\bfam\b",
        "family",
    ),
    RegexSubstitution(
        "Burglary",
        r"\bburg\b",
        "burglary",
    ),
    RegexSubstitution(
        "Murder",
        r"\bmur\b",
        "murder",
    ),
    RegexSubstitution(
        "conspiracy to commit",
        rf"\bconsp{sep}comm\b",
        "conspiracy to commit",
    ),
    RegexSubstitution(
        "Representation",
        r"\brep\b",
        "representation",
    ),
    RegexSubstitution(
        "Previous",
        r"\bprev\b",
        "previous",
    ),
    RegexSubstitution(  # TODO revisit this - 'com' can also be 'commit'
        "Common",
        r"\bcom\b",
        "common",
    ),
    RegexSubstitution(
        "of a",
        r"\bofa\b",
        "of a",
    ),
    RegexSubstitution(  # TODO revisit this - 'viol' relates to 'violation' too
        "violent",
        r"\bviol\b",
        "violent",
    ),
    RegexSubstitution(
        "perform",
        r"\bperf\b",
        "perform",
    ),
    RegexSubstitution(
        "household",
        r"\b(?:hh|hsehld|hhld)\b",
        "household",
    ),
    RegexSubstitution(
        "Other",
        r"\both\b",
        "other",
    ),
    # WEAPON TERMS =========
    RegexSubstitution(
        "Weapon", r"\b(?:wea|wpn|weapn|weap|weapo)\b", "weapon", priority=20
    ),
    RegexSubstitution(
        "Weapons", r"\b(?:wea|wpn|weapn|weap|weapo)s\b", "weapons", priority=20
    ),
    RegexSubstitution("dangerous weapon", r"\b(?:dwpn|dw)\b", "dangerous weapon"),
    RegexSubstitution(
        "dangerous weapon 2", rf"\bd{sep}(?:w|wpn)\b", "dangerous weapon"
    ),
    RegexSubstitution(
        "concealed weapon", rf"\bconcealed{sep}(?:w|wpn)\b", "concealed weapon"
    ),
    # HARM terms =======
    RegexSubstitution(
        "Bodily Harm",
        rf"\b(?:bod{sep}ha?rm|bh)\b",
        "bodily harm",
    ),
    RegexSubstitution(
        "physical",
        r"\bphy\b",
        "physical",
    ),
    RegexSubstitution(
        "harmful",
        r"\bharmfl\b",
        "harmful",
    ),
    RegexSubstitution(
        "Great Bodily",
        rf"\b(?:gr|grt){sep}bodily\b",
        "great bodily",
    ),
    RegexSubstitution(
        "Great Bodily Injury",
        r"\bgbi\b",
        "great bodily injury",
    ),
    RegexSubstitution(
        "Substantial Bodily Harm",
        r"\bsbh\b",
        "substantial bodily harm",
    ),
    RegexSubstitution(
        "injury",
        r"\b(?:injry|inj)\b",
        "injury",
    ),
    RegexSubstitution(
        "inflict",
        r"\binflt\b",
        "inflict",
    ),
    RegexSubstitution(
        "Great Bodily Harm",
        rf"\bgr{sep}bod{sep}harm\b",
        "great bodily harm",
    ),
    RegexSubstitution(
        "Great Bodily Harm 2",
        r"\bgbh\b",
        "great bodily harm",
    ),
    # ====
    RegexSubstitution(  # TODO: revisit PERS can be person too
        "Personal",
        r"\bpers\b",
        "personal",
    ),
    RegexSubstitution(
        "persons",
        r"\bprsns\b",
        "persons",
    ),
    RegexSubstitution(
        "person",
        r"\b(?:prsn|per|perso)\b",
        "person",
    ),
    RegexSubstitution("election day", rf"\belec{sep}day\b", "election day"),
    RegexSubstitution(
        "temporary",
        r"\btemp\b",
        "temporary",
    ),
    RegexSubstitution(
        "improper",
        r"\bimprop\b",
        "improper",
    ),
    RegexSubstitution(
        "false",
        r"\bfls\b",
        "false",
    ),
    RegexSubstitution(
        "responsibility",
        r"\bresp\b",
        "responsibility",
    ),
    RegexSubstitution(
        "advertise",
        r"\bad\b",
        "advertise",
    ),
    RegexSubstitution(
        "imprisonment",
        r"\b(?:imprison|impris|imprsn)\b",
        "imprisonment",
    ),
    RegexSubstitution(
        "prohibited",
        r"\bproh\b",
        "prohibited",
    ),
    RegexSubstitution(
        "under influence",
        rf"\bunder{sep}(?:infl|influ)\b",
        "under influence",
        priority=5,
    ),
    RegexSubstitution(
        "stolen",
        r"\bstln\b",
        "stolen",
    ),
    RegexSubstitution(
        "years",
        r"\byrs\b",
        "years",
    ),
    RegexSubstitution(
        "intent",
        r"\bint\b",
        "intent",
    ),
    RegexSubstitution(
        "passage",
        r"\bpassg\b",
        "passage",
    ),
    RegexSubstitution(
        "withdraw",
        r"\bwit\b",
        "withdraw",
    ),
    RegexSubstitution(
        "manufacturing or delivering",
        r"\bman\Wdel\b",
        "manufacturing delivering",
    ),
    RegexSubstitution(  # Revisit this
        "minimum mandatory",
        r"\bmin\Wman\b",
        "minimum mandatory",
    ),
    RegexSubstitution(
        "stranger",
        r"\bstr(?:ngr)?\b",
        "stranger",
    ),
    RegexSubstitution(
        "personal use",
        r"\bpers use\b",
        "personal use",
    ),
    RegexSubstitution(
        "force",
        r"\bfo?rc\b",
        "force",
    ),
    RegexSubstitution(
        "operate",
        r"\b(?:oper|op|opr)\b",
        "operate",
    ),
    RegexSubstitution(
        "occupied",
        r"\bocc\b",
        "occupied",
    ),
    RegexSubstitution(
        "health care facility",
        r"\bhealth{sep}care{sep}fac\b",
        "health care facility",
        priority=5,
    ),
    RegexSubstitution(
        "residence",
        r"\bres\b",
        "residence",
    ),
    RegexSubstitution(
        "terrorism threats",
        rf"\bterr{sep}(?:thre|thrts)\b",
        "terrorism threats",
    ),
    RegexSubstitution(
        "false report",
        rf"\bfals{sep}rprt\b",
        "false report",
    ),
    RegexSubstitution(
        "government",
        r"\bgovt\b",
        "government",
    ),
    RegexSubstitution(
        "advocating",
        r"\badvoc\b",
        "advocating",
    ),
    RegexSubstitution(
        "government property",
        r"\bgov{sep}property\b",
        "government property",
    ),
    RegexSubstitution(
        "general assembly",
        r"\bgen{sep}assembly\b",
        "general assembly",
    ),
    # NOTE: added negative lookahead because was seeing "by off" when updating
    # statutory rape terms & "by offense" is not correct
    RegexSubstitution(
        "offense",
        r"\b(?<!by )(?:offense|offen|off|offe)\b",
        "offense",
    ),
    RegexSubstitution(
        "information",
        r"\b(?:info|infor)\b",
        "information",
    ),
    # LEWD charge cat
    RegexSubstitution(
        "pornography",
        r"\b(?:porn|porno)\b",
        "pornography",
    ),
    RegexSubstitution(
        "compelling",
        r"\bcompel\b",
        "compelling",
    ),
    RegexSubstitution(
        "prostitution",
        r"\bprostit\b",
        "prostitution",
    ),
    RegexSubstitution(
        "computer",
        r"\bcomputr\b",
        "computer",
    ),
    RegexSubstitution(
        "incapable",
        r"\bincap\b",
        "incapable",
    ),
    RegexSubstitution(
        "juvenile",
        r"\b(?:juv|juven)\b",
        "juvenile",
    ),
    RegexSubstitution(
        "involving",
        r"\b(?:involv|invlv)\b",
        "involving",
    ),
    RegexSubstitution(
        "equipment",
        r"\bequip\b",
        "equipment",
    ),
    RegexSubstitution(
        "hazardous",
        r"\bhaz\b",
        "hazardous",
    ),
    RegexSubstitution(  # NOTE: assault and battery unless A,B is followed by C
        "assault and battery",
        rf"\b(?:a\&b|a{sep}b|a \& b|ab)(?!c)\b",
        "assault and battery",
    ),
    RegexSubstitution(  # NOTE: assault and battery unless A,B is followed by C
        "assault and battery 2",
        rf"\b(?:a\&b|a{sep}b|a \& b|ab)(?!\Wc)\b",
        "assault and battery",
    ),
    RegexSubstitution(  # NOTE: assault and battery unless A,B is followed by C
        "assault and battery 2",
        rf"\b(?:a\&b|a{sep}b|a \& b|ab)(?! c)\b",
        "assault and battery",
    ),
    RegexSubstitution(
        "promote distribution",
        rf"\bpromote{sep}distrb\b",
        "promote distribution",
    ),
    RegexSubstitution(
        "child molestation first degree",
        rf"\b(?:child|chld|ch){sep}(?:molestation|molest|mol){sep}1\b",
        "child molestation first degree",
    ),
    RegexSubstitution(
        "child molestation second degree",
        rf"\b(?:child|chld|ch){sep}(?:molestation|molest|mol){sep}2\b",
        "child molestation second degree",
    ),
    RegexSubstitution(
        "child molestation third degree",
        rf"\b(?:child|chld|ch){sep}(?:molestation|molest|mol){sep}3\b",
        "child molestation third degree",
    ),
    RegexSubstitution(
        "child molestation",
        rf"\b(?:child|chld|ch){sep}(?:molestation|molest|mol)\b",
        "child molestation",
        priority=5,
    ),
    RegexSubstitution(
        "molestation",
        r"\b(?:molestation|molest|mol)\b",
        "molestation",
    ),
    RegexSubstitution(
        "indecent conduct exposure",
        rf"\bind{sep}cond{sep}expos\b",
        "indecent conduct exposure",
    ),
    RegexSubstitution(
        "indecent",
        r"\bindec\b",
        "indecent",
    ),
    RegexSubstitution(
        "indecent liberties",
        rf"\bind{sep}lib\b",
        "indecent liberties",
    ),
    RegexSubstitution(
        "moving",
        r"\bmov\b",
        "moving",
    ),
    RegexSubstitution(
        "depiction",
        r"\bdptn\b",
        "depiction",
    ),
    RegexSubstitution(
        "child luring",
        rf"\bchil{sep}lrng\b",
        "child luring",
    ),
    RegexSubstitution(
        "dissemination",
        r"\b(?:dissm|dissem)\b",
        "dissemination",
    ),
    RegexSubstitution(
        "possession of depictions of minor engaged in sexually explicit conduct",
        rf"\bposs{sep}(?:depict|dep){sep}(?:minor|min){sep}eng{sep}sex{sep}(?:exp|expct){sep}conduct\b",
        "possession of depictions of minor engaged in sexually explicit conduct",
        priority=3,
    ),
    RegexSubstitution(
        "dealing of depictions of minor engaged in sexually explicit conduct",
        rf"\bdeal{sep}(?:depict|dep){sep}(?:minor|min){sep}eng{sep}sex{sep}(?:exp|expct){sep}conduct\b",
        "dealing of depictions of minor engaged in sexually explicit conduct",
        priority=3,
    ),
    RegexSubstitution(
        "viewing of depictions of minor engaged in sexually explicit conduct",
        rf"\bview{sep}(?:depict|dep){sep}(?:minor|min){sep}eng{sep}sex{sep}(?:exp|expct){sep}conduct\b",
        "viewing of depictions of minor engaged in sexually explicit conduct",
        priority=3,
    ),
    RegexSubstitution(
        "online sexual corruption of a child",
        rf"\bonline{sep}sex{sep}corrupt{sep}child\b",
        "online sexual corruption of a child",
    ),
    RegexSubstitution(
        "lewd or lascivious act",
        rf"\b(?:L\&L|L{sep}L)\b",
        "lewd or lascivious act",
    ),
    RegexSubstitution(
        "exposure",
        r"\bexpos\b",
        "exposure",
    ),
    # SEXUAL OFFENSES  =====
    RegexSubstitution(
        "Criminal Sexual Conduct",
        r"\bcsc\b",
        "criminal sexual conduct",
    ),
    RegexSubstitution(
        "sexual",
        r"\bsexl\b",
        "sexual",
    ),
    RegexSubstitution(
        "explicit",
        r"\bexplct\b",
        "explicit",
    ),
    RegexSubstitution(
        "sexual offense",
        rf"\b(?:sexual|sex){sep}(?:offense|offen|off)\b",
        "sexual offense",
    ),
    RegexSubstitution(
        "sexual offenses",
        rf"\b(?:sexual|sex){sep}(?:offense|offen|off)s\b",
        "sexual offenses",
    ),
    RegexSubstitution(
        "sexual assault",
        rf"\b(?:sexual|sex){sep}(?:assault|assult|assualt|ass|asst)\b",
        "sexual assault",
    ),
    RegexSubstitution(
        "sexual contact",
        rf"\b(?:sexual|sex){sep}(?:contact)\b",
        "sexual contact",
    ),
    RegexSubstitution(
        "sexual act",
        rf"\b(?:sexual|sex){sep}(?:act|acts)\b",
        "sexual act",
    ),
    RegexSubstitution(
        "sexual act 2",
        r"\bsxact\b",
        "sexual act",
    ),
    RegexSubstitution(
        "sexual abuse",
        rf"\b(?:sexual|sex){sep}(?:abuse|ab)\b",
        "sexual abuse",
    ),
    RegexSubstitution(
        "commit sex abuse",
        rf"\bcomm{sep}sex{sep}abuse\b",
        "commit sex abuse",
    ),
    RegexSubstitution(
        "commit sex act",
        rf"\bcomm{sep}sex{sep}act\b",
        "commit sex act",
    ),
    RegexSubstitution(
        "commit sex abuse minor",
        r"\bcommsexabuseminor\b",
        "commit sex abuse minor",
        priority=20,
    ),
    RegexSubstitution(
        "sexual battery",
        rf"\b(?:sexual|sex){sep}(?:battery|batt|bat)\b",
        "sexual battery",
    ),
    RegexSubstitution(  # TODO: should these actually map to "sexual misconduct"?
        "sexual conduct",
        rf"\b(?:sexual|sex){sep}(?:conduct|cndct|cond|con)\b",
        "sexual conduct",
    ),
    RegexSubstitution(
        "sexual penetration",
        rf"\b(?:sexual|sex){sep}(?:penetration|pen)\b",
        "sexual penetration",
    ),
    # TODO: Revisit - hard to tell if exp/expl maps to "exploitation" or "explicit"
    RegexSubstitution(
        "sexual exploitation",
        rf"\b(?:sexual|sex){sep}(?:exploitation|exploit)\b",
        "sexual exploitation",
    ),
    RegexSubstitution(
        "sexual performance",
        rf"\b(?:sexual|sex){sep}(?:performance|perform)\b",
        "sexual performance",
    ),
    RegexSubstitution(
        "sexual imposition",
        rf"\b(?:sexual|sex){sep}(?:imposition|imp)\b",
        "sexual imposition",
    ),
    RegexSubstitution(
        "sex with",
        rf"\bsex{sep}w\b",
        "sex with",
    ),
    # TODO: Revisit - hard to tell if offen/off maps to "offender" or "offense"
    RegexSubstitution(
        "sex offender",
        rf"\b(?:sexual|sex){sep}(?:offender|offend|offndr|ofndr)\b",
        "sex offender",
    ),
    RegexSubstitution(
        "sexual predator",
        rf"\b(?:sexual|sex){sep}(?:predator|pred)\b",
        "sexual predator",
    ),
    RegexSubstitution(
        "voluntary sexual relations",
        rf"\bvol{sep}sex{sep}rel\b",
        "voluntary sexual relations",
    ),
    RegexSubstitution(
        "sex related",
        rf"\bsex{sep}(?:reltd|rel)\b",
        "sex related",
    ),
    RegexSubstitution(
        "sex related 2",
        r"\bsexreltd\b",
        "sex related",
    ),
    RegexSubstitution(
        "statutory rape",
        rf"\bstat{sep}rape\b",
        "statutory rape",
    ),
    RegexSubstitution(
        "rape first degree",
        rf"\brape{sep}(?:1|1st|i)\b",
        "rape first degree",
    ),
    RegexSubstitution(
        "rape second degree",
        rf"\brape{sep}(?:2|2nd|ii)\b",
        "rape second degree",
    ),
    RegexSubstitution(
        "rape third degree",
        rf"\brape{sep}(?:3|3rd|iii)\b",
        "rape third degree",
    ),
    RegexSubstitution(
        "sodomy first degree",
        rf"\bsodomy{sep}(?:1|1st|i)\b",
        "sodomy first degree",
    ),
    RegexSubstitution(
        "sodomy second degree",
        rf"\bsodomy{sep}(?:2|2nd|ii)\b",
        "sodomy second degree",
    ),
    RegexSubstitution(
        "sodomy third degree",
        rf"\bsodomy{sep}(?:3|3rd|iii)\b",
        "sodomy third degree",
    ),
    RegexSubstitution(
        "incest first degree",
        rf"\bincest{sep}(?:1|1st|i)\b",
        "incest first degree",
    ),
    RegexSubstitution(
        "incest second degree",
        rf"\bincest{sep}(?:2|2nd|ii)\b",
        "incest second degree",
    ),
    RegexSubstitution(
        "sex first degree",
        rf"\bsex{sep}(?:1|1st|i)\b",
        "sex first degree",
    ),
    RegexSubstitution(
        "sex second degree",
        rf"\bsex{sep}(?:2|2nd|ii)\b",
        "sex second degree",
    ),
    RegexSubstitution(
        "criminal sexual conduct first degree",
        rf"\bcsc{sep}(?:1|1st|i)\b",
        "criminal sexual conduct first degree",
        priority=5,
    ),
    RegexSubstitution(
        "criminal sexual conduct second degree",
        rf"\bcsc{sep}(?:2|2nd|ii)\b",
        "criminal sexual conduct second degree",
        priority=5,
    ),
    RegexSubstitution(
        "criminal sexual conduct third degree",
        rf"\bcsc{sep}(?:3|3rd|ii)\b",
        "criminal sexual conduct third degree",
        priority=5,
    ),
    RegexSubstitution(
        "criminal sexual conduct fourth degree",
        rf"\bcsc{sep}(?:4|4th|iv)\b",
        "criminal sexual conduct fourth degree",
        priority=5,
    ),
    RegexSubstitution(
        "sodomy",
        r"\bsod\b",
        "sodomy",
    ),
    RegexSubstitution(
        "engage sexual act",
        rf"\benga{sep}sex{sep}act\b",
        "engage sexual act",
    ),
    RegexSubstitution(
        "engage sexual act 2",
        rf"\beng{sep}sex\b",
        "engage sexual act",
    ),
    RegexSubstitution("no force", rf"\bno{sep}frc\b", "no force", priority=5),
    RegexSubstitution(
        "force or coercion",
        rf"\bfrc{sep}or{sep}coercn\b",
        "force or coercion",
        priority=5,
    ),
    RegexSubstitution(
        "coercion",
        r"\b(?:coer|coercn)\b",
        "coercion",
    ),
    RegexSubstitution(
        "position of authority",
        rf"\bpos{sep}auth\b",
        "position of authority",
        priority=4,
    ),
    RegexSubstitution(
        "position of authority 2",
        rf"\bpos{sep}of{sep}auth\b",
        "position of authority",
        priority=4,
    ),
    RegexSubstitution(
        "person in authority",
        rf"\bper{sep}aut\b",
        "person in authority",
        priority=4,
    ),
    RegexSubstitution(
        "other family",
        rf"\b(?:othr|oth|other){sep}(?:family|fam)\b",
        "other family",
        priority=4,
    ),
    RegexSubstitution(
        "immoral",
        r"\b(?:immoral|imoral|imm|imor)\b",
        "immoral",
        priority=4,
    ),
    RegexSubstitution(
        "purpose",
        r"\bpurp\b",
        "purpose",
        priority=4,
    ),
    RegexSubstitution(
        "communication with minor for immoral purpose",
        rf"\b(?:communication|comm|com){sep}(?:with|w){sep}(?:minor|min){sep}(?:immoral|imoral|imm|imor)\b",
        "communication with minor for immoral purpose",
        priority=4,
    ),
    RegexSubstitution(
        "communication with minor for immoral purpose 2",
        rf"\bcomm{sep}minor{sep}imm\b",
        "communication with minor for immoral purpose",
        priority=4,
    ),
    RegexSubstitution(
        "communication with minor",
        rf"\bcom{sep}w{sep}minor\b",
        "communication with minor",
        priority=4,
    ),
    # EMBEZZLEMENT ===
    RegexSubstitution(
        "Embezzlement",
        r"\b(?:embezzle|embezz|embez|embzzlmnt|embz)\b",
        "embezzlement",
    ),
    RegexSubstitution(
        "real estate",
        rf"\breal{sep}estat\b",
        "real estate",
    ),
    RegexSubstitution(
        "chattel",
        r"\bchatl\b",
        "chattel",
    ),
    RegexSubstitution(
        "received",
        r"\b(?:receiv|rcvd)\b",
        "received",
    ),
    RegexSubstitution(
        "mortgagor",
        r"\bmortgr\b",
        "mortgagor",
    ),
    RegexSubstitution(
        "agreement",
        r"\bagrmnt\b",
        "agreement",
    ),
    RegexSubstitution(
        "public",
        r"\b(?:pub|publ|pblc)\b",
        "public",
    ),
    RegexSubstitution(
        "behavior",
        r"\bbehav\b",
        "behavior",
    ),
    RegexSubstitution(
        "private",
        r"\bpriv\b",
        "private",
    ),
    RegexSubstitution(
        "corporation",
        r"\bcorp\b",
        "corporation",
    ),
    RegexSubstitution(
        "purchase",
        r"\bpurc\b",
        "purchase",
    ),
    # NOTE: pol may also be police - saw pol dog for example (police dog)
    RegexSubstitution(
        "political",
        r"\b(?:pol|polit|politcl)\b",
        "political",
    ),
    RegexSubstitution("police dog", rf"\bpol{sep}dog\b", "police dog", priority=5),
    RegexSubstitution(
        "payroll",
        r"\bpayrll\b",
        "payroll",
    ),
    RegexSubstitution(
        "law enforcement",
        rf"\blaw{sep}enf\b",
        "law enforcement",
    ),
    RegexSubstitution(
        "incident",
        r"\bincdnt\b",
        "incident",
    ),
    RegexSubstitution(
        "report",
        r"\brept\b",
        "report",
    ),
    RegexSubstitution(
        "transfer",
        r"\btrnsf\b",
        "transfer",
    ),
    RegexSubstitution(
        "capital assets",
        rf"\bcptl{sep}asts\b",
        "capital assets",
    ),
    RegexSubstitution(
        "clerk of court",
        rf"\bclrk{sep}of{sep}crt\b",
        "clerk of court",
    ),
    RegexSubstitution(
        "insufficient",
        r"\binsuf\b",
        "insufficient",
    ),
    RegexSubstitution(
        "corporate officer", rf"\bcorp{sep}officer\b", "corporate officer", priority=5
    ),
    RegexSubstitution(
        "institution",
        r"\b(?:instit|inst)\b",
        "institution",
    ),
    RegexSubstitution(
        "organization",
        r"\borg\b",
        "organization",
    ),
    RegexSubstitution(
        "animals",
        r"\banmls\b",
        "animals",
    ),
    RegexSubstitution(
        "animal",
        r"\banml\b",
        "animal",
    ),
    RegexSubstitution(
        "software",
        r"\bsoftwr\b",
        "software",
    ),
    RegexSubstitution(
        "transit or service bus",
        rf"\btrans{sep}serv{sep}bus\b",
        "transit or service bus",
    ),
    RegexSubstitution(
        "insurance agent",
        rf"\binsur{sep}agent\b",
        "insurance agent",
    ),
    RegexSubstitution(
        "official",
        r"\b(?:offic|offl|offcl|officl)\b",
        "official",
    ),
    RegexSubstitution(  # TODO: is 'misapp' ... misappropriation or misapplication?
        "misappropriation",
        r"\b(?:misappro|misapp)\b",
        "misappropriation",
    ),
    RegexSubstitution(
        "misapplication",
        r"\bmisapl\b",
        "misappropriation",
    ),
    RegexSubstitution(
        "fiduciary",
        r"\bfiduc\b",
        "fiduciary",
    ),
    RegexSubstitution(
        "financial",
        r"\bfinan\b",
        "financial",
    ),
    RegexSubstitution(
        "funds",
        r"\bfnds\b",
        "funds",
    ),
    # FELONY - UNSPECIFIED terms
    RegexSubstitution(
        "rendering assistance",
        rf"\brend{sep}assist\b",
        "rendering assistance",
        priority=5,
    ),
    RegexSubstitution(
        "criminal assistance",
        rf"\b(?:crim|criminal){sep}assist\b",
        "criminal assistance",
        priority=4,
    ),
    RegexSubstitution(
        "consummate",
        r"\b(?:consu|consummat)\b",
        "consummate",
        priority=4,
    ),
    RegexSubstitution(
        "deliver",
        r"\bdelive\b",
        "deliver",
        priority=4,
    ),
    RegexSubstitution(
        "to commit",
        rf"\bto{sep}comm\b",
        "to commit",
        priority=4,
    ),
    RegexSubstitution(
        "violation of",
        rf"\b(?:viol?|vio){sep}of\b",
        "violation of",
        priority=4,
    ),
    RegexSubstitution(
        "violation of civil",
        rf"\bvol?{sep}civil\b",
        "violation of civil",
        priority=4,
    ),
    RegexSubstitution("rendering", r"\brend\b", "rendering"),
    RegexSubstitution(
        "assistance first degree",
        rf"\bassistance{sep}1\b",
        "assistance first degree",
        priority=30,
    ),
    RegexSubstitution(
        "assistance second degree",
        rf"\bassistance{sep}2\b",
        "assistance second degree",
        priority=30,
    ),
    RegexSubstitution(
        "assistance third degree",
        rf"\bassistance{sep}3\b",
        "assistance third degree",
        priority=30,
    ),
    RegexSubstitution(
        "class",
        r"\bclas\b",
        "class",
    ),
    RegexSubstitution(
        "accessory",
        r"\b(?:accessry|accsry)\b",
        "accessory",
    ),
    RegexSubstitution(
        "dependency",
        r"\bdepndncy\b",
        "dependency",
    ),
    RegexSubstitution(
        "unspecified",
        r"\bunspfd\b",
        "unspecified",
    ),
    RegexSubstitution(
        "responsibility",
        r"\brespon?\b",
        "responsibility",
    ),
    RegexSubstitution(
        "classification",
        r"\bclassif\b",
        "classification",
    ),
    RegexSubstitution(
        "vice president",
        r"\bvp\b",
        "vice president",
        priority=30,
    ),
    # BRIBERY terms
    RegexSubstitution(
        "personal",
        r"\bpersona\b",
        "personal",
    ),
    RegexSubstitution(
        "assistance",
        r"\basst\b",
        "assistance",
    ),
    RegexSubstitution(
        "service",
        r"\bserv\b",
        "service",
    ),
    RegexSubstitution(
        "facilitation",
        r"\b(?:facil|fac)\b",
        "facilitation",
    ),
    RegexSubstitution(
        "smuggling",
        r"\bsmug\b",
        "smuggling",
    ),
    RegexSubstitution(
        "health",
        r"\bhlth\b",
        "health",
    ),
    # NOTE: 'off' tends to be 'offense' hence the priority on this one
    RegexSubstitution(
        "official position", rf"\boff{sep}position\b", "official position", priority=5
    ),
    RegexSubstitution(
        "participants",
        r"\bparticipnts\b",
        "participants",
    ),
    RegexSubstitution(
        "contestant",
        r"\bcntst\b",
        "contestant",
    ),
    RegexSubstitution(
        "accept",
        r"\baccpt\b",
        "accept",
    ),
    RegexSubstitution(
        "campaign contribution",
        rf"\bcamp{sep}cont\b",
        "campaign contribution",
    ),
    RegexSubstitution(
        "influence",
        r"\b(?:inflnce|influenc)\b",
        "influence",
    ),
    RegexSubstitution(
        "compensation",
        r"\bcompens\b",
        "compensation",
    ),
    RegexSubstitution(
        "treatment",
        r"\btreatm\b",
        "treatment",
    ),
    RegexSubstitution(
        "commercial bribe",
        rf"\b(?:comm|comm\'l){sep}bribe\b",
        "commercial bribe",
    ),
    RegexSubstitution(
        "false testimony",
        rf"\bfalse{sep}test\b",
        "false testimony",
    ),
    RegexSubstitution(
        "miscellaneous",
        r"\bmisc\b",
        "miscellaneous",
    ),
    RegexSubstitution(
        "impersonating",
        r"\bimpers\b",
        "impersonating",
    ),
    RegexSubstitution(
        "receiving",
        r"\brecv\b",
        "receiving",
    ),
    RegexSubstitution(
        "interfere with official process",
        rf"\binterfere{sep}w{sep}offc{sep}proc\b",
        "interfere with official process",
        priority=5,
    ),
    RegexSubstitution("public record", rf"\b(?:public|pub){sep}rec\b", "public record"),
    RegexSubstitution(
        "public servant",
        rf"\b(?:public|pub){sep}(?:servant|srv|srvnt)\b",
        "public servant",
    ),
    RegexSubstitution(  # NOTE: 'wit' also maps to 'withdraw', hence priority here
        "witness juror",
        rf"\b(?:witness|wit){sep}(?:juror|jur)\b",
        "witness juror",
        priority=5,
    ),
    RegexSubstitution(
        "umpire referee", rf"\b(?:umpire|ump){sep}(?:referee|ref)\b", "umpire referee"
    ),
    # FAMILY RELATED OFFENSES
    RegexSubstitution(
        "custody interference",
        rf"\bcust{sep}inter\b",
        "custody interference",
    ),
    RegexSubstitution(
        "custody interference second degree",
        rf"\bcust{sep}inter{sep}2\b",
        "custody interference second degree",
        priority=5,
    ),
    RegexSubstitution(
        "abandonment",
        r"\babandonmnt\b",
        "abandonment",
    ),
    RegexSubstitution(
        "unattended",
        r"\bunatt\b",
        "unattended",
    ),
    RegexSubstitution(
        "endanger",
        r"\b(?:endngr|endgr|endang)\b",
        "endanger",
    ),
    RegexSubstitution(
        "welfare",
        r"\b(?:wlfre|wlfr)\b",
        "welfare",
    ),
    RegexSubstitution(
        "endanger welfare",
        rf"\b(?:endngr|endgr|endang){sep}(?:wlfre|wlfr|wel)\b",
        "endanger welfare",
    ),
    RegexSubstitution(
        "neglect",
        r"\bneglct\b",
        "neglect",
    ),
    RegexSubstitution(
        "contribute",
        r"\bcontrib\b",
        "contribute",
    ),
    RegexSubstitution(
        "delinquincy",
        r"\b(?:dlnqncy|delinq)\b",
        "delinquincy",
    ),
    RegexSubstitution(
        "service",
        r"\bsrvc\b",
        "service",
    ),
    RegexSubstitution(
        "misrepresentation",
        r"\bmisrep\b",
        "misrepresentation",
    ),
    RegexSubstitution(
        "disabled",
        r"\bdisabld\b",
        "disabled",
    ),
    # ===
    RegexSubstitution(
        "system of records exempt",
        rf"\bsor{sep}exempt\b",
        "system of records exempt",
    ),
    RegexSubstitution(
        "type",
        r"\btyp\b",
        "type",
    ),
    RegexSubstitution(
        "misconduct",
        r"\b(?:miscond|miscon)\b",
        "misconduct",
    ),
    RegexSubstitution(
        "mischief",
        r"\bmisch\b",
        "mischief",
    ),
    RegexSubstitution(
        "probation revocation",
        rf"\bprob{sep}(?:rev|revo)\b",
        "probation revocation",
    ),
    RegexSubstitution(
        "management",
        r"\bmgmt\b",
        "management",
    ),
    RegexSubstitution(
        "subsistence",
        r"\bsubsist\b",
        "subsistence",
    ),
    RegexSubstitution(
        "penalty group",
        r"\bpg\b",
        "penalty group",
    ),
    RegexSubstitution(
        "community custody",
        r"\bcomm custody\b",
        "community custody",
    ),
    RegexSubstitution(
        "contempt",
        r"\bcntmpt\b",
        "contempt",
    ),
    RegexSubstitution(
        "counterfeit",
        r"\b(?:cntft|cntrft|cntrfeit|cnterft|contrft|contrfit)\b",
        "counterfeit",
    ),
    RegexSubstitution(
        "counts",
        r"\b(?:cts|cnts)\b",
        "counts",
    ),
    RegexSubstitution(
        "victim",
        r"\b(?:vict|vctm|vic)\b",
        "victim",
    ),
    # NUMBER TERMS ===========
    RegexSubstitution("first", r"\b1st\b", "first", priority=20),
    RegexSubstitution(
        "first degree", rf"\b(?:first|1|1st){sep}(?:dgr|dg|de|d)\b", "first degree"
    ),
    RegexSubstitution("first degree 2", r"\b1dg\b", "first degree"),
    RegexSubstitution(
        "circumstances in the first degree",
        rf"\bcircumstances{sep}1\b",
        "circumstances in the first degree",
    ),
    RegexSubstitution("second", r"\b2nd\b", "second", priority=20),
    RegexSubstitution(
        "second degree", rf"\b(?:second|2|2nd){sep}(?:dgr|dg|de|d)\b", "second degree"
    ),
    RegexSubstitution(
        "circumstances in the second degree",
        rf"\bcircumstances{sep}2\b",
        "circumstances in the second degree",
    ),
    RegexSubstitution("third", r"\b3rd\b", "third", priority=20),
    RegexSubstitution(
        "third degree", rf"\b(?:third|3|3rd){sep}(?:dgr|dg|de|d)\b", "third degree"
    ),
    RegexSubstitution(
        "circumstances in the third degree",
        rf"\bcircumstances{sep}3\b",
        "circumstances in the third degree",
    ),
    RegexSubstitution("fourth", r"\b4th\b", "fourth", priority=20),
    RegexSubstitution("fifth", r"\b5th\b", "fifth", priority=20),
    RegexSubstitution("sixth", r"\b6th\b", "sixth", priority=20),
    RegexSubstitution("seventh", r"\b7th\b", "seventh", priority=20),
    RegexSubstitution("eighth", r"\b8th\b", "eighth", priority=20),
    RegexSubstitution("ninth", r"\b9th\b", "ninth", priority=20),
    RegexSubstitution("tenth", r"\b10th\b", "tenth", priority=20),
    # SCHEDULE terms ===========
    # observed "l" for use of "i" across schedule terms
    RegexSubstitution(
        "Schedule", r"\b(?:sc?he?d?|sch|sched|schd)\b", "schedule", priority=9
    ),
    RegexSubstitution(
        "schedule one",
        rf"\bschedule{sep}(?:i|1|l)\b",
        "schedule one",
    ),
    RegexSubstitution(
        "schedule two",
        rf"\bschedule{sep}(?:ii|2|ll)\b",
        "schedule two",
    ),
    RegexSubstitution(
        "schedule three",
        rf"\bschedule{sep}(?:iii|3|lll)\b",
        "schedule three",
    ),
    RegexSubstitution(
        "schedule four",
        rf"\bschedule{sep}(?:iv|4|lv)\b",
        "schedule four",
    ),
    RegexSubstitution(
        "schedule five",
        rf"\bschedule{sep}(?:v|5)\b",
        "schedule five",
    ),
    RegexSubstitution(
        "schedule six",
        rf"\bschedule{sep}(?:vi|6|vl)\b",
        "schedule six",
    ),
    # DRIVING TERMS ===========
    RegexSubstitution(
        "driving",
        r"\bdrvg\b",
        "driving",
    ),
    RegexSubstitution(
        "driving 2",
        rf"\bdriv{sep}g\b",
        "driving",
    ),
    RegexSubstitution(
        "failure to yield",
        r"\bfty\b",
        "failure to yield",
    ),
    RegexSubstitution(
        "permit",
        r"\bperm\b",
        "permit",
    ),
    RegexSubstitution(
        "registration",
        r"\b(?:regis|registra)\b",
        "registration",
    ),
    RegexSubstitution(
        "driving under the influence",
        r"\bdui\b",
        "driving under the influence",
    ),
    RegexSubstitution(
        "driving while impaired",
        r"\bdwi\b",
        "driving while impaired",
    ),
    RegexSubstitution(
        "driving while license suspended",
        r"\bdwls\b",
        "driving while license suspended",
    ),
    RegexSubstitution(
        "driving while license revoked",
        r"\bdwlr\b",
        "driving while license revoked",
    ),
    RegexSubstitution(
        "revoked",
        r"\brevkd\b",
        "revoked",
    ),
    RegexSubstitution(
        "reckless endangerment",
        rf"\breckles{sep}endanger\b",
        "reckless endangerment",
    ),
    RegexSubstitution(
        "highway",
        rf"\bhi{sep}way\b",
        "highway",
    ),
    RegexSubstitution(
        "reckless driving",
        rf"\brek{sep}dr?\b",
        "reckless driving",
    ),
    # ========
    RegexSubstitution(
        "retail theft",
        rf"\bretail{sep}thft\b",
        "retail theft",
    ),
    RegexSubstitution(
        "impregnate girl",
        rf"\b(?:impregnate|impreg){sep}(?:girl|grl)\b",
        "impregnate girl",
    ),
    RegexSubstitution(
        "worker compensation",
        rf"\bwrkr{sep}cmp\b",
        "worker compensation",
    ),
    RegexSubstitution(
        "disregard",
        r"\bdisreg\b",
        "disregard",
    ),
    RegexSubstitution(
        "electrical appliance",
        rf"\belct{sep}appl\b",
        "electrical appliance",
    ),
    RegexSubstitution(
        "serial number",
        rf"\b(?:serial|ser){sep}(?:number|nmbr|num|nu|no)\b",
        "serial number",
    ),
    # DISTRIBUTION / FURNISH / TRAFFICK TERMS =======
    # TODO: revisit traff/traf', more likely to be traffick/ing
    # but could be traffic (cars)
    RegexSubstitution(
        "traffick",
        r"\b(?:tfk|traff|traf)\b",
        "traffick",
    ),
    # TODO: revisit adding 'dist', more likely to be distribution
    # but could be disturbance
    RegexSubstitution(
        "distribution",
        r"\b(?:distr|distrib)\b",
        "distribution",
    ),
    RegexSubstitution(
        "attempted distribution",
        rf"\b(?:at|att|attempted){sep}dist\b",
        "attempted distribution",
        priority=5,
    ),
    RegexSubstitution(
        "illegal distribution",
        rf"\billgl{sep}dist\b",
        "intent distribution",
        priority=5,
    ),
    RegexSubstitution(
        "buy distribute",
        rf"\bbuy{sep}dist\b",
        "buy distribute",
    ),
    RegexSubstitution(
        "intent distribute",
        rf"\b(?:intent|int){sep}dist\b",
        "intent distribute",
        priority=5,
    ),
    RegexSubstitution(
        "intent to distribute",
        rf"\b(?:intent|int){sep}to{sep}dist\b",
        "intent to distribute",
        priority=5,
    ),
    RegexSubstitution(
        "distribution possession",
        rf"\bdist{sep}(?:possession|possess|poss)\b",
        "distribution possession",
        priority=5,
    ),
    RegexSubstitution(
        "unauthorized distribution",
        rf"\b(?:unauthorized|unauth|unau|unauthd){sep}dist\b",
        "unauthorized distribution",
        priority=5,
    ),
    RegexSubstitution(
        "possession distribution",
        rf"\b(?:possession|possess|poss){sep}dist\b",
        "possession distribution",
        priority=5,
    ),
    RegexSubstitution(
        "unlaw distribution",
        rf"\b(?:unlawful|unlaw){sep}dist\b",
        "unlawful distribution",
        priority=5,
    ),
    RegexSubstitution(
        "distribution controlled",
        rf"\bdist{sep}(?:controlled|cntrld|cntrl|contrlld)\b",
        "distribution controlled",
        priority=5,
    ),
    RegexSubstitution(
        "distribute schedule",
        rf"\bdist{sep}(?:schedule|sch|sched)\b",
        "distribute schedule",
        priority=5,
    ),
    RegexSubstitution(
        "furnish",
        r"\b(?:furnishing|furn)\b",
        "furnish",
    ),
    # TODO: revisit adding 'man', more likely to be manufacture/ing
    # but could have other meaning
    RegexSubstitution(
        "manufacturing",
        r"\b(?:manuf|manu|mfg|manf|manfac)\b",
        "manufacturing",
    ),
    RegexSubstitution(
        "manufacturing distribution sell",
        rf"\b(?:manuf|manu|man|mfg|manf|manfac){sep}dist{sep}sell\b",
        "manufacturing distribution sell",
        priority=5,
    ),
    RegexSubstitution(
        "record sell rent distribute",
        rf"\brecord{sep}sell{sep}rent{sep}dist\b",
        "record sell rent distribute",
        priority=5,
    ),
    RegexSubstitution(
        "sell distribute",
        rf"\bsell{sep}dist\b",
        "sell distribute",
        priority=5,
    ),
    RegexSubstitution(
        "sale distribute",
        rf"\bsale{sep}dist\b",
        "sale distribute",
        priority=5,
    ),
    RegexSubstitution(
        "offer agree to distribute",
        rf"\boffer{sep}agree{sep}to{sep}dist\b",
        "offer agree distribute",
        priority=5,
    ),
    RegexSubstitution(
        "arrange to distribute",
        rf"\barrange{sep}to{sep}dist\b",
        "arrange to distribute",
        priority=5,
    ),
    RegexSubstitution(
        "arrange to distribute 2",
        rf"\barrange{sep}dist\b",
        "arrange to distribute",
        priority=5,
    ),
    RegexSubstitution(
        "controlled substance distribution",
        rf"\bcontr{sep}sub{sep}dist\b",
        "controlled substance distribution",
        priority=5,
    ),
    RegexSubstitution(
        "manufacturing deliver distribution",
        rf"\b(?:manuf|manu|man|mfg|manf){sep}del{sep}dist\b",
        "manufacturing deliver distribution",
        priority=5,
    ),
    RegexSubstitution(
        "possession distribution manufacturing",
        rf"\bposs{sep}dist{sep}manuf\b",
        "possession distribution manufacturing",
        priority=5,
    ),
    RegexSubstitution(
        "with intent to distribute",
        r"\bwitd\b",
        "with intent to distribute",
        priority=5,
    ),
    RegexSubstitution(
        "possession with intent to distribute",
        rf"\bposs{sep}(?:with|w){sep}(?:intent|int|i){sep}dist\b",
        "possession with intent to distribute",
        priority=5,
    ),
    RegexSubstitution(
        "manufacturing distribution possession",
        rf"\b(?:manuf|manu|man|mfg|manf){sep}dist{sep}(?:p|poss|pos)\b",
        "manufacturing distribution possession",
        priority=5,
    ),
    RegexSubstitution(
        "manufacturing distribution",
        rf"\b(?:manuf|manu|man|mfg|manf){sep}dist\b",
        "manufacturing distribution",
        priority=5,
    ),
    RegexSubstitution(
        "distribution obscene material",
        rf"\bdist{sep}(?:obscene|obs|obsc){sep}(?:material|mat|mtrl)\b",
        "distribution obscene material",
        priority=5,
    ),
    RegexSubstitution(
        "harmful material",
        rf"\b(?:harmful|hrmf){sep}(?:material|mat|mtrl)\b",
        "harmful material",
        priority=5,
    ),
    RegexSubstitution(
        "obscene material distribution",
        rf"\b(?:obscene|obs|obsc){sep}(?:material|mat|mtrl){sep}dist\b",
        "obscene material distribution",
        priority=5,
    ),
    RegexSubstitution(
        "material",
        r"\b(?:matrl|mat|mtrl)\b",
        "material",
        priority=5,
    ),
    RegexSubstitution(
        "distribution child porn",
        rf"\bdist{sep}child{sep}porn\b",
        "distribution child porn",
        priority=5,
    ),
    RegexSubstitution(
        "distribution controlled substances",
        rf"\bdist{sep}cds\b",
        "distribution controlled substances",
        priority=5,
    ),
    RegexSubstitution(
        "controlled substances distribution ",
        rf"\bcds{sep}dist\b",
        "controlled substances distribution ",
        priority=5,
    ),
    RegexSubstitution(
        "distribution narcotics",
        rf"\bdist{sep}narc\b",
        "distribution narcotics",
        priority=5,
    ),
    RegexSubstitution(
        "deliver or distribution",
        rf"\bdel{sep}or{sep}dist\b",
        "deliver or distribution",
        priority=5,
    ),
    RegexSubstitution(
        "criminal distribution",
        rf"\bcriminal{sep}dist\b",
        "criminal distribution",
        priority=5,
    ),
    RegexSubstitution(
        "purchase",
        r"\bpur\b",
        "purchase",
    ),
    # DRUG TERMS ===========
    RegexSubstitution(
        "marijuana",
        r"\b(?:marij|marihuana|mari|marijuan|marijua|mariju|mj)\b",
        "marijuana",
    ),
    RegexSubstitution(
        "hydrocodone",
        r"\bhydroc\b",
        "hydrocodone",
    ),
    RegexSubstitution(
        "cocaine",
        r"\b(?:cocain|coca|cocai|cocne)\b",
        "cocaine",
    ),
    RegexSubstitution(
        "crack or cocaine",
        r"\bcoc\b",
        "crack or cocaine",
    ),
    RegexSubstitution(
        "rohypnol",
        r"\brohypnl\b",
        "rohypnol",
    ),
    RegexSubstitution(
        "heroine",
        r"\bher\b",
        "heroine",
    ),
    RegexSubstitution(
        "heroine",
        r"\bher\b",
        "heroine",
    ),
    RegexSubstitution(
        "ecstasy",
        r"\bmdma\b",
        "ecstasy",
    ),
    RegexSubstitution(
        "methamphetamine",
        r"\b(?:meth|metham|methamphet|methamph)\b",
        "methamphetamine",
    ),
    RegexSubstitution(
        "paraphernalia",
        r"\b(?:para|paraph|paraphenalia|parap)\b",
        "paraphernalia",
    ),
    RegexSubstitution(
        "grams",
        r"\b(?:gr|gms|grms)\b",
        "grams",
    ),
    RegexSubstitution(
        "gram",
        r"\bgm\b",
        "gram",
    ),
    RegexSubstitution(
        "kilograms",
        r"\bkg\b",
        "kilograms",
    ),
    RegexSubstitution(
        "pounds",
        r"\blb\b",
        "pounds",
    ),
    RegexSubstitution(
        "ounces",
        r"\boz\b",
        "ounces",
    ),
    # ALCOHOL / LIQUOR terms ===========
    RegexSubstitution(
        "alcoholic beverage", r"\balc\Wbev\b", "alcoholic beverage", priority=5
    ),
    RegexSubstitution(
        "beverage",
        r"\bbev\b",
        "beverage",
    ),
    RegexSubstitution(
        "blood alcohol concentration",
        r"\bbac\b",
        "blood alcohol concentration",
    ),
    RegexSubstitution(
        "alcohol",
        r"\b(?:alc|alch|alchol|alcohl|alco|alcoh|alcoho)\b",
        "alcohol",
    ),
    RegexSubstitution(
        "over legal",
        rf"\b(?:over|ov){sep}(?:legal|leg)\b",
        "over legal",
    ),
    RegexSubstitution(
        "supply",
        r"\bsupp\b",
        "supply",
    ),
    RegexSubstitution(
        "liquor",
        r"\bliq\b",
        "liquor",
    ),
    RegexSubstitution(
        "distill",
        r"\bdstl\b",
        "distill",
    ),
    RegexSubstitution(
        "minor in possession",
        r"\bmip\b",
        "minor in possession",
    ),
    RegexSubstitution(
        "premises",
        r"\bprem\b",
        "premises",
    ),
    RegexSubstitution(
        "consume",
        r"\bcnsum\b",
        "consume",
    ),
    RegexSubstitution(
        "intoxication",
        r"\bintox\b",
        "intoxication",
    ),
    RegexSubstitution(
        "available",
        r"\bavail\b",
        "available",
    ),
    RegexSubstitution(
        "unlicensed",
        r"\bunlic\b",
        "unlicensed",
    ),
    RegexSubstitution(
        "large amount",
        rf"\blg{sep}amt\b",
        "large amount",
    ),
    RegexSubstitution(
        "small amount",
        rf"\bsm{sep}amt\b",
        "small amount",
    ),
    RegexSubstitution(
        "required",
        r"\breq\b",
        "required",
    ),
    RegexSubstitution(
        "violate prohibition",
        rf"\bvio{sep}prohibition\b",
        "violate prohibition",
    ),
    RegexSubstitution(
        "enticement",
        r"\bentcmnt\b",
        "enticement",
    ),
    # SUBSTANCE TERMS ========
    RegexSubstitution(
        "Substance",
        r"\b(?:sub|subs|substanc|substan|substnces|subtance|substa|substnc|sunstance|subst)\b",
        "substance",
        20,
    ),
    RegexSubstitution("controlled", r"\b(?:cntrld|cntrl|contrlld)\b", "controlled", 20),
    RegexSubstitution(
        "controlled dangerous substances",
        r"\bcds\b",
        "controlled dangerous substances",
    ),
    RegexSubstitution(
        "solicitation of controlled substances",
        rf"\bsol{sep}cds\b",
        "solicitation of controlled substances",
        priority=4,
    ),
    RegexSubstitution(
        "solicitation",
        r"\b(?:solct|sol|solicit|solic)\b",
        "solicitation",
    ),
    RegexSubstitution(
        "solicitation of narcotics",
        rf"\bsol{sep}narc\b",
        "solicitation of narcotics",
        priority=4,
    ),
    RegexSubstitution(
        "Controlled Substance",
        rf"\bcont?r?{sep}?subs?t?(?:\b|stance\b)",
        "controlled substance",
    ),
    RegexSubstitution(
        "Controlled Substance 2",
        r"\bc\W?s\b",
        "controlled substance",
    ),
    RegexSubstitution(
        "unlawful possession of a controlled substance",
        r"\bupcs\b",
        "unlawful possession of a controlled substance",
    ),
]


def prep_text(text):
    # Remove Commas from Numbers
    text = re.sub(r"(\d+?),(\d+?)", r"\1\2", text)
    # TODO: double check this `'s` regex
    text = re.sub(r"\b(\S+?)'(s)", r"\1\2", text)
    # replace hyphens with spaces
    text = re.sub("-", " ", text)
    # replace forward-slashes with spaces
    text = re.sub("/", " ", text)
    return text


def cleaner(text):
    if pd.isnull(text):
        return ""
    # Prepare text for regex substitions
    text = prep_text(text)
    # Do all substitutions (Case insensitive on raw text)
    substitutions_sorted = sorted(substitutions, key=lambda s: s.priority)
    for substitution in substitutions_sorted:
        text = re.sub(substitution.regex, substitution.replacement, text)
    # Remove any terms we don't want
    for removal in removals:
        text = re.sub(removal.regex, " ", text)
    # Then remove remaining punctuation
    for punct in all_punctuation:
        text = text.replace(punct, " ")
    text = " ".join(text.split())  # removes extra spaces: "  " → " "
    text = text.lower()
    return text
