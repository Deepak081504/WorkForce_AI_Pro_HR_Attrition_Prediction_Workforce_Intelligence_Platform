# WorkForce AI Pro – HR Attrition Prediction & Workforce Intelligence Platform

## 📌 Project Overview

WorkForce AI Pro is an AI-powered Human Resource Management and Workforce Intelligence platform designed to manage employees, attendance, leave, payroll, communication, documents, workforce analytics, and employee attrition prediction.

The platform combines a modern HR management system with Machine Learning to help HR teams identify employees who may be at risk of leaving and take preventive actions.

---

## 🎯 Objectives

- Manage employee information and workforce data
- Manage departments, roles, shifts, attendance, and leave
- Manage payroll information
- Provide employee notifications and communication
- Manage employee documents
- Predict employee attrition risk using Machine Learning
- Monitor employee risk levels
- Forecast future workforce requirements
- Provide workforce analytics and dashboards
- Generate reports and export data
- Support HR decision-making using AI recommendations

---

## 🛠️ Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Alembic
- JWT Authentication
- Python-Jose
- Passlib

### Frontend

- React
- Vite
- Tailwind CSS
- Axios
- Recharts
- Lucide React

### Artificial Intelligence & Machine Learning

- Python
- Pandas
- NumPy
- Scikit-learn
- Random Forest Classifier
- Joblib

### Development Tools

- Visual Studio Code
- PostgreSQL
- Git
- GitHub
- Docker

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │      React Frontend     │
                    │   Vite + Tailwind CSS   │
                    │   Recharts + Axios      │
                    └────────────┬────────────┘
                                 │
                                 │ REST API
                                 ▼
                    ┌─────────────────────────┐
                    │      FastAPI Backend    │
                    │ Authentication & APIs   │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌────────────┐     ┌──────────────┐   ┌──────────────┐
       │ PostgreSQL │     │ ML Prediction │   │ WebSocket    │
       │  Database  │     │    Engine     │   │ Real-Time    │
       └────────────┘     └──────────────┘   └──────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ HR Intelligence │
                        │ Risk & Forecast │
                        └─────────────────┘

Project Structure

WorkForce_AI_Pro_HR_Attrition_Prediction_Workforce_Intelligence_Platform/
│
├── backend/
│   │
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── ml/
│   │   └── main.py
│   │
│   ├── alembic/
│   ├── uploads/
│   ├── ml_models/
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── README.md
└── .gitignore

🔐 Phase 1 – Core Workforce Management
1. Authentication & Authorization

The authentication system provides secure user access using JWT-based authentication.

Features
User Registration
User Login
Access Token
Refresh Token
Get Current User
Forgot Password
Reset Password
Role-Based Access Control
Supported Roles
ADMIN
HR
MANAGER
EMPLOYEE

2. Employee Management

Employee Management allows HR teams to maintain employee information.

Features
Create Employee
List Employees
Get Employee Details
Update Employee
Delete Employee
Department Assignment
Manager Assignment
Employee Status Management

Employee information includes:

Employee Code
Name
Email
Phone
Date of Birth
Joining Date
Designation
Department
Manager
Status
3. Department & Role Management

The platform provides department and role management.

Department Features
Create Department
View Departments
Update Department
Delete Department
Role Features
Create Role
View Roles
Update Role
Delete Role
4. Attendance & Shift Management

The system manages employee shifts and daily attendance.

Shift Management
Create Shift
View Shifts
Update Shift
Delete Shift
Attendance Management
Employee Check-in
Employee Check-out
Attendance Status
Shift Assignment
Attendance Date
Remarks
Duplicate Attendance Validation
5. Leave Management

The Leave Management module manages leave types and employee leave requests.

Features
Create Leave Type
Update Leave Type
Delete Leave Type
Create Leave Request
View Leave Requests
Update Leave Request
Delete Leave Request
Leave Duration Calculation

Example Leave Types:

Annual Leave
Sick Leave
Casual Leave
Maternity Leave
Paternity Leave
6. Payroll Management

Payroll Management stores employee salary and payroll information.

