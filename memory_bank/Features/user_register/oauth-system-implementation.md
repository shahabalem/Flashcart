# auth-system-implementation.md

## Requirements

- OAuth2 implementation
- Support for Google Oauth2 
- Rate limiting on auth endpoints
- combine login and register in one endpoint (front project doesn't know that user is now or not)
- 

## Technical Decisions

-   Using Passport.py for provider integration
-   JWT for session management
-   Redis for rate limiting