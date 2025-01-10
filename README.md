# Book Review Service API

A RESTful API built with FastAPI for managing book reviews and user interactions. This project demonstrates expertise in building scalable backend systems using Python and modern web technologies.

## 🛠 Technical Stack

-   **Framework**: FastAPI - High-performance async web framework
-   **Database**: PostgreSQL with SQLModel ORM
-   **Authentication**: JWT-based auth system with refresh tokens
-   **Caching**: Redis for token management and session storage
-   **Task Queue**: Celery for handling async operations like email notifications
-   **Testing**: Comprehensive test coverage using pytest with async support
-   **API Documentation**: Auto-generated OpenAPI/Swagger docs

## 🏗 Architecture Highlights

### Clean Architecture

-   Modular design with separate layers for routes, services, and models
-   Clear separation of concerns between auth, books, and reviews modules
-   Dependency injection pattern for better testability and maintainability

### Security Features

-   JWT-based authentication with access and refresh tokens
-   Password hashing with bcrypt
-   Role-based access control (Admin/User roles)
-   Email verification system
-   Redis-based token blocklist for secure logout

### Database Design

-   SQLModel for type-safe database operations
-   Async database operations with SQLAlchemy
-   Database migrations using Alembic
-   Proper relationship modeling between users, books, and reviews

### Modern Python Practices

-   Type hints throughout the codebase
-   Async/await for non-blocking operations
-   Pydantic models for request/response validation
-   Extensive use of Python's newest features

### Testing & Quality

-   Comprehensive test suite with pytest
-   Async test support with pytest-asyncio
-   Test fixtures and mocks for database and external services
-   Pre-commit hooks for code quality
-   Ruff and Black for code formatting

## 🎯 Key Features

-   User authentication and authorization
-   Book management system
-   Review system with ratings
-   Email notifications
-   Role-based access control
-   Async operations for better performance
-   Comprehensive API documentation
-   Token-based security

This project demonstrates my expertise in:

-   Building production-ready REST APIs
-   Working with modern Python frameworks
-   Implementing secure authentication systems
-   Database design and management
-   Writing testable and maintainable code
-   Following best practices in software development
