# apps/core/seed_data/business_profiles.py

BUSINESS_PROFILES = [
    {
        "name": "Jow Feeds & Farm Supplies",
        "owner_name": "Momodou Jallow",
        "owner_position": "Founder & CEO",
        "description": "Jow Feeds is the leading supplier of quality poultry feed and farm equipment in The Gambia. Founded in 2018, the company serves over 500 farmers across the country with reliable, affordable feed formulations.",
        "short_description": "Leading supplier of poultry feed and farm equipment",
        "email": "info@jowfeeds.gm",
        "phone": "+220 123 4567",
        "website": "https://jowfeeds.gm",
        "location": "Brikama",
        "address": "Brikama Industrial Area, West Coast Region",
        "sector_name": "Agriculture",
        "is_partner": True,
        "is_verified": True,
        "is_featured": True,
        "partner_type": "supplier",
        "interview_date": "2024-01-15",
        "interviewed_by": "Ebrima Barry",
        "status": "published"
    },
    {
        "name": "Banjul Taxi Co-op",
        "owner_name": "Lamin Sarr",
        "owner_position": "General Manager",
        "description": "Banjul Taxi Co-op is a cooperative of 50+ taxi drivers providing reliable transportation services in the Greater Banjul Area. Known for their green-and-white branded vehicles and professional service.",
        "short_description": "Leading taxi cooperative in Greater Banjul Area",
        "email": "info@banjultaxi.gm",
        "phone": "+220 234 5678",
        "location": "Banjul",
        "address": "Albert Market Area, Banjul",
        "sector_name": "Transportation & Logistics",
        "is_partner": True,
        "is_verified": True,
        "is_featured": True,
        "partner_type": "service_provider",
        "interview_date": "2024-02-10",
        "interviewed_by": "Ebrima Barry",
        "status": "published"
    },
    {
        "name": "Gambia Solar Solutions",
        "owner_name": "Fatou Jammeh",
        "owner_position": "Managing Director",
        "description": "Gambia Solar Solutions specializes in solar panel installation, maintenance, and energy consulting for residential and commercial clients. They've installed over 1,000 systems nationwide.",
        "short_description": "Premier solar installation company",
        "email": "info@gambiasolar.gm",
        "phone": "+220 345 6789",
        "website": "https://gambiasolar.gm",
        "location": "Serrekunda",
        "address": "Kairaba Avenue, Serrekunda",
        "sector_name": "Renewable Energy",
        "is_partner": True,
        "is_verified": True,
        "is_featured": False,
        "partner_type": "service_provider",
        "interview_date": "2024-03-05",
        "interviewed_by": "Ebrima Barry",
        "status": "published"
    },
    {
        "name": "Kairaba Tech Hub",
        "owner_name": "Ousman Darboe",
        "owner_position": "Founder",
        "description": "Kairaba Tech Hub is a co-working space and tech incubator supporting Gambian startups. They offer training, mentorship, and connection to investors.",
        "short_description": "Tech incubator and co-working space",
        "email": "hello@kairabatech.gm",
        "phone": "+220 456 7890",
        "location": "Kololi",
        "address": "Senegambia Area, Kololi",
        "sector_name": "Technology & IT",
        "is_partner": True,
        "is_verified": True,
        "is_featured": False,
        "partner_type": "service_provider",
        "interview_date": "2024-03-20",
        "interviewed_by": "Ebrima Barry",
        "status": "published"
    },
    {
        "name": "Atlantic Fisheries",
        "owner_name": "Mariama Njie",
        "owner_position": "Owner",
        "description": "Atlantic Fisheries is a commercial fishing and fish processing business based in Tanji. They supply fresh and smoked fish to local markets and export to Senegal.",
        "short_description": "Commercial fishing and fish processing",
        "email": "atlanticfisheries@gmail.com",
        "phone": "+220 567 8901",
        "location": "Tanji",
        "sector_name": "Agriculture",
        "is_partner": False,
        "is_verified": True,
        "is_featured": True,
        "interview_date": "2024-04-12",
        "interviewed_by": "Ebrima Barry",
        "status": "published"
    },
    {
        "name": "Gambia Realty Group",
        "owner_name": "Alieu Ceesay",
        "owner_position": "CEO",
        "description": "Gambia Realty Group is a full-service real estate agency handling residential and commercial properties, property management, and real estate investment consulting.",
        "short_description": "Full-service real estate agency",
        "email": "info@gambiarealty.gm",
        "phone": "+220 678 9012",
        "website": "https://gambiarealty.gm",
        "location": "Brusubi",
        "sector_name": "Real Estate & Construction",
        "is_partner": True,
        "is_verified": True,
        "is_featured": False,
        "partner_type": "service_provider",
        "interview_date": "2024-04-25",
        "interviewed_by": "Ebrima Barry",
        "status": "published"
    }
]

BUSINESS_PROFILE_FEATURES = [
    {
        "business_name": "Jow Feeds & Farm Supplies",
        "title": "500+ Farmers Served",
        "description": "Supplying over 500 poultry farmers across all regions of The Gambia",
        "icon": "Users",
        "order": 1
    },
    {
        "business_name": "Jow Feeds & Farm Supplies",
        "title": "30% Cost Reduction",
        "description": "Helped farmers reduce feed costs by 30% through bulk purchasing",
        "icon": "TrendingDown",
        "order": 2
    },
    {
        "business_name": "Banjul Taxi Co-op",
        "title": "50+ Vehicles",
        "description": "Fleet of over 50 well-maintained taxis serving Greater Banjul",
        "icon": "Car",
        "order": 1
    },
    {
        "business_name": "Gambia Solar Solutions",
        "title": "1,000+ Installations",
        "description": "Over 1,000 solar systems installed across the country",
        "icon": "Sun",
        "order": 1
    },
    {
        "business_name": "Kairaba Tech Hub",
        "title": "50+ Startups",
        "description": "Supported over 50 tech startups through incubation programs",
        "icon": "Rocket",
        "order": 1
    }
]

BUSINESS_PROFILE_TESTIMONIALS = [
    {
        "business_name": "Jow Feeds & Farm Supplies",
        "quote": "E-biz connected us with serious buyers and helped us expand our customer base significantly. The exposure has been invaluable.",
        "author_name": "Momodou Jallow",
        "author_position": "Founder",
        "is_featured": True,
        "order": 1
    },
    {
        "business_name": "Banjul Taxi Co-op",
        "quote": "Being featured on E-biz brought us new corporate clients. Our bookings increased by 40% within two months.",
        "author_name": "Lamin Sarr",
        "author_position": "General Manager",
        "is_featured": True,
        "order": 2
    },
    {
        "business_name": "Gambia Solar Solutions",
        "quote": "The market insights from E-biz helped us understand our customer needs better. Highly recommended for any business in Gambia.",
        "author_name": "Fatou Jammeh",
        "author_position": "Managing Director",
        "is_featured": False,
        "order": 3
    }
]