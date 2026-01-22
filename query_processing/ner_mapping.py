named_entity_map = {
    "bangladesh": "বাংলাদেশ",
    "dhaka": "ঢাকা",
    "cricket": "ক্রিকেট",
    "বাংলাদেশ": "bangladesh",
    "ঢাকা": "dhaka"
}

def map_named_entities(tokens):
    mapped = []
    for t in tokens:
        if t in named_entity_map:
            mapped.append(named_entity_map[t])
        mapped.append(t)
    return mapped
