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
### Create identical .env files both in the root folder and the src folder with the following:
PGPASSWORD=YOUR_PASSWORD
DB_USERNAME=YOUR_USERNAME
DB_PASSWORD=YOUR_PASSWORD
DB_HOST=db
DB_PORT=5432
DB_NAME=pet_parent
SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=HS256
AWS_ACCESS_KEY_ID=YOUR_ACCESS_ID
AWS_SECRET_ACCESS_KEY=YOUR_ACCESS_KEY

Be sure to have Docker installed.
https://www.docker.com/products/docker-desktop/
```bash
# Clone the repository
git clone https://github.com/tvanaken/HappyPaws.git
cd happypaws

# Build the application
Docker compose up

# Open the application
http://localhost:8000/Login_page/
```
### Login/Sign-up
![Screenshot 2024-04-20 152726](https://github.com/tvanaken/HappyPaws/assets/89529903/c2375a09-9679-4e46-bdb2-c8cef8171c71)

### Profile
<img width="959" alt="profile" src="https://github.com/tvanaken/HappyPaws/assets/89529903/a2c9b81c-9e65-4077-a308-d5491539c1f8">

### Add Pet Form
![Screenshot 2024-05-06 070628](https://github.com/tvanaken/HappyPaws/assets/89529903/653e4d14-8028-4f5a-9370-73b9d3933aa2)

### Diet Recommendations based on pet's breed. age, and activity level
![food](https://github.com/tvanaken/HappyPaws/assets/89529903/b2e84247-48e0-44be-94ef-aad03e824548)

### JavaScript FullCalendar
<img width="959" alt="calendar" src="https://github.com/tvanaken/HappyPaws/assets/89529903/3d0e408a-5411-4e24-97d7-aab277a02d2f">

### Forum. Able to be filtered by breed and/or keywords
<img width="959" alt="Forum" src="https://github.com/tvanaken/HappyPaws/assets/89529903/265d7528-9957-488c-8de9-cc477b026e7c">

### Users are able to comment on forum posts
<img width="959" alt="post" src="https://github.com/tvanaken/HappyPaws/assets/89529903/e1e636c4-5964-46a0-bf39-0e9b88c18b3e">

