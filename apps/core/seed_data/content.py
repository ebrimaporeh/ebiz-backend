# apps/core/seed_data/content.py
from datetime import datetime, timedelta

# Helper to generate dates
def get_date(days_ago):
    return (datetime.now() - timedelta(days=days_ago)).date()

ARTICLES = [
    {
        "title": "Complete Guide to Starting a Taxi Business in Gambia",
        "slug": "complete-guide-taxi-business-gambia",
        "excerpt": "Detailed analysis of capital requirements, licensing process, daily operations, and profit margins for taxi services in urban and rural Gambia.",
        "content": """
        <h2>Introduction</h2>
        <p>The taxi business in Gambia presents a viable opportunity for entrepreneurs looking to enter the transportation sector. With growing urban population and increasing tourism, demand for reliable transportation continues to rise.</p>
        
        <h2>Capital Requirements</h2>
        <p>Starting a taxi business requires an initial investment of D150,000 to D300,000 depending on vehicle condition and type. Key costs include vehicle purchase (D120,000-D250,000), licensing (D5,000-D10,000), insurance (D15,000-D25,000), and initial fuel (D5,000-D10,000).</p>
        
        <h2>Licensing Process</h2>
        <p>Taxi operators must register with GRA, obtain a taxi permit from the local council, and ensure the vehicle passes roadworthiness inspection. Additional requirements include driver's license and public service vehicle license.</p>
        
        <h2>Daily Operations</h2>
        <p>Successful taxi operations require vehicle inspection before each shift, tracking mileage and fuel consumption, maintaining cleanliness, and providing excellent customer service.</p>
        """,
        "author": "GBI Research Team",
        "read_time": 12,
        "is_premium": False,
        "is_featured": True,
        "status": "published",
        "sector_name": "Transportation & Logistics",
        "business_name": "Taxi Services",
        "published_days_ago": 10
    },
    {
        "title": "Poultry Farming ROI Analysis 2024",
        "slug": "poultry-farming-roi-analysis-2024",
        "excerpt": "Comprehensive breakdown of investment requirements, operational costs, and revenue projections for modern poultry farming in Gambia.",
        "content": """
        <h2>Market Overview</h2>
        <p>The Gambian poultry market is valued at over D1.2 billion annually, with significant growth potential as local production currently meets only 40% of national demand.</p>
        
        <h2>Investment Breakdown</h2>
        <p>Small-scale operations (100-300 birds) require D50,000-D100,000 investment. Medium-scale (500-1,500 birds) requires D150,000-D250,000. Large-scale operations (3,000+ birds) require D1 million or more.</p>
        
        <h2>Profitability Analysis</h2>
        <p>Net profit margins range from 15-25% for small-scale, 20-30% for medium-scale, and 25-35% for large-scale operations. Payback period averages 6-8 months for small-scale and 5-7 months for larger operations.</p>
        
        <h2>Risk Factors</h2>
        <p>Key risks include disease outbreaks (Newcastle, Gumboro), feed price volatility, and market price fluctuations. Mitigation strategies include strict biosecurity, bulk feed purchasing, and market diversification.</p>
        """,
        "author": "Dr. Alieu Jallow",
        "read_time": 18,
        "is_premium": True,
        "is_featured": True,
        "status": "published",
        "sector_name": "Agriculture",
        "business_name": "Poultry Farming - Broilers",
        "published_days_ago": 15
    },
    {
        "title": "The Rise of Software Development in The Gambia",
        "slug": "rise-software-development-gambia",
        "excerpt": "Exploring the growing software development sector, talent availability, client markets, and investment opportunities.",
        "content": """
        <h2>Industry Growth</h2>
        <p>The software development sector in Gambia has grown 35% annually over the past three years, driven by increasing internet penetration, digital literacy, and remote work opportunities.</p>
        
        <h2>Talent Pool</h2>
        <p>Gambia boasts a growing community of self-taught and formally trained developers. University programs in computer science are expanding, and coding bootcamps are emerging.</p>
        
        <h2>Client Markets</h2>
        <p>Local businesses need custom software solutions for inventory management, accounting, and customer relationships. International clients offer remote development opportunities with higher rates.</p>
        
        <h2>Getting Started</h2>
        <p>Starting a software agency requires minimal capital (laptop, internet, skills). Success depends on portfolio building, networking, and delivering quality work consistently.</p>
        """,
        "author": "Tech Insights Team",
        "read_time": 15,
        "is_premium": False,
        "is_featured": True,
        "status": "published",
        "sector_name": "Technology & IT",
        "business_name": "Software Development Agency",
        "published_days_ago": 20
    },
    {
        "title": "Starting a Private School in Gambia: Complete Guide",
        "slug": "private-school-investment-guide-gambia",
        "excerpt": "Complete regulatory framework, setup costs, and operational requirements for establishing private schools in Gambia.",
        "content": """
        <h2>Regulatory Framework</h2>
        <p>Private schools must register with the Ministry of Basic and Secondary Education, obtain a license, and comply with curriculum standards and facility requirements.</p>
        
        <h2>Investment Requirements</h2>
        <p>Setting up a primary school requires D500,000-D2 million depending on scale and location. Costs include land/building (D200,000-D1 million), furniture and equipment (D100,000-D300,000), and initial staff salaries (D50,000-D150,000).</p>
        
        <h2>Operational Considerations</h2>
        <p>Key success factors include qualified teachers, competitive tuition pricing, good location, and parent communication. Marketing and reputation building are essential for enrollment growth.</p>
        """,
        "author": "Education Division",
        "read_time": 20,
        "is_premium": True,
        "is_featured": False,
        "status": "published",
        "sector_name": "Education & Training",
        "business_name": "Private School",
        "published_days_ago": 25
    },
    {
        "title": "Solar Energy Business Opportunities in Gambia",
        "slug": "solar-energy-business-opportunities-gambia",
        "excerpt": "Analysis of the growing renewable energy sector, focusing on solar power installation, maintenance services, and government incentives.",
        "content": """
        <h2>Market Potential</h2>
        <p>With abundant sunshine throughout the year (average 8-10 hours daily), Gambia presents excellent opportunities for solar energy businesses. The market has grown 40% annually over the past two years.</p>
        
        <h2>Business Models</h2>
        <p>Opportunities include solar panel installation and maintenance, solar product distribution (panels, batteries, inverters), energy consulting, and pay-as-you-go solar financing for households.</p>
        
        <h2>Government Incentives</h2>
        <p>The government offers tax incentives for renewable energy businesses and has partnered with development organizations to promote solar adoption through subsidies and financing programs.</p>
        
        <h2>Getting Started</h2>
        <p>Starting a solar business requires technical training (2-6 months), equipment suppliers, and marketing to residential and commercial customers. Initial investment ranges from D500,000 to D2 million.</p>
        """,
        "author": "Energy Solutions Division",
        "read_time": 17,
        "is_premium": False,
        "is_featured": True,
        "status": "published",
        "sector_name": "Renewable Energy",
        "business_name": "Solar Installation",
        "published_days_ago": 30
    }
]

