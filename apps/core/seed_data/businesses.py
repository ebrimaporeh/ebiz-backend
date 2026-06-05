"""
Businesses seed data - UPDATED with year field
"""

BUSINESSES = [
    {
        "name": "Poultry Farming - Broilers",
        "sector_name": "Agriculture",
        "short_description": "Raise broiler chickens for meat production in 6-8 week cycles",
        "overview": """Broiler poultry farming involves raising chickens specifically for meat production over an 8-week cycle. This business model is well-suited to The Gambia's growing urban population and increasing demand for affordable protein.

Day-to-day operations include feeding, watering, health monitoring, litter management, and biosecurity measures. At the end of each cycle, birds are sold live to market women, restaurants, or directly to consumers.

The business requires dedicated housing, reliable feed supply, and basic biosecurity practices. With proper management, a small-scale operation can generate consistent income and be expanded over time.""",
        "opportunity_thesis": """The Gambia imports a significant portion of its poultry meat. Local production cannot meet demand, creating a persistent market gap. Rising input costs (feed, chicks) have pushed small farmers out, but those who manage efficiently capture premium prices.

Key opportunities:
1. Growing restaurant and hotel demand for fresh local chicken
2. Government import substitution policies favoring local production
3. Vertical integration opportunities (feed milling, day-old chick production)
4. Export potential to Senegal during poultry shortages""",
        "is_featured": True,
        "status": "published",
        "has_scales": True
    },
    {
        "name": "Taxi Services",
        "sector_name": "Transportation & Logistics",
        "short_description": "Provide passenger transport services in urban and tourist areas",
        "overview": """Taxi services in The Gambia provide essential transportation for residents and tourists. The business involves operating a vehicle to transport passengers for fares, typically negotiated or metered.

Daily operations include vehicle maintenance, fuel management, route planning, and customer service. Success depends on knowledge of routes, reliability, and building regular client relationships.

The business can start with one vehicle and expand to a fleet over time. Key locations include Banjul, Serrekunda, tourist areas, and the airport.""",
        "opportunity_thesis": """The tourism industry in The Gambia creates consistent demand for reliable transport. Many tourists prefer private taxis over public transport. The diaspora market also needs airport transfers and family transport.

Key opportunities:
1. Airport transfers to tourist areas
2. Corporate accounts with hotels and tour operators
3. App-based booking integration
4. Specialized services for events and weddings""",
        "is_featured": True,
        "status": "published",
        "has_scales": True
    },
    {
        "name": "Solar Panel Installation",
        "sector_name": "Renewable Energy",
        "short_description": "Install and maintain solar energy systems for homes and businesses",
        "overview": """Solar panel installation provides renewable energy solutions to address The Gambia's unreliable grid electricity. Services include site assessment, system design, installation, and ongoing maintenance.

Daily operations include customer consultations, installation work, system testing, and troubleshooting. Technical knowledge of electrical systems and solar technology is essential.

The business serves residential customers, small businesses, and larger commercial installations.""",
        "opportunity_thesis": """The Gambia has abundant sunshine year-round. High electricity costs and unreliable grid supply drive demand for solar alternatives. Government incentives and falling equipment costs make solar increasingly accessible.

Key opportunities:
1. Residential solar for homes and compounds
2. Commercial installations for businesses and hotels
3. Solar water pumping for agriculture
4. Battery storage and backup systems""",
        "is_featured": True,
        "status": "published",
        "has_scales": True
    },
    {
        "name": "Mobile Money Agency",
        "sector_name": "Financial Services",
        "short_description": "Provide mobile money services including deposits, withdrawals, and transfers",
        "overview": """Mobile money agencies provide essential financial services to unbanked populations. Services include cash deposits, withdrawals, money transfers, bill payments, and mobile credit purchases.

Daily operations include cash management, transaction processing, customer service, and security procedures. The business requires trust and reliability to build regular customers.

Location is critical - successful agencies are placed in high-traffic areas near markets, transport hubs, and residential zones.""",
        "opportunity_thesis": """Mobile money adoption in The Gambia continues to grow rapidly. Many people rely on mobile money as their primary financial tool. Banks are partnering with agents to extend their reach.

Key opportunities:
1. High-traffic retail locations
2. Bill payment services
3. Salary disbursement partnerships with employers
4. Integration with e-commerce platforms""",
        "is_featured": False,
        "status": "published",
        "has_scales": True
    },
]

