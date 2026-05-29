# Muddo Agro Chemicals LTD — Deployment Guide

## 🚀 Quick Start (Development)

```bash
# 1. Create virtual environment
python3 -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment file and configure
cp .env.example .env
# Edit .env with your values (at minimum set DJANGO_SECRET_KEY)

# 4. Run migrations
python manage.py migrate

# 5. Seed real product data (18 products, 11 distributors, 4 demo agents)
python manage.py seed_data

# 6. Start development server
python manage.py runserver
```

Open **http://127.0.0.1:8000**

---

## 🔑 Default Credentials

| Role          | URL                         | Username | Password        |
|---------------|-----------------------------|----------|-----------------|
| Administrator | /login/ → Administrator     | admin    | muddo@admin2024 |
| Field Agent   | /login/ → Field Agent       | alice    | agent@2024      |
| Field Agent   | /login/ → Field Agent       | robert   | agent@2024      |
| Field Agent   | /login/ → Field Agent       | grace    | agent@2024      |
| Field Agent   | /login/ → Field Agent       | patrick  | agent@2024      |

> ⚠️ **Change all passwords immediately** via Admin → Settings before going live.

---

## 🌐 Key URLs

| URL                              | Description                  |
|----------------------------------|------------------------------|
| `/`                              | Home page                    |
| `/pesticides/`                   | Pesticide products           |
| `/herbicides/`                   | Herbicide products           |
| `/fungicides/`                   | Fungicide products           |
| `/other-products/`               | Fertilizers & equipment      |
| `/product/<id>/`                 | Product detail               |
| `/product/<id>/spec-sheet/`      | Download PDF spec sheet      |
| `/compare/`                      | Side-by-side comparison      |
| `/distributors/`                 | Store locator                |
| `/contact/`                      | Contact form                 |
| `/track/?ref=ENQ-XXXXXXXX`       | Track enquiry by ref number  |
| `/search/?q=…`                   | Search products              |
| `/about/`                        | About us & FAQ               |
| `/login/`                        | Staff login                  |
| `/admin-panel/`                  | Admin dashboard              |
| `/admin-panel/products/`         | Manage products              |
| `/admin-panel/inventory/`        | Stock management             |
| `/admin-panel/requests/`         | Customer enquiries           |
| `/admin-panel/agents/`           | Field agents                 |
| `/admin-panel/chat/`             | Message agents               |
| `/admin-panel/settings/`         | Admin settings               |
| `/agent/dashboard/`              | Agent portal                 |
| `/django-admin/`                 | Django built-in admin        |
| `/sitemap.xml`                   | XML sitemap                  |

---

## 🖥️ Production Setup (Ubuntu + Nginx + Gunicorn)

### 1. Server dependencies
```bash
sudo apt update && sudo apt install python3-pip python3-venv nginx certbot python3-certbot-nginx -y
```

### 2. App setup
```bash
sudo mkdir -p /var/www/muddo_agro
cd /var/www/muddo_agro
# Upload your code here or clone from git
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env && nano .env   # Fill in all production values
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --noinput
```

### 3. Systemd service (copy muddo_agro.service)
```bash
sudo cp muddo_agro.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now muddo_agro
sudo systemctl status muddo_agro
```

### 4. Nginx config (copy muddo_agro.nginx)
```bash
sudo cp muddo_agro.nginx /etc/nginx/sites-available/muddo_agro
# Edit server_name in the file to your domain
sudo ln -s /etc/nginx/sites-available/muddo_agro /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### 5. SSL with Let's Encrypt
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## ☁️ Deploy on Render.com (Free Tier)

1. Push code to GitHub
2. New Web Service → connect repo
3. **Build Command:**
   ```
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py seed_data
   ```
4. **Start Command:**
   ```
   gunicorn muddo_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```
5. Add environment variables (see `.env.example`)

---

## ⚙️ Environment Variables (.env)

| Variable              | Required | Description                                     |
|-----------------------|----------|-------------------------------------------------|
| `DJANGO_SECRET_KEY`   | **Yes**  | Long random string — change from default        |
| `DEBUG`               | No       | `False` in production, `True` for dev           |
| `ALLOWED_HOSTS`       | **Yes**  | Comma-separated: `yourdomain.com,www.yourdomain.com` |
| `MAIL_PASSWORD`       | No       | Gmail App Password — enables email notifications |
| `MAIL_USERNAME`       | No       | Gmail address (default: muddoagro811@gmail.com) |
| `GA_MEASUREMENT_ID`   | No       | Google Analytics 4 ID (G-XXXXXXXXXX)            |
| `GOOGLE_MAPS_KEY`     | No       | Google Maps JS API key — enables directions     |
| `WHATSAPP_NUMBER`     | No       | WhatsApp number without + (default: 256772507582)|

---

## ✅ Production Checklist

- [ ] Change admin password (Admin → Settings)
- [ ] Change all agent passwords (Admin → Settings → Reset Agent Password)
- [ ] Set `DEBUG=False` in `.env`
- [ ] Set a strong `DJANGO_SECRET_KEY` (50+ random characters)
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Configure Gmail App Password for email notifications
- [ ] Add Google Maps API key for distributor map directions
- [ ] Set up SSL certificate (HTTPS)
- [ ] Run `python manage.py collectstatic`
- [ ] Test contact form sends email
- [ ] Test PDF spec sheet download
- [ ] Verify all 18 products display correctly

---

## 📦 Project Structure

```
muddo_project/
├── manage.py
├── requirements.txt
├── .env.example
├── muddo.db                    ← SQLite database (auto-created)
├── muddo_project/              ← Django config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/                   ← Home, about, contact, search, compare, track
│   │   ├── management/commands/seed_data.py
│   │   └── templatetags/muddo_filters.py
│   ├── products/               ← Product catalogue + PDF spec sheets
│   ├── inventory/              ← Stock management
│   ├── agents/                 ← Agent accounts, login, PDF reports
│   ├── requests_app/           ← Supply requests
│   ├── messaging/              ← Admin ↔ Agent real-time chat
│   ├── distributors/           ← Store locator
│   └── analytics/              ← Full admin dashboard + all admin views
├── templates/
│   ├── base.html               ← Main site layout
│   ├── index.html              ← Home page
│   ├── about.html
│   ├── contact.html
│   ├── distributors.html
│   ├── search.html
│   ├── track.html
│   ├── compare.html
│   ├── 404.html
│   ├── auth/login.html
│   ├── products/               ← Product templates
│   ├── admin/                  ← Full admin panel (11 templates)
│   └── agent/                  ← Agent portal (2 templates)
├── static/
│   ├── css/                    ← 10 CSS files
│   ├── js/                     ← 5 JS files
│   ├── images/                 ← Logo + 12 product images
│   ├── manifest.json           ← PWA manifest
│   └── sw.js                   ← Service worker (offline support)
└── media/                      ← Uploaded product images (auto-created)
```
