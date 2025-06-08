# Technical & Workflow Conventions: AI-Powered Language Learning Backend

This document outlines the essential guidelines, workflow practices, and technical standards for the development of the AI-Powered Language Learning Backend. Adhering to these conventions ensures consistency, code quality, and efficient collaboration.

---

### 🛠 Project Setup & Context

**Project Name:** AI-Powered Language Learning Backend
**Objective:** To provide a robust, intelligent backend for a mobile language learning application, focused on AI-optimized content and spaced repetition.
**Key Technologies:**

- **Backend:** Python 3.x, Django 5.x, Django REST Framework, PostgreSQL, MongoDB
- **Frontend (Conceptual):** Flutter 3.x (Dart), Provider for state management (Note: This backend project will support a mobile frontend)
- **Dev Tools:** Git, GitHub, Docker (for containerization)
- **Logging Aggregation:** Elastic database (for centralized logging)

**MVP Exclusions (Backend Scope):**
Advanced conversational AI, full-scale NLP for free-form language practice, complex integrated payment systems, direct user-to-user communication features, comprehensive analytics dashboards, multi-language support for the backend system itself (focused on single target language processing).

---

### ⚙️ Workflow & Task Execution

1.  **Plan First:** For any multi-line code changes or modifications to existing functionality, plan your approach. Get alignment before execution.
2.  **Design Ambiguity:** If a task is unclear or involves significant design choices, ask clarifying questions. Propose multiple approaches with their trade-offs when necessary.
3.  **Incremental Progress:** Break down complex tasks into smaller, manageable sub-tasks. Complete and validate each before moving to the next.
4.  **Project Conventions:** Always refer to this document (`technical_conventions.md`) for guidance on naming, folder structure, and other project standards. If still unsure, clarify before proceeding.
5.  **Scope Control:** If a task seems too broad, suggest narrowing its scope or specify the exact files/directories you intend to modify.
6.  **Minimal Diff:** Avoid reformatting unrelated lines or making unnecessary changes that inflate the code difference in pull requests.
7.  **Module Focus:** When possible, keep changes localized within a single module or component, unless a broader refactor is explicitly planned.
8.  **Multiple Options:** When asked for solutions, provide several options with their pros and cons.
9.  **Dependencies:** Do not introduce new third-party libraries or major external services without prior discussion and approval.
10. **Working Directory:** Assume the project root is the default working directory unless a specific path is provided.
11. **Database Migrations:** SQL files (e.g., for PostgreSQL) should use sequential numbering (e.g., `001_create_users_table.sql`). These migrations must be reviewed before execution.

---

### ✨ Code Style & Formatting

#### Python (PEP 8 Adherence)

- **Indentation:** Use **4 spaces** for indentation, **no tabs**.
- **String Quotes:** Prefer **single quotes** (`'like this'`) for consistency, unless double quotes are needed for strings containing single quotes.
- **Line Length:** Strive for lines **≤ 79 characters**. Break long lines thoughtfully.
- **Imports:** Always use **explicit imports**; avoid wildcard imports (`from module import *`). Organize imports according to PEP 8.

#### Dart (Flutter - for frontend team awareness)

