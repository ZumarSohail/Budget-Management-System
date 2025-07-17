# Budget Management System

A Django + Celery system for managing advertising budgets with automated campaign controls.

## Setup & Run Locally

### Prerequisites

- Python 3.10+
- Redis
- PostgreSQL

### Installation Steps

1. **Create virtual environment**
   python -m venv venv

2. **Activate virtual environment**
   - Windows:
     .\venv\Scripts\activate
3. **Install dependencies**
   pip install -r requirements.txt

4. **Configure environment**
   Create `.env` file in project root:

   ```env
   SECRET_KEY=your_secret_key_here
   REDIS_URL=redis://localhost:6379/0


   ```

5. **Database setup**
   python manage.py makemigrations
   python manage.py migrate

6. **Create admin user**
   python manage.py createsuperuser

7. **Start services** (run in separate terminals)

   - Redis server:
     ```bash
     redis-server
     ```
   - Django development server:
     ```bash
     python manage.py runserver
     ```
   - Celery worker (Windows):
     ```bash
     celery -A adagency worker --pool=solo --loglevel=info
     ```
   - Celery beat scheduler:
     ```bash
     celery -A adagency beat --loglevel=info
     ```

8. **Access admin interface**
   http://localhost:8000/admin

## Data Models & Relationships

### Brand

- **Fields**:
  - `name`: Brand name
  - `daily_budget`: Daily spending limit
  - `monthly_budget`: Monthly spending limit
  - `daily_spend`: Current day's spend
  - `monthly_spend`: Current month's spend
- **Relationships**:
  - One-to-Many with Campaign (1 Brand → Many Campaigns)

### Campaign

- **Fields**:
  - `brand`: ForeignKey to Brand
  - `name`: Campaign name
  - `status`: Active/Paused state
  - `schedule`: Dayparting configuration (JSON)
    ```json
    {
      "days": ["mon", "tue", "wed"],
      "start_time": "09:00",
      "end_time": "17:00"
    }
    ```
- **Methods**:
  - `is_within_schedule()`: Checks if current time is within scheduled hours

## System Daily Workflow

1. **Spend Recording**

   - External systems call `record_spend(campaign_id, amount)`
   - Updates brand's daily/monthly spend atomically
   - Creates spend log for auditing

2. **Periodic Budget Checks** (Every 5 minutes)

   - Check all campaigns
   - Pause campaigns if:
     - Brand's daily or monthly budget is exceeded
     - Current time is outside scheduled hours
   - Activate campaigns when:
     - Budget allows and schedule permits

3. **Daily Reset** (00:00 UTC)

   - Reset all brands' daily_spend to 0
   - Reactivate eligible campaigns

4. **Monthly Reset** (00:00 UTC on 1st of month)
   - Reset all brands' monthly_spend to 0
   - Reactivate eligible campaigns

## Assumptions & Simplifications

1. **Timezone Handling**:

   - All operations use UTC timezone
   - Dayparting schedules should be provided in UTC

2. **Currency**:

   - Single currency system (no conversion)
   - Budgets in decimal format

3. **Scheduling**:

   - Dayparting uses 24-hour format
   - Days abbreviated as ["mon", "tue", etc.]
   - Empty schedule means always active

4. **Budget Enforcement**:

   - Immediate status changes
   - No manual approval workflows

5. **Performance**:
   - Bulk operations for reset tasks
   - Periodic checks at 5-minute intervals

```

```
