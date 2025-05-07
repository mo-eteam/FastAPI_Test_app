# FastAPI Test Application Design Document

## 1. Project Overview
- **Name**: FastAPI Test Application
- **Purpose**: Role-based API with User and Category Management
- **Technology Stack**: 
  - Backend: FastAPI
  - Database: PostgreSQL
  - ORM: SQLAlchemy (Async)
  - Authentication: JWT
  - Containerization: Docker

## 2. System Architecture
### 2.1 High-Level Components
- **Web Server**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT-based
- **Containerization**: Docker Compose

### 2.2 Architecture Diagram
```
[Client] <-> [FastAPI Server] <-> [PostgreSQL Database]
           |
           v
      [Authentication Layer]
```

## 3. Database Schema

### 3.1 Users Table
- **Fields**:
  - `id`: Primary Key (Integer)
  - `username`: Unique String
  - `email`: Unique String
  - `hashed_password`: String
  - `role`: Enum (ADMIN, USER, COMPANY_ADMIN)
  - `company_id`: Foreign Key to Companies
  - `created_at`: Timestamp
  - `last_login`: Timestamp

### 3.2 Companies Table
- **Fields**:
  - `id`: Primary Key (String)
  - `name`: String

### 3.3 Prompt Management Table
- **Fields**:
  - `id`: Primary Key (Integer)
  - `company_id`: Foreign Key to Companies
  - `prompt_title`: String
  - `prompt`: Text
  - `created_at`: Timestamp
  - `updated_at`: Timestamp

## 4. Authentication Flow
1. User registers/logs in
2. Server validates credentials
3. Generate JWT token
4. Token used for subsequent authenticated requests

## 5. API Endpoints

### 5.1 Authentication Endpoints
- `POST /api/auth/register`: User registration
- `POST /api/auth/login`: User login
- `POST /api/auth/token`: Token refresh

### 5.2 User Endpoints
- `GET /api/users/`: List users
- `GET /api/users/{user_id}`: Get user details
- `PUT /api/users/{user_id}`: Update user
- `DELETE /api/users/{user_id}`: Delete user

### 5.3 Company Endpoints
- `GET /api/categories/`: List companies
- `POST /api/categories/`: Create company
- `GET /api/categories/{company_id}`: Get company details

### 5.4 Prompt Endpoints
- `GET /api/prompts/{company_id}`: Get prompts for a company
- `POST /api/prompts/`: Create new prompt
- `PUT /api/prompts/{prompt_id}`: Update prompt

## 6. Role-Based Access Control
- **ADMIN**: Full system access
- **USER**: Limited access to specific resources
- **COMPANY_ADMIN**: Manage company-specific resources

## 7. Security Considerations
- Password hashing with bcrypt
- JWT token-based authentication
- Role-based access control
- HTTPS enforcement
- Input validation

## 8. Error Handling
- Custom error responses
- Logging of critical errors
- Graceful error messages

## 9. Performance Considerations
- Async database operations
- Connection pooling
- Efficient query design

## 10. Future Improvements
- Rate limiting
- More granular permissions
- Comprehensive logging
- Enhanced error tracking

## 11. Development Best Practices
- Modular code structure
- Dependency injection
- Comprehensive testing
- Continuous integration

## 12. Deployment
- Containerized with Docker
- Environment-specific configurations
- Easy scalability

## 13. Sequence Diagrams

### 13.1 User Authentication
```
Client -> AuthController: Login Request
AuthController -> UserRepository: Validate Credentials
UserRepository -> Database: Check User
Database --> UserRepository: User Verified
UserRepository --> AuthController: User Details
AuthController -> TokenService: Generate JWT
TokenService --> AuthController: JWT Token
AuthController --> Client: Login Success
```

### 13.2 Prompt Retrieval
```
Client -> PromptController: Get Prompts Request
PromptController -> AuthMiddleware: Validate Token
AuthMiddleware -> TokenService: Verify JWT
TokenService --> AuthMiddleware: Token Valid
AuthMiddleware -> PromptController: Access Granted
PromptController -> PromptRepository: Fetch Prompts
PromptRepository -> Database: Query Prompts
Database --> PromptRepository: Prompt Data
PromptRepository --> PromptController: Prompts
PromptController --> Client: Return Prompts
```

## 14. Development Setup
- Clone repository
- Set up `.env`
- Run `docker-compose up --build`

## 15. Testing Strategy
- Unit Tests
- Integration Tests
- API Endpoint Tests
- Security Vulnerability Tests
