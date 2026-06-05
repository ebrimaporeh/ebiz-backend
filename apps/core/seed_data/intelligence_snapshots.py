"""
Intelligence Snapshots seed data - Primary read model for frontend
"""

def build_snapshot_data(business_name, scale_type, year, sector_name):
    """Helper to build snapshot data structure"""
    return {
        "subject": {
            "name": business_name,
            "slug": business_name.lower().replace(" ", "-"),
            "has_scales": True,
            "sector": sector_name,
        },
        "year": year,
        "scale": {
            "type": scale_type,
        },
        "metrics": {},
        "feasibility_overall": {},
        "feasibility_factors": [],
        "risks": [],
        "cost_breakdown": [],
        "revenue": {},
        "opportunities": [],
    }


INTELLIGENCE_SNAPSHOTS = [
    # Poultry - Medium - 2024
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "year": 2024,
        "version": 1,
        "is_latest": True,
        "status": "published",
        "data": {
            "subject": {
                "name": "Poultry Farming - Broilers",
                "slug": "poultry-farming-broilers",
                "has_scales": True,
                "sector": "Agriculture",
            },
            "year": 2024,
            "scale": {
                "type": "medium",
                "definition": "500-1,500 birds",
                "target_market": "Restaurants, hotels, major markets",
                "labor_needed": "1-2 full-time employees",
                "location_type": "Peri-urban commercial farm",
            },
            "metrics": {
                "startup_cost": {
                    "value": 264000,
                    "display": "D264,000",
                    "source": "GAMBIH Field Survey 2024"
                },
                "working_capital": {
                    "value": 80000,
                    "display": "D80,000",
                    "source": "GAMBIH Field Survey 2024"
                },
                "gross_margin": {
                    "value": 30.4,
                    "display": "30.4%",
                    "source": "GAMBIH Revenue Analysis"
                },
                "net_margin": {
                    "value": 25.9,
                    "display": "25.9%",
                    "source": "GAMBIH Revenue Analysis"
                },
                "payback_period": {
                    "min": 6,
                    "max": 8,
                    "unit": "months",
                    "display": "6-8 months",
                    "source": "Financial metric calculation"
                },
            },
            "feasibility_overall": {
                "score": 7.5,
                "label": "Good feasibility with manageable challenges"
            },
            "feasibility_factors": [
                {"name": "Market demand", "score": 8, "source": "Field Survey 2024"},
                {"name": "Competition", "score": 6, "source": "Field Survey 2024"},
                {"name": "Startup capital accessibility", "score": 5, "source": "Field Survey 2024"},
                {"name": "Profitability potential", "score": 7, "source": "Revenue analysis"},
                {"name": "Feed supply reliability", "score": 5, "source": "Field Survey 2024"},
            ],
            "risks": [
                {
                    "name": "Disease Outbreak",
                    "category": "operational",
                    "likelihood": 4,
                    "impact": 10,
                    "score": 40,
                    "level": "high",
                    "mitigation": "Strict biosecurity protocols, vaccination schedule",
                    "source": "Field Survey 2024"
                },
                {
                    "name": "Feed Price Volatility",
                    "category": "supply",
                    "likelihood": 8,
                    "impact": 7,
                    "score": 56,
                    "level": "high",
                    "mitigation": "Bulk purchasing, local feed alternatives",
                    "source": "Field Survey 2024"
                },
                {
                    "name": "Imported Chicken Competition",
                    "category": "market",
                    "likelihood": 6,
                    "impact": 5,
                    "score": 30,
                    "level": "medium",
                    "mitigation": "Fresh local chicken differentiation",
                    "source": "Market analysis 2024"
                },
            ],
            "cost_breakdown": [
                {"name": "Registration & Licenses", "amount_raw": 9500, "percentage": 3.6, "category": "registration"},
                {"name": "Housing Construction", "amount_raw": 95000, "percentage": 36.0, "category": "premises"},
                {"name": "Feeders & Drinkers", "amount_raw": 7500, "percentage": 2.8, "category": "equipment"},
                {"name": "Day-old Chicks (500)", "amount_raw": 55000, "percentage": 20.8, "category": "inventory"},
                {"name": "Initial Feed Stock", "amount_raw": 45000, "percentage": 17.0, "category": "inventory"},
                {"name": "Water System", "amount_raw": 15000, "percentage": 5.7, "category": "equipment"},
                {"name": "Other Equipment", "amount_raw": 37000, "percentage": 14.0, "category": "equipment"},
            ],
            "revenue": {
                "net_profit_per_cycle": [57480, 57480, 57480, 57480, 57480, 57480],
                "cumulative_cash_flow": [-161220, -103740, -46260, 11220, 68700, 126180]
            },
            "opportunities": [
                {
                    "name": "Feed Production",
                    "description": "Start a local feed mill to supply farmers",
                    "investment_range": "D500K–D2M",
                    "roi_range": "25–35%"
                },
                {
                    "name": "Hatchery",
                    "description": "Produce day-old chicks locally",
                    "investment_range": "D1M–D5M",
                    "roi_range": "30–40%"
                },
            ],
            "cycle_unit": "weeks",
            "cycle_duration": 8,
            "cycles_per_year": 6,
        },
        "startup_cost": 264000,
        "gross_margin_pct": 30.4,
        "payback_months": 7.0,
        "feasibility_score": 7.5,
        "risk_score": 42,
        "min_investment": 150000,
        "max_investment": 350000,
        "summary_text": "Medium-scale broiler poultry farming in The Gambia requires D150,000-350,000 startup capital. With proper management, 30%+ gross margins are achievable. Main risks are disease outbreaks and feed price volatility. Payback period is 6-8 months."
    },
    
    # Poultry - Small - 2024
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "year": 2024,
        "version": 1,
        "is_latest": True,
        "status": "published",
        "data": {
            "subject": {
                "name": "Poultry Farming - Broilers",
                "slug": "poultry-farming-broilers",
                "has_scales": True,
                "sector": "Agriculture",
            },
            "year": 2024,
            "scale": {
                "type": "small",
                "definition": "100-300 birds",
                "target_market": "Local households, small restaurants",
                "labor_needed": "1 part-time owner",
                "location_type": "Backyard or small dedicated structure",
            },
            "metrics": {
                "startup_cost": {"value": 89000, "display": "D89,000", "source": "GAMBIH Field Survey 2024"},
                "working_capital": {"value": 30000, "display": "D30,000", "source": "GAMBIH Field Survey 2024"},
                "gross_margin": {"value": 28.5, "display": "28.5%", "source": "GAMBIH Revenue Analysis"},
                "net_margin": {"value": 24.2, "display": "24.2%", "source": "GAMBIH Revenue Analysis"},
                "payback_period": {"min": 7, "max": 9, "unit": "months", "display": "7-9 months"},
            },
            "feasibility_overall": {"score": 7.2, "label": "Good feasibility for part-time entrepreneurs"},
            "feasibility_factors": [
                {"name": "Market demand", "score": 7, "source": "Field Survey 2024"},
                {"name": "Competition", "score": 5, "source": "Field Survey 2024"},
                {"name": "Startup capital", "score": 6, "source": "Field Survey 2024"},
                {"name": "Profitability", "score": 8, "source": "Revenue analysis"},
            ],
            "risks": [
                {"name": "Disease", "score": 40, "level": "high", "mitigation": "Biosecurity"},
                {"name": "Feed Costs", "score": 45, "level": "medium", "mitigation": "Bulk buying"},
            ],
            "cost_breakdown": [],
            "revenue": {"net_profit_per_cycle": [17244, 17244, 17244], "cumulative_cash_flow": [-54512, -37268, -20024]},
        },
        "startup_cost": 89000,
        "gross_margin_pct": 28.5,
        "payback_months": 8.0,
        "feasibility_score": 7.2,
        "risk_score": 42,
        "min_investment": 50000,
        "max_investment": 120000,
        "summary_text": "Small-scale broiler poultry is accessible with D50,000-120,000. Good for part-time farmers."
    },
    
    # Taxi - Medium - 2024
    {
        "business_name": "Taxi Services",
        "scale_type": "medium",
        "year": 2024,
        "version": 1,
        "is_latest": True,
        "status": "published",
        "data": {
            "subject": {
                "name": "Taxi Services",
                "slug": "taxi-services",
                "has_scales": True,
                "sector": "Transportation & Logistics",
            },
            "year": 2024,
            "scale": {
                "type": "medium",
                "definition": "3-5 vehicles",
                "target_market": "Hotels, tour operators, corporate clients",
                "labor_needed": "3-5 drivers + dispatcher",
                "location_type": "Tourist areas, major hotels",
            },
            "metrics": {
                "startup_cost": {"value": 650000, "display": "D650,000", "source": "Operator Survey 2024"},
                "working_capital": {"value": 100000, "display": "D100,000", "source": "Operator Survey 2024"},
                "gross_margin": {"value": 58.0, "display": "58.0%", "source": "Operator Survey 2024"},
                "net_margin": {"value": 38.0, "display": "38.0%", "source": "Operator Survey 2024"},
                "payback_period": {"min": 14, "max": 18, "unit": "months", "display": "14-18 months"},
            },
            "feasibility_overall": {"score": 7.5, "label": "Good feasibility with strong tourism linkage"},
            "risks": [
                {"name": "Fuel Price Increases", "score": 56, "level": "high", "mitigation": "Fuel efficiency tracking"},
                {"name": "Vehicle Breakdowns", "score": 42, "level": "medium", "mitigation": "Regular maintenance"},
            ],
            "opportunities": [
                {"name": "App-based Booking", "description": "Mobile app for taxi dispatch", "investment_range": "D100K-D300K"},
                {"name": "Airport Transfer Service", "description": "Specialized airport service", "investment_range": "D200K-D500K"},
            ],
        },
        "startup_cost": 650000,
        "gross_margin_pct": 58.0,
        "payback_months": 16.0,
        "feasibility_score": 7.5,
        "risk_score": 49,
        "min_investment": 500000,
        "max_investment": 800000,
        "summary_text": "Medium-scale taxi business requires D500,000-800,000 for 3-5 vehicles. Strong margins due to tourism demand."
    },
    
    # Solar - Medium - 2024
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "medium",
        "year": 2024,
        "version": 1,
        "is_latest": True,
        "status": "published",
        "data": {
            "subject": {
                "name": "Solar Panel Installation",
                "slug": "solar-panel-installation",
                "has_scales": True,
                "sector": "Renewable Energy",
            },
            "year": 2024,
            "scale": {
                "type": "medium",
                "definition": "3-5 technicians",
                "target_market": "Businesses, hotels, larger residential",
                "labor_needed": "3-5 technicians + sales/admin",
                "location_type": "Commercial area with showroom",
            },
            "metrics": {
                "startup_cost": {"value": 350000, "display": "D350,000", "source": "Industry Assessment 2024"},
                "gross_margin": {"value": 45.0, "display": "45.0%", "source": "Industry Assessment 2024"},
                "net_margin": {"value": 30.0, "display": "30.0%", "source": "Industry Assessment 2024"},
                "payback_period": {"value": 6, "unit": "months", "display": "6 months"},
            },
            "feasibility_overall": {"score": 7.8, "label": "Strong feasibility with growing demand"},
        },
        "startup_cost": 350000,
        "gross_margin_pct": 45.0,
        "payback_months": 6.0,
        "feasibility_score": 7.8,
        "risk_score": 35,
        "min_investment": 250000,
        "max_investment": 500000,
        "summary_text": "Solar installation business requires D250,000-500,000. High margins (45%) with growing demand."
    },
]