Features
Employee Salary
Pay Period
Pay Date
Basic Salary
Allowances
Deductions
Bonus
Payroll Status
7. Notifications & Alerts

The notification module provides important workforce notifications.

Features
Create Notification
View Notifications
Notification Type
Notification Message
User-based Notifications

Notification types include:

INFO
WARNING
ALERT
8. One-to-One Chat & Communication

The platform provides employee-to-employee communication through one-to-one messaging.

Features
Send Message
Receive Message
Sender and Receiver
Message Content
User-based Communication
9. Document Management

The Document Management module allows HR teams to upload and manage employee documents.

Features
Upload Employee Documents
Store File Information
Employee Document Mapping
View Documents
Download Documents
Delete Documents

Example documents:

Offer Letter
Employment Agreement
Salary Certificate
Payslip
Performance Review
Leave Approval Letter
10. Dashboard & Workforce Analytics

The dashboard provides an overview of workforce information.

Dashboard Information
Total Employees
Active Employees
Department Distribution
Attendance Overview
Leave Overview
Payroll Information
Attrition Risk
Workforce Trends

Charts and visual analytics are provided using Recharts.

🤖 Phase 2 – HR Attrition Prediction & AI Intelligence
11. Dataset Management

Dataset Management is used to upload, store, validate, and manage employee HR datasets for AI model training and prediction.

Features
Upload CSV Dataset
Store Dataset Information
Dataset Validation
Dataset Listing
Dataset Management
AI Training Data Preparation

12. AI Attrition Prediction Engine

The AI Attrition Prediction Engine is used to predict the probability of an employee leaving the company using their HR and workforce data.

Machine Learning Algorithm
Random Forest Classifier
ML Pipeline
HR Dataset
     │
     ▼
Data Validation
     │
     ▼
Feature Selection
     │
     ▼
Data Preprocessing
     │
     ▼
Random Forest Training
     │
     ▼
Model Serialization
     │
     ▼
Employee Prediction
     │
     ▼
Attrition Probability
     │
     ▼
Risk Level
Risk Levels
LOW
MEDIUM
HIGH

⚠️ 13. Employee Risk Monitoring

Employee Risk Monitoring is used to continuously identify and monitor employees who are at low, medium, or high risk of attrition, so HR can take early preventive actions.

Features
Attrition Probability
Risk Level
Employee Risk History
High-Risk Employee Identification
Risk Monitoring

📈 14. Workforce Forecasting

Workforce Forecasting predicts future workforce requirements based on historical employee headcount data.

Input
Historical Period
Historical Headcount
Forecast Periods

Forecasting Use Cases
Workforce Growth Planning
Employee Requirement Planning
Future Headcount Estimation
Workforce Trend Analysis

15. Attrition Analytics Dashboard

The Attrition Analytics Dashboard provides visual insights into employee attrition and workforce risk.

Analytics
Total Employees
Attrition Rate
High-Risk Employees
Medium-Risk Employees
Low-Risk Employees
Department-wise Risk
Attrition Trends
Workforce Trends
💡 16. HR Intervention & Decision Support

This module helps HR teams take appropriate actions based on employee risk information.

Example Actions
High Attrition Risk
        │
        ▼
HR Review
        │
        ├── Career Development
        ├── Training
        ├── Workload Review
        ├── Employee Engagement
        └── Retention Discussion
🔔 17. Smart Notification & Alert Engine

The Smart Notification & Alert Engine is designed to provide workforce-related alerts.

Examples
High Attrition Risk Alert
Workforce Forecast Alert
Attendance Alert
Leave Alert
Workforce Status Alert
⚡ 18. Real-Time Workforce Monitoring

Real-Time Workforce Monitoring provides real-time workforce updates through WebSocket communication.

Use Cases
Live Workforce Updates
Real-Time Notifications
Workforce Status Updates
Real-Time Dashboard Updates

Technology:

FastAPI WebSocket
🚀 Phase 3 – Advanced Enterprise Features
19. Reports & Export System

The Reports & Export module generates workforce reports.

