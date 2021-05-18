import re
from dataclasses import dataclass
from string import punctuation
import pandas as pd

all_punctuation = punctuation + "‘’·—»"
# keep in dollar signs
all_punctuation = all_punctuation.replace("$", "")


# "regex separator"
# captures the following: 1+ spaces OR 1+ non-word characters (ex: "/", "-"), OR 1 word boundary
# apply the this variable using an `fr` string in the regex substituion (ex: `fr"\bw{sep}force\b"`)
sep = "(?: +|\W+|\b)"


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
    RegexSubstitution("Less Than", fr"\b(?:&LT;|lt)\b", " less than "),
    RegexSubstitution("Less Than 2", fr"\blt(?=\d+)\b", "less than "),
    RegexSubstitution("Less Than 3", fr"\<", " less than "),
    RegexSubstitution("Greater Than", fr"\b(?:&GT;|gt|\>)\b", " greater than "),
    RegexSubstitution("Greater Than 2", fr"\bgt(?=\d+)\b", "greater than "),
    RegexSubstitution("Greater Than 3", fr"\>", " greater than "),
    # WITH terms ===========
    RegexSubstitution("With Out", fr"\bw{sep}(?:o|out)\b", "without"),
    RegexSubstitution("With Out 2", fr"\bwo\b", "without"),
    RegexSubstitution("Within", fr"\bw{sep}(?:i|in)\b", "within", priority=5),
    RegexSubstitution(
        "With Intent",
        fr"\bw{sep}\s?in?t?e?n?t?\b",
        "with intent",
    ),
    RegexSubstitution(
        "with a",
        fr"\bw{sep}a\b",
        "with a",
    ),
    RegexSubstitution(
        "with health",
        fr"\bw{sep}health\b",
        "with health",
    ),
    RegexSubstitution(
        "with own",
        fr"\bw{sep}own\b",
        "with own",
    ),
    RegexSubstitution(
        "with report",
        fr"\bw{sep}report\b",
        "with report",
    ),
    RegexSubstitution(
        "with license",
        fr"\bw{sep}license\b",
        "with license",
    ),
    RegexSubstitution(
        "with murder",
        fr"\bw{sep}murder\b",
        "with murder",
    ),
    RegexSubstitution(
        "with injury",
        fr"\bw{sep}(?:injury|inj|injry)\b",
        "with injury",
    ),
    RegexSubstitution(
        "with turned",
        fr"\bw{sep}turned\b",
        "with turned",
    ),
    RegexSubstitution(
        "with altered",
        fr"\bw{sep}alt\b",
        "with altered",
    ),
    RegexSubstitution(
        "with deadly",
        fr"\bw{sep}deadly\b",
        "with deadly",
    ),
    RegexSubstitution(
        "with dangerous weapon",
        fr"\b(?:with|w){sep}(?:dangerous|d){sep}(?:weapon|wpn|weapn|weap)\b",
        "with dangerous weapon",
        priority=5,
    ),
    RegexSubstitution(
        "with child",
        fr"\b(?:with|w){sep}(?:child|chi|chld)\b",
        "with child",
    ),
    RegexSubstitution(
        "with minor",
        fr"\bw{sep}minor\b",
        "with minor",
    ),
    RegexSubstitution(
        "with kidnapping",
        fr"\bw{sep}kidnapping\b",
        "with kidnapping",
    ),
    RegexSubstitution(
        "with agency",
        fr"\bw{sep}agency\b",
        "with agency",
    ),
    RegexSubstitution(
        "with firearm",
        fr"\bw{sep}firearm\b",
        "with firearm",
    ),
    RegexSubstitution(
        "with weapon",
        fr"\bw{sep}(?:weapon|wpn|weapn|weap)\b",
        "with weapon",
    ),
    RegexSubstitution(
        "with knife",
        fr"\bw{sep}knife\b",
        "with knife",
    ),
    RegexSubstitution(
        "with force",
        fr"\bw{sep}force\b",
        "with force",
    ),
    RegexSubstitution(
        "with extenuating circumstances",
        fr"\bw{sep}ext{sep}circumstances\b",
        "with extenuating circumstances",
    ),
    RegexSubstitution(
        "with prior",
        fr"\bw{sep}prior\b",
        "with prior",
    ),
    RegexSubstitution(
        "with previous",
        fr"\bw{sep}previous\b",
        "with previous",
    ),
    RegexSubstitution(
        "with domestic violence",
        fr"\bw{sep}dv\b",
        "with domestic violence",
    ),
    RegexSubstitution(
        "with suspended",
        fr"\bw{sep}suspended\b",
        "with suspended",
    ),
    RegexSubstitution(  # doublecheck this
        "vehicle with",
        fr"\bvehicle{sep}w{sep}",
        "vehicle with",
    ),
    RegexSubstitution(  # TODO: is this "possession with" or "possession weapon"? see concealed weapon as example
        "possession with",
        fr"\b(?:possession|possess|poss){sep}w{sep}",
        "possession with",
    ),
    RegexSubstitution(
        "possession with intent",
        fr"\bp{sep}with{sep}intent",
        "possession with intent",
        priority=30,
    ),
    RegexSubstitution(
        "neglect with",
        fr"\bneglect{sep}w{sep}",
        "neglect with",
    ),
    RegexSubstitution(
        "cooperate with",
        fr"\bcooperate{sep}w{sep}",
        "cooperate with",
    ),
    RegexSubstitution(
        "interfere with",
        fr"\b(?:inter|interfere){sep}w{sep}",
        "interfere with",
    ),
    RegexSubstitution(  # TODO consolidate tamper/tampering?
        "tamper with",
        fr"\btamper{sep}w{sep}",
        "tamper with",
    ),
    RegexSubstitution(
        "tampering with",
        fr"\btampering{sep}w{sep}",
        "tampering with",
    ),
    RegexSubstitution(
        "assault with",
        fr"\bassault{sep}w{sep}",
        "assault with",
    ),
    # FIREARM TERMS
    RegexSubstitution(
        "firearm with altered identification numbers",
        fr"\bfirearm{sep}(?:with|w){sep}alter\b",
        "firearm with altered identification numbers",
    ),
    RegexSubstitution(
        "firearm",
        fr"\bf{sep}a\b",
        "firearm",
    ),
    RegexSubstitution(
        "intimidation",
        fr"\b(?:intim|intimid)\b",
        "intimidation",
    ),
    # DOMESTIC VIOLENCE TERMS / PROTECTION / RESTRAINING ORDERS
    RegexSubstitution(
        "protective order",
        fr"\b(?:protective|protection|prot){sep}(?:order|ord|or)\b",
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
        fr"\bd{sep}v\b",
        "domestic violence",
    ),
    RegexSubstitution(
        "witness testimony",
        fr"\bwit{sep}tes\b",
        "witness testimony",
    ),
    # CONVICTION TERMS ==
    RegexSubstitution(
        "misdemeanor conviction",
        fr"\b(?:misdemeanor|misd){sep}(?:convic|conv)\b",
        "misdemeanor conviction",
    ),
    RegexSubstitution(
        "prior conviction",
        fr"\b(?:prior|pr|pri){sep}(?:convic|conv)\b",
        "prior conviction",
    ),
    # ==== GENERAL TERMS =====
    RegexSubstitution(  # NOTE: added a negative lookbehind for 'mentally' so we won't override 'mentally ill' cases
        "illegal",
        fr"\b(?<!mentally )(?:ill|illeg|illgl)\b",
        "illegal",
    ),
    RegexSubstitution("commercial fish", fr"\bcomm{sep}fish\b", "commercial fish"),
    RegexSubstitution("vessel", fr"\bvess\b", "vessel"),
    RegexSubstitution(
        "traffic control device",
        fr"\btraff{sep}control{sep}dev\b",
        "traffic control device",
    ),
    RegexSubstitution("non-culpable", fr"\bnonculp\b", "non-culpable"),
    RegexSubstitution("prohibited", fr"\bprohib\b", "prohibited"),
    RegexSubstitution("nuisance", fr"\bnuis\b", "nuisance"),
    RegexSubstitution("obstruction", fr"\bobstr\b", "obstruction"),
    RegexSubstitution("pedestrian", fr"\bped\b", "pedestrian"),
    RegexSubstitution("conduct", fr"\bcond\b", "conduct", priority=20),
    RegexSubstitution(
        "subsequent",
        fr"\bsubsq\b",
        "subsequent",
    ),
    RegexSubstitution(
        "disturbing the peace",
        fr"\bdist{sep}peace\b",
        "disturbing the peace",
    ),
    RegexSubstitution(
        "offender accountability act",
        fr"\boaa\b",
        "offender accountability act",
    ),
    RegexSubstitution(
        "against",
        fr"\b(?:agnst|agin)\b",
        "against",
    ),
    RegexSubstitution(
        "child",
        fr"\b(?:chil|chld)\b",
        "child",
    ),
    RegexSubstitution(
        "school",
        fr"\bschl\b",
        "school",
    ),
    RegexSubstitution(
        "multiple",
        fr"\bmult\b",
        "multiple",
    ),
    RegexSubstitution(
        "assailant",
        fr"\bassail\b",
        "assailant",
    ),
    RegexSubstitution(
        "public disturbance",
        fr"\b(?:public|pub|publ){sep}(?:disturbance|disturb|dist)\b",
        "public disturbance",
    ),
    RegexSubstitution(
        "interfere",
        fr"\b(?:interf|interfer)\b",
        "interfere",
    ),
    RegexSubstitution(  # TODO should we leave obstructing/obstruction separate terms or lump into obstruct?
        "obstructing",
        fr"\bob\b",
        "obstructing",
    ),
    RegexSubstitution(
        "law enforcement officer",
        fr"\bleo\b",
        "law enforcement officer",
    ),
    RegexSubstitution(
        "officer",
        fr"\b(?:offcr|ofcr)\b",
        "officer",
    ),
    RegexSubstitution(
        "minor",
        fr"\b(?:min|minr|mnr)\b",
        "minor",
    ),
    RegexSubstitution(
        "distance within 300 feet of park",
        fr"\bdist{sep}300{sep}park\b",
        "distance within 300 feet of park",
        priority=5,
    ),
    RegexSubstitution(
        "distance within 300",
        fr"{sep}dist{sep}w{sep}i{sep}300\b",
        "distance within 300",
        priority=5,
    ),
    RegexSubstitution(
        "major",
        fr"\bmajr\b",
        "major",
    ),
    RegexSubstitution(
        "willful",
        fr"\b(?:wilfl|wlfl)\b",
        "willful",
    ),
    RegexSubstitution(
        "issue worthless checks",
        fr"\b(?:issue|iss){sep}(?:worthless|wrthlss|wrtls){sep}(?:checks|cks)\b",
        "worthless",
    ),
    RegexSubstitution(
        "issue multiple worthless checks",
        fr"\b(?:issue|iss){sep}(?:multiple|mltpl){sep}(?:worthless|wrthlss|wrtls){sep}(?:checks|cks)\b",
        "worthless",
    ),
    RegexSubstitution(
        "unauthorized",
        fr"\b(?:unauth|unau|unauthd)\b",
        "unauthorized",
    ),
    RegexSubstitution(
        "child support",
        fr"\b(?:child|chld|chi){sep}(?:support|supp|sup)\b",
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
    RegexSubstitution(  # NOTE: added negative look ahead so we don't remap "at risk" to "attempted risk"
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
    RegexSubstitution(  # NOTE: removed 'con' because shows up in some DV-related text, may not be a one-size fits all regex / 'consp' to conspiracy or conspire?
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
        fr"\b(?:public|pub|publ){sep}(?:disturbance|dist)\b",
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
        fr"\belec{sep}pwr\b",
        "electric power",
    ),
    RegexSubstitution(
        "commit false", fr"\bcom?{sep}false\b", "commit false", priority=5
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
        fr"\b(?:mtr|mot){sep}(?:vehicle|veh)\b",
        "motor vehicle",
    ),
    RegexSubstitution(
        "motor vehicle 2",
        fr"\bm{sep}v\b",
        "motor vehicle",
    ),
    RegexSubstitution(
        "motor vehicle 3",
        fr"\b(?:mtv|mv)\b",
        "motor vehicle",
    ),
    RegexSubstitution("odometer", fr"\bodom\b", "odometer"),
    RegexSubstitution(
        "red light",
        fr"\bred{sep}light\b",
        "red light",
    ),
    RegexSubstitution(
        "vehicle sound system",
        fr"\bveh{sep}snd{sep}sys\b",
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
        fr"\bfem\b",
        "female",
    ),
    RegexSubstitution(
        "age female",
        fr"\bage{sep}f\b",
        "age female",
    ),
    RegexSubstitution(
        "old female",
        fr"\bold{sep}f\b",
        "old female",
    ),
    RegexSubstitution(
        "older female",
        fr"\bolder{sep}f\b",
        "older female",
    ),
    RegexSubstitution(
        "13 female",
        fr"\b13{sep}f\b",
        "13 female",
    ),
    RegexSubstitution(
        "15 female",
        fr"\b15{sep}f\b",
        "15 female",
    ),
    RegexSubstitution(
        "17 female",
        fr"\b17{sep}f\b",
        "17 female",
    ),
    # AGE / MALE
    RegexSubstitution(
        "age male",
        fr"\bage{sep}m\b",
        "age male",
    ),
    RegexSubstitution(
        "old male",
        fr"\bold{sep}m\b",
        "old male",
    ),
    RegexSubstitution(
        "older male",
        fr"\bolder{sep}m\b",
        "older male",
    ),
    RegexSubstitution(
        "13 male",
        fr"\b13{sep}m\b",
        "13 male",
    ),
    RegexSubstitution(
        "15 male",
        fr"\b15{sep}m\b",
        "15 male",
    ),
    RegexSubstitution(
        "17 male",
        fr"\b17{sep}m\b",
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
        fr"\battempted{sep}(?:rob|robb)\b",
        "attempted robbery",
    ),
    RegexSubstitution(
        "Detainer Robbery",
        fr"\bdetainer{sep}(?:rob|robb)\b",
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
        fr"\bconsp{sep}comm\b",
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
        "dangerous weapon 2", fr"\bd{sep}(?:w|wpn)\b", "dangerous weapon"
    ),
    RegexSubstitution(
        "concealed weapon", fr"\bconcealed{sep}(?:w|wpn)\b", "concealed weapon"
    ),
    # HARM terms =======
    RegexSubstitution(
        "Bodily Harm",
        fr"\b(?:bod{sep}ha?rm|bh)\b",
        "bodily harm",
    ),
    RegexSubstitution(
        "physical",
        fr"\bphy\b",
        "physical",
    ),
    RegexSubstitution(
        "harmful",
        fr"\bharmfl\b",
        "harmful",
    ),
    RegexSubstitution(
        "Great Bodily",
        fr"\b(?:gr|grt){sep}bodily\b",
        "great bodily",
    ),
    RegexSubstitution(
        "Great Bodily Injury",
        fr"\bgbi\b",
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
        fr"\bgr{sep}bod{sep}harm\b",
        "great bodily harm",
    ),
    RegexSubstitution(
        "Great Bodily Harm 2",
        fr"\bgbh\b",
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
    RegexSubstitution("election day", fr"\belec{sep}day\b", "election day"),
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
        fr"\bunder{sep}(?:infl|influ)\b",
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
        fr"\bterr{sep}(?:thre|thrts)\b",
        "terrorism threats",
    ),
    RegexSubstitution(
        "false report",
        fr"\bfals{sep}rprt\b",
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
    RegexSubstitution(  # NOTE: added negative lookahead because was seeing "by off" when updating statutory rape terms & "by offense" is not correct
        "offense",
        fr"\b(?<!by )(?:offense|offen|off|offe)\b",
        "offense",
    ),
    RegexSubstitution(
        "information",
        fr"\b(?:info|infor)\b",
        "information",
    ),
    # LEWD charge cat
    RegexSubstitution(
        "pornography",
        fr"\b(?:porn|porno)\b",
        "pornography",
    ),
    RegexSubstitution(
        "compelling",
        fr"\bcompel\b",
        "compelling",
    ),
    RegexSubstitution(
        "prostitution",
        fr"\bprostit\b",
        "prostitution",
    ),
    RegexSubstitution(
        "computer",
        fr"\bcomputr\b",
        "computer",
    ),
    RegexSubstitution(
        "incapable",
        fr"\bincap\b",
        "incapable",
    ),
    RegexSubstitution(
        "juvenile",
        fr"\b(?:juv|juven)\b",
        "juvenile",
    ),
    RegexSubstitution(
        "involving",
        fr"\b(?:involv|invlv)\b",
        "involving",
    ),
    RegexSubstitution(
        "equipment",
        fr"\bequip\b",
        "equipment",
    ),
    RegexSubstitution(
        "hazardous",
        fr"\bhaz\b",
        "hazardous",
    ),
    RegexSubstitution(  # NOTE: assault and battery unless A,B is followed by C
        "assault and battery",
        fr"\b(?:a\&b|a{sep}b|a \& b|ab)(?!c)\b",
        "assault and battery",
    ),
    RegexSubstitution(  # NOTE: assault and battery unless A,B is followed by C
        "assault and battery 2",
        fr"\b(?:a\&b|a{sep}b|a \& b|ab)(?!\Wc)\b",
        "assault and battery",
    ),
    RegexSubstitution(  # NOTE: assault and battery unless A,B is followed by C
        "assault and battery 2",
        fr"\b(?:a\&b|a{sep}b|a \& b|ab)(?! c)\b",
        "assault and battery",
    ),
    RegexSubstitution(
        "promote distribution",
        fr"\bpromote{sep}distrb\b",
        "promote distribution",
    ),
    RegexSubstitution(
        "child molestation first degree",
        fr"\b(?:child|chld|ch){sep}(?:molestation|molest|mol){sep}1\b",
        "child molestation first degree",
    ),
    RegexSubstitution(
        "child molestation second degree",
        fr"\b(?:child|chld|ch){sep}(?:molestation|molest|mol){sep}2\b",
        "child molestation second degree",
    ),
    RegexSubstitution(
        "child molestation third degree",
        fr"\b(?:child|chld|ch){sep}(?:molestation|molest|mol){sep}3\b",
        "child molestation third degree",
    ),
    RegexSubstitution(
        "child molestation",
        fr"\b(?:child|chld|ch){sep}(?:molestation|molest|mol)\b",
        "child molestation",
        priority=5,
    ),
    RegexSubstitution(
        "molestation",
        fr"\b(?:molestation|molest|mol)\b",
        "molestation",
    ),
    RegexSubstitution(
        "indecent conduct exposure",
        fr"\bind{sep}cond{sep}expos\b",
        "indecent conduct exposure",
    ),
    RegexSubstitution(
        "indecent",
        fr"\bindec\b",
        "indecent",
    ),
    RegexSubstitution(
        "indecent liberties",
        fr"\bind{sep}lib\b",
        "indecent liberties",
    ),
    RegexSubstitution(
        "moving",
        fr"\bmov\b",
        "moving",
    ),
    RegexSubstitution(
        "depiction",
        fr"\bdptn\b",
        "depiction",
    ),
    RegexSubstitution(
        "child luring",
        fr"\bchil{sep}lrng\b",
        "child luring",
    ),
    RegexSubstitution(
        "dissemination",
        fr"\b(?:dissm|dissem)\b",
        "dissemination",
    ),
    RegexSubstitution(
        "possession of depictions of minor engaged in sexually explicit conduct",
        fr"\bposs{sep}(?:depict|dep){sep}(?:minor|min){sep}eng{sep}sex{sep}(?:exp|expct){sep}conduct\b",
        "possession of depictions of minor engaged in sexually explicit conduct",
        priority=3,
    ),
    RegexSubstitution(
        "dealing of depictions of minor engaged in sexually explicit conduct",
        fr"\bdeal{sep}(?:depict|dep){sep}(?:minor|min){sep}eng{sep}sex{sep}(?:exp|expct){sep}conduct\b",
        "dealing of depictions of minor engaged in sexually explicit conduct",
        priority=3,
    ),
    RegexSubstitution(
        "viewing of depictions of minor engaged in sexually explicit conduct",
        fr"\bview{sep}(?:depict|dep){sep}(?:minor|min){sep}eng{sep}sex{sep}(?:exp|expct){sep}conduct\b",
        "viewing of depictions of minor engaged in sexually explicit conduct",
        priority=3,
    ),
    RegexSubstitution(
        "online sexual corruption of a child",
        fr"\bonline{sep}sex{sep}corrupt{sep}child\b",
        "online sexual corruption of a child",
    ),
    RegexSubstitution(
        "lewd or lascivious act",
        fr"\b(?:L\&L|L{sep}L)\b",
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
        fr"\b(?:sexual|sex){sep}(?:offense|offen|off)\b",
        "sexual offense",
    ),
    RegexSubstitution(
        "sexual offenses",
        fr"\b(?:sexual|sex){sep}(?:offense|offen|off)s\b",
        "sexual offenses",
    ),
    RegexSubstitution(
        "sexual assault",
        fr"\b(?:sexual|sex){sep}(?:assault|assult|assualt|ass|asst)\b",
        "sexual assault",
    ),
    RegexSubstitution(
        "sexual contact",
        fr"\b(?:sexual|sex){sep}(?:contact)\b",
        "sexual contact",
    ),
    RegexSubstitution(
        "sexual act",
        fr"\b(?:sexual|sex){sep}(?:act|acts)\b",
        "sexual act",
    ),
    RegexSubstitution(
        "sexual act 2",
        fr"\bsxact\b",
        "sexual act",
    ),
    RegexSubstitution(
        "sexual abuse",
        fr"\b(?:sexual|sex){sep}(?:abuse|ab)\b",
        "sexual abuse",
    ),
    RegexSubstitution(
        "commit sex abuse",
        fr"\bcomm{sep}sex{sep}abuse\b",
        "commit sex abuse",
    ),
    RegexSubstitution(
        "commit sex act",
        fr"\bcomm{sep}sex{sep}act\b",
        "commit sex act",
    ),
    RegexSubstitution(
        "commit sex abuse minor",
        fr"\bcommsexabuseminor\b",
        "commit sex abuse minor",
        priority=20,
    ),
    RegexSubstitution(
        "sexual battery",
        fr"\b(?:sexual|sex){sep}(?:battery|batt|bat)\b",
        "sexual battery",
    ),
    RegexSubstitution(  # TODO: should these actually map to "sexual misconduct"?
        "sexual conduct",
        fr"\b(?:sexual|sex){sep}(?:conduct|cndct|cond|con)\b",
        "sexual conduct",
    ),
    RegexSubstitution(
        "sexual penetration",
        fr"\b(?:sexual|sex){sep}(?:penetration|pen)\b",
        "sexual penetration",
    ),
    RegexSubstitution(  # TODO: Revisit - hard to tell if exp/expl maps to "exploitation" or "explicit"
        "sexual exploitation",
        fr"\b(?:sexual|sex){sep}(?:exploitation|exploit)\b",
        "sexual exploitation",
    ),
    RegexSubstitution(
        "sexual performance",
        fr"\b(?:sexual|sex){sep}(?:performance|perform)\b",
        "sexual performance",
    ),
    RegexSubstitution(
        "sexual imposition",
        fr"\b(?:sexual|sex){sep}(?:imposition|imp)\b",
        "sexual imposition",
    ),
    RegexSubstitution(
        "sex with",
        fr"\bsex{sep}w\b",
        "sex with",
    ),
    RegexSubstitution(  # TODO: Revisit - hard to tell if offen/off maps to "offender" or "offense"
        "sex offender",
        fr"\b(?:sexual|sex){sep}(?:offender|offend|offndr|ofndr)\b",
        "sex offender",
    ),
    RegexSubstitution(
        "sexual predator",
        fr"\b(?:sexual|sex){sep}(?:predator|pred)\b",
        "sexual predator",
    ),
    RegexSubstitution(
        "voluntary sexual relations",
        fr"\bvol{sep}sex{sep}rel\b",
        "voluntary sexual relations",
    ),
    RegexSubstitution(
        "sex related",
        fr"\bsex{sep}(?:reltd|rel)\b",
        "sex related",
    ),
    RegexSubstitution(
        "sex related 2",
        fr"\bsexreltd\b",
        "sex related",
    ),
    RegexSubstitution(
        "statutory rape",
        fr"\bstat{sep}rape\b",
        "statutory rape",
    ),
    RegexSubstitution(
        "rape first degree",
        fr"\brape{sep}(?:1|1st|i)\b",
        "rape first degree",
    ),
    RegexSubstitution(
        "rape second degree",
        fr"\brape{sep}(?:2|2nd|ii)\b",
        "rape second degree",
    ),
    RegexSubstitution(
        "rape third degree",
        fr"\brape{sep}(?:3|3rd|iii)\b",
        "rape third degree",
    ),
    RegexSubstitution(
        "sodomy first degree",
        fr"\bsodomy{sep}(?:1|1st|i)\b",
        "sodomy first degree",
    ),
    RegexSubstitution(
        "sodomy second degree",
        fr"\bsodomy{sep}(?:2|2nd|ii)\b",
        "sodomy second degree",
    ),
    RegexSubstitution(
        "sodomy third degree",
        fr"\bsodomy{sep}(?:3|3rd|iii)\b",
        "sodomy third degree",
    ),
    RegexSubstitution(
        "incest first degree",
        fr"\bincest{sep}(?:1|1st|i)\b",
        "incest first degree",
    ),
    RegexSubstitution(
        "incest second degree",
        fr"\bincest{sep}(?:2|2nd|ii)\b",
        "incest second degree",
    ),
    RegexSubstitution(
        "sex first degree",
        fr"\bsex{sep}(?:1|1st|i)\b",
        "sex first degree",
    ),
    RegexSubstitution(
        "sex second degree",
        fr"\bsex{sep}(?:2|2nd|ii)\b",
        "sex second degree",
    ),
    RegexSubstitution(
        "criminal sexual conduct first degree",
        fr"\bcsc{sep}(?:1|1st|i)\b",
        "criminal sexual conduct first degree",
        priority=5,
    ),
    RegexSubstitution(
        "criminal sexual conduct second degree",
        fr"\bcsc{sep}(?:2|2nd|ii)\b",
        "criminal sexual conduct second degree",
        priority=5,
    ),
    RegexSubstitution(
        "criminal sexual conduct third degree",
        fr"\bcsc{sep}(?:3|3rd|ii)\b",
        "criminal sexual conduct third degree",
        priority=5,
    ),
    RegexSubstitution(
        "criminal sexual conduct fourth degree",
        fr"\bcsc{sep}(?:4|4th|iv)\b",
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
        fr"\benga{sep}sex{sep}act\b",
        "engage sexual act",
    ),
    RegexSubstitution(
        "engage sexual act 2",
        fr"\beng{sep}sex\b",
        "engage sexual act",
    ),
    RegexSubstitution("no force", fr"\bno{sep}frc\b", "no force", priority=5),
    RegexSubstitution(
        "force or coercion",
        fr"\bfrc{sep}or{sep}coercn\b",
        "force or coercion",
        priority=5,
    ),
    RegexSubstitution(
        "coercion",
        fr"\b(?:coer|coercn)\b",
        "coercion",
    ),
    RegexSubstitution(
        "position of authority",
        fr"\bpos{sep}auth\b",
        "position of authority",
        priority=4,
    ),
    RegexSubstitution(
        "position of authority 2",
        fr"\bpos{sep}of{sep}auth\b",
        "position of authority",
        priority=4,
    ),
    RegexSubstitution(
        "person in authority",
        fr"\bper{sep}aut\b",
        "person in authority",
        priority=4,
    ),
    RegexSubstitution(
        "other family",
        fr"\b(?:othr|oth|other){sep}(?:family|fam)\b",
        "other family",
        priority=4,
    ),
    RegexSubstitution(
        "immoral",
        fr"\b(?:immoral|imoral|imm|imor)\b",
        "immoral",
        priority=4,
    ),
    RegexSubstitution(
        "purpose",
        fr"\bpurp\b",
        "purpose",
        priority=4,
    ),
    RegexSubstitution(
        "communication with minor for immoral purpose",
        fr"\b(?:communication|comm|com){sep}(?:with|w){sep}(?:minor|min){sep}(?:immoral|imoral|imm|imor)\b",
        "communication with minor for immoral purpose",
        priority=4,
    ),
    RegexSubstitution(
        "communication with minor for immoral purpose 2",
        fr"\bcomm{sep}minor{sep}imm\b",
        "communication with minor for immoral purpose",
        priority=4,
    ),
    RegexSubstitution(
        "communication with minor",
        fr"\bcom{sep}w{sep}minor\b",
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
        fr"\breal{sep}estat\b",
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
        fr"\b(?:pub|publ|pblc)\b",
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
        fr"\bcorp\b",
        "corporation",
    ),
    RegexSubstitution(
        "purchase",
        fr"\bpurc\b",
        "purchase",
    ),
    RegexSubstitution(  # NOTE: pol may also be police - saw pol dog for example (police dog)
        "political",
        fr"\b(?:pol|polit|politcl)\b",
        "political",
    ),
    RegexSubstitution("police dog", fr"\bpol{sep}dog\b", "police dog", priority=5),
    RegexSubstitution(
        "payroll",
        fr"\bpayrll\b",
        "payroll",
    ),
    RegexSubstitution(
        "law enforcement",
        fr"\blaw{sep}enf\b",
        "law enforcement",
    ),
    RegexSubstitution(
        "incident",
        fr"\bincdnt\b",
        "incident",
    ),
    RegexSubstitution(
        "report",
        fr"\brept\b",
        "report",
    ),
    RegexSubstitution(
        "transfer",
        fr"\btrnsf\b",
        "transfer",
    ),
    RegexSubstitution(
        "capital assets",
        fr"\bcptl{sep}asts\b",
        "capital assets",
    ),
    RegexSubstitution(
        "clerk of court",
        fr"\bclrk{sep}of{sep}crt\b",
        "clerk of court",
    ),
    RegexSubstitution(
        "insufficient",
        fr"\binsuf\b",
        "insufficient",
    ),
    RegexSubstitution(
        "corporate officer", fr"\bcorp{sep}officer\b", "corporate officer", priority=5
    ),
    RegexSubstitution(
        "institution",
        fr"\b(?:instit|inst)\b",
        "institution",
    ),
    RegexSubstitution(
        "organization",
        fr"\borg\b",
        "organization",
    ),
    RegexSubstitution(
        "animals",
        fr"\banmls\b",
        "animals",
    ),
    RegexSubstitution(
        "animal",
        fr"\banml\b",
        "animal",
    ),
    RegexSubstitution(
        "software",
        fr"\bsoftwr\b",
        "software",
    ),
    RegexSubstitution(
        "transit or service bus",
        fr"\btrans{sep}serv{sep}bus\b",
        "transit or service bus",
    ),
    RegexSubstitution(
        "insurance agent",
        fr"\binsur{sep}agent\b",
        "insurance agent",
    ),
    RegexSubstitution(
        "official",
        fr"\b(?:offic|offl|offcl|officl)\b",
        "official",
    ),
    RegexSubstitution(  # TODO: is 'misapp' ... misappropriation or misapplication?
        "misappropriation",
        fr"\b(?:misappro|misapp)\b",
        "misappropriation",
    ),
    RegexSubstitution(
        "misapplication",
        fr"\bmisapl\b",
        "misappropriation",
    ),
    RegexSubstitution(
        "fiduciary",
        fr"\bfiduc\b",
        "fiduciary",
    ),
    RegexSubstitution(
        "financial",
        fr"\bfinan\b",
        "financial",
    ),
    RegexSubstitution(
        "funds",
        fr"\bfnds\b",
        "funds",
    ),
    # FELONY - UNSPECIFIED terms
    RegexSubstitution(
        "rendering assistance",
        fr"\brend{sep}assist\b",
        "rendering assistance",
        priority=5,
    ),
    RegexSubstitution(
        "criminal assistance",
        fr"\b(?:crim|criminal){sep}assist\b",
        "criminal assistance",
        priority=4,
    ),
    RegexSubstitution(
        "consummate",
        fr"\b(?:consu|consummat)\b",
        "consummate",
        priority=4,
    ),
    RegexSubstitution(
        "deliver",
        fr"\bdelive\b",
        "deliver",
        priority=4,
    ),
    RegexSubstitution(
        "to commit",
        fr"\bto{sep}comm\b",
        "to commit",
        priority=4,
    ),
    RegexSubstitution(
        "violation of",
        fr"\b(?:viol?|vio){sep}of\b",
        "violation of",
        priority=4,
    ),
    RegexSubstitution(
        "violation of civil",
        fr"\bvol?{sep}civil\b",
        "violation of civil",
        priority=4,
    ),
    RegexSubstitution("rendering", fr"\brend\b", "rendering"),
    RegexSubstitution(
        "assistance first degree",
        fr"\bassistance{sep}1\b",
        "assistance first degree",
        priority=30,
    ),
    RegexSubstitution(
        "assistance second degree",
        fr"\bassistance{sep}2\b",
        "assistance second degree",
        priority=30,
    ),
    RegexSubstitution(
        "assistance third degree",
        fr"\bassistance{sep}3\b",
        "assistance third degree",
        priority=30,
    ),
    RegexSubstitution(
        "class",
        fr"\bclas\b",
        "class",
    ),
    RegexSubstitution(
        "accessory",
        fr"\b(?:accessry|accsry)\b",
        "accessory",
    ),
    RegexSubstitution(
        "dependency",
        fr"\bdepndncy\b",
        "dependency",
    ),
    RegexSubstitution(
        "unspecified",
        fr"\bunspfd\b",
        "unspecified",
    ),
    RegexSubstitution(
        "responsibility",
        fr"\brespon?\b",
        "responsibility",
    ),
    RegexSubstitution(
        "classification",
        fr"\bclassif\b",
        "classification",
    ),
    RegexSubstitution(
        "vice president",
        fr"\bvp\b",
        "vice president",
        priority=30,
    ),
    # BRIBERY terms
    RegexSubstitution(
        "personal",
        fr"\bpersona\b",
        "personal",
    ),
    RegexSubstitution(
        "assistance",
        fr"\basst\b",
        "assistance",
    ),
    RegexSubstitution(
        "service",
        fr"\bserv\b",
        "service",
    ),
    RegexSubstitution(
        "facilitation",
        fr"\b(?:facil|fac)\b",
        "facilitation",
    ),
    RegexSubstitution(
        "smuggling",
        fr"\bsmug\b",
        "smuggling",
    ),
    RegexSubstitution(
        "health",
        fr"\bhlth\b",
        "health",
    ),
    RegexSubstitution(  # NOTE: 'off' tends to be 'offense' hence the priority on this one
        "official position", fr"\boff{sep}position\b", "official position", priority=5
    ),
    RegexSubstitution(
        "participants",
        fr"\bparticipnts\b",
        "participants",
    ),
    RegexSubstitution(
        "contestant",
        fr"\bcntst\b",
        "contestant",
    ),
    RegexSubstitution(
        "accept",
        fr"\baccpt\b",
        "accept",
    ),
    RegexSubstitution(
        "campaign contribution",
        fr"\bcamp{sep}cont\b",
        "campaign contribution",
    ),
    RegexSubstitution(
        "influence",
        fr"\b(?:inflnce|influenc)\b",
        "influence",
    ),
    RegexSubstitution(
        "compensation",
        fr"\bcompens\b",
        "compensation",
    ),
    RegexSubstitution(
        "treatment",
        fr"\btreatm\b",
        "treatment",
    ),
    RegexSubstitution(
        "commercial bribe",
        fr"\b(?:comm|comm\'l){sep}bribe\b",
        "commercial bribe",
    ),
    RegexSubstitution(
        "false testimony",
        fr"\bfalse{sep}test\b",
        "false testimony",
    ),
    RegexSubstitution(
        "miscellaneous",
        fr"\bmisc\b",
        "miscellaneous",
    ),
    RegexSubstitution(
        "impersonating",
        fr"\bimpers\b",
        "impersonating",
    ),
    RegexSubstitution(
        "receiving",
        fr"\brecv\b",
        "receiving",
    ),
    RegexSubstitution(
        "interfere with official process",
        fr"\binterfere{sep}w{sep}offc{sep}proc\b",
        "interfere with official process",
        priority=5,
    ),
    RegexSubstitution("public record", fr"\b(?:public|pub){sep}rec\b", "public record"),
    RegexSubstitution(
        "public servant",
        fr"\b(?:public|pub){sep}(?:servant|srv|srvnt)\b",
        "public servant",
    ),
    RegexSubstitution(  # NOTE: 'wit' also maps to 'withdraw', hence priority here
        "witness juror",
        fr"\b(?:witness|wit){sep}(?:juror|jur)\b",
        "witness juror",
        priority=5,
    ),
    RegexSubstitution(
        "umpire referee", fr"\b(?:umpire|ump){sep}(?:referee|ref)\b", "umpire referee"
    ),
    # FAMILY RELATED OFFENSES
    RegexSubstitution(
        "custody interference",
        fr"\bcust{sep}inter\b",
        "custody interference",
    ),
    RegexSubstitution(
        "custody interference second degree",
        fr"\bcust{sep}inter{sep}2\b",
        "custody interference second degree",
        priority=5,
    ),
    RegexSubstitution(
        "abandonment",
        fr"\babandonmnt\b",
        "abandonment",
    ),
    RegexSubstitution(
        "unattended",
        fr"\bunatt\b",
        "unattended",
    ),
    RegexSubstitution(
        "endanger",
        fr"\b(?:endngr|endgr|endang)\b",
        "endanger",
    ),
    RegexSubstitution(
        "welfare",
        fr"\b(?:wlfre|wlfr)\b",
        "welfare",
    ),
    RegexSubstitution(
        "endanger welfare",
        fr"\b(?:endngr|endgr|endang){sep}(?:wlfre|wlfr|wel)\b",
        "endanger welfare",
    ),
    RegexSubstitution(
        "neglect",
        fr"\bneglct\b",
        "neglect",
    ),
    RegexSubstitution(
        "contribute",
        fr"\bcontrib\b",
        "contribute",
    ),
    RegexSubstitution(
        "delinquincy",
        fr"\b(?:dlnqncy|delinq)\b",
        "delinquincy",
    ),
    RegexSubstitution(
        "service",
        fr"\bsrvc\b",
        "service",
    ),
    RegexSubstitution(
        "misrepresentation",
        fr"\bmisrep\b",
        "misrepresentation",
    ),
    RegexSubstitution(
        "disabled",
        fr"\bdisabld\b",
        "disabled",
    ),
    # ===
    RegexSubstitution(
        "system of records exempt",
        fr"\bsor{sep}exempt\b",
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
        fr"\bprob{sep}(?:rev|revo)\b",
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
        "first degree", fr"\b(?:first|1|1st){sep}(?:dgr|dg|de|d)\b", "first degree"
    ),
    RegexSubstitution("first degree 2", fr"\b1dg\b", "first degree"),
    RegexSubstitution(
        "circumstances in the first degree",
        fr"\bcircumstances{sep}1\b",
        "circumstances in the first degree",
    ),
    RegexSubstitution("second", r"\b2nd\b", "second", priority=20),
    RegexSubstitution(
        "second degree", fr"\b(?:second|2|2nd){sep}(?:dgr|dg|de|d)\b", "second degree"
    ),
    RegexSubstitution(
        "circumstances in the second degree",
        fr"\bcircumstances{sep}2\b",
        "circumstances in the second degree",
    ),
    RegexSubstitution("third", r"\b3rd\b", "third", priority=20),
    RegexSubstitution(
        "third degree", fr"\b(?:third|3|3rd){sep}(?:dgr|dg|de|d)\b", "third degree"
    ),
    RegexSubstitution(
        "circumstances in the third degree",
        fr"\bcircumstances{sep}3\b",
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
        fr"\bschedule{sep}(?:i|1|l)\b",
        "schedule one",
    ),
    RegexSubstitution(
        "schedule two",
        fr"\bschedule{sep}(?:ii|2|ll)\b",
        "schedule two",
    ),
    RegexSubstitution(
        "schedule three",
        fr"\bschedule{sep}(?:iii|3|lll)\b",
        "schedule three",
    ),
    RegexSubstitution(
        "schedule four",
        fr"\bschedule{sep}(?:iv|4|lv)\b",
        "schedule four",
    ),
    RegexSubstitution(
        "schedule five",
        fr"\bschedule{sep}(?:v|5)\b",
        "schedule five",
    ),
    RegexSubstitution(
        "schedule six",
        fr"\bschedule{sep}(?:vi|6|vl)\b",
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
        fr"\bdriv{sep}g\b",
        "driving",
    ),
    RegexSubstitution(
        "failure to yield",
        fr"\bfty\b",
        "failure to yield",
    ),
    RegexSubstitution(
        "permit",
        fr"\bperm\b",
        "permit",
    ),
    RegexSubstitution(
        "registration",
        fr"\b(?:regis|registra)\b",
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
        fr"\breckles{sep}endanger\b",
        "reckless endangerment",
    ),
    RegexSubstitution(
        "highway",
        fr"\bhi{sep}way\b",
        "highway",
    ),
    RegexSubstitution(
        "reckless driving",
        fr"\brek{sep}dr?\b",
        "reckless driving",
    ),
    # ========
    RegexSubstitution(
        "retail theft",
        fr"\bretail{sep}thft\b",
        "retail theft",
    ),
    RegexSubstitution(
        "impregnate girl",
        fr"\b(?:impregnate|impreg){sep}(?:girl|grl)\b",
        "impregnate girl",
    ),
    RegexSubstitution(
        "worker compensation",
        fr"\bwrkr{sep}cmp\b",
        "worker compensation",
    ),
    RegexSubstitution(
        "disregard",
        fr"\bdisreg\b",
        "disregard",
    ),
    RegexSubstitution(
        "electrical appliance",
        fr"\belct{sep}appl\b",
        "electrical appliance",
    ),
    RegexSubstitution(
        "serial number",
        fr"\b(?:serial|ser){sep}(?:number|nmbr|num|nu|no)\b",
        "serial number",
    ),
    # DISTRIBUTION / FURNISH / TRAFFICK TERMS =======
    RegexSubstitution(  # TODO: revisit traff/traf', more likely to be traffick/ing but could be traffic (cars)
        "traffick",
        r"\b(?:tfk|traff|traf)\b",
        "traffick",
    ),
    RegexSubstitution(  # TODO: revisit adding 'dist', more likely to be distribution but could be disturbance
        "distribution",
        r"\b(?:distr|distrib)\b",
        "distribution",
    ),
    RegexSubstitution(
        "attempted distribution",
        fr"\b(?:at|att|attempted){sep}dist\b",
        "attempted distribution",
        priority=5,
    ),
    RegexSubstitution(
        "illegal distribution",
        fr"\billgl{sep}dist\b",
        "intent distribution",
        priority=5,
    ),
    RegexSubstitution(
        "buy distribute",
        fr"\bbuy{sep}dist\b",
        "buy distribute",
    ),
    RegexSubstitution(
        "intent distribute",
        fr"\b(?:intent|int){sep}dist\b",
        "intent distribute",
        priority=5,
    ),
    RegexSubstitution(
        "intent to distribute",
        fr"\b(?:intent|int){sep}to{sep}dist\b",
        "intent to distribute",
        priority=5,
    ),
    RegexSubstitution(
        "distribution possession",
        fr"\bdist{sep}(?:possession|possess|poss)\b",
        "distribution possession",
        priority=5,
    ),
    RegexSubstitution(
        "unauthorized distribution",
        fr"\b(?:unauthorized|unauth|unau|unauthd){sep}dist\b",
        "unauthorized distribution",
        priority=5,
    ),
    RegexSubstitution(
        "possession distribution",
        fr"\b(?:possession|possess|poss){sep}dist\b",
        "possession distribution",
        priority=5,
    ),
    RegexSubstitution(
        "unlaw distribution",
        fr"\b(?:unlawful|unlaw){sep}dist\b",
        "unlawful distribution",
        priority=5,
    ),
    RegexSubstitution(
        "distribution controlled",
        fr"\bdist{sep}(?:controlled|cntrld|cntrl|contrlld)\b",
        "distribution controlled",
        priority=5,
    ),
    RegexSubstitution(
        "distribute schedule",
        fr"\bdist{sep}(?:schedule|sch|sched)\b",
        "distribute schedule",
        priority=5,
    ),
    RegexSubstitution(
        "furnish",
        r"\b(?:furnishing|furn)\b",
        "furnish",
    ),
    RegexSubstitution(  # TODO: revisit adding 'man', more likely to be manufacture/ing but could have other meaning
        "manufacturing",
        r"\b(?:manuf|manu|mfg|manf|manfac)\b",
        "manufacturing",
    ),
    RegexSubstitution(
        "manufacturing distribution sell",
        fr"\b(?:manuf|manu|man|mfg|manf|manfac){sep}dist{sep}sell\b",
        "manufacturing distribution sell",
        priority=5,
    ),
    RegexSubstitution(
        "record sell rent distribute",
        fr"\brecord{sep}sell{sep}rent{sep}dist\b",
        "record sell rent distribute",
        priority=5,
    ),
    RegexSubstitution(
        "sell distribute",
        fr"\bsell{sep}dist\b",
        "sell distribute",
        priority=5,
    ),
    RegexSubstitution(
        "sale distribute",
        fr"\bsale{sep}dist\b",
        "sale distribute",
        priority=5,
    ),
    RegexSubstitution(
        "offer agree to distribute",
        fr"\boffer{sep}agree{sep}to{sep}dist\b",
        "offer agree distribute",
        priority=5,
    ),
    RegexSubstitution(
        "arrange to distribute",
        fr"\barrange{sep}to{sep}dist\b",
        "arrange to distribute",
        priority=5,
    ),
    RegexSubstitution(
        "arrange to distribute 2",
        fr"\barrange{sep}dist\b",
        "arrange to distribute",
        priority=5,
    ),
    RegexSubstitution(
        "controlled substance distribution",
        fr"\bcontr{sep}sub{sep}dist\b",
        "controlled substance distribution",
        priority=5,
    ),
    RegexSubstitution(
        "manufacturing deliver distribution",
        fr"\b(?:manuf|manu|man|mfg|manf){sep}del{sep}dist\b",
        "manufacturing deliver distribution",
        priority=5,
    ),
    RegexSubstitution(
        "possession distribution manufacturing",
        fr"\bposs{sep}dist{sep}manuf\b",
        "possession distribution manufacturing",
        priority=5,
    ),
    RegexSubstitution(
        "with intent to distribute",
        fr"\bwitd\b",
        "with intent to distribute",
        priority=5,
    ),
    RegexSubstitution(
        "possession with intent to distribute",
        fr"\bposs{sep}(?:with|w){sep}(?:intent|int|i){sep}dist\b",
        "possession with intent to distribute",
        priority=5,
    ),
    RegexSubstitution(
        "manufacturing distribution possession",
        fr"\b(?:manuf|manu|man|mfg|manf){sep}dist{sep}(?:p|poss|pos)\b",
        "manufacturing distribution possession",
        priority=5,
    ),
    RegexSubstitution(
        "manufacturing distribution",
        fr"\b(?:manuf|manu|man|mfg|manf){sep}dist\b",
        "manufacturing distribution",
        priority=5,
    ),
    RegexSubstitution(
        "distribution obscene material",
        fr"\bdist{sep}(?:obscene|obs|obsc){sep}(?:material|mat|mtrl)\b",
        "distribution obscene material",
        priority=5,
    ),
    RegexSubstitution(
        "harmful material",
        fr"\b(?:harmful|hrmf){sep}(?:material|mat|mtrl)\b",
        "harmful material",
        priority=5,
    ),
    RegexSubstitution(
        "obscene material distribution",
        fr"\b(?:obscene|obs|obsc){sep}(?:material|mat|mtrl){sep}dist\b",
        "obscene material distribution",
        priority=5,
    ),
    RegexSubstitution(
        "material",
        fr"\b(?:matrl|mat|mtrl)\b",
        "material",
        priority=5,
    ),
    RegexSubstitution(
        "distribution child porn",
        fr"\bdist{sep}child{sep}porn\b",
        "distribution child porn",
        priority=5,
    ),
    RegexSubstitution(
        "distribution controlled substances",
        fr"\bdist{sep}cds\b",
        "distribution controlled substances",
        priority=5,
    ),
    RegexSubstitution(
        "controlled substances distribution ",
        fr"\bcds{sep}dist\b",
        "controlled substances distribution ",
        priority=5,
    ),
    RegexSubstitution(
        "distribution narcotics",
        fr"\bdist{sep}narc\b",
        "distribution narcotics",
        priority=5,
    ),
    RegexSubstitution(
        "deliver or distribution",
        fr"\bdel{sep}or{sep}dist\b",
        "deliver or distribution",
        priority=5,
    ),
    RegexSubstitution(
        "criminal distribution",
        fr"\bcriminal{sep}dist\b",
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
        fr"\b(?:over|ov){sep}(?:legal|leg)\b",
        "over legal",
    ),
    RegexSubstitution(
        "supply",
        fr"\bsupp\b",
        "supply",
    ),
    RegexSubstitution(
        "liquor",
        fr"\bliq\b",
        "liquor",
    ),
    RegexSubstitution(
        "distill",
        r"\bdstl\b",
        "distill",
    ),
    RegexSubstitution(
        "minor in possession",
        fr"\bmip\b",
        "minor in possession",
    ),
    RegexSubstitution(
        "premises",
        fr"\bprem\b",
        "premises",
    ),
    RegexSubstitution(
        "consume",
        fr"\bcnsum\b",
        "consume",
    ),
    RegexSubstitution(
        "intoxication",
        fr"\bintox\b",
        "intoxication",
    ),
    RegexSubstitution(
        "available",
        fr"\bavail\b",
        "available",
    ),
    RegexSubstitution(
        "unlicensed",
        fr"\bunlic\b",
        "unlicensed",
    ),
    RegexSubstitution(
        "large amount",
        fr"\blg{sep}amt\b",
        "large amount",
    ),
    RegexSubstitution(
        "small amount",
        fr"\bsm{sep}amt\b",
        "small amount",
    ),
    RegexSubstitution(
        "required",
        fr"\breq\b",
        "required",
    ),
    RegexSubstitution(
        "violate prohibition",
        fr"\bvio{sep}prohibition\b",
        "violate prohibition",
    ),
    RegexSubstitution(
        "enticement",
        fr"\bentcmnt\b",
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
        fr"\bsol{sep}cds\b",
        "solicitation of controlled substances",
        priority=4,
    ),
    RegexSubstitution(
        "solicitation",
        fr"\b(?:solct|sol|solicit|solic)\b",
        "solicitation",
    ),
    RegexSubstitution(
        "solicitation of narcotics",
        fr"\bsol{sep}narc\b",
        "solicitation of narcotics",
        priority=4,
    ),
    RegexSubstitution(
        "Controlled Substance",
        fr"\bcont?r?{sep}?subs?t?(?:\b|stance\b)",
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
