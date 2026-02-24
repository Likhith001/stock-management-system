📦 Stock Manager – Inventory & Sales Management System

A full-stack Inventory and Sales Management System built using Django, designed to manage products, track sales, calculate profits, generate invoices, and provide business analytics through an interactive dashboard.

🚀 Features
🔐 Authentication & Role-Based Access

User Signup & Login

Admin, Staff, and User roles

Role-based permissions

Secure access control using Django authentication

📦 Product Management

Add / Edit / Delete products (Admin only)

SKU-based unique identification

Category management

Purchase & Selling price tracking

Minimum stock threshold

Real-time stock quantity updates

🛒 Sales Management

Create sales with multiple products

Automatic stock deduction

Transaction-safe operations using transaction.atomic()

Sale header + Sale items relational structure

📊 Business Analytics Dashboard

Total Sales

Total Revenue

Total Profit

Monthly Revenue Chart (Chart.js)

Monthly Profit Chart

Stock Status Pie Chart

Low stock detection

📈 Financial Calculations

Profit = (Selling Price − Purchase Price) × Quantity

Monthly profit aggregation using Django ORM

Revenue aggregation using Sum() and F() expressions

📄 Invoice System

Download invoice as PDF (ReportLab)

Professional formatted invoice

Dynamic sale data rendering

📁 CSV Export

Export full sales report

Includes:

Sale ID

Date

Product

Quantity

Price

Total

Profit

📧 Email Integration

Automatic invoice email after sale creation

Configurable SMTP backend

Console email backend for development

📜 Activity Logging

Logs product creation, update, deletion

Logs sale creation

Tracks user, action, and timestamp

Admin-only access

🏗️ Tech Stack
Layer	Technology
Backend	Django
Database	SQLite
Frontend	HTML, Bootstrap
Charts	Chart.js
PDF Generation	ReportLab
Email	Django SMTP Backend
🗂️ Project Structure
dashboard/
│
├── dashboard/          # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── app/                # Main application
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   └── static/
│
├── db.sqlite3
└── manage.py
🧠 Key Concepts Used

Django ORM

ForeignKey relationships

QuerySets

Aggregation (Sum, Count)

F() expressions

ExpressionWrapper

Transaction management

Role-based authentication

CSV file generation

SMTP email integration

Template inheritance

Data visualization

🔄 How It Works

User logs in

Admin manages products

Staff creates sales

Stock updates automatically

Profit & revenue calculated dynamically

Dashboard displays analytics

Invoice can be downloaded or emailed

Sales report can be exported as CSV

🛠️ Installation
# Clone the repository
git clone https://github.com/your-username/stock-manager.git

# Navigate to project
cd stock-manager

# Create virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver
📌 Future Enhancements

Customer management

REST API integration (Django REST Framework)

Multi-branch inventory

Low stock email automation

Profit margin analytics

ML-based demand forecasting

🎯 Purpose

This project demonstrates:

Backend development skills

Database design

Financial analytics implementation

Transaction handling

Role-based security

Real-world business logic implementation
