# Tech Context

## Technologies used
- Backend: Python 3.x, Django, Django Rest Framework
- Databases: MongoDB, PostgreSQL
- Containerization: Docker, Docker Compose
- Caching: Redis
- Task Queue: Celery
- Authentication: Django Rest Framework JWT, Django Rest Framework Social OAuth2 JWT
- API Documentation: Django Rest Swagger
- Frontend: Flutter

## Development setup
The project is designed to run within Docker containers. Local development requires Docker and Docker Compose installed. Database setup and migrations are handled via Django's `manage.py` commands, executed within the Docker containers.

## Technical constraints
- Mobile-first approach for the frontend.
- Integration with external Dictionary APIs.
- AI optimization for word information.
- Efficient spaced repetition algorithm implementation.

## Dependencies
(To be detailed in `requirements.txt` within the main project directory, which is currently inaccessible.)

## Tool usage patterns
- Docker/Docker Compose for environment management.
- Django's `manage.py` for backend operations (migrations, running server, etc.).
- Git for version control.
- IDEs like VS Code for development.
