# apps/core/seed_data/businesses.py

BUSINESSES = [
    {
        "name": "Poultry Farming - Broilers",
        "sector_name": "Agriculture",
        "short_description": "Raising chickens for meat production",
        "overview": "Poultry farming is one of the most popular agribusinesses in The Gambia, driven by high demand for chicken meat across households, restaurants, and events. This business involves raising broiler chickens from day-old chicks to market weight in 6-8 weeks.",
        "opportunity_thesis": "The Gambia imports over 60% of its poultry products, creating a significant gap for local producers. With rising protein demand and government support for agriculture, broiler farming offers strong potential for consistent returns.",
        "is_featured": True,
        "status": "published"
    },
    {
        "name": "Taxi Services",
        "sector_name": "Transportation & Logistics",
        "short_description": "Urban and inter-city passenger transport",
        "overview": "Taxi services are essential for daily commuting in Gambian cities. This business involves operating vehicles for hire, serving both local residents and tourists.",
        "opportunity_thesis": "With growing urban population and tourism sector, demand for reliable transportation continues to rise. Entry barriers are moderate with good potential for steady income.",
        "is_featured": True,
        "status": "published"
    },
    {
        "name": "Software Development Agency",
        "sector_name": "Technology & IT",
        "short_description": "Custom software and web development services",
        "overview": "Software development agencies provide custom solutions for businesses, government, and international clients. Services include web apps, mobile apps, and enterprise software.",
        "opportunity_thesis": "Digital transformation is accelerating in The Gambia. With remote work opportunities, local developers can serve both local and international clients.",
        "is_featured": True,
        "status": "published"
    },
    {
        "name": "Private School",
        "sector_name": "Education & Training",
        "short_description": "Primary and secondary education services",
        "overview": "Private schools offer alternative education options for families seeking quality education. This business requires investment in facilities, qualified teachers, and curriculum development.",
        "opportunity_thesis": "Growing middle class and demand for quality education create opportunities for private schools. Government support for education makes this a stable sector.",
        "is_featured": False,
        "status": "published"
    },
    {
        "name": "Supermarket",
        "sector_name": "Retail & Commerce",
        "short_description": "Retail store selling groceries and household items",
        "overview": "Supermarkets serve daily shopping needs of urban residents. Success depends on location, inventory management, and customer service.",
        "opportunity_thesis": "Urbanization and changing shopping habits favor modern retail formats. There's opportunity for both neighborhood stores and larger supermarket chains.",
        "is_featured": False,
        "status": "published"
    },
    {
        "name": "Real Estate Agency",
        "sector_name": "Real Estate & Construction",
        "short_description": "Property sales, rentals, and management",
        "overview": "Real estate agencies connect property buyers/sellers and manage rental properties. Services include property valuation, marketing, and transaction facilitation.",
        "opportunity_thesis": "Growing housing demand and diaspora investment create opportunities. Property values have shown consistent appreciation in urban areas.",
        "is_featured": True,
        "status": "published"
    },
    {
        "name": "Pharmacy",
        "sector_name": "Healthcare & Pharmaceuticals",
        "short_description": "Retail pharmacy selling medications and health products",
        "overview": "Pharmacies provide essential healthcare products and services. Requires licensed pharmacist and compliance with health regulations.",
        "opportunity_thesis": "Healthcare spending is increasing. Pharmacies in strategic locations can generate steady income with proper inventory management.",
        "is_featured": False,
        "status": "published"
    },
    {
        "name": "Solar Installation",
        "sector_name": "Renewable Energy",
        "short_description": "Solar panel installation and maintenance",
        "overview": "Solar installation businesses provide renewable energy solutions for homes, businesses, and institutions. Services include assessment, installation, and maintenance.",
        "opportunity_thesis": "With abundant sunshine and unreliable grid power, solar energy has huge potential. Government incentives support renewable energy adoption.",
        "is_featured": True,
        "status": "published"
    },
    {
        "name": "Vegetable Gardening",
        "sector_name": "Agriculture",
        "short_description": "Commercial vegetable production",
        "overview": "Commercial vegetable gardening involves growing high-demand vegetables for local markets, hotels, and supermarkets.",
        "opportunity_thesis": "Tourism creates demand for fresh vegetables year-round. With irrigation, farmers can produce multiple cycles annually.",
        "is_featured": False,
        "status": "published"
    },
    {
        "name": "Trucking & Logistics",
        "sector_name": "Transportation & Logistics",
        "short_description": "Goods transportation and delivery services",
        "overview": "Trucking businesses transport goods between regions and across borders. Services include freight, distribution, and logistics management.",
        "opportunity_thesis": "Trade and commerce depend on reliable transportation. Cross-border trade with Senegal and other neighbors creates consistent demand.",
        "is_featured": False,
        "status": "published"
    },
    {
        "name": "Digital Marketing Agency",
        "sector_name": "Technology & IT",
        "short_description": "Social media management and online marketing",
        "overview": "Digital marketing agencies help businesses build online presence through social media, SEO, email marketing, and content creation.",
        "opportunity_thesis": "Businesses increasingly recognize the need for online presence. Low startup costs make this accessible for young entrepreneurs.",
        "is_featured": False,
        "status": "published"
    },
    {
        "name": "Fishing Business",
        "sector_name": "Agriculture",
        "short_description": "Commercial fishing and fish processing",
        "overview": "Fishing businesses operate along Gambia's coastline, harvesting fish for local consumption and export. Includes fresh fish sales and processing.",
        "opportunity_thesis": "Gambia's coastal location provides abundant fishing resources. Export opportunities to Europe and other markets exist.",
        "is_featured": True,
        "status": "published"
    },
    {
        "name": "Restaurant",
        "sector_name": "Tourism & Hospitality",
        "short_description": "Food service for locals and tourists",
        "overview": "Restaurants serve prepared meals to customers. Success depends on location, menu quality, and customer service.",
        "opportunity_thesis": "Tourism creates steady demand for dining options. Local entrepreneurs can serve both tourist and local markets.",
        "is_featured": False,
        "status": "published"
    },
    {
        "name": "Forex Exchange",
        "sector_name": "Financial Services",
        "short_description": "Currency exchange and money transfer services",
        "overview": "Forex bureaus exchange foreign currency and facilitate money transfers for diaspora remittances.",
        "opportunity_thesis": "Diaspora remittances are a major economic driver. Licensed forex bureaus serve this steady market.",
        "is_featured": False,
        "status": "published"
    }
]

