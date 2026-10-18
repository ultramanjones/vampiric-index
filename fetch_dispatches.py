"""Fetch and persist acute HVI dispatches from Google News RSS."""

import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

SEARCHES = {
    "US": {
        "query": "United States (labor strike OR inflation OR federal debt OR protest suppression)",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "GB": {
        "query": "United Kingdom economy",
        "language": "en-GB",
        "region": "GB",
        "edition": "GB:en",
    },
    "FR": {
        "query": "France (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "FR",
        "edition": "FR:en",
    },
    "DE": {
        "query": "Germany (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "MX": {
        "query": "Mexico (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "CN": {
        "query": "China (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "JP": {
        "query": "Japan (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "IN": {
        "query": "India (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-IN",
        "region": "IN",
        "edition": "IN:en",
    },
    "IT": {
        "query": "Italy (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "IT",
        "edition": "IT:en",
    },
    "CA": {
        "query": "Canada (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-CA",
        "region": "CA",
        "edition": "CA:en",
    },
    "RU": {
        "query": "Russia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "US",
        "edition": "US:en",
    },
    "BR": {
        "query": "Brazil (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "BR",
        "edition": "BR:en",
    },
    "KR": {
        "query": "South Korea (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "KR",
        "edition": "KR:en",
    },
    "AU": {
        "query": "Australia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-AU",
        "region": "AU",
        "edition": "AU:en",
    },
    "ES": {
        "query": "Spain (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "ES",
        "edition": "ES:en",
    },
    "ID": {
        "query": "Indonesia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "ID",
        "edition": "ID:en",
    },
    "NL": {
        "query": "Netherlands (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "NL",
        "edition": "NL:en",
    },
    "TR": {
        "query": "Turkey (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "TR",
        "edition": "TR:en",
    },
    "SA": {
        "query": "Saudi Arabia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "SA",
        "edition": "SA:en",
    },
    "CH": {
        "query": "Switzerland labor OR strike OR inflation OR debt",
        "language": "en",
        "region": "CH",
        "edition": "CH:en",
    },
    "PL": {
        "query": "Poland (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "PL",
        "edition": "PL:en",
    },
    "BE": {
        "query": "Belgium inflation",
        "language": "en",
        "region": "BE",
        "edition": "BE:en",
    },
    "AR": {
        "query": "Argentina (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "AR",
        "edition": "AR:en",
    },
    "IE": {
        "query": "Ireland economy",
        "language": "en-IE",
        "region": "IE",
        "edition": "IE:en",
    },
    "SE": {
        "query": "Sweden inflation",
        "language": "en",
        "region": "SE",
        "edition": "SE:en",
    },
    "SG": {
        "query": "Singapore (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-SG",
        "region": "SG",
        "edition": "SG:en",
    },
    "AE": {
        "query": "United Arab Emirates (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "AE",
        "edition": "AE:en",
    },
    "IL": {
        "query": "Israel (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "IL",
        "edition": "IL:en",
    },
    "AT": {
        "query": "Austria inflation",
        "language": "en",
        "region": "AT",
        "edition": "AT:en",
    },
    "TH": {
        "query": "Thailand inflation",
        "language": "en",
        "region": "TH",
        "edition": "TH:en",
    },
    "NO": {
        "query": "Norway inflation",
        "language": "en",
        "region": "NO",
        "edition": "NO:en",
    },
    "VN": {
        "query": "Vietnam inflation",
        "language": "en",
        "region": "VN",
        "edition": "VN:en",
    },
    "IR": {
        "query": "Iran (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "IR",
        "edition": "IR:en",
    },
    "PH": {
        "query": "Philippines inflation",
        "language": "en",
        "region": "PH",
        "edition": "PH:en",
    },
    "BD": {
        "query": "Bangladesh (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "BD",
        "edition": "BD:en",
    },
    "DK": {
        "query": "Denmark economy",
        "language": "en",
        "region": "DK",
        "edition": "DK:en",
    },
    "MY": {
        "query": "Malaysia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "MY",
        "edition": "MY:en",
    },
    "CO": {
        "query": "Colombia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "CO",
        "edition": "CO:en",
    },
    "ZA": {
        "query": "South Africa (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-ZA",
        "region": "ZA",
        "edition": "ZA:en",
    },
    "EG": {
        "query": "Egypt (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "EG",
        "edition": "EG:en",
    },
    "RO": {
        "query": "Romania (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "RO",
        "edition": "RO:en",
    },
    "PK": {
        "query": "Pakistan (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "PK",
        "edition": "PK:en",
    },
    "CZ": {
        "query": "Czechia economy",
        "language": "en",
        "region": "CZ",
        "edition": "CZ:en",
    },
    "CL": {
        "query": "Chile economy",
        "language": "en",
        "region": "CL",
        "edition": "CL:en",
    },
    "PT": {
        "query": "Portugal (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "PT",
        "edition": "PT:en",
    },
    "FI": {
        "query": "Finland economy",
        "language": "en",
        "region": "FI",
        "edition": "FI:en",
    },
    "PE": {
        "query": "Peru economy",
        "language": "en",
        "region": "PE",
        "edition": "PE:en",
    },
    "KZ": {
        "query": "Kazakhstan (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "KZ",
        "edition": "KZ:en",
    },
    "IQ": {
        "query": "Iraq economy",
        "language": "en",
        "region": "IQ",
        "edition": "IQ:en",
    },
    "DZ": {
        "query": "Algeria economy",
        "language": "en",
        "region": "DZ",
        "edition": "DZ:en",
    },
    "NZ": {
        "query": "New Zealand (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-NZ",
        "region": "NZ",
        "edition": "NZ:en",
    },
    "GR": {
        "query": "Greece (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "GR",
        "edition": "GR:en",
    },
    "NG": {
        "query": "Nigeria (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "NG",
        "edition": "NG:en",
    },
    "HU": {
        "query": "Hungary (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "HU",
        "edition": "HU:en",
    },
    "QA": {
        "query": "Qatar debt",
        "language": "en",
        "region": "QA",
        "edition": "QA:en",
    },
    "KW": {
        "query": "Kuwait debt",
        "language": "en",
        "region": "KW",
        "edition": "KW:en",
    },
    "MA": {
        "query": "Morocco (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "MA",
        "edition": "MA:en",
    },
    "ET": {
        "query": "Ethiopia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "ET",
        "edition": "ET:en",
    },
    "SK": {
        "query": "Slovakia economy",
        "language": "en",
        "region": "SK",
        "edition": "SK:en",
    },
    "DO": {
        "query": "Dominican Republic economy",
        "language": "en",
        "region": "DO",
        "edition": "DO:en",
    },
    "EC": {
        "query": "Ecuador (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "EC",
        "edition": "EC:en",
    },
    "UZ": {
        "query": "Uzbekistan economy",
        "language": "en",
        "region": "UZ",
        "edition": "UZ:en",
    },
    "VE": {
        "query": "Venezuela (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "VE",
        "edition": "VE:en",
    },
    "KE": {
        "query": "Kenya (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "KE",
        "edition": "KE:en",
    },
    "BG": {
        "query": "Bulgaria",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "GT": {
        "query": "Guatemala",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "OM": {
        "query": "Oman",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "AO": {
        "query": "Angola",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "LK": {
        "query": "Sri Lanka (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "LK",
        "edition": "LK:en",
    },
    "CR": {
        "query": "Costa Rica economía",
        "language": "es-419",
        "region": "CR",
        "edition": "CR:es-419",
    },
    "LU": {
        "query": "Luxembourg",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "HR": {
        "query": "Croatia",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "RS": {
        "query": "Serbia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "RS",
        "edition": "RS:en",
    },
    "CI": {
        "query": "Cote d'Ivoire",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "PA": {
        "query": "Panama economy",
        "language": "en-US",
        "region": "PA",
        "edition": "PA:en",
    },
    "LT": {
        "query": "Lithuania economy",
        "language": "en-US",
        "region": "LT",
        "edition": "LT:en",
    },
    "GH": {
        "query": "Ghana economy",
        "language": "en-US",
        "region": "GH",
        "edition": "GH:en",
    },
    "UY": {
        "query": "Uruguay economy",
        "language": "en-US",
        "region": "UY",
        "edition": "UY:en",
    },
    "TZ": {
        "query": "Tanzania economy",
        "language": "en-US",
        "region": "TZ",
        "edition": "TZ:en",
    },
    "BY": {
        "query": "Belarus (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "BY",
        "edition": "BY:en",
    },
    "CD": {
        "query": "Democratic Republic of the Congo economy",
        "language": "en",
        "region": "CD",
        "edition": "CD:en",
    },
    "AZ": {
        "query": "Azerbaijan economy",
        "language": "en",
        "region": "AZ",
        "edition": "AZ:en",
    },
    "MM": {
        "query": "Myanmar (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "MM",
        "edition": "MM:en",
    },
    "SI": {
        "query": "Slovenia economy",
        "language": "en",
        "region": "SI",
        "edition": "SI:en",
    },
    "JO": {
        "query": "Jordan economy",
        "language": "en",
        "region": "JO",
        "edition": "JO:en",
    },
    "BO": {
        "query": "Bolivia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "BO",
        "edition": "BO:en",
    },
    "UG": {
        "query": "Uganda (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "UG",
        "edition": "UG:en",
    },
    "CM": {
        "query": "Cameroon economy",
        "language": "en",
        "region": "CM",
        "edition": "CM:en",
    },
    "TN": {
        "query": "Tunisia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "TN",
        "edition": "TN:en",
    },
    "LY": {
        "query": "Libya economy",
        "language": "en",
        "region": "LY",
        "edition": "LY:en",
    },
    "BH": {
        "query": "Bahrain (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "BH",
        "edition": "BH:en",
    },
    "KH": {
        "query": "Cambodia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "KH",
        "edition": "KH:en",
    },
    "PY": {
        "query": "Paraguay economy",
        "language": "en",
        "region": "PY",
        "edition": "PY:en",
    },
    "TM": {
        "query": "Turkmenistan economy",
        "language": "en",
        "region": "TM",
        "edition": "TM:en",
    },
    "LV": {
        "query": "Latvia economy",
        "language": "en",
        "region": "LV",
        "edition": "LV:en",
    },
    "NP": {
        "query": "Nepal economy",
        "language": "en",
        "region": "NP",
        "edition": "NP:en",
    },
    "EE": {
        "query": "Estonia economy",
        "language": "en",
        "region": "EE",
        "edition": "EE:en",
    },
    "ZW": {
        "query": "Zimbabwe economy",
        "language": "en",
        "region": "ZW",
        "edition": "ZW:en",
    },
    "CY": {
        "query": "Cyprus economy",
        "language": "en",
        "region": "CY",
        "edition": "CY:en",
    },
    "HN": {
        "query": "Honduras economy",
        "language": "en",
        "region": "HN",
        "edition": "HN:en",
    },
    "SV": {
        "query": "El Salvador economy",
        "language": "en",
        "region": "SV",
        "edition": "SV:en",
    },
    "GE": {
        "query": "Georgia country (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "GE",
        "edition": "GE:en",
    },
    "IS": {
        "query": "Iceland economy",
        "language": "en",
        "region": "IS",
        "edition": "IS:en",
    },
    "SN": {
        "query": "Senegal (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "SN",
        "edition": "SN:en",
    },
    "PG": {
        "query": "Papua New Guinea",
        "language": "en",
        "region": "PG",
        "edition": "PG:en",
    },
    "BA": {
        "query": "Bosnia and Herzegovina",
        "language": "en",
        "region": "BA",
        "edition": "BA:en",
    },
    "AL": {
        "query": "Albania",
        "language": "en",
        "region": "AL",
        "edition": "AL:en",
    },
    "ML": {
        "query": "Mali news",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "AM": {
        "query": "Armenia economy",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "TT": {
        "query": "\"Trinidad and Tobago\" government",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "ZM": {
        "query": "Zambia economy",
        "language": "en",
        "region": "ZM",
        "edition": "ZM:en",
    },
    "MT": {
        "query": "Malta economy",
        "language": "en",
        "region": "MT",
        "edition": "MT:en",
    },
    "GN": {
        "query": "Guinea economy",
        "language": "en",
        "region": "GN",
        "edition": "GN:en",
    },
    "GY": {
        "query": "Guyana economy",
        "language": "en",
        "region": "GY",
        "edition": "GY:en",
    },
    "HT": {
        "query": "Haiti economy",
        "language": "en",
        "region": "HT",
        "edition": "HT:en",
    },
    "MN": {
        "query": "Mongolia economy",
        "language": "en",
        "region": "MN",
        "edition": "MN:en",
    },
    "BF": {
        "query": "Burkina Faso economy",
        "language": "en",
        "region": "BF",
        "edition": "BF:en",
    },
    "MZ": {
        "query": "Mozambique economy",
        "language": "en",
        "region": "MZ",
        "edition": "MZ:en",
    },
    "JM": {
        "query": "Jamaica economy",
        "language": "en-JM",
        "region": "JM",
        "edition": "JM:en",
    },
    "BJ": {
        "query": "Benin economy",
        "language": "en",
        "region": "BJ",
        "edition": "BJ:en",
    },
    "GA": {"query": "Gabon economy", "language": "en", "region": "GA", "edition": "GA:en"},
    "TD": {"query": "Chad economy", "language": "en", "region": "TD", "edition": "TD:en"},
    "NE": {"query": "Niger economy", "language": "en", "region": "NE", "edition": "NE:en"},
    "NI": {"query": "Nicaragua economy", "language": "en", "region": "NI", "edition": "NI:en"},
    "BW": {"query": "Botswana economy", "language": "en", "region": "BW", "edition": "BW:en"},
    "MD": {"query": "Moldova economy", "language": "en", "region": "MD", "edition": "MD:en"},
    "KG": {"query": "Kyrgyzstan economy", "language": "en", "region": "KG", "edition": "KG:en"},
    "AF": {"query": "Afghanistan economy", "language": "en", "region": "AF", "edition": "AF:en"},
    "MG": {"query": "Madagascar economy", "language": "en", "region": "MG", "edition": "MG:en"},
    "MK": {"query": "North Macedonia economy", "language": "en", "region": "MK", "edition": "MK:en"},
}

# Google News search is not a structured country filter. A panel must not
# receive a generic or neighboring-country result merely because it matched a
# broad risk term, so publish only headlines that identify the country itself.
COUNTRY_TERMS = {
    "US": ("united states", "u.s.", "u.s.a.", "america", "american"),
    "CN": ("china", "chinese"),
    "DE": ("germany", "german"),
    "JP": ("japan", "japanese"),
    "IN": ("india", "indian"),
    "GB": ("united kingdom", "britain", "british", "england", "english"),
    "FR": ("france", "french", "paris"),
    "IT": ("italy", "italian", "rome"),
    "CA": ("canada", "canadian"),
    "RU": ("russia", "russian", "moscow"),
    "BR": ("brazil", "brazilian"),
    "KR": ("south korea", "korea", "korean", "seoul"),
    "MX": ("mexico", "mexican"),
    "AU": ("australia", "australian"),
    "ES": ("spain", "spanish", "madrid"),
    "ID": ("indonesia", "indonesian", "jakarta"),
    "TR": ("turkey", "turkish", "turkiye", "ankara"),
    "SA": ("saudi", "saudi arabia", "riyadh"),
    "NL": ("netherlands", "dutch", "amsterdam", "the hague"),
    "CH": ("switzerland", "swiss", "geneva", "zurich", "bern"),
    "PL": ("poland", "polish", "warsaw"),
    "BE": ("belgium", "belgian", "brussels"),
    "AR": ("argentina", "argentine", "buenos aires"),
    "IE": ("ireland", "irish", "dublin"),
    "SE": ("sweden", "swedish", "stockholm"),
    "SG": ("singapore", "singaporean"),
    "AE": ("united arab emirates", "emirati", "dubai", "abu dhabi"),
    "IL": ("israel", "israeli", "jerusalem", "tel aviv"),
    "AT": ("austria", "austrian", "vienna"),
    "TH": ("thailand", "thai", "bangkok"),
    "NO": ("norway", "norwegian", "oslo"),
    "VN": ("vietnam", "vietnamese", "hanoi", "ho chi minh"),
    "IR": ("iran", "iranian", "tehran"),
    "PH": ("philippines", "philippine", "filipino", "manila"),
    "BD": ("bangladesh", "bangladeshi", "dhaka"),
    "DK": ("denmark", "danish", "copenhagen"),
    "MY": ("malaysia", "malaysian", "kuala lumpur"),
    "CO": ("colombia", "colombian", "bogota", "bogotá"),
    "ZA": ("south africa", "south african", "pretoria", "cape town", "johannesburg"),
    "EG": ("egypt", "egyptian", "cairo"),
    "RO": ("romania", "romanian", "bucharest"),
    "PK": ("pakistan", "pakistani", "islamabad", "karachi", "lahore"),
    "CZ": ("czechia", "czech republic", "czech", "prague"),
    "CL": ("chile", "chilean", "santiago"),
    "PT": ("portugal", "portuguese", "lisbon"),
    "FI": ("finland", "finnish", "helsinki"),
    "PE": ("peru", "peruvian", "lima"),
    "KZ": ("kazakhstan", "kazakh", "astana", "almaty"),
    "IQ": ("iraq", "iraqi", "baghdad", "basra", "erbil"),
    "DZ": ("algeria", "algerian", "algiers"),
    "NZ": ("new zealand", "new zealand's", "new zealander", "wellington", "auckland"),
    "GR": ("greece", "greek", "athens"),
    "NG": ("nigeria", "nigerian", "abuja", "lagos"),
    "HU": ("hungary", "hungarian", "budapest"),
    "QA": ("qatar", "qatari", "doha"),
    "KW": ("kuwait", "kuwaiti"),
    "MA": ("morocco", "moroccan", "rabat", "casablanca"),
    "ET": ("ethiopia", "ethiopian", "addis ababa"),
    "SK": ("slovakia", "slovak", "bratislava"),
    "DO": ("dominican republic", "dominican", "santo domingo"),
    "EC": ("ecuador", "ecuadorian", "quito", "guayaquil"),
    "UZ": ("uzbekistan", "uzbek", "tashkent"),
    "VE": ("venezuela", "venezuelan", "caracas"),
    "KE": ("kenya", "kenyan", "nairobi"),
    "BG": ("bulgaria", "bulgarian", "sofia"),
    "GT": ("guatemala", "guatemalan", "guatemala city"),
    "OM": ("oman", "omani", "muscat"),
    "AO": ("angola", "angolan", "luanda"),
    "LK": ("sri lanka", "sri lankan", "colombo"),
    "CR": ("costa rica", "costa rican", "san jose", "san josé"),
    "LU": ("luxembourg", "luxembourgish"),
    "HR": ("croatia", "croatian", "zagreb"),
    "RS": ("serbia", "serbian", "belgrade"),
    "CI": ("cote d'ivoire", "côte d'ivoire", "ivory coast", "ivoirian", "abidjan"),
    "PA": ("panama", "panamanian", "panama city"),
    "LT": ("lithuania", "lithuanian", "vilnius"),
    "GH": ("ghana", "ghanaian", "accra"),
    "UY": ("uruguay", "uruguayan", "montevideo"),
    "TZ": ("tanzania", "tanzanian", "dar es salaam", "dodoma"),
    "BY": ("belarus", "belarusian", "minsk"),
    "CD": ("democratic republic of the congo", "d.r. congo", "dr congo", "congolese", "kinshasa"),
    "AZ": ("azerbaijan", "azerbaijani", "baku"),
    "MM": ("myanmar", "burmese", "yangon", "naypyidaw"),
    "SI": ("slovenia", "slovenian", "ljubljana"),
    "JO": ("jordan", "jordanian", "amman"),
    "BO": ("bolivia", "bolivian", "la paz", "sucre"),
    "UG": ("uganda", "ugandan", "kampala"),
    "CM": ("cameroon", "cameroonian", "yaounde", "yaoundé", "douala"),
    "TN": ("tunisia", "tunisian", "tunis"),
    "LY": ("libya", "libyan", "tripoli", "benghazi"),
    "BH": ("bahrain", "bahraini", "manama"),
    "KH": ("cambodia", "cambodian", "phnom penh"),
    "PY": ("paraguay", "paraguayan", "asuncion", "asunción"),
    "TM": ("turkmenistan", "turkmen", "ashgabat"),
    "LV": ("latvia", "latvian", "riga", "rīga"),
    "NP": ("nepal", "nepali", "kathmandu"),
    "EE": ("estonia", "estonian", "tallinn"),
    "ZW": ("zimbabwe", "zimbabwean", "harare"),
    "CY": ("cyprus", "cypriot", "nicosia"),
    "HN": ("honduras", "honduran", "tegucigalpa", "san pedro sula"),
    "SV": ("el salvador", "salvadoran", "san salvador"),
    "GE": ("georgia", "georgian", "tbilisi"),
    "IS": ("iceland", "icelandic", "reykjavik", "reykjavík"),
    "SN": ("senegal", "senegalese", "dakar"),
    "PG": ("papua new guinea", "papua new guinean", "port moresby"),
    "BA": ("bosnia and herzegovina", "bosnian", "sarajevo", "bih"),
    "AL": ("albania", "albanian", "tirana", "tirane"),
    "ML": ("mali", "malian", "bamako"),
    "AM": ("armenia", "armenian", "yerevan"),
    "TT": ("trinidad and tobago", "trinidad", "tobago", "port of spain"),
    "ZM": ("zambia", "zambian", "lusaka"),
    "MT": ("malta", "maltese", "valletta"),
    "GN": ("guinea", "guinean", "conakry"),
    "GY": ("guyana", "guyanese", "georgetown"),
    "HT": ("haiti", "haitian", "port-au-prince"),
    "MN": ("mongolia", "mongolian", "ulaanbaatar", "ulaan baatar"),
    "BF": ("burkina faso", "burkinabe", "ouagadougou"),
    "MZ": ("mozambique", "mozambican", "maputo"),
    "JM": ("jamaica", "jamaican", "kingston"),
    "BJ": ("benin", "beninese", "porto-novo", "cotonou"),
    "GA": ("gabon", "gabonese", "libreville"),
    "TD": ("chad", "chadian", "n'djamena", "ndjamena"),
    "NE": ("niger", "nigerien", "niamey"),
    "NI": ("nicaragua", "nicaraguan", "managua"),
    "BW": ("botswana", "botswanan", "gaborone"),
    "MD": ("moldova", "moldovan", "chisinau", "chișinău"),
    "KG": ("kyrgyzstan", "kyrgyz", "bishkek"),
    "AF": ("afghanistan", "afghan", "kabul"),
    "MG": ("madagascar", "malagasy", "antananarivo"),
    "MK": ("north macedonia", "macedonian", "skopje"),
}


def rss_url(search):
    """Build a Google News RSS URL for one country-specific acute-risk query."""
    parameters = urllib.parse.urlencode({
        "q": search["query"],
        "hl": search["language"],
        "gl": search["region"],
        "ceid": search["edition"],
    })
    return f"https://news.google.com/rss/search?{parameters}"


def article_headline(title, source):
    """Return the article headline without Google News' publisher suffix."""
    source_suffix = f" - {source}"
    return title[:-len(source_suffix)] if title.endswith(source_suffix) else title


def is_country_relevant(country_code, title, source):
    """Return whether the article headline identifies its assigned country.

    Google News appends `` - Publisher`` to titles. Strip that suffix first so
    a publisher such as France 24 cannot make unrelated Iran coverage appear in
    France's panel.
    """
    normalized_headline = article_headline(title, source).casefold()
    return any(term in normalized_headline for term in COUNTRY_TERMS[country_code])


def text_of(item, tag):
    element = item.find(tag)
    return element.text.strip() if element is not None and element.text else ""


def fetch_dispatches(country_code):
    """Return the first two usable Google News dispatches for a country."""
    search = SEARCHES[country_code]
    request = urllib.request.Request(
        rss_url(search),
        headers={"User-Agent": "VampiricIndexDispatchFetcher/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        root = ET.fromstring(response.read())

    dispatches = []
    seen_headlines = set()
    for item in root.findall("./channel/item"):
        title = text_of(item, "title")
        url = text_of(item, "link")
        publication_date = text_of(item, "pubDate")
        source = text_of(item, "source")
        if not all((title, source, publication_date, url)):
            continue
        if not is_country_relevant(country_code, title, source):
            continue
        normalized_headline = article_headline(title, source).casefold()
        if normalized_headline in seen_headlines:
            continue
        seen_headlines.add(normalized_headline)
        dispatches.append({
            "title": title,
            "source": source,
            "publication_date": publication_date,
            "url": url,
        })
        if len(dispatches) == 2:
            break
    return dispatches


def print_dispatches(countries):
    for country in countries:
        print(f"{country['country_code']} — {country['name']}")
        for dispatch in country["acute_dispatch"]:
            print(f"  - {dispatch['title']}")
            print(f"    {dispatch['source']} | {dispatch['publication_date']}")
            print(f"    {dispatch['url']}")


def main():
    path = sys.argv[1] if len(sys.argv) == 2 else "data.json"
    if len(sys.argv) > 2:
        print("Usage: python3 fetch_dispatches.py [data.json]", file=sys.stderr)
        return 2

    try:
        with open(path, encoding="utf-8") as data_file:
            payload = json.load(data_file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Unable to load {path}: {error}", file=sys.stderr)
        return 1

    countries = payload.get("countries") if isinstance(payload, dict) else None
    if not isinstance(countries, list):
        print("data.json must contain a countries array.", file=sys.stderr)
        return 1

    errors = []
    fetched = {}
    for country in countries:
        code = country.get("country_code") if isinstance(country, dict) else None
        if code not in SEARCHES:
            errors.append(f"Unsupported or missing country code: {code!r}")
            continue
        try:
            dispatches = fetch_dispatches(code)
        except (OSError, ET.ParseError) as error:
            errors.append(f"{code}: unable to fetch RSS feed: {error}")
            continue
        if not dispatches:
            errors.append(f"{code}: RSS feed contained no usable headlines")
            continue
        fetched[code] = dispatches

    if errors:
        print("Dispatch update failed; data.json was not changed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    for country in countries:
        country["acute_dispatch"] = fetched[country["country_code"]]

    try:
        with open(path, "w", encoding="utf-8") as data_file:
            json.dump(payload, data_file, indent=2, ensure_ascii=False)
            data_file.write("\n")
    except OSError as error:
        print(f"Unable to write {path}: {error}", file=sys.stderr)
        return 1

    print_dispatches(countries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
