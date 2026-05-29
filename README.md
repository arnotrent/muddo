# 🌿 Muddo Agro Chemicals LTD — Official Website

A professional Django web application for **Muddo Agro Chemicals LTD (MACL)**, Uganda's trusted MAAIF-registered distributor of pesticides, herbicides, fungicides, fertilizers and spraying equipment.

---

## ✨ Features

### Public Website
- **Product Catalogue** — 18 real MACL products across 4 categories with full technical specifications
- **PDF Spec Sheets** — Download professional data sheets for any product
- **Product Comparison** — Side-by-side comparison of up to 3 products
- **Store Locator** — 11 authorised outlets across all 4 regions of Uganda, filter by region
- **Contact Form** — With reference number tracking system
- **Search** — Full-text search across products, active ingredients, crops and distributors
- **Newsletter** — Email subscription with footer form
- **Dark Mode** — Full dark/light theme with localStorage persistence
- **PWA** — Progressive Web App with offline caching via service worker
- **SEO** — Sitemap, robots.txt, structured data (JSON-LD), Open Graph tags

### Admin Panel (`/admin-panel/`)
- **Dashboard** — KPI cards, recent enquiries, low stock alerts, agent status
- **Product Management** — Add/delete products with image upload, bulk CSV import
- **Inventory** — Real-time stock tracking with reorder alerts and activity log
- **Enquiry Management** — Filter, update status, reply by email
- **Distributor Management** — Add/remove outlets with GPS coordinates
- **Agent Management** — Add/deactivate field agents, reset passwords, PDF reports
- **Supply Requests** — Approve/deny agent requests with automatic notifications
- **Real-time Chat** — Instant messaging between admin and field agents
- **Newsletter** — Subscriber management
- **Settings** — Password management, system information

### Agent Portal (`/agent/dashboard/`)
- Submit supply requests to HQ
- Track request status (Pending / Approved / Denied)
- Real-time chat with admin
- View full product catalogue

---

## 🚀 Quick Start

```bash
git clone <your-repo> muddo_agro && cd muddo_agro
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open **http://127.0.0.1:8000**

Login at **http://127.0.0.1:8000/login/**
- Admin: `admin` / `muddo@admin2024`
- Agent: `alice` / `agent@2024`

---

## 🏢 About MACL

**Muddo Agro Chemicals LTD (MACL)**
Container Village Nakivubo, Equity Bank Basement V013
P.O Box 25240, Kampala, Uganda

- **Tel:** 0772-507582 / 0702-507582 / 0772 971620 / 0701-971620
- **Email:** kulanju_w@yahoo.com
- **Facebook:** [MUDDO AGRO Chemicals LTD](https://facebook.com/p/MUDDO-AGRO-Chemicals-LTD-100063836929481/)

---

## 📋 Real Products in This System

| Category | Products |
|----------|---------|
| Herbicides | MUDDOSATE 480SL, MD MAIZE PLUS 40OD, MAX 2.4-D 720SL, MD AMETRYN 500SC, WEED IT 75.7 XL |
| Pesticides | MD ACELEMECTIN 48EC, MD FOS 48EC, TOP FENOS 50EC, MD THION 350EC, MD THOATE 40EC |
| Fungicides | TOP-LAXLY M 72WP, MD TOP LAXLYN 72WP, TOPLAXLY 72WP, COPPER OXYCHLORIDE 850WP |
| Fertilizers & Equipment | UREA 46%N, NPK 17:17:17, FOLIAR BOOST 20-20-20+TE, KNAPSACK SPRAYER 16L |

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 4.2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Static Files | WhiteNoise |
| PDF Generation | ReportLab |
| Frontend | Vanilla JS, CSS custom properties, PWA |
| Deployment | Gunicorn + Nginx / Render.com |

---

## 📁 See DEPLOY.md for full deployment instructions.
