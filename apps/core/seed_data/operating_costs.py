"""
Operating costs seed data - UPDATED for new schema
Uses period_number, period_type, cost_category instead of week_range and feed_* fields
"""

OPERATING_COSTS = [
    # Poultry - Small Scale - Cycle 1
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "year": 2024,
        "period_number": 1,
        "period_type": "cycle",
        "costs": [
            {"category": "feed_starter", "amount": 4500},
            {"category": "utilities", "amount": 300},
            {"category": "water", "amount": 200},
            {"category": "medication", "amount": 400},
            {"category": "labor", "amount": 0},
            {"category": "transport_misc", "amount": 200},
        ]
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "year": 2024,
        "period_number": 2,
        "period_type": "cycle",
        "costs": [
            {"category": "feed_grower", "amount": 5800},
            {"category": "utilities", "amount": 300},
            {"category": "water", "amount": 200},
            {"category": "medication", "amount": 300},
            {"category": "labor", "amount": 0},
            {"category": "transport_misc", "amount": 200},
        ]
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "year": 2024,
        "period_number": 3,
        "period_type": "cycle",
        "costs": [
            {"category": "feed_finisher", "amount": 6200},
            {"category": "utilities", "amount": 300},
            {"category": "water", "amount": 200},
            {"category": "medication", "amount": 250},
            {"category": "labor", "amount": 0},
            {"category": "transport_misc", "amount": 250},
        ]
    },
    
    # Poultry - Medium Scale - Cycle 1
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "year": 2024,
        "period_number": 1,
        "period_type": "cycle",
        "costs": [
            {"category": "feed_starter", "amount": 22500},
            {"category": "utilities", "amount": 1000},
            {"category": "water", "amount": 500},
            {"category": "medication", "amount": 1500},
            {"category": "labor", "amount": 3000},
            {"category": "transport_misc", "amount": 800},
        ]
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "year": 2024,
        "period_number": 2,
        "period_type": "cycle",
        "costs": [
            {"category": "feed_grower", "amount": 29000},
            {"category": "utilities", "amount": 1000},
            {"category": "water", "amount": 500},
            {"category": "medication", "amount": 1000},
            {"category": "labor", "amount": 3000},
            {"category": "transport_misc", "amount": 800},
        ]
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "year": 2024,
        "period_number": 3,
        "period_type": "cycle",
        "costs": [
            {"category": "feed_finisher", "amount": 31000},
            {"category": "utilities", "amount": 1000},
            {"category": "water", "amount": 500},
            {"category": "medication", "amount": 800},
            {"category": "labor", "amount": 3000},
            {"category": "transport_misc", "amount": 1000},
        ]
    },
    
    # Poultry - Large Scale - Cycle 1
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "large",
        "year": 2024,
        "period_number": 1,
        "period_type": "cycle",
        "costs": [
            {"category": "feed_starter", "amount": 90000},
            {"category": "utilities", "amount": 3500},
            {"category": "water", "amount": 1500},
            {"category": "medication", "amount": 5000},
            {"category": "labor", "amount": 12000},
            {"category": "transport_misc", "amount": 3000},
        ]
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "large",
        "year": 2024,
        "period_number": 2,
        "period_type": "cycle",
        "costs": [
            {"category": "feed_grower", "amount": 116000},
            {"category": "utilities", "amount": 3500},
            {"category": "water", "amount": 1500},
            {"category": "medication", "amount": 3500},
            {"category": "labor", "amount": 12000},
            {"category": "transport_misc", "amount": 3000},
        ]
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "large",
        "year": 2024,
        "period_number": 3,
        "period_type": "cycle",
        "costs": [
            {"category": "feed_finisher", "amount": 124000},
            {"category": "utilities", "amount": 3500},
            {"category": "water", "amount": 1500},
            {"category": "medication", "amount": 3000},
            {"category": "labor", "amount": 12000},
            {"category": "transport_misc", "amount": 4000},
        ]
    },
    
    # Taxi Services - Small Scale (Monthly)
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "year": 2024,
        "period_number": 1,
        "period_type": "month",
        "costs": [
            {"category": "fuel", "amount": 15000},
            {"category": "maintenance", "amount": 3000},
            {"category": "insurance", "amount": 5000},
            {"category": "licensing", "amount": 2000},
            {"category": "labor", "amount": 0},
        ]
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "medium",
        "year": 2024,
        "period_number": 1,
        "period_type": "month",
        "costs": [
            {"category": "fuel", "amount": 60000},
            {"category": "maintenance", "amount": 10000},
            {"category": "insurance", "amount": 15000},
            {"category": "licensing", "amount": 5000},
            {"category": "labor", "amount": 15000},
        ]
    },
    
    # Solar Installation - Medium Scale (Monthly)
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "medium",
        "year": 2024,
        "period_number": 1,
        "period_type": "month",
        "costs": [
            {"category": "labor", "amount": 45000},
            {"category": "transport_misc", "amount": 10000},
            {"category": "marketing", "amount": 8000},
            {"category": "utilities", "amount": 5000},
            {"category": "rent", "amount": 15000},
        ]
    },
    
    # Mobile Money Agency - Small Scale (Monthly)
    {
        "business_name": "Mobile Money Agency",
        "scale_type": "small",
        "year": 2024,
        "period_number": 1,
        "period_type": "month",
        "costs": [
            {"category": "rent", "amount": 5000},
            {"category": "utilities", "amount": 1500},
            {"category": "labor", "amount": 3000},
            {"category": "marketing", "amount": 1000},
        ]
    },
]