BUSINESS_SCALES = [
    # Poultry - Small
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "year": 2024,
        "capacity_definition": "100–300 birds",
        "target_market": "Local households, small restaurants, weekend market sellers",
        "location_type": "Backyard or small dedicated structure",
        "labor_needed": "1 part-time owner",
        "overall_feasibility_score": 7.2
    },
    # Poultry - Medium
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "year": 2024,
        "capacity_definition": "500–1,500 birds",
        "target_market": "Restaurants, hotels, major markets, regular wholesale buyers",
        "location_type": "Peri-urban commercial farm",
        "labor_needed": "1-2 full-time employees",
        "overall_feasibility_score": 7.5
    },
    # Poultry - Large
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "large",
        "year": 2024,
        "capacity_definition": "2,000–5,000 birds",
        "target_market": "Wholesalers, processing facilities, export markets",
        "location_type": "Rural commercial farm with dedicated infrastructure",
        "labor_needed": "3+ full-time employees plus supervisor",
        "overall_feasibility_score": 6.8
    },
    # Taxi - Small
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "year": 2024,
        "capacity_definition": "1 vehicle",
        "target_market": "Local residents, airport passengers, tourists",
        "location_type": "Urban area, near transport hubs",
        "labor_needed": "1 driver/owner",
        "overall_feasibility_score": 8.0
    },
    # Taxi - Medium
    {
        "business_name": "Taxi Services",
        "scale_type": "medium",
        "year": 2024,
        "capacity_definition": "3-5 vehicles",
        "target_market": "Hotels, tour operators, corporate clients",
        "location_type": "Tourist areas, major hotels, airport",
        "labor_needed": "3-5 drivers + dispatcher",
        "overall_feasibility_score": 7.5
    },
    # Solar - Small
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "small",
        "year": 2024,
        "capacity_definition": "1-2 technicians",
        "target_market": "Residential homes, small shops",
        "location_type": "Urban residential areas",
        "labor_needed": "1-2 technicians + owner",
        "overall_feasibility_score": 8.2
    },
    # Solar - Medium
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "medium",
        "year": 2024,
        "capacity_definition": "3-5 technicians",
        "target_market": "Businesses, hotels, larger residential",
        "location_type": "Commercial and high-end residential",
        "labor_needed": "3-5 technicians + sales/admin",
        "overall_feasibility_score": 7.8
    },
    # Mobile Money - Small
    {
        "business_name": "Mobile Money Agency",
        "scale_type": "small",
        "year": 2024,
        "capacity_definition": "Single kiosk/shop",
        "target_market": "Local community, market customers",
        "location_type": "High-traffic retail location",
        "labor_needed": "1-2 agents",
        "overall_feasibility_score": 8.5
    },
]

CAPITAL_ITEMS = [
    # Poultry - Small
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "registration",
        "item_name": "Business registration and licenses",
        "quantity": 1,
        "unit_cost": 5000,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "premises",
        "item_name": "Poultry house construction (materials)",
        "quantity": 1,
        "unit_cost": 35000,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "equipment",
        "item_name": "Feeders and drinkers",
        "quantity": 5,
        "unit_cost": 400,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "inventory",
        "item_name": "Day-old chicks (100 birds)",
        "quantity": 100,
        "unit_cost": 110,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "inventory",
        "item_name": "Initial feed stock",
        "quantity": 200,
        "unit_cost": 45,
        "priority": "essential"
    },
    
    # Poultry - Medium
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "registration",
        "item_name": "Business registration and licenses",
        "quantity": 1,
        "unit_cost": 9500,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "premises",
        "item_name": "Poultry house construction (materials)",
        "quantity": 1,
        "unit_cost": 95000,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "equipment",
        "item_name": "Feeders and drinkers",
        "quantity": 15,
        "unit_cost": 500,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "inventory",
        "item_name": "Day-old chicks (500 birds)",
        "quantity": 500,
        "unit_cost": 110,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "inventory",
        "item_name": "Initial feed stock",
        "quantity": 1000,
        "unit_cost": 45,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "equipment",
        "item_name": "Water pump and storage",
        "quantity": 1,
        "unit_cost": 15000,
        "priority": "recommended"
    },
    
    # Taxi - Small
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "category": "equipment",
        "item_name": "Vehicle (used sedan)",
        "quantity": 1,
        "unit_cost": 150000,
        "priority": "essential"
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "category": "registration",
        "item_name": "Taxi license and permits",
        "quantity": 1,
        "unit_cost": 10000,
        "priority": "essential"
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "category": "working_cap",
        "item_name": "Initial fuel and maintenance",
        "quantity": 1,
        "unit_cost": 10000,
        "priority": "essential"
    },
    
    # Solar - Small
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "small",
        "category": "equipment",
        "item_name": "Tool kit and equipment",
        "quantity": 1,
        "unit_cost": 50000,
        "priority": "essential"
    },
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "small",
        "category": "registration",
        "item_name": "Business registration",
        "quantity": 1,
        "unit_cost": 5000,
        "priority": "essential"
    },
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "small",
        "category": "inventory",
        "item_name": "Demo solar kit",
        "quantity": 1,
        "unit_cost": 30000,
        "priority": "essential"
    },
]