VIDEOS = [
    {
        "title": "How to Start a Poultry Farm in Gambia",
        "slug": "how-to-start-poultry-farm-gambia",
        "description": "Step-by-step guide to starting a profitable poultry farming business in The Gambia, covering housing, feeding, vaccination, and marketing.",
        "platform": "youtube",
        "platform_video_id": "dQw4w9WgXcQ",
        "duration": 480,  # 8 minutes in seconds
        "is_premium": False,
        "is_featured": True,
        "status": "published",
        "sector_name": "Agriculture",
        "business_name": "Poultry Farming - Broilers",
        "published_days_ago": 5
    },
    {
        "title": "Taxi Business Economics: What You Need to Know",
        "slug": "taxi-business-economics-gambia",
        "description": "Analysis of taxi business profitability in The Gambia including costs, revenue projections, and tips for maximizing income.",
        "platform": "youtube",
        "platform_video_id": "dQw4w9WgXcQ",
        "duration": 420,  # 7 minutes
        "is_premium": False,
        "is_featured": False,
        "status": "published",
        "sector_name": "Transportation & Logistics",
        "business_name": "Taxi Services",
        "published_days_ago": 12
    },
    {
        "title": "Interview: Successful Solar Entrepreneur in Gambia",
        "slug": "interview-solar-entrepreneur-gambia",
        "description": "In-depth interview with a successful solar energy entrepreneur sharing insights on starting and growing a renewable energy business.",
        "platform": "youtube",
        "platform_video_id": "dQw4w9WgXcQ",
        "duration": 900,  # 15 minutes
        "is_premium": True,
        "is_featured": True,
        "status": "published",
        "sector_name": "Renewable Energy",
        "business_name": "Solar Installation",
        "published_days_ago": 18
    },
    {
        "title": "Real Estate Investment Tips for Diaspora Gambians",
        "slug": "real-estate-investment-diaspora",
        "description": "Essential tips for diaspora Gambians looking to invest in real estate back home, including legal considerations and property selection.",
        "platform": "youtube",
        "platform_video_id": "dQw4w9WgXcQ",
        "duration": 600,  # 10 minutes
        "is_premium": True,
        "is_featured": False,
        "status": "published",
        "sector_name": "Real Estate & Construction",
        "business_name": "Real Estate Agency",
        "published_days_ago": 22
    }
]