BUSINESS_SCALES = [
    # Poultry Farming - Broilers
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "capacity_definition": "100-300 birds",
        "target_market": "Local households, street food vendors",
        "location_type": "Backyard/Compound",
        "labor_needed": "1 person part-time",
        "overall_feasibility_score": 7.2
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "capacity_definition": "500-1,500 birds",
        "target_market": "Restaurants, markets, institutions",
        "location_type": "Peri-urban areas",
        "labor_needed": "1-2 full-time",
        "overall_feasibility_score": 6.5
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "large",
        "capacity_definition": "3,000+ birds",
        "target_market": "Hotels, supermarkets, exporters",
        "location_type": "Rural commercial plots",
        "labor_needed": "3+ employees",
        "overall_feasibility_score": 7.8
    },
    # Taxi Services
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "capacity_definition": "1 vehicle",
        "target_market": "Local residents, tourists",
        "location_type": "Urban areas",
        "labor_needed": "Owner-operator",
        "overall_feasibility_score": 7.5
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "medium",
        "capacity_definition": "3-5 vehicles",
        "target_market": "Tourists, corporate clients",
        "location_type": "Tourist areas, airports",
        "labor_needed": "2-3 drivers",
        "overall_feasibility_score": 7.0
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "large",
        "capacity_definition": "10+ vehicles",
        "target_market": "Corporate, government, tour operators",
        "location_type": "Multiple locations",
        "labor_needed": "5+ employees",
        "overall_feasibility_score": 8.0
    },
    # Software Development
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "capacity_definition": "1-3 developers",
        "target_market": "Local small businesses",
        "location_type": "Home office",
        "labor_needed": "Freelancers",
        "overall_feasibility_score": 8.2
    },
    {
        "business_name": "Software Development Agency",
        "scale_type": "medium",
        "capacity_definition": "5-10 developers",
        "target_market": "Local and international clients",
        "location_type": "Office space",
        "labor_needed": "4-6 full-time",
        "overall_feasibility_score": 8.5
    },
    {
        "business_name": "Software Development Agency",
        "scale_type": "large",
        "capacity_definition": "20+ developers",
        "target_market": "Enterprise, international",
        "location_type": "Commercial office",
        "labor_needed": "15+ employees",
        "overall_feasibility_score": 9.0
    }
]

