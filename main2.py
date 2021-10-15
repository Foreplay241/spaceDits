expertise_dict = {
    "Aries": ["Health", "Ram Dash", "Fire"],
    "Taurus": ["Health", "Stronger Hull", "Earth"],
    "Gemini": ["Shield", "Twin for a min", "Air"],
    "Cancer": ["Shield", "Tidal wave blast", "Water"],
    "Leo": ["Health", "Sonic boom stun", "Fire"],
    "Virgo": ["Health", "Life after Death", "Earth"],
    "Libra": ["Shield", "Set hull_points equal to shield", "Air"],
    "Scorpio": ["Shield", "Medium Arrow angled", "Water"],
    "Sagittarius": ["Health", "Giant Arrow", "Fire"],
    "Capricorn": ["Health", "Drop Bombs", "Earth"],
    "Aquarius": ["Shield", "Extra Shields", "Air"],
    "Pisces": ["Shield", "Jet stream", "Water"]
}

for key in expertise_dict:
    print("- __" + key + "-__ Extra " + expertise_dict[key][0] +
          ", can use " + expertise_dict[key][1] +
          ", associated with " + expertise_dict[key][2])
