# Online Store

## Overview
This project is an **online store**, built using **Django, PostgreSQL, Celery (RabbitMQ as a broker), and Razorpay for payments**. The platform is deployed on a **Digital Ocean droplet** with **Nginx and Gunicorn**.

## Features
- **User Authentication**: Supports Django authentication and Google social login.
- **Product Browsing & Search**: Users can browse products and search for specific items.
- **Cart Management**: Implements Django sessions for adding/removing items to/from the cart.
- **Order Processing**: Secure order placement with invoice generation.
- **Secure Payments**: Integrated Razorpay with webhook verification.
- **Task Handling**: Uses Celery with RabbitMQ for background tasks.
- **Admin Dashboard**: Admin panel for managing users, orders, and products.

## Target Audience
- **Small and Medium Businesses (SMBs)** looking for an affordable e-commerce solution.
- **End-users** who need a user-friendly platform for purchasing products.
- **Developers & Entrepreneurs** wanting to expand or customize the platform for niche markets.

## Tech Stack
- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Frontend**: Django Templates (can be extended with React/Vue)
- **Task Queue**: Celery with RabbitMQ
- **Payments**: Razorpay
- **Deployment**: Digital Ocean, Nginx, Gunicorn

## Installation & Setup

### 1. Clone the Repository
```sh
 git clone https://github.com/snaveen891/ecomsite.git
 cd ecomsite
```

### 2. Set Up a Virtual Environment
```sh
 python3 -m venv venv
 source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
 pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root and add:
```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/your_db_name
RAZORPAY_KEY=your_razorpay_key
RAZORPAY_SECRET=your_razorpay_secret
```

### 5. Run Migrations
```sh
 python manage.py migrate
```

### 6. Create a Superuser
```sh
 python manage.py createsuperuser
```

### 7. Start the Server
```sh
 python manage.py runserver
```
Access the app at `http://127.0.0.1:8000/`.

### 8. Set Up Celery & RabbitMQ
Start RabbitMQ:
```sh
 sudo service rabbitmq-server start
```
Start Celery:
```sh
 celery -A ecomsite worker --loglevel=info
```

## Deployment
The project is deployed on **Digital Ocean** using **Nginx and Gunicorn**. For deployment, follow these steps:
1. **Set up a Digital Ocean droplet** and install necessary dependencies.
2. **Configure PostgreSQL on the server**.
3. **Set up Gunicorn and Nginx**.
4. **Set up Celery workers**.

## License
This project is licensed under the MIT License.