CAPITAL_ITEMS = [
    # Poultry - Small Scale
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "registration",
        "item_name": "Business Registration",
        "quantity": 1,
        "unit_cost": 1500,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "premises",
        "item_name": "Backyard Setup",
        "quantity": 1,
        "unit_cost": 15000,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "equipment",
        "item_name": "Feeders",
        "quantity": 4,
        "unit_cost": 800,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "equipment",
        "item_name": "Drinkers",
        "quantity": 4,
        "unit_cost": 600,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "inventory",
        "item_name": "Day-old Chicks",
        "quantity": 100,
        "unit_cost": 110,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "inventory",
        "item_name": "Starter Feed",
        "quantity": 200,
        "unit_cost": 45,
        "priority": "essential"
    },
    # Poultry - Medium Scale
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "registration",
        "item_name": "Business Registration",
        "quantity": 1,
        "unit_cost": 5000,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "premises",
        "item_name": "Land Preparation",
        "quantity": 1,
        "unit_cost": 15000,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "premises",
        "item_name": "Poultry House",
        "quantity": 1,
        "unit_cost": 60000,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "inventory",
        "item_name": "Day-old Chicks",
        "quantity": 500,
        "unit_cost": 110,
        "priority": "essential"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "inventory",
        "item_name": "Starter Feed",
        "quantity": 1000,
        "unit_cost": 45,
        "priority": "essential"
    },
    # Taxi - Small Scale
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "category": "registration",
        "item_name": "Business License",
        "quantity": 1,
        "unit_cost": 5000,
        "priority": "essential"
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "category": "equipment",
        "item_name": "Vehicle",
        "quantity": 1,
        "unit_cost": 800000,
        "priority": "essential"
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "category": "equipment",
        "item_name": "Taxi Meter",
        "quantity": 1,
        "unit_cost": 15000,
        "priority": "essential"
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "category": "registration",
        "item_name": "Insurance",
        "quantity": 1,
        "unit_cost": 25000,
        "priority": "essential"
    },
    # Software - Small Scale
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "category": "equipment",
        "item_name": "Laptop",
        "quantity": 1,
        "unit_cost": 50000,
        "priority": "essential"
    },
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "category": "equipment",
        "item_name": "Software Licenses",
        "quantity": 1,
        "unit_cost": 15000,
        "priority": "essential"
    },
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "category": "registration",
        "item_name": "Business Registration",
        "quantity": 1,
        "unit_cost": 5000,
        "priority": "essential"
    }
]

