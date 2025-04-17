
# CampusPerks 🎓🛍️

CampusPerks is a college-focused discount discovery platform that connects students with local deals offered by stores affiliated with their universities.

---

## 🚀 Features

- Student dashboard with personalized discounts
- Admin portal for managing stores and deals
- Data-driven recommendations (optional ML integration)
- Streamlit frontend, Flask backend, MySQL database

---

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Flask (Blueprints, REST API)
- **Database**: MySQL
- **ORM**: Raw SQL via PyMySQL
- **Dev Tools**: Docker, Faker, VSCode, Git

---

## 🗂 Directory Structure

```bash
CampusPerks-CS3200_Project/
├── api/                  # Backend
│   ├── backend/
│   │   ├── discounts/
│   │   ├── users/
│   │   ├── ...
│   │   └── rest_entry.py
│   ├── .env
│   └── requirements.txt
│
├── app/                  # Streamlit frontend
│   └── src/
│       ├── student_home.py
│       ├── admin_home.py
│       └── ...
│
├── database-files/       # SQL setup scripts
│   ├── campus-perks.sql
│   └── faker.sql
│
├── docker-compose.yml
└── README.md
```

---

## 🧪 Local Setup (Dev)

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/CampusPerks-CS3200_Project.git
cd CampusPerks-CS3200_Project

# 2. Start all services
docker compose up --build

# 3. Visit app:
# Frontend: http://localhost:8501
# Backend:  http://localhost:4000
```

---

## 🌐 API Overview

**Base URL**: `http://localhost:4000`

| Route                  | Method | Description                    |
|-----------------------|--------|--------------------------------|
| `/d/discounts`        | GET    | Get all discounts              |
| `/d/discounts`        | POST   | Add a new discount             |
| `/d/discounts/<id>`   | PUT    | Update a discount              |
| `/d/discounts/<id>`   | DELETE | Delete a discount              |
| `/sd/bookmark`        | POST   | Bookmark a discount            |
| `/cl/clubs`           | GET    | List all clubs                 |
| `/col/colleges`       | GET    | List all colleges              |

---

## 👤 Authors

- Marcus Yi
- Molly Varrenti
- Amelia Rogers
- Emma Foley

---
## 📽️ Demo Video

Link: https://youtu.be/cAvfPbyvxkI

---
### 🔐 Environment Variables

  ```env
  DB_USER=root
  DB_PASSWORD=yourpassword
  DB_HOST=db
  DB_NAME=campusPerks_db

---

🏫 Northeastern University — CS3200 — Spring 2025
