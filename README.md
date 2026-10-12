# Community Marketplace for Services

## Project Description
Community Marketplace is a web application that connects customers with local service providers. Customers can explore available services, view provider details, and book services. Service providers can create profiles and manage booking requests.

## Technologies Used
- Python
- Django
- MySQL (local development)
- PostgreSQL (deployment)
- HTML and CSS
- Git and GitHub

## Main Features
- User registration and login
- Service provider profiles
- Browse and search services
- Book services
- Provider dashboard
- Accept or reject booking requests
- View customer bookings

## Project Structure
- `bookings/` – Booking management
- `community_marketplace/` – Main Django project settings and URLs
- `reviews/` – Reviews application
- `services/` – Service providers and service listings
- `users/` – User registration and authentication
- `templates/` – HTML templates
- `static/` – Static files and images
- `manage.py` – Django management utility
- `requirements.txt` – Python dependencies
- `build.sh` – Deployment build script

## Live Website
https://community-marketplace-sqk3.onrender.com/

## GitHub Repository
https://github.com/BhumikaKolluru/community_marketplace

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/BhumikaKolluru/community_marketplace.git
   ```
2. Navigate to the project directory:
   ```bash
   cd community_marketplace
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the database settings and required environment variables.
5. Run database migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Purpose
The project aims to support local businesses and help customers find service providers within their community.
