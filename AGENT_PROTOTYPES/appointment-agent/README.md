# Appointment Booking Agents Vertical Starter Kit

## Tech Stack:
- Agent : LangGraph, Composio (Tools Library), Voice Orchestrator (Bland.com)
- LLMs: Gemini-2.0-flash-exp 
- Interface (NextJS15)
- Deployment (Vercel, LangGraph Cloud)
- Tests (LangSmith, LLM Unit Tests Code.)
- Development (IDE: VS-Code/Cursor) + Google Collab + Docker
- SCM [GitHub] panaversity/learn-agentic-ai/AGENTIC_PROTOTYPES/appointments_agent
- CRM/Calendar/System [Google Calendar, Gmail]

## User Story
* User Wants to Book an Appointment with Dentist Clinic
* Share available time schedule (i.e: Monday 09-06 PM)
* At what time can I come and my preferences are 4 PM DATE.
* User wants to know about Wait Time and Queue Number.
* User Booking Confirmation (email/phone call)

## Features

- [x] Connect Google Calendar (Replaceable with any Calendar or CRM)
- [x] Greet Users and Collect basic Info
- [x] Check for Available Time Slots for the Dental Clinic (Can be any Business)
- [x] Suggest TimeSlots and Confirm the final One with User
- [x] Schedule Booking in Google Calendar
- [x] Create a save a Draft Email in Gmail (Replaceable with any Mail Service)
- [x] Confirmation Call after Booking Appointment using Bland API (Just replace the function call with any providor of your choice)
- [ ] Cron Job to schedule calls
- [ ] Change TimeZone from UTC to User Specific
- [ ] Add Voice Modality with providers (Twillio, Vapi, Bland)

### Pending User Stories
[ ] 0. Business Availability Slots
[ ] 1. Queue Number and Wait Time
[ ] 2. If email is invalid or if phone don't dials try again later -- If not confirmed priority customer can take slot.

## Directory Structure

- All prototyping notebooks are in the `prototypes` directory
- All final agents live in the `src` directory

## Getting Started

### Prerequisites

1. Docker
2. Composio, Google AI Studio and LangSmith API Key
3. Setup the following either in Composio dashboard or through CLI/Jupyter Notebook:
   ```bash
   composio add googlecalendar gmail
   composio triggers enable GMAIL_NEW_GMAIL_MESSAGE
   ```

### Local Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/...
   cd ...
   ```

2. **Create a `.env` file:**

   ```bash
   cp .env.example .env
   ```

   Update the environment variables as needed.

3. **Run LangGraph Server:**

   #### Using Docker

   - Install Docker Desktop
   - Open Docker Desktop
   - Run container:
     ```bash
     docker compose up
     ```
   - Or run in detached mode:
     ```bash
     docker compose up -d
     ```

4. **Access LangGraph Studio**
   - Open [LangGraph Studio](https://smith.langchain.com/studio/thread?baseUrl=http%3A%2F%2F127.0.0.1%3A8123)

### Development

**Applying Changes:**

1. Stop the container:
   ```bash
   docker compose down
   ```
2. Restart the container:
   ```bash
   docker compose up -d
   ```
   Note: Changes outside the `src` directory requires rebuilding the image.

### Alternative Setup Methods

#### A. Using LangGraph CLI

1. Install uv package manager:

   ```bash
   pip install uv
   ```

2. Create and activate virtual environment:

   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. Install packages from pyproject.toml:

   ```bash
   uv run
   ```

4. Run LangGraph Server:
   ```bash
   uv pip install langgraph-cli
   uv run langgraph up
   ```
   Note: If you encounter errors, stop all containers, run `docker system prune`, and try again.

#### B. Using Google Gemini Instead of OpenAI

To switch models, update line 26 in `configuration.py`:

```python
# From:
default="openai/gpt-4o"
# To:
default="google_genai/gemini-1.5-flash"
```
