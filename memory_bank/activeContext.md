# Active Context: AI-Powered Language Learning Backend

## Current Work Focus

- Completed OTP-based authentication system
- Integrated Kaveh Negar SMS service
- Documented authentication API in Swagger

## Recent Changes

- Added KAVEH_NEGAR_API_KEY to environment variables
- Created authentication serializers and services
- Implemented OTP request and verification views
- Configured authentication URLs

## Next Steps

- Write unit tests for authentication endpoints
- Implement rate limiting for OTP requests
- Add Swagger documentation for new endpoints

## Key Decisions

- Using Redis with 2-minute TTL for OTP caching
- New users created with is_active=False until OTP verification
- JWT tokens issued upon successful OTP verification

## Completed Tasks

1. Implemented OTP request and verification endpoints
2. Integrated Kaveh Negar SMS service
3. Created Redis caching service for OTPs
4. Configured authentication URLs

## Learnings

- Kaveh Negar Python SDK simplifies SMS integration
- Django's get_or_create() is efficient for user management
- Careful line length management needed for Flake8 compliance
