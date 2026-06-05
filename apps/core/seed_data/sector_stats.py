# apps/core/seed_data/sector_stats.py

SECTOR_STATS = [
    # Agriculture
    {"sector_name": "Agriculture", "label": "Market Size", "value": 2.4, "unit": "D", "year": 2024, "is_headline": True, "display_order": 1},
    {"sector_name": "Agriculture", "label": "Annual Growth Rate", "value": 12, "unit": "%", "year": 2024, "is_headline": True, "display_order": 2},
    {"sector_name": "Agriculture", "label": "Total Businesses", "value": 3200, "unit": "number", "year": 2024, "is_headline": True, "display_order": 3},
    {"sector_name": "Agriculture", "label": "Employment in Sector", "value": 45000, "unit": "number", "year": 2024, "is_headline": False, "display_order": 4},
    {"sector_name": "Agriculture", "label": "Average Household Spend (Food)", "value": 500, "unit": "D", "year": 2024, "is_headline": False, "display_order": 5},
    {"sector_name": "Agriculture", "label": "Export Value", "value": 850, "unit": "D", "year": 2024, "is_headline": False, "display_order": 6},
    {"sector_name": "Agriculture", "label": "Import Dependency (Poultry)", "value": 65, "unit": "%", "year": 2024, "is_headline": False, "display_order": 7},
    {"sector_name": "Agriculture", "label": "Youth Employment Rate", "value": 32, "unit": "%", "year": 2024, "is_headline": False, "display_order": 8},
    {"sector_name": "Agriculture", "label": "Market Size", "value": 1.8, "unit": "D", "year": 2022, "is_headline": False, "display_order": 1},
    {"sector_name": "Agriculture", "label": "Market Size", "value": 2.1, "unit": "D", "year": 2023, "is_headline": False, "display_order": 1},

    # Transportation & Logistics
    {"sector_name": "Transportation & Logistics", "label": "Market Size", "value": 1.2, "unit": "D", "year": 2024, "is_headline": True, "display_order": 1},
    {"sector_name": "Transportation & Logistics", "label": "Annual Growth Rate", "value": 8, "unit": "%", "year": 2024, "is_headline": True, "display_order": 2},
    {"sector_name": "Transportation & Logistics", "label": "Total Businesses", "value": 2500, "unit": "number", "year": 2024, "is_headline": True, "display_order": 3},
    {"sector_name": "Transportation & Logistics", "label": "Average Monthly Spend on Transport", "value": 450, "unit": "D", "year": 2024, "is_headline": False, "display_order": 4},
    {"sector_name": "Transportation & Logistics", "label": "Active Taxis (GBA)", "value": 2800, "unit": "number", "year": 2024, "is_headline": False, "display_order": 5},
    {"sector_name": "Transportation & Logistics", "label": "Tourist Transport Revenue", "value": 350, "unit": "D", "year": 2024, "is_headline": False, "display_order": 6},
    {"sector_name": "Transportation & Logistics", "label": "Market Size", "value": 0.95, "unit": "D", "year": 2022, "is_headline": False, "display_order": 1},
    {"sector_name": "Transportation & Logistics", "label": "Market Size", "value": 1.08, "unit": "D", "year": 2023, "is_headline": False, "display_order": 1},

    # Renewable Energy
    {"sector_name": "Renewable Energy", "label": "Market Size", "value": 0.35, "unit": "D", "year": 2024, "is_headline": True, "display_order": 1},
    {"sector_name": "Renewable Energy", "label": "Annual Growth Rate", "value": 25, "unit": "%", "year": 2024, "is_headline": True, "display_order": 2},
    {"sector_name": "Renewable Energy", "label": "Total Businesses", "value": 85, "unit": "number", "year": 2024, "is_headline": True, "display_order": 3},
    {"sector_name": "Renewable Energy", "label": "Solar Installations (2024)", "value": 3200, "unit": "number", "year": 2024, "is_headline": False, "display_order": 4},
    {"sector_name": "Renewable Energy", "label": "NAWEC Grid Reliability", "value": 65, "unit": "%", "year": 2024, "is_headline": False, "display_order": 5},
    {"sector_name": "Renewable Energy", "label": "Government Renewable Target", "value": 30, "unit": "%", "year": 2030, "is_headline": False, "display_order": 6},
    {"sector_name": "Renewable Energy", "label": "Market Size", "value": 0.18, "unit": "D", "year": 2022, "is_headline": False, "display_order": 1},
    {"sector_name": "Renewable Energy", "label": "Market Size", "value": 0.26, "unit": "D", "year": 2023, "is_headline": False, "display_order": 1},

    # Financial Services
    {"sector_name": "Financial Services", "label": "Mobile Money Users", "value": 1800000, "unit": "number", "year": 2024, "is_headline": True, "display_order": 1},
    {"sector_name": "Financial Services", "label": "Bank Penetration Rate", "value": 35, "unit": "%", "year": 2024, "is_headline": True, "display_order": 2},
    {"sector_name": "Financial Services", "label": "Total Banks", "value": 14, "unit": "number", "year": 2024, "is_headline": False, "display_order": 3},

    # Technology & IT
    {"sector_name": "Technology & IT", "label": "Internet Penetration", "value": 45, "unit": "%", "year": 2024, "is_headline": True, "display_order": 1},
    {"sector_name": "Technology & IT", "label": "Mobile Subscriptions", "value": 2800000, "unit": "number", "year": 2024, "is_headline": True, "display_order": 2},
    {"sector_name": "Technology & IT", "label": "Active Tech Hubs", "value": 8, "unit": "number", "year": 2024, "is_headline": False, "display_order": 3},

    # Tourism & Hospitality
    {"sector_name": "Tourism & Hospitality", "label": "Annual Tourist Arrivals", "value": 200000, "unit": "number", "year": 2024, "is_headline": True, "display_order": 1},
    {"sector_name": "Tourism & Hospitality", "label": "Average Hotel Occupancy", "value": 65, "unit": "%", "year": 2024, "is_headline": True, "display_order": 2},
    {"sector_name": "Tourism & Hospitality", "label": "Total Hotels", "value": 120, "unit": "number", "year": 2024, "is_headline": False, "display_order": 3},
    {"sector_name": "Tourism & Hospitality", "label": "Tourism Revenue", "value": 150, "unit": "D", "year": 2024, "is_headline": False, "display_order": 4},

    # Healthcare & Pharmaceuticals
    {"sector_name": "Healthcare & Pharmaceuticals", "label": "Number of Clinics", "value": 85, "unit": "number", "year": 2024, "is_headline": True, "display_order": 1},
    {"sector_name": "Healthcare & Pharmaceuticals", "label": "Pharmacy Density", "value": 45, "unit": "number", "year": 2024, "is_headline": False, "display_order": 2},
    {"sector_name": "Healthcare & Pharmaceuticals", "label": "Health Insurance Penetration", "value": 12, "unit": "%", "year": 2024, "is_headline": False, "display_order": 3},

    # Retail & Commerce
    {"sector_name": "Retail & Commerce", "label": "Number of Supermarkets", "value": 35, "unit": "number", "year": 2024, "is_headline": True, "display_order": 1},
    {"sector_name": "Retail & Commerce", "label": "E-commerce Growth Rate", "value": 25, "unit": "%", "year": 2024, "is_headline": True, "display_order": 2},
    {"sector_name": "Retail & Commerce", "label": "Average Monthly Spend", "value": 800, "unit": "D", "year": 2024, "is_headline": False, "display_order": 3},
]
