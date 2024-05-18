# HappyPaws

## Introduction
HappyPaws is a comprehensive web application designed to enhance the overall well-being of pets by providing owners with access to veterinary-level diet knowledge, custom reminders, and a vibrant forum for community interaction.

## Features
- **Pet Profiles**: Users can create detailed profiles for their pets including medical history and dietary preferences.
- **Custom Reminders**: Set reminders for medications, vet visits, play dates, etc.
- **Nutritional Guidance**: Access a database of pet food and supplements to discover the best options for your pet.
- **Community Forum**: Engage with other pet owners to exchange tips and stories.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI, Python
- **Database**: PostgreSQL
- **Cloud Services**: AWS S3 for image hosting
- **Security**: OAuth2 authentication, Bcrypt for password hashing
- **Containerization**: Docker

## Setup and Installation
```bash
# Clone the repository
git clone https://github.com/your-username/happypaws.git
cd happypaws

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
