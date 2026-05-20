# apps/core/seed_data/operations_checklists.py

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
        "description": "Ensure clean water is available. Clean drinkers if necessary.",
        "time_of_day": "Morning",
        "responsible": "Farm Worker",
        "duration_minutes": 20,
        "order": 3
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Litter Management",
        "description": "Check litter condition. Add fresh bedding if needed.",
        "time_of_day": "Midday",
        "responsible": "Farm Worker",
        "duration_minutes": 30,
        "order": 4
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "daily",
        "task_name": "Evening Check",
        "description": "Final check of birds, feed, and water. Record any observations.",
        "time_of_day": "Evening",
        "responsible": "Farm Manager",
        "duration_minutes": 20,
        "order": 5
    },
    # Poultry - Weekly Tasks
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "weekly",
        "task_name": "Equipment Inspection",
        "description": "Inspect feeders, drinkers, and heating equipment for proper function.",
        "time_of_day": "",
        "responsible": "Farm Manager",
        "duration_minutes": 60,
        "order": 1
    },
    {
        "business_name": "Poultry Farming - Broilers",
        "scale_type": "all",
        "task_type": "weekly",
        "task_name": "Vaccination",
        "description": "Administer scheduled vaccinations based on the vaccination calendar.",
        "time_of_day": "",
        "responsible": "Vet/Farm Manager",
        "duration_minutes": 120,
        "order": 2
    },
    # Taxi - Daily Tasks
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "task_type": "daily",
        "task_name": "Vehicle Inspection",
        "description": "Check tires, oil, fuel, lights, and overall vehicle condition.",
        "time_of_day": "Morning",
        "responsible": "Driver",
        "duration_minutes": 15,
        "order": 1
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "task_type": "daily",
        "task_name": "Clean Vehicle",
        "description": "Clean interior and exterior of the vehicle.",
        "time_of_day": "Morning",
        "responsible": "Driver",
        "duration_minutes": 20,
        "order": 2
    },
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "task_type": "daily",
        "task_name": "Record Keeping",
        "description": "Record daily trips, income, fuel purchases, and expenses.",
        "time_of_day": "Evening",
        "responsible": "Owner/Driver",
        "duration_minutes": 15,
        "order": 3
    },
    # Taxi - Weekly Tasks
    {
        "business_name": "Taxi Services",
        "scale_type": "small",
        "task_type": "weekly",
        "task_name": "Full Vehicle Check",
        "description": "Comprehensive inspection including brakes, suspension, and electrical systems.",
        "time_of_day": "",
        "responsible": "Mechanic",
        "duration_minutes": 60,
        "order": 1
    },
    # Software Agency - Daily Tasks
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "task_type": "daily",
        "task_name": "Stand-up Meeting",
        "description": "Team meeting to discuss progress, blockers, and plans for the day.",
        "time_of_day": "Morning",
        "responsible": "Team Lead",
        "duration_minutes": 15,
        "order": 1
    },
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "task_type": "daily",
        "task_name": "Code Review",
        "description": "Review team members' code for quality and best practices.",
        "time_of_day": "Afternoon",
        "responsible": "Senior Developer",
        "duration_minutes": 60,
        "order": 2
    },
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "task_type": "daily",
        "task_name": "Client Communication",
        "description": "Respond to client messages, provide updates, and address concerns.",
        "time_of_day": "Midday",
        "responsible": "Project Manager",
        "duration_minutes": 30,
        "order": 3
    },
    # Software Agency - Weekly Tasks
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "task_type": "weekly",
        "task_name": "Sprint Planning",
        "description": "Plan tasks and priorities for the upcoming sprint.",
        "time_of_day": "",
        "responsible": "Project Manager",
        "duration_minutes": 60,
        "order": 1
    },
    {
        "business_name": "Software Development Agency",
        "scale_type": "small",
        "task_type": "weekly",
        "task_name": "Sprint Review",
        "description": "Review completed work and demonstrate to stakeholders.",
        "time_of_day": "",
        "responsible": "Project Manager",
        "duration_minutes": 60,
        "order": 2
    }
]