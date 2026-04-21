# JP Enterprises Saharsa Website (Flask)

Modern responsive business website + inventory admin panel for **JP Enterprises Saharsa | Bihar**.

## Features
- Apple-style modern UI (black/white/blue)
- Mobile-first responsive sections: Hero, Products, Why Us, Reviews, Location, Contact
- Sticky call + floating WhatsApp buttons
- SEO meta tags for local keywords
- Flask backend with SQLite inventory
- Admin login + Add Product + Delete Product

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open: `http://127.0.0.1:5000`

## Admin Login
- URL: `/admin/login`
- Username: `admin` (override with `ADMIN_USERNAME`)
- Password: `jp@2022` (override with `ADMIN_PASSWORD`)

## Deploy
- Works on Render / Netlify (frontend only) / any Flask host.
- Set environment variable `FLASK_SECRET_KEY` in production.
