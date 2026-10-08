# Cloud-Based Courier Tracking System

A beginner-friendly courier tracking mini-project built with Flask, SQLite, HTML, CSS and JavaScript.

## Features

- Customer courier tracking using Tracking ID
- Courier details and current location
- Delivery status
- Expected delivery date
- Admin dashboard
- Add new courier
- Update courier location/status
- Delete courier
- SQLite cloud-ready database structure
- JSON tracking API

## Demo Tracking IDs

- CT1001
- CT1002
- CT1003

## Project Structure

```text
Cloud-Based-Courier-Tracking-System/
│
├── app.py
├── requirements.txt
├── README.md
├── courier.db              # Created automatically after first run
│
├── templates/
│   ├── index.html
│   ├── tracking.html
│   └── admin.html
│
└── static/
    ├── style.css
    └── script.js
```

## How to Run in VS Code

### 1. Open the project folder

Open `Cloud-Based-Courier-Tracking-System` in VS Code.

### 2. Open terminal

Run:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install Flask

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

### 5. Open in browser

```text
http://127.0.0.1:5000
```

Admin dashboard:

```text
http://127.0.0.1:5000/admin
```

## How to Use

1. Enter `CT1001` on the home page.
2. Click Track Courier.
3. View sender, receiver, route, current location and status.
4. Open `/admin` to add or update courier details.

## API

Example:

```text
http://127.0.0.1:5000/api/track/CT1001
```

The API returns courier information as JSON.

## Cloud Deployment

For a cloud version, the Flask application can be deployed to services such as Render, Railway, AWS, Azure or Google Cloud. For production, SQLite can be replaced with a managed cloud database such as PostgreSQL, MySQL or a cloud NoSQL database.

## Technologies

- Frontend: HTML5, CSS3, JavaScript
- Backend: Python Flask
- Database: SQLite
- API: REST-style JSON endpoint
- Cloud concept: deployable web service + cloud database migration
