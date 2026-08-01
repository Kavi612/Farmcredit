"""Enums, colors, and form defaults for the farmer UI."""

from __future__ import annotations

STATES = ["AP", "BR", "GJ", "HR", "KA", "MH", "MP", "PB", "RJ", "TG", "TN", "UP"]

STATE_NAMES = {
    "AP": "Andhra Pradesh",
    "BR": "Bihar",
    "GJ": "Gujarat",
    "HR": "Haryana",
    "KA": "Karnataka",
    "MH": "Maharashtra",
    "MP": "Madhya Pradesh",
    "PB": "Punjab",
    "RJ": "Rajasthan",
    "TG": "Telangana",
    "TN": "Tamil Nadu",
    "UP": "Uttar Pradesh",
}

DISTRICTS_BY_STATE: dict[str, list[str]] = {
    "AP": ["AP-Coastal", "AP-Rayalaseema", "AP-Upland"],
    "BR": ["BR-Gangetic", "BR-North", "BR-South"],
    "GJ": ["GJ-Central", "GJ-North", "GJ-Saurashtra", "GJ-South"],
    "HR": ["HR-East", "HR-South", "HR-West"],
    "KA": ["KA-Central", "KA-Coastal", "KA-North", "KA-South"],
    "MH": ["MH-Konkan", "MH-Marathwada", "MH-Vidarbha", "MH-Western"],
    "MP": ["MP-Bundelkhand", "MP-Chambal", "MP-Mahakoshal", "MP-Malwa"],
    "PB": ["PB-Doaba", "PB-Majha", "PB-Malwa"],
    "RJ": ["RJ-Hadoti", "RJ-Marwar", "RJ-Mewar", "RJ-Shekhawati"],
    "TG": ["TG-Central", "TG-North", "TG-South"],
    "TN": ["TN-Delta", "TN-North", "TN-South", "TN-West"],
    "UP": ["UP-Bundelkhand", "UP-Central", "UP-Eastern", "UP-Western"],
}

CROPS = [
    "Cotton",
    "Groundnut",
    "Maize",
    "Millet",
    "Mustard",
    "Pulses",
    "Rice",
    "Soybean",
    "Sugarcane",
    "Wheat",
]

SEASONS = ["Kharif", "Rabi"]
SOILS = ["Alluvial", "Black", "ClayLoam", "Laterite", "Red", "Sandy"]
IRRIGATION = ["Canal", "Drip", "Rainfed", "Tubewell"]

RISK_COLORS = {
    "Low": "#2e7d32",
    "Medium": "#f9a825",
    "High": "#ef6c00",
    "Critical": "#c62828",
}

RISK_BG = {
    "Low": "#e8f5e9",
    "Medium": "#fff8e1",
    "High": "#fff3e0",
    "Critical": "#ffebee",
}

DEFAULT_FEATURES = {
    "state": "MH",
    "district": "MH-Vidarbha",
    "crop_type": "Soybean",
    "season": "Kharif",
    "land_size_ha": 1.2,
    "soil_type": "Black",
    "rainfall_mm": 780.0,
    "irrigation_type": "Tubewell",
    "loan_amount_inr": 180000,
    "prior_loan_count": 2,
    "prior_default_flag": 0,
    "repayment_score": 62.0,
    "annual_income_inr": 165000,
    "existing_debt_inr": 70000,
}
