# 🌿 Muddo Agro Chemicals LTD — Official Website

Django web application for **Muddo Agro Chemicals LTD (MACL)**, Uganda's MAAIF-registered agrochemical distributor.

## 🚀 Quick Start

```bash
unzip muddo_agro_django.zip && cd muddo_project
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open **http://127.0.0.1:8000** — Login at `/login/`

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | muddo@admin2024 |
| Agent | alice / robert / grace / patrick | agent@2024 |

## 📱 Device Compatibility

- **Mobile (320px+)** — Full mobile menu, stacked layouts, optimised touch targets (44px min)
- **Tablet (640–959px)** — 2-column grids, adapted navigation  
- **Desktop (960px+)** — Full navbar with dropdown menus, multi-column layouts

## 🧭 Navigation Features

- Sticky navbar with scroll shadow
- Mega dropdown for Products (Pesticides / Herbicides / Fungicides / Fertilizers / Compare)
- Hamburger mobile menu with search, CTAs and all links
- WhatsApp FAB (bottom-right) on every page
- Back-to-top button
- Dark/light mode toggle (persisted in localStorage)

## ☁️ Deploy on Render.com

Build command:
```
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py seed_data
```

Start command:
```
gunicorn muddo_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

See `render.yaml` — just connect your GitHub repo and deploy.

## 📦 What's Included

- **18 real MACL products** — pesticides, herbicides, fungicides, fertilizers, equipment
- **11 distributor outlets** — all 4 regions of Uganda with GPS coordinates
- **30 HTML templates** — fully responsive, no quote/CTA section
- **PDF spec sheets** — professional ReportLab-generated data sheets per product
- **Admin panel** — full product/inventory/agent/chat/enquiry management
- **Agent portal** — supply requests, real-time chat with admin
- **PWA-ready** — service worker, manifest, offline caching
