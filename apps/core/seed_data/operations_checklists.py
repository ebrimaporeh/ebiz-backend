"""
Operations checklists seed data
"""

OPERATIONS_CHECKLISTS = [
    # Poultry - Daily Tasks
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Morning Check",
        "description": "Check birds for any signs of illness or distress. Verify feed and water levels.",
        "time_of_day": "Morning",
        "responsible": "Farm Manager",
        "duration_minutes": 30,
        "order": 1
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Feeding",
        "description": "Provide fresh feed according to the feeding schedule for the birds' age.",
        "time_of_day": "Morning",
        "responsible": "Farm Worker",
        "duration_minutes": 45,
        "order": 2
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Water Check",
        "description": "Ensure waterers are clean and functioning. Refill as needed.",
        "time_of_day": "Midday",
        "responsible": "Farm Worker",
        "duration_minutes": 20,
        "order": 3
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Litter Management",
        "description": "Turn or add bedding material to keep litter dry and reduce ammonia.",
        "time_of_day": "Afternoon",
        "responsible": "Farm Worker",
        "duration_minutes": 45,
        "order": 4
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Evening Check",
        "description": "Final check of birds, feed, water, and security before close.",
        "time_of_day": "Evening",
        "responsible": "Farm Manager",
        "duration_minutes": 25,
        "order": 5
    },
    
    # Poultry - Weekly Tasks
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "weekly",
        "task_name": "Deep Cleaning",
        "description": "Thorough cleaning of feeders, drinkers, and equipment.",
        "responsible": "Farm Worker",
        "duration_minutes": 120,
        "order": 1
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "weekly",
        "task_name": "Health Inspection",
        "description": "Catch and examine sample birds for weight gain and health issues.",
        "responsible": "Farm Manager",
        "duration_minutes": 90,
        "order": 2
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "weekly",
        "task_name": "Inventory Check",
        "description": "Count remaining feed and medication supplies. Reorder if needed.",
        "responsible": "Farm Manager",
        "duration_minutes": 45,
        "order": 3
    },
    
    # Poultry - Monthly Tasks
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "monthly",
        "task_name": "Financial Reconciliation",
        "description": "Review income, expenses, and profit for the month.",
        "responsible": "Owner/Manager",
        "duration_minutes": 120,
        "order": 1
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "monthly",
        "task_name": "Equipment Maintenance",
        "description": "Inspect and service fans, heaters, and water systems.",
        "responsible": "Farm Manager",
        "duration_minutes": 180,
        "order": 2
    },
    
    # Taxi Services - Daily Tasks
    {
        "business_name": "Taxi Services",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Vehicle Inspection",
        "description": "Check tyres, oil, water, lights, and brakes before starting shift.",
        "time_of_day": "Morning",
        "responsible": "Driver",
        "duration_minutes": 15,
        "order": 1
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Vehicle Cleaning",
        "description": "Clean interior and exterior of vehicle.",
        "time_of_day": "Morning",
        "responsible": "Driver",
        "duration_minutes": 20,
        "order": 2
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Fuel Check",
        "description": "Refuel as needed and record mileage.",
        "time_of_day": "Morning",
        "responsible": "Driver",
        "duration_minutes": 10,
        "order": 3
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Cash Reconciliation",
        "description": "Count daily earnings and record in logbook.",
        "time_of_day": "Evening",
        "responsible": "Driver",
        "duration_minutes": 15,
        "order": 4
    },
    
    # Taxi - Weekly Tasks
    {
        "business_name": "Taxi Services",
        "scale_type": "all",
        "task_type": "weekly",
        "task_name": "Professional Car Wash",
        "description": "Full professional cleaning of vehicle.",
        "responsible": "Driver",
        "duration_minutes": 60,
        "order": 1
    },
    
    # Solar Installation - Daily Tasks
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Tool Check",
        "description": "Verify all tools and equipment are present and in working order.",
        "time_of_day": "Morning",
        "responsible": "Technician",
        "duration_minutes": 15,
        "order": 1
    },
    {
        "business_name": "Solar Panel Installation",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Site Safety Check",
        "description": "Review site safety before beginning installation work.",
        "time_of_day": "Morning",
        "responsible": "Site Supervisor",
        "duration_minutes": 20,
        "order": 2
    },
    
    # Mobile Money - Daily Tasks
    {
        "business_name": "Mobile Money Agency",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Cash Count",
        "description": "Count float and record beginning balance.",
        "time_of_day": "Morning",
        "responsible": "Agent",
        "duration_minutes": 10,
        "order": 1
    },
    {
        "business_name": "Mobile Money Agency",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "End-of-Day Reconciliation",
        "description": "Reconcile transactions and count ending cash balance.",
        "time_of_day": "Evening",
        "responsible": "Agent",
        "duration_minutes": 20,
        "order": 2
    },
]