RISKS = [
    # Poultry Risks
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "operational",
        "specific_risk": "Disease Outbreak",
        "likelihood": 3,
        "impact": 4,
        "mitigation_strategy": "Maintain strict biosecurity, follow vaccination schedule"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "market",
        "specific_risk": "Feed Price Volatility",
        "likelihood": 4,
        "impact": 3,
        "mitigation_strategy": "Buy feed in bulk, explore local feed alternatives"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "financial",
        "specific_risk": "Cash Flow Gaps",
        "likelihood": 3,
        "impact": 3,
        "mitigation_strategy": "Maintain emergency fund of 30% of operating costs"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "operational",
        "specific_risk": "Disease Outbreak",
        "likelihood": 4,
        "impact": 5,
        "mitigation_strategy": "Strict vaccination protocol, quarantine new birds"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "category": "market",
        "specific_risk": "Price Competition",
        "likelihood": 4,
        "impact": 3,
        "mitigation_strategy": "Differentiate through quality, build direct customer relationships"
    },
    # Taxi Risks
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "category": "financial",
        "specific_risk": "High Fuel Costs",
        "likelihood": 5,
        "impact": 3,
        "mitigation_strategy": "Fuel-efficient routes, regular maintenance"
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "category": "operational",
        "specific_risk": "Vehicle Breakdown",
        "likelihood": 3,
        "impact": 4,
        "mitigation_strategy": "Regular maintenance, emergency repair fund"
    }
]

FEASIBILITY_FACTORS = [
    # Poultry Small Scale
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "market",
        "sub_category": "Market Size",
        "rating": 8,
        "notes": "Growing demand for chicken meat",
        "data_source": "GBoS 2024"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "capital",
        "sub_category": "Startup Cost",
        "rating": 7,
        "notes": "D50,000 - D100,000 range accessible",
        "data_source": "Field Survey 2024"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "profitability",
        "sub_category": "ROI Potential",
        "rating": 7,
        "notes": "15-25% net margin achievable",
        "data_source": "Field Interviews"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "category": "skills",
        "sub_category": "Technical Knowledge",
        "rating": 6,
        "notes": "Basic animal husbandry needed",
        "data_source": "Training Needs Assessment"
    },
    # Taxi Small Scale
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "category": "market",
        "sub_category": "Market Size",
        "rating": 8,
        "notes": "Strong demand in urban areas",
        "data_source": "GBoS 2024"
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "category": "capital",
        "sub_category": "Startup Cost",
        "rating": 5,
        "notes": "High vehicle cost barrier",
        "data_source": "Field Survey 2024"
    },
    # Software Small Scale
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "category": "market",
        "sub_category": "Market Size",
        "rating": 7,
        "notes": "Growing digital transformation demand",
        "data_source": "Industry Data"
    },
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "category": "capital",
        "sub_category": "Startup Cost",
        "rating": 9,
        "notes": "Low startup cost, just laptop and skills",
        "data_source": "Field Survey 2024"
    },
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "category": "profitability",
        "sub_category": "ROI Potential",
        "rating": 9,
        "notes": "High margins with remote clients",
        "data_source": "Industry Data"
    }
]

FINANCIAL_METRICS = [
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "small",
        "breakeven_cycles": 4.2,
        "gross_margin_percent": 38.3,
        "net_margin_percent": 34.1,
        "roi_percent": 143.9,
        "payback_months": 6.0,
        "data_source": "GBI Research 2024"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "medium",
        "breakeven_cycles": 3.5,
        "gross_margin_percent": 30.4,
        "net_margin_percent": 25.9,
        "roi_percent": 82.3,
        "payback_months": 7.3,
        "data_source": "GBI Research 2024"
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "large",
        "breakeven_cycles": 3.0,
        "gross_margin_percent": 40.0,
        "net_margin_percent": 36.4,
        "roi_percent": 113.5,
        "payback_months": 5.3,
        "data_source": "GBI Research 2024"
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "breakeven_cycles": 12.0,
        "gross_margin_percent": 35.0,
        "net_margin_percent": 25.0,
        "roi_percent": 45.0,
        "payback_months": 18.0,
        "data_source": "GBI Research 2024"
    },
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "breakeven_cycles": 3.0,
        "gross_margin_percent": 70.0,
        "net_margin_percent": 50.0,
        "roi_percent": 200.0,
        "payback_months": 4.0,
        "data_source": "GBI Research 2024"
    }
]