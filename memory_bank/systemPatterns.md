# System Patterns

## System architecture
The system is a Django-based backend with MongoDB for document-based data and PostgreSQL for relational data. It is containerized using Docker.

## Key technical decisions
- Backend: Django, Django Rest Framework
- Databases: MongoDB (document), PostgreSQL (relational)
- Containerization: Docker
- Caching: Redis
- Task Queue: Celery
- Authentication: Django Rest Framework JWT, Django Rest Framework Social OAuth2 JWT
- API Documentation: Django Rest Swagger
- 

## Design patterns in use
(To be documented as development progresses)

## Component relationships
- Django application interacts with MongoDB and PostgreSQL.
- Redis for caching and Celery for background tasks.
- Django Rest Framework handles API endpoints.

## Critical implementation paths
- Word import and AI optimization.
- Deck creation and word categorization.
- Spaced repetition algorithm (FSRF) for learning.
- User authentication and registration.
