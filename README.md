# Stock Manager — Inventory & Sales Management System

> A full-stack inventory and sales management system built with **Django**, designed for real-world business operations — product tracking, sales processing, profit analytics, invoice generation, and CSV reporting, all behind a role-based authentication layer.

---

## Overview

Stock Manager gives businesses a single place to manage their entire product lifecycle — from procurement to sale. Admins control the product catalog, staff process sales, and the system handles everything downstream: stock deduction, profit calculation, invoice delivery, and business analytics rendered through an interactive dashboard.

**Tech split:** 62% Python · 36% HTML · 1% CSS

---

## Features

### Authentication & Access Control
- User signup and login
- Three roles: **Admin**, **Staff**, **User**
- Role-based permissions enforced at the view level
- Secure session management via Django's built-in auth system

### Product Management *(Admin only)*
- Add, edit, and delete products
- SKU-based unique identification
- Category tagging
- Purchase price and selling price tracking
- Minimum stock threshold configuration
- Real-time quantity updates on every sale

### Sales Management
- Multi-product sales in a single transaction
- Automatic stock deduction on sale creation
- Transaction-safe operations using `transaction.atomic()`
- Relational structure: **Sale Header → Sale Items**

### Business Analytics Dashboard
- Total Sales · Total Revenue · Total Profit (live)
- Monthly Revenue and Profit bar charts (Chart.js)
- Stock Status pie chart
- Low-stock alerts

### Financial Engine
```
Profit = (Selling Price − Purchase Price) × Quantity
```
- Monthly profit and revenue aggregation via Django ORM
- Uses `Sum()`, `F()`, and `ExpressionWrapper` for efficient DB-level computation

### Invoice System
- Download sale invoices as **PDF** (ReportLab)
- Professionally formatted with dynamic sale data
- Auto-email invoice to customer after sale creation (SMTP)

### CSV Export
Sales report export including: Sale ID · Date · Product · Quantity · Unit Price · Total · Profit

### Activity Logging *(Admin only)*
- Logs product creation, update, and deletion events
- Logs all sale creation events
- Tracks: user · action · timestamp

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | Django |
| Database | SQLite |
| Frontend | HTML, Bootstrap |
| Charts | Chart.js |
| PDF Generation | ReportLab |
| Email | Django SMTP Backend |

---

## Project Structure

```
stock-management-system/
│
└── dashboard/
    ├── dashboard/          # Project configuration
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    └── app/                # Main application
        ├── models.py
        ├── views.py
        ├── forms.py
        ├── urls.py
        ├── admin.py
        ├── templates/
        └── static/
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Likhith001/stock-management-system.git
cd stock-management-system/dashboard

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create a superuser (Admin)
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

### Email Configuration

For development, the console email backend is used (invoices print to terminal):

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

For production, swap in your SMTP credentials:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yourprovider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@email.com'
EMAIL_HOST_PASSWORD = 'your_password'
```

---

## Application Flow

```
User logs in
    │
    ├── Admin → Manages product catalog (add/edit/delete)
    │
    ├── Staff → Creates sales (multi-product)
    │               │
    │               ├── Stock auto-deducts
    │               ├── Profit calculated
    │               ├── Invoice generated (PDF)
    │               └── Invoice emailed to customer
    │
    └── Dashboard → Live analytics (revenue, profit, charts)
                        └── Export sales report as CSV
```

---

## Key Django Concepts Used

- **ORM**: `ForeignKey` relationships, QuerySets, aggregation with `Sum`, `Count`, `F()`, `ExpressionWrapper`
- **Transaction management**: `transaction.atomic()` for sale integrity
- **Role-based auth**: Custom permission checks per view
- **Template inheritance**: DRY front-end with `{% extends %}`
- **File generation**: PDF (ReportLab), CSV (Python `csv` module)
- **SMTP integration**: Automated post-sale invoice emails

---

## Roadmap

- [ ] Customer management module
- [ ] REST API (Django REST Framework)
- [ ] Multi-branch inventory support
- [ ] Automated low-stock email alerts
- [ ] Profit margin analytics and trend forecasting
- [ ] ML-based demand forecasting

---

## Author

**Likhith** — ML Engineer · Django Backend · Full-Stack

[GitHub](https://github.com/Likhith001)

---

## License

Open source. Fork it, build on it, ship it.
