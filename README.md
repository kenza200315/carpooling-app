# Carpooling Web Application v2.0

A modern carpooling platform similar to BlaBlaCar or InDrive with price negotiation, secure authentication, payment processing, and comprehensive reservation management.

## Features

### Core Features
- ✅ **Trip Management** - Drivers can create and manage trips
- ✅ **Ride Search** - Passengers can search available trips with filters
- ✅ **Price Negotiation** - Passengers propose prices, drivers accept/reject/counter
- ✅ **Offer Management** - Full offer lifecycle management

### Security & Authentication
- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **Password Hashing** - bcrypt password hashing for security
- ✅ **Role-Based Access Control** - Driver, Passenger, Admin roles
- ✅ **User Registration & Login** - Secure user management

### Payment System
- ✅ **Payment Processing** - Simulated payment system
- ✅ **Multiple Payment Methods** - Credit card, PayPal, Stripe
- ✅ **Payment Status Tracking** - Pending, Paid, Refunded
- ✅ **Revenue Reporting** - Admin dashboard for revenue tracking

### Reservation System
- ✅ **Seat Reservations** - Passengers can reserve seats
- ✅ **Reservation Status** - Pending, Confirmed, Cancelled
- ✅ **Capacity Management** - Automatic seat availability tracking

### Reviews & Ratings
- ✅ **Five-Star Ratings** - 1-5 star rating system
- ✅ **User Reviews** - Comments and feedback system
- ✅ **Reputation Management** - Build user profiles and trust

### Notifications
- ✅ **Real-Time Alerts** - Price proposals, offer status, reservations
- ✅ **Notification History** - View all notifications
- ✅ **Read/Unread Status** - Track notification engagement

### Admin Dashboard
- ✅ **User Management** - View and manage all users
- ✅ **Trip Control** - Remove problematic trips
- ✅ **System Statistics** - Dashboard with key metrics
- ✅ **Revenue Analytics** - Financial reporting

### Testing
- ✅ **Automated Tests** - pytest integration
- ✅ **API Testing** - Full endpoint coverage

## Local Deployment

### Prerequisites
- Python 3.8+
- pip

### Setup Instructions

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the application**
   - Frontend: http://localhost:8000/static/index.html
   - API Docs: http://localhost:8000/docs

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Setup Instructions

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Frontend: http://localhost:8000/static/index.html
   - API Docs: http://localhost:8000/docs
   - Database: localhost:5432

3. **Stop the application**
   ```bash
   docker-compose down
   ```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Trips
- `GET /trips` - List all trips
- `GET /trips/search?departure_city=X&destination_city=Y&max_price=Z` - Search trips
- `POST /trips` - Create a new trip
- `DELETE /trips/{id}` - Delete a trip

### Offers
- `POST /offers` - Create price offer
- `GET /offers/{trip_id}` - View offers for a trip
- `PATCH /offers/{id}` - Update offer status
- `PATCH /offers/{id}/counter` - Send counter offer

### Payments
- `POST /payments` - Process payment
- `GET /payments/{trip_id}` - View trip payments

### Reservations
- `POST /reservations` - Create reservation
- `GET /reservations/{trip_id}` - View trip reservations

### Reviews
- `POST /reviews` - Submit review (1-5 stars)
- `GET /reviews/{trip_id}` - View trip reviews

### Notifications
- `GET /notifications` - Get all notifications
- `POST /notifications` - Create notification

### Admin
- `GET /admin/users` - List all users
- `GET /admin/stats` - System statistics
- `DELETE /admin/trips/{id}` - Remove trip

## Testing

Run automated tests:
```bash
pytest tests/
```

## Security Features

- JWT Authentication with bcrypt password hashing
- Role-based access control (Driver, Passenger, Admin)
- CORS support for frontend requests
- Pydantic input validation
- Secure error handling

## Architecture

- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: SQLite (local) / PostgreSQL (production via Docker)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: JWT tokens

## File Structure

```
├── main.py                  # Application entry point
├── database.py              # Database config
├── models.py                # SQLAlchemy models
├── schemas.py               # Pydantic schemas
├── security.py              # Authentication
├── requirements.txt         # Dependencies
├── routers/                 # API route handlers
│   ├── auth.py
│   ├── trips.py
│   ├── offers.py
│   ├── payments.py
│   ├── reservations.py
│   ├── reviews.py
│   ├── notifications.py
│   └── admin.py
├── static/                  # Frontend files
│   ├── index.html
│   ├── trips.html
│   ├── create_trip.html
│   ├── offer.html
│   ├── styles.css
│   └── app.js
├── tests/                   # Automated tests
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

## Environment Variables

```
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///./carpool.db
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Troubleshooting

**Port 8000 already in use**
```bash
python -m uvicorn main:app --port 8001
```

**Database issues**
```bash
rm carpool.db  # Reset database
```

**Dependency errors**
```bash
pip install -r requirements.txt --force-reinstall
```

## Version

v2.0.0 - Enhanced edition with authentication, payments, reservations, reviews, and Docker support