# Audiovate

**Audiovate** is a music distribution and analytics platform built for artists, label executives, data analysts, and system administrators. It centralizes the relationship between tracks, streaming data, royalty splits, and financial reporting into a single source of truth, eliminating the opacity and inefficiency of traditional music distribution.

> Built for CS 3200 — Database Design, Spring 2026 @ Northeastern University

---

## Team

| Name | Specialty |
|------|------|
| **Bridget Minogue** | Artist Persona |
| **Massimo Mastromattei** | Data Analyst Persona |
| **Shamar Aitcheson** | Label Head Persona |
| **Charles Sherer** | System Admin Persona |

---

## Features by User Role

- **Artists** — Upload and manage releases, edit metadata, set release dates, view streaming stats and earnings per platform
- **Data Analysts** — Roster performance dashboards, geographic listener maps, platform revenue breakdowns, track engagement and skip-rate analysis
- **Label Heads** — Royalty split management, artist roster oversight, asset and deadline tracking
- **System Administrators** — System log monitoring, help request management, workload balancing across admins

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | [Streamlit](https://streamlit.io/) |
| Backend API | [Flask](https://flask.palletsprojects.com/) (REST) |
| Database | MySQL 9 |
| Infrastructure | Docker + Docker Compose |

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [Git](https://git-scm.com/) for cloning the repository
- *(Optional — for IDE support only)* [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install) with Python 3.11

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/bridget-minogue/Audiovate.git
cd Audiovate
```

### 2. Create the Environment File

The API and database both require a `.env.audiovate` file inside the `api/` directory. This file is **not committed to the repository** (it contains secrets).

Create the file at `api/.env.audiovate` with the following contents:

```env
SECRET_KEY=<your-secret-key>
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=Audiovate
MYSQL_ROOT_PASSWORD=<your-mysql-root-password>
```

Replace `<your-secret-key>` with any random string and `<your-mysql-root-password>` with a password of your choice. These values must match across the file — do not change the `DB_USER`, `DB_HOST`, `DB_PORT`, or `DB_NAME` fields.

> ⚠️ **Never commit this file to GitHub.** It is listed in `.gitignore` for this reason.

### 3. Start the Containers

```bash
docker compose up -d
```

This will build and start three containers:

| Container | Description | Port |
|-----------|-------------|------|
| `web-app` | Streamlit frontend | `http://localhost:8501` |
| `web-api` | Flask REST API | `http://localhost:4000` |
| `mysql_db` | MySQL database | `localhost:3200` |

On first run, the database will be automatically initialized from the SQL files in `dataset/`. This may take 30–60 seconds for the seed data to fully load.

### 4. Open the App

Navigate to **[http://localhost:8501](http://localhost:8501)** in your browser and select a user persona to log in.

---

## Useful Docker Commands

```bash
# Start all containers in the background
docker compose up -d

# Stop and remove all containers
docker compose down

# Stop containers without removing them
docker compose stop

# Restart containers (e.g. after a code change that crashed a container)
docker compose restart

# View logs for a specific container
docker compose logs web-api
docker compose logs mysql_db

# Rebuild and restart after changes to Dockerfile or dependencies
docker compose up -d --build
```

### Resetting the Database

If you modify any SQL files in `dataset/`, you must fully recreate the database container for changes to take effect:

```bash
docker compose down && docker volume prune -f && docker compose up -d
```

> **Note:** `docker volume prune -f` removes all unused Docker volumes, which causes the database to be re-seeded from scratch on the next `up`.

---

## Project Structure

```
Audiovate/
├── app/                    # Streamlit frontend
│   └── src/
│       ├── Home.py         # Login / persona selection page
│       ├── pages/          # One file per app page, organized by role prefix
│       └── modules/
│           └── nav.py      # Sidebar navigation and RBAC logic
├── api/                    # Flask REST API
│   ├── backend_app.py      # App entry point
│   ├── backend/
│   │   └── audiovate_routes/   # Route blueprints organized by resource
│   ├── requirements.txt
│   └── .env.audiovate      # ⚠️ Secret config — create this manually (see above)
├── dataset/                # SQL seed data (loaded into MySQL on container creation)
├── database-files/         # Schema definition SQL
├── docker-compose.yaml     # Container orchestration
└── README.md
```

### Page Naming Convention

Streamlit pages are prefixed by role number:

| Prefix | Role |
|--------|------|
| `00_` | Artist |
| `10_` | Data Analyst |
| `20_` | System Administrator |
| `30_` | Label Head |

---

## Development Notes

- **Hot reloading** — Changes to `app/src/` and `api/` are reflected immediately without restarting containers. In Streamlit, click **Always Rerun** in the browser for live updates.
- **Database changes** — Modifying `.sql` files requires a full container + volume teardown (see *Resetting the Database* above).
- **Local Python install (optional)** — Installing dependencies locally gives your IDE autocomplete and linting, but the app always runs inside Docker:

```bash
cd api && pip install -r requirements.txt
cd ../app/src && pip install -r requirements.txt
```

---

## API Overview

The REST API is available at `http://localhost:4000`. Key endpoint groups:

| Prefix | Resource |
|--------|----------|
| `/artists` | Artist profiles, performance, platform metrics, track engagement, listener locations |
| `/users` | User roster performance |
| `/releases` | Release management |
| `/helpRequests` | Support ticket system |
| `/systemLogs` | System event logs |
| `/payoutProfiles` | Royalty split configuration |

---
