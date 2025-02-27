AnimalCorePro is a comprehensive animal data management system designed for tracking and processing information about various animal types, breeds, individual characteristics, and weight records. It features user registration and management, along with API access and a React-based frontend.
Data Structure
•	AnimalType: Stores information about animal types (e.g., cow, horse) with unique identifiers.
•	Breed: Contains breed details, linking them to animal types.
•	Animal: Maintains individual records, including inventory number, gender, name, arrival date, age, breed, and parent reference.
•	Weighting: Records animal weight measurements with a restriction of one entry per animal per date.
User Roles & Permissions
•	Admin: Full access to all data and management features.
•	User: Restricted access, only able to view their own weight records.
Core Features
•	CRUD operations for all data entities with validation.
•	User registration with unique logins and email activation.
•	API for seamless system interaction.
•	React-based frontend for registration, data visualization, and editing.
Tech Stack
•	Backend: Python (Django)
•	Frontend: React
•	Database: SQLite
AnimalCorePro offers a structured and efficient solution for managing animal-related data while ensuring secure user access and streamlined operations.