Supported Reports
Employees
Attendance
Leaves
Payroll
Attrition Risk
Export Formats
CSV
Excel
20. Audit Logs & Activity Tracking

Audit Logs maintain records of important user and system activities.

Features
User Activity Tracking
Resource Activity Tracking
Audit History
User-based Audit Logs
Resource-based Audit Logs
21. Workflow & Task Management

Workflow and Task Management allows managers and HR teams to assign and track workforce-related tasks.

Features
Create Task
Assign Task
Task Priority
Due Date
Task Description
Task Tracking

23. AI Recommendation Engine

The AI Recommendation Engine provides workforce-related recommendations using employee risk information.

Example
Employee Risk
     │
     ▼
Risk Analysis
     │
     ▼
HR Recommendation
     │
     ├── Career Development
     ├── Training
     ├── Leadership Development
     └── Employee Engagement
🔎 24. Advanced Search & Filtering

The system supports advanced employee search and filtering.

Search Options
Employee Name
Employee Code
Department
Status
Designation

Example:

Search: Vijay

Department: Engineering

Status: ACTIVE
🎨 25. Professional Enterprise UI/UX

The frontend is designed with a modern enterprise HR SaaS interface.

UI Features
Responsive Design
Modern Dashboard
Gradient Cards
Analytics Charts
Sidebar Navigation
Top Navigation
Employee Management Screens
AI Risk Visualization
Workforce Analytics
Responsive Layout
Modern Icons and Animations
🔐 Role-Based Access Control

The application supports four major user roles.

Role	Description
ADMIN	Full system access
HR	HR and workforce management
MANAGER	Team and employee management
EMPLOYEE	Employee-level access

Access to protected APIs is controlled using JWT authentication and role-based authorization.

🗄️ Database

The project uses PostgreSQL as the relational database.

Main Data Areas
Users
Employees
Departments
Roles
Shifts
Attendance
Leave Types
Leave Requests
Payroll
Notifications
Messages
Documents
Datasets
Predictions
Tasks
Performance Reviews
Recommendations
Audit Logs

Database migrations are managed using Alembic.

🔑 JWT Authentication Flow
User
 │
 ▼
Login
 │
 ▼
FastAPI Authentication
 │
 ▼
JWT Access Token
 │
 ├──────────────► Protected APIs
 │
 ▼
Refresh Token
 │
 ▼
New Access Token
🧪 Testing

The backend APIs were tested using Swagger UI.

Swagger documentation:

http://localhost:8000/docs

Testing includes:

Authentication APIs
Employee APIs
Department APIs
Role APIs
Shift APIs
Attendance APIs
Leave APIs
Payroll APIs
Notification APIs
Chat APIs
Document APIs
Dataset APIs
ML Training APIs
Attrition Prediction APIs
Employee Risk APIs
Workforce Forecasting APIs
Reports APIs
Audit Log APIs
Workflow APIs
Performance Review APIs
AI Recommendation APIs
Advanced Search APIs

📈 Machine Learning Model

The project uses a Random Forest Classifier for employee attrition prediction.

Input Features
Age
Monthly Income
Years at Company
Years in Current Role
Job Satisfaction
Environment Satisfaction
Work-Life Balance
Overtime
Job Level
Number of Companies Worked
Output
Attrition Probability
Risk Level
Model Version
Prediction Timestamp

Example:

Employee: Vijay Raj
Attrition Probability: 30.5%
Risk Level: LOW
Model: random_forest_v1
🔒 Security

The application implements:

JWT Authentication
Password Hashing
Role-Based Authorization
Protected API Endpoints
Access Token Expiration
Refresh Token
Password Reset Token
Active User Validation
Environment-based Configuration

Sensitive configuration such as database passwords and secret keys should be stored in .env and should not be committed to GitHub.

🚀 Future Enhancements

Possible future improvements include:

Advanced ML models
Automated email notifications
More workforce forecasting algorithms
Advanced HR analytics
Model performance monitoring
Cloud deployment
Advanced employee engagement analytics
