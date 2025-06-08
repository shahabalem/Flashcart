# Project Brief: AI-Powered Language Learning Backend

## 1. Project Vision & Goals

- **Vision:** Empower MENA region learners (18-40) with an efficient, personalized mobile language learning experience, overcoming content confusion and time constraints via AI optimization and structured iteration.

- **Primary Goal(s):**

  - **MVP Launch:** Deliver a functional Django backend with user authentication, online dictionary integration, initial AI word optimization, and a basic FSRS-based linter model.
  - **User Engagement:** Achieve 15% average daily active user retention (engagement with linter/quiz) within three months post-MVP.

- **Problem Statement:** Current language learning solutions often overwhelm users with uncurated content, lack personalized paths, and fail to sustain motivation for adults with limited time and a preference for structured learning.

---

## 2. Scope (Minimum Viable Product - MVP)

- **In Scope (Backend Focus):**

  - **User Management:** Authentication (login/registration).
  - **Online Dictionary Integration:** API connectivity for word data.
  - **Initial AI Word Optimization:** AI model to process dictionary data for learning (via prompts).
  - **FSRS-based Linter Model:** Core logic for spaced repetition, progress tracking.
  - **Word Categorization (Decks):** User ability to group words into custom decks.
  - **Basic Quiz Integration:** Simple quizzes linked to the linter model.

- **Out of Scope (For MVP):**
  - Full conversational AI or advanced NLP for free-form practice.
  - Native mobile application development (this is a backend project).
  - Extensive social features or community forums.

---

## 3. Target Users / User Persona

- **Persona Name:** The "Driven but Dispersed" Learner
- **Demographics:** MENA region, 18-40 years, college students/professionals, CEFR A1-C2.
- **Behaviors:** Prefers short, partial learning bursts; seeks quick efficiency; leans towards structured, traditional learning.
- **Drivers:** Career advancement, improved communication, migration/travel.
- **Pain Points:** Content overload/confusion, limited time, irrelevant learning, motivation fluctuations.

---

## 4. Technical Stack

- **Backend Framework:** Django / Django REST Framework
- **Frontend Framework:**: Flutter
- **Database:** PostgreSQL, MongoDB
