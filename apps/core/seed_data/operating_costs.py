# apps/core/seed_data/operating_costs.py

OPERATING_COSTS = [
    # Poultry - Small Scale
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "week_range": "1-2",
        "feed_starter": 4500,
        "feed_grower": 0,
        "feed_finisher": 0,
        "utilities": 300,
        "water": 200,
        "medication": 400,
        "labor": 0,
        "transport_misc": 200
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "week_range": "3-4",
        "feed_starter": 4500,
        "feed_grower": 0,
        "feed_finisher": 0,
        "utilities": 300,
        "water": 200,
        "medication": 300,
        "labor": 0,
        "transport_misc": 200
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "week_range": "5-6",
        "feed_starter": 0,
        "feed_grower": 6000,
        "feed_finisher": 0,
        "utilities": 300,
        "water": 200,
        "medication": 200,
        "labor": 0,
        "transport_misc": 300
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "week_range": "7-8",
        "feed_starter": 0,
        "feed_grower": 6000,
        "feed_finisher": 3600,
        "utilities": 300,
        "water": 200,
        "medication": 100,
        "labor": 0,
        "transport_misc": 400
    },
    # Poultry - Medium Scale
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "week_range": "1-2",
        "feed_starter": 22500,
        "feed_grower": 0,
        "feed_finisher": 0,
        "utilities": 1500,
        "water": 800,
        "medication": 2000,
        "labor": 3000,
        "transport_misc": 1000
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "week_range": "3-4",
        "feed_starter": 22500,
        "feed_grower": 0,
        "feed_finisher": 0,
        "utilities": 1500,
        "water": 800,
        "medication": 1500,
        "labor": 3000,
        "transport_misc": 1000
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "week_range": "5-6",
        "feed_starter": 0,
        "feed_grower": 30000,
        "feed_finisher": 0,
        "utilities": 1500,
        "water": 800,
        "medication": 1000,
        "labor": 3000,
        "transport_misc": 1500
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "week_range": "7-8",
        "feed_starter": 0,
        "feed_grower": 30000,
        "feed_finisher": 18000,
        "utilities": 1500,
        "water": 800,
        "medication": 500,
        "labor": 3000,
        "transport_misc": 2000
    },
    # Taxi - Small Scale (Monthly costs as weekly equivalents)
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "week_range": "1-4",
        "feed_starter": 0,
        "feed_grower": 0,
        "feed_finisher": 0,
        "utilities": 0,
        "water": 0,
        "medication": 0,
        "labor": 0,
        "transport_misc": 10000
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "week_range": "5-8",
        "feed_starter": 0,
        "feed_grower": 0,
        "feed_finisher": 0,
        "utilities": 0,
        "water": 0,
        "medication": 0,
        "labor": 0,
        "transport_misc": 10000
    }
]