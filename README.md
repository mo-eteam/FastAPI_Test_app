# Role-Based API Application

## Prerequisites
- Docker
- Docker Compose

## Setup and Running

1. Clone the repository
```bash
git clone <your-repo-url>
cd Test_app
```

2. Create .env file
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Build and Run
```bash
docker-compose up --build
```

## Default Credentials
- Admin User
  - Username: admin
  - Password: adminpassword

- Test User
  - Username: testuser
  - Password: userpassword

## API Endpoints
- `/docs` - Swagger UI
- `/redoc` - ReDoc documentation
- `/auth/token` - Token generation endpoint

## Features
- Role-based access control
- JWT Authentication
- Async SQLAlchemy
- PostgreSQL database
- Docker deployment

## Development
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `pytest`

## Security
- Passwords are hashed
- JWT tokens with expiration
- Role-based access control