TAGS = [
    {"name": "Startup Guide", "articles": [0, 1], "videos": [0]},
    {"name": "Investment", "articles": [1, 3], "videos": [1, 3]},
    {"name": "ROI Analysis", "articles": [1], "videos": [1]},
    {"name": "Technology", "articles": [2], "videos": []},
    {"name": "Education", "articles": [3], "videos": []},
    {"name": "Renewable Energy", "articles": [4], "videos": [2]},
    {"name": "Agriculture", "articles": [1], "videos": [0]},
    {"name": "Transportation", "articles": [0], "videos": [1]},
    {"name": "Real Estate", "articles": [], "videos": [3]},
    {"name": "Diaspora Investment", "articles": [], "videos": [3]},
]

COMMENTS = [
    {
        "article_title": "Complete Guide to Starting a Taxi Business in Gambia",
        "user_name": "Lamin Sarr",
        "user_email": "lamin@example.com",
        "content": "This is very helpful! I've been considering starting a taxi service. The breakdown of costs is realistic and useful.",
        "is_approved": True
    },
    {
        "article_title": "Complete Guide to Starting a Taxi Business in Gambia",
        "user_name": "Fatou Jammeh",
        "user_email": "fatou@example.com",
        "content": "What about electric vehicles? Are there any incentives for eco-friendly taxis?",
        "is_approved": True
    },
    {
        "article_title": "Poultry Farming ROI Analysis 2024",
        "user_name": "Momodou Jallow",
        "user_email": "momodou@example.com",
        "content": "Excellent analysis! I've been in poultry for 5 years and this matches my experience. The feed cost breakdown is spot on.",
        "is_approved": True
    },
    {
        "article_title": "Poultry Farming ROI Analysis 2024",
        "user_name": "Aminata Sarr",
        "user_email": "aminata@example.com",
        "content": "Where can I find quality day-old chicks? Any supplier recommendations?",
        "is_approved": False
    }
]

CASE_STUDIES = [
    {
        "title": "How Jow Feeds Grew from a Small Shop to Market Leader",
        "slug": "jow-feeds-success-story",
        "excerpt": "The inspiring journey of Jow Feeds from a small feed shop in Brikama to the leading poultry feed supplier in The Gambia.",
        "content": """
        <h2>The Beginning</h2>
        <p>Momodou Jallow started Jow Feeds in 2018 with just D50,000 and a small shop in Brikama market. Recognizing the gap in quality, affordable poultry feed, he focused on building relationships with farmers.</p>
        
        <h2>Growth Strategy</h2>
        <p>By offering bulk purchasing discounts, free delivery, and technical advice to farmers, Jow Feeds built a loyal customer base. Within two years, they expanded to a larger warehouse and added equipment sales.</p>
        
        <h2>Challenges Overcome</h2>
        <p>Key challenges included feed price volatility, competition from imported feed, and cash flow management during the off-season. Strategic partnerships with importers and farmer cooperatives helped overcome these.</p>
        
        <h2>Key Lessons</h2>
        <p>Success came from understanding customer needs, building trust, and investing in relationships. Today, Jow Feeds serves over 500 farmers and continues to grow.</p>
        """,
        "business_name": "Jow Feeds & Farm Supplies",
        "business_type": "Feed Supplier",
        "sector_name": "Agriculture",
        "initial_investment": 50000,
        "revenue_generated": 5000000,
        "roi_percent": 9900,
        "timeline_months": 60,
        "is_success": True,
        "key_lessons": "Focus on customer relationships, bulk purchasing for cost savings, diversify product offerings, invest in reliable logistics.",
        "author": "Ebrima Barry",
        "is_featured": True,
        "status": "published",
        "published_days_ago": 40
    },
    {
        "title": "Banjul Taxi Co-op: Organizing for Success",
        "slug": "banjul-taxi-coop-success",
        "excerpt": "How a cooperative of taxi drivers transformed individual operations into a unified, professional service.",
        "content": """
        <h2>The Challenge</h2>
        <p>Before forming the cooperative, taxi drivers in Banjul faced challenges including price undercutting, poor vehicle maintenance, and lack of bargaining power with suppliers.</p>
        
        <h2>The Solution</h2>
        <p>In 2020, 30 drivers formed Banjul Taxi Co-op with uniform pricing, shared maintenance facilities, bulk fuel purchasing, and a central dispatch system.</p>
        
        <h2>Results</h2>
        <p>The cooperative now has 50+ members, increased individual incomes by 40%, reduced maintenance costs by 25%, and secured corporate contracts with hotels and businesses.</p>
        
        <h2>Key Takeaways</h2>
        <p>Collective action and professional standards transformed individual struggling businesses into a thriving cooperative model that benefits all members.</p>
        """,
        "business_name": "Banjul Taxi Co-op",
        "business_type": "Taxi Cooperative",
        "sector_name": "Transportation & Logistics",
        "initial_investment": 25000,
        "revenue_generated": None,
        "roi_percent": None,
        "timeline_months": 36,
        "is_success": True,
        "key_lessons": "Collective bargaining power, standardization improves customer trust, shared resources reduce costs.",
        "author": "Ebrima Barry",
        "is_featured": True,
        "status": "published",
        "published_days_ago": 35
    }
]