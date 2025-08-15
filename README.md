# Coopalytics 🎓

[![Docker](https://img.shields.io/badge/Containerized-Docker-blue?logo=docker)](https://www.docker.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?logo=streamlit)](https://streamlit.io/)
[![Flask](https://img.shields.io/badge/Backend-Flask-green?logo=flask)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-orange?logo=mysql)](https://www.mysql.com/)

A comprehensive co-op management system designed to streamline the cooperative education process for students, employers, and administrators at Northeastern University.

## 📋 Project Overview

Coopalytics is a full-stack web application that facilitates the entire co-op lifecycle, from position posting to application management and administrative oversight. The platform provides tailored experiences for four distinct user types:

### 🎯 Key Features

- **Student Portal**: Browse positions, submit applications, manage profiles, and track application status
- **Academic Advisor Portal**: Monitor your advisees' application progress, analyze placement trends, identify students needing support, and access comprehensive analytics
- **Employer Dashboard**: Post co-op positions, review applications, manage company profiles, and make hiring decisions
- **Admin Panel**: Oversee all positions, manage user accounts, review flagged content, and maintain system integrity
- **Real-time Application Management**: Status updates, notifications, and comprehensive tracking
- **Advanced Filtering**: Search positions by industry, location, skills, and other criteria
- **Diversity & Inclusion Analytics**: DEI reporting and insights for administrators

### 👥 Target Users

- **Students**: Seeking co-op opportunities and managing their application process
- **Advisors**: Managing students' application processes and overlooking student data
- **Employers**: Posting positions and managing the hiring process
- **System Administrators**: Overseeing platform operations and maintaining data integrity

### 🛠️ Technology Stack

- **Frontend**: Streamlit (Python-based web framework)
- **Backend API**: Flask with RESTful endpoints
- **Database**: MySQL with comprehensive relational schema
- **Containerization**: Docker & Docker Compose for easy deployment
- **Authentication**: Session-based user management
- **Styling**: Custom CSS with responsive design

## 🚀 Getting Started

### Prerequisites

Before running Coopalytics, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started) (version 20.0 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or higher)
- Git for cloning the repository

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/Coopalytics.git
   cd Coopalytics
   ```

2. **Start the Application**
   ```bash
   # Start all containers in detached mode
   docker-compose up -d
   ```

3. **Verify Container Status**
   ```bash
   # Check that all containers are running
   docker-compose ps
   ```

4. **Access the Application**
   - **Streamlit Frontend**: [http://localhost:8501](http://localhost:8501)
   - **Flask API**: [http://localhost:4000](http://localhost:4000)
   - **MySQL Database**: `localhost:3306` (for direct database access)

### Initial Setup

The application includes pre-populated sample data for immediate testing:
- Sample student, employer, and admin accounts
- Co-op positions across various industries
- Application records and company profiles

## 📁 Application Structure

```
Coopalytics/
├── app/                          # Streamlit Frontend Application
│   ├── src/
│   │   ├── pages/               # Individual page components
│   │   │   ├── 1*_Student_*.py  # Student-facing pages
│   │   │   ├── 2*_Employer_*.py # Employer-facing pages
│   │   │   └── 3*_Admin_*.py    # Admin-facing pages
│   │   ├── modules/             # Shared components and utilities
│   │   └── Home.py              # Main application entry point
│   └── Dockerfile               # Frontend container configuration
├── api/                         # Flask Backend API
│   ├── backend/
│   │   ├── applications/        # Application management endpoints
│   │   ├── coopPositions/       # Position management endpoints
│   │   ├── users/               # User management endpoints
│   │   └── db_connection.py     # Database connection utilities
│   └── Dockerfile               # Backend container configuration
├── database-files/              # MySQL Database Setup
│   ├── 01-coopalytics-schema.sql  # Database schema definition
│   └── 02-coopalytics-data.sql    # Sample data insertion
├── docker-compose.yaml           # Container orchestration
└── README.md                    # This file
```

### Key Components

- **Frontend (`/app`)**: Streamlit-based user interface with role-based page access
- **Backend API (`/api`)**: Flask RESTful API with modular endpoint organization
- **Database (`/database-files`)**: MySQL schema and sample data for immediate functionality

## 💻 Usage

### User Personas & Access

The application supports three distinct user personas, each with tailored functionality:

#### 🎓 Student Persona
- **Dashboard**: View application status and recommended positions
- **Position Search**: Browse and filter available co-op opportunities
- **Application Management**: Submit applications and track their progress
- **Profile Management**: Update personal information and skills

#### 🏢 Employer Persona
- **Company Dashboard**: Manage company profile and posted positions
- **Position Management**: Create, edit, and manage co-op postings
- **Application Review**: View and process student applications
- **Candidate Profiles**: Access detailed student information and documents

#### 🔧 Administrator Persona
- **System Overview**: Monitor platform activity and user engagement
- **Position Moderation**: Review, approve, or flag co-op postings
- **User Management**: Oversee student and employer accounts
- **DEI Analytics**: Access diversity and inclusion reporting tools

### Navigation

1. **Home Page**: Select your user persona to access role-specific features
2. **Sidebar Navigation**: Use the left sidebar to navigate between different sections
3. **Quick Actions**: Utilize dashboard widgets for common tasks
4. **Search & Filters**: Apply filters to find relevant positions or applications

## 🔧 Development

### Container Management

```bash
# Stop all containers
docker-compose down

# View container logs
docker logs web-app        # Streamlit frontend logs
docker logs web-api        # Flask backend logs
docker logs coopalytics-db # MySQL database logs

# Rebuild containers after code changes
docker-compose up -d --build

# Restart specific container
docker-compose restart web-app
```

### Environment Configuration

The application uses Docker environment variables defined in `docker-compose.yaml`:

- **Database Configuration**: MySQL credentials and connection settings
- **API Configuration**: Flask server settings and CORS policies
- **Frontend Configuration**: Streamlit server configuration

### Database Access

```bash
# Access MySQL database directly
docker exec -it coopalytics-db mysql -u root -p

# Export database backup
docker exec coopalytics-db mysqldump -u root -p coopalytics > backup.sql
```

**Port Conflicts**
```bash
# If ports 8501 or 4000 are in use, modify docker-compose.yaml
# Change the port mapping: "8502:8501" for frontend, "4001:4000" for backend
```

**Container Startup Issues**
```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs

# Restart all containers
docker-compose down && docker-compose up -d
```

**Database Connection Problems**
```bash
# Reset database container
docker-compose down
docker volume rm coopalytics_mysql_data
docker-compose up -d
```

**Application Not Loading**
- Ensure all containers are running: `docker-compose ps`
- Check for port conflicts on 8501 and 4000
- Verify Docker daemon is running
- Clear browser cache and try again

### Performance Optimization

- **Container Resources**: Adjust memory limits in `docker-compose.yaml` if needed
- **Database Performance**: Monitor MySQL logs for slow queries
- **Frontend Caching**: Streamlit automatically caches data; restart container to clear cache

## 📝 License

This project is developed for educational purposes as part of the CS3200 Database Design course at Northeastern University.

## 🤝 Contributing

This is an academic project. For questions or issues, please contact the development team or course instructors.

---

=======

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/Coopalytics.git
   cd Coopalytics
   ```

2. **Start the Application**
   ```bash
   # Start all containers in detached mode
   docker-compose up -d
   ```

3. **Verify Container Status**
   ```bash
   # Check that all containers are running
   docker-compose ps
   ```

4. **Access the Application**
   - **Streamlit Frontend**: [http://localhost:8501](http://localhost:8501)
   - **Flask API**: [http://localhost:4000](http://localhost:4000)
   - **MySQL Database**: `localhost:3306` (for direct database access)

### Initial Setup

The application includes pre-populated sample data for immediate testing:
- Sample student, employer, and admin accounts
- Co-op positions across various industries
- Application records and company profiles

## 📁 Application Structure

```
Coopalytics/
├── app/                          # Streamlit Frontend Application
│   ├── src/
│   │   ├── pages/               # Individual page components
│   │   │   ├── 1*_Student_*.py  # Student-facing pages
│   │   │   ├── 2*_Employer_*.py # Employer-facing pages
│   │   │   └── 3*_Admin_*.py    # Admin-facing pages
│   │   ├── modules/             # Shared components and utilities
│   │   └── Home.py              # Main application entry point
│   └── Dockerfile               # Frontend container configuration
├── api/                         # Flask Backend API
│   ├── backend/
│   │   ├── applications/        # Application management endpoints
│   │   ├── coopPositions/       # Position management endpoints
│   │   ├── users/               # User management endpoints
│   │   └── db_connection.py     # Database connection utilities
│   └── Dockerfile               # Backend container configuration
├── database-files/              # MySQL Database Setup
│   ├── 01-coopalytics-schema.sql  # Database schema definition
│   └── 02-coopalytics-data.sql    # Sample data insertion
├── docker-compose.yaml           # Container orchestration
└── README.md                    # This file
```

### Key Components

- **Frontend (`/app`)**: Streamlit-based user interface with role-based page access
- **Backend API (`/api`)**: Flask RESTful API with modular endpoint organization
- **Database (`/database-files`)**: MySQL schema and sample data for immediate functionality

## 💻 Usage

### User Personas & Access

The application supports four distinct user personas, each with tailored functionality:

#### 🎓 Student Persona
- **Dashboard**: View application status and recommended positions
- **Position Search**: Browse and filter available co-op opportunities
- **Application Management**: Submit applications and track their progress
- **Profile Management**: Update personal information and skills

#### 👨‍🏫 Advisor Persona
- **Advisor Dashboard**: View and manage advisor profile
- **Student Management**: View and flag assigned students' profiles and application status
- **Placement Analytics**: Monitor and filter detailed statistics for student placement
- **Company Partnerships**: Access detailed company information and ratings

#### 🏢 Employer Persona
- **Company Dashboard**: Manage company profile and posted positions
- **Position Management**: Create, edit, and manage co-op postings
- **Application Review**: View and process student applications
- **Candidate Profiles**: Access detailed student information and documents

#### 🔧 Administrator Persona
- **System Overview**: Monitor platform activity and user engagement
- **Position Moderation**: Review, approve, or flag co-op postings
- **User Management**: Oversee student and employer accounts
- **DEI Analytics**: Access diversity and inclusion reporting tools

### Navigation

1. **Home Page**: Select your user persona to access role-specific features
2. **Sidebar Navigation**: Use the left sidebar to navigate between different sections
3. **Quick Actions**: Utilize dashboard widgets for common tasks
4. **Search & Filters**: Apply filters to find relevant positions or applications

## 🔧 Development

### Container Management

```bash
# Stop all containers
docker-compose down

# View container logs
docker logs web-app        # Streamlit frontend logs
docker logs web-api        # Flask backend logs
docker logs coopalytics-db # MySQL database logs

# Rebuild containers after code changes
docker-compose up -d --build

# Restart specific container
docker-compose restart web-app
```

### Environment Configuration

The application uses Docker environment variables defined in `docker-compose.yaml`:

- **Database Configuration**: MySQL credentials and connection settings
- **API Configuration**: Flask server settings and CORS policies
- **Frontend Configuration**: Streamlit server configuration

### Database Access

```bash
# Access MySQL database directly
docker exec -it coopalytics-db mysql -u root -p

# Export database backup
docker exec coopalytics-db mysqldump -u root -p coopalytics > backup.sql
```

**Port Conflicts**
```bash
# If ports 8501 or 4000 are in use, modify docker-compose.yaml
# Change the port mapping: "8502:8501" for frontend, "4001:4000" for backend
```

**Container Startup Issues**
```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs

# Restart all containers
docker-compose down && docker-compose up -d
```

**Database Connection Problems**
```bash
# Reset database container
docker-compose down
docker volume rm coopalytics_mysql_data
docker-compose up -d
```

**Application Not Loading**
- Ensure all containers are running: `docker-compose ps`
- Check for port conflicts on 8501 and 4000
- Verify Docker daemon is running
- Clear browser cache and try again

### Performance Optimization

- **Container Resources**: Adjust memory limits in `docker-compose.yaml` if needed
- **Database Performance**: Monitor MySQL logs for slow queries
- **Frontend Caching**: Streamlit automatically caches data; restart container to clear cache

## 📝 License

This project is developed for educational purposes as part of the CS3200 Database Design course at Northeastern University.

## 🤝 Contributing

This is an academic project. For questions or issues, please contact the development team or course instructors.

---

**Built with ❤️ by Co-op Huntrix**