RISKS = [
    # Poultry - Medium
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "operational",
        "specific_risk": "Disease outbreak (Newcastle, Avian Influenza)",
        "likelihood": 4,
        "impact": 10,
        "mitigation_strategy": "Strict biosecurity protocols, vaccination schedule, quarantine new birds, limit visitor access"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "supply",
        "specific_risk": "Feed price volatility",
        "likelihood": 8,
        "impact": 7,
        "mitigation_strategy": "Buy feed in bulk during low-price periods, explore local feed alternatives, consider feed formulation"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "market",
        "specific_risk": "Price competition from frozen imported chicken",
        "likelihood": 6,
        "impact": 5,
        "mitigation_strategy": "Differentiate as fresh local chicken, build relationships with restaurants/hotels, obtain 'Gambia Grown' certification"
    },
    
    # Taxi - Medium
    {
        "business_name": "Taxi Services",
        "scale_type": "medium",
        "category": "operational",
        "specific_risk": "Vehicle breakdowns and maintenance costs",
        "likelihood": 7,
        "impact": 6,
        "mitigation_strategy": "Regular preventive maintenance, set aside maintenance fund, have backup vehicle"
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "medium",
        "category": "financial",
        "specific_risk": "Fuel price increases",
        "likelihood": 8,
        "impact": 7,
        "mitigation_strategy": "Monitor fuel efficiency, adjust fares when needed, consider LPG conversion"
    },
    
    # Solar - Medium
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "medium",
        "category": "operational",
        "specific_risk": "Component quality and warranty issues",
        "likelihood": 5,
        "impact": 7,
        "mitigation_strategy": "Source from reputable suppliers, test components before installation, maintain warranty documentation"
    },
]

FEASIBILITY_FACTORS = [
    # Poultry - Medium
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "market",
        "sub_category": "Market demand",
        "rating": 8,
        "notes": "Growing urban population, consistent demand from restaurants and hotels",
        "data_source": "Field Survey 2024"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "market",
        "sub_category": "Competition",
        "rating": 6,
        "notes": "Several local producers but still supply gap; imported chicken is main competitor",
        "data_source": "Field Survey 2024"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "financial",
        "sub_category": "Startup capital accessibility",
        "rating": 5,
        "notes": "D150k-250k required; limited formal lending for agriculture",
        "data_source": "Field Survey 2024"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "financial",
        "sub_category": "Profitability potential",
        "rating": 7,
        "notes": "30%+ margins achievable with good management and feed cost control",
        "data_source": "Revenue projection analysis"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "operations",
        "sub_category": "Feed supply reliability",
        "rating": 5,
        "notes": "Feed prices volatile, imported ingredients, occasional shortages",
        "data_source": "Field Survey 2024"
    },
    
    # Taxi - Medium
    {
        "business_name": "Taxi Services",
        "scale_type": "medium",
        "category": "market",
        "sub_category": "Market demand",
        "rating": 9,
        "notes": "Strong tourism sector, growing urban population, limited public transport",
        "data_source": "GBoS Tourism Report 2024"
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "medium",
        "category": "financial",
        "sub_category": "Startup capital accessibility",
        "rating": 7,
        "notes": "Vehicle financing available from some banks and microfinance institutions",
        "data_source": "Bank interview 2024"
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "medium",
        "category": "regulatory",
        "sub_category": "Licensing burden",
        "rating": 6,
        "notes": "Multiple permits required but process is straightforward",
        "data_source": "GRA and Council interviews"
    },
    
    # Solar - Medium
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "medium",
        "category": "market",
        "sub_category": "Market demand",
        "rating": 8,
        "notes": "High electricity costs drive demand; government renewable energy targets",
        "data_source": "NAWEC and Ministry of Energy reports"
    },
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "medium",
        "category": "technical",
        "sub_category": "Skills availability",
        "rating": 6,
        "notes": "Limited certified solar technicians; training required",
        "data_source": "Industry assessment 2024"
    },
]

FINANCIAL_METRICS = [
    # Poultry - Small
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "breakeven_cycles": 3,
        "gross_margin_percent": 28.5,
        "net_margin_percent": 24.2,
        "roi_percent": 112,
        "payback_months": 8,
        "data_source": "Field Survey 2024"
    },
    # Poultry - Medium
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "breakeven_cycles": 2.5,
        "gross_margin_percent": 30.4,
        "net_margin_percent": 25.9,
        "roi_percent": 95,
        "payback_months": 7,
        "data_source": "Field Survey 2024"
    },
    # Poultry - Large
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "large",
        "breakeven_cycles": 2,
        "gross_margin_percent": 32.0,
        "net_margin_percent": 27.5,
        "roi_percent": 85,
        "payback_months": 6.5,
        "data_source": "Field Survey 2024"
    },
    # Taxi - Small
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "breakeven_cycles": 12,
        "gross_margin_percent": 55.0,
        "net_margin_percent": 35.0,
        "roi_percent": 45,
        "payback_months": 18,
        "data_source": "Operator interviews 2024"
    },
    # Taxi - Medium
    {
        "business_name": "Taxi Services",
        "scale_type": "medium",
        "breakeven_cycles": 10,
        "gross_margin_percent": 58.0,
        "net_margin_percent": 38.0,
        "roi_percent": 40,
        "payback_months": 16,
        "data_source": "Operator interviews 2024"
    },
    # Solar - Small
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "small",
        "breakeven_cycles": 6,
        "gross_margin_percent": 45.0,
        "net_margin_percent": 30.0,
        "roi_percent": 150,
        "payback_months": 6,
        "data_source": "Industry analysis 2024"
    },
]