- **Indentation:** Use **2 spaces** for indentation, **no tabs**. (Standard for Dart)
- **String Quotes:** Prefer **single quotes** (`'like this'`) for consistency.
- **Line Length:** Strive for lines **≤ 80 characters**.
- **Style Guide:** Follow [Dart Style Guide](https://dart.dev/guides/language/effective-dart/style).

---

### 🧱 Architecture & Best Practices

#### Django (Backend)

- **Views:** Prefer **class-based views** with Django REST Framework for API endpoints.
- **RESTfulness:** Structure API endpoints to be **RESTful**, utilizing appropriate HTTP methods (GET, POST, PUT, DELETE).
- **App Structure:** Use **separate Django apps** for distinct functional domains (e.g., `users`, `dictionaries`, `learning`).
- **Database Queries:** Apply `select_related`/`prefetch_related` to optimize database queries and avoid N+1 issues.
- **Model Managers:** Use custom model managers for encapsulating complex or frequently used query logic.
- **Models:** Prefer Django forms/ModelForms unless DRF serializers are in use for data handling.
- **Structure:** Relative to Django project root (e.g., `backend/app_name/`).

---

### ✅ Testing

- **API Tests (Backend):** Use Django's `TestCase` or DRF's `APITestCase`. Place tests in a `tests/` subdirectory within each app.
- **Flutter Tests (Frontend - for team awareness):** Recommend unit/widget tests using `flutter_test`.
- **Goals:** Tests should be Isolated, Repeatable, and Fast.
- **Coverage:** Aim for a reasonable test coverage percentage (e.g., **70% initial target**).
- **New API Endpoints:** All new API endpoints **must** have corresponding unit tests and E2E tests.

---

### 📝 Documentation & Comments

- **Docstrings:** Every function, method, and class must have clear docstrings (Python). Explain their purpose, arguments, and return values.
- **Inline Comments:** Use inline comments for non-obvious logic or complex algorithms.
- **Django Model Fields:** Use `help_text` for Django model fields where helpful to explain their purpose or constraints.
- **Flutter Widgets:** Comment Flutter widgets with their purpose and key properties.
- **Tags:** Use `TODO:` for incomplete features/placeholders and `FIXME:` for known bugs that need addressing.

---

### 🔐 Security

- **Input Validation:** Sanitize and validate **all** user inputs on the backend.
- **Password Hashing:** Use strong, industry-standard hashing (e.g., `bcrypt` via Django's default password hasher).
- **Secrets:** Manage sensitive values (API keys, credentials) using environment variables (`.env` files are local, never commit them).
- **Credentials:** Never hardcode credentials or sensitive values.
- **Auth/AuthZ:** Enforce proper authentication and authorization.
- **HTTPS:** Ensure all API interactions are over HTTPS.
- **Restricted Access:** DO NOT read or modify files like `.env` files or any file containing API keys/credentials (e.g., `**/config/secrets.*`).

---

### 🚀 Performance

- **Database Optimizations:** Continuously look for opportunities to optimize heavy or frequent database queries using indexing, `select_related`/`prefetch_related`.
- **Caching:** Consider caching strategies for frequently accessed, slow-to-generate data using Redis.
- **Algorithms:** Prefer efficient algorithms and data structures where performance is critical.
- **Flutter Performance:** Use `const` constructors and `RepaintBoundary` when appropriate.

---

### 🧪 Error Handling & Debugging

- **Exception Handling:** Use `try-except` blocks in Python and `try-catch` in Dart to gracefully handle potential errors.
- **Meaningful Messages:** Provide clear, user-friendly error messages for API consumers.
- **Logging:** Implement a comprehensive logging strategy (`info`, `warning`, `error`) for backend operations and integrate with the Elastic database log aggregator. All API must have log.
- **Error Differentiation:** Clearly differentiate between expected errors (e.g., 400 Bad Request) and unexpected server errors (e.g., 500 Internal Server Error).
- **Error Handlers:** All functions must have error handlers.

---

### 📁 File & Project Management

- **Structure:** Follow the established file structure (e.g., `backend/app_name/models.py`, `frontend/lib/src/features/`).
- **Renaming/Deletion:** Do **not** rename or delete files or directories without explicit approval or a clearly defined refactoring plan.
- **New Features:** When proposing a new feature, outline the necessary file changes and additions.

---

### 🔄 Version Control

- **System:** Use Git for version control, with GitHub as the code repository.
- **Commit Style:** Use [Conventional Commits](https://www.conventionalcommits.org/) for clear and consistent commit messages.
  - **Examples:** `feat: implement user registration API`, `fix: correct FSRS algorithm bug`, `docs: update project brief`.
- **Atomic Commits:** Stage and commit all changes together that form a single logical unit of work.
- **Gitignore:** Do **not** modify `.gitignore` unless adding genuinely new file types that should be ignored.

---

### 📐 Design Patterns

- **Coupling & Cohesion:** Strive for loose coupling (modules are independent) and high cohesion (elements within a module are related).
- **Extensibility:** Design models and APIs with future extensibility in mind.
- **Simplicity:** Prefer clear, simple solutions over overly complex or abstract patterns.

---

### 🌍 Ethics & Inclusion

- **Fairness:** Ensure the backend logic and data handling promote a fair and unbiased user experience.
- **Data Privacy:** Protect user personal data and adhere to relevant privacy regulations.

---

### 🧩 Custom Project Rules

1.  **API Documentation:** All new API endpoints **must** include Swagger/OpenAPI documentation comments with example requests and responses.
2.  **Semi-structured Data:** Utilize **PostgreSQL JSONField** for semi-structured or flexible data where appropriate, especially for AI-optimized word information.
3.  **Logging Aggregation:** Integrate with the **Elastic database** for centralized logging and monitoring.
4.  **API Versioning:** Implement **URL-based API versioning** (e.g., `/api/v1/`) for all external-facing endpoints to ensure long-term maintainability. Endpoints must be backward compatible.
5.  **Health Check:** Include a simple health check endpoint (e.g., `/api/v1/health/`) for monitoring service uptime.
6.  **Variable Naming:** All variables must be clear and `snake_case`.
7.  **Function Naming:** All functions must have clear names in `snake_case`.
8.  **Comments:** All functions must have clear comments.
