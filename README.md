# Computer Science Department Portal

This repository contains the official web application for the Computer Science Department. **This portal is currently operational and actively used in production at Rajarshi Shahu Mahavidyalaya, Latur (Autonomous)**.

The application features a complete Flask backend with functionalities including:
- Student signup and secure login
- Blog submission and approval workflow
- Contact form handling
- Comprehensive Admin panel for managing blogs, contacts, faculty, events, notifications, gallery, and research
- Local JSON database fallback

## Run Locally

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env to set SECRET_KEY and other vars
python run.py
```

## Notes
- Email functionality requires configuration. Set `MAIL_USERNAME` and `MAIL_PASSWORD` in your `.env` file if real email functionality is required.
- By default, the application uses a local `database.json` file as a database (created automatically if not present).
- Upcoming features: Update in home page hero image and sort notifications.
