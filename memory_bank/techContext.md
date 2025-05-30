# Tech Context

## Technologies used
- Backend: Python 3.x, Django, Django Rest Framework
- Databases: MongoDB, PostgreSQL
- Containerization: Docker, Docker Compose
- Caching: Redis
- Task Queue: Celery
- Authentication: Django Rest Framework JWT, Django Rest Framework Social OAuth2 JWT
- API Documentation: Django Rest Swagger

## Development setup
The project is designed to run within Docker containers. Local development requires Docker and Docker Compose installed. Database setup and migrations are handled via Django's `manage.py` commands, executed within the Docker containers.

## Technical constraints
- All API must be Backward compatible
- All variable and function name must be well define and snack case
- Efficient spaced repetition algorithm implementation.
- Integration with external Dictionary APIs.
- Project have standrad versioning

functions
- all function must have docstring
- all function must have type hinting
- all function must have unit test
- all function must have integration test

endpoints
- all endpoints must have swagger documentation with example request and response
- all endpoints must have version and backward compatible
- all endpoints must have E2E Test

## Dependencies
- To be detailed in `requirements.txt` within the main project directory

## Tool usage patterns
- Docker/Docker Compose for environment management.
- Django's `manage.py` for backend operations (migrations, running server, etc.).
- Git for version control.
- IDEs like VS Code for development.
