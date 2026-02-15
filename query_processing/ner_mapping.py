# Basic bilingual entity dictionary
ENTITY_MAP = {
    "Bangladesh": "বাংলাদেশ",
    "Dhaka": "ঢাকা",
    "Sheikh Hasina": "শেখ হাসিনা",
    "India": "ভারত",
    "USA": "যুক্তরাষ্ট্র",
    "United States": "যুক্তরাষ্ট্র",

    # reverse mapping
    "বাংলাদেশ": "Bangladesh",
    "ঢাকা": "Dhaka",
    "ভারত": "India",
    "যুক্তরাষ্ট্র": "United States"
}

def map_named_entities(query: str) -> str:
    """
    Replace known named entities across languages.
    """

    for key, value in ENTITY_MAP.items():
        if key in query:
            query = query.replace(key, value)

    return query
