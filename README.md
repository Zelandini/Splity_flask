# Splity

Splity is a full-stack expense-sharing application for creating groups, recording shared expenses, calculating balances and simplifying repayments between friends.

**Live application:** [https://3-24-244-206.sslip.io](https://3-24-244-206.sslip.io)

## Why I Built It

While travelling with friends in 2025, I became frustrated by bill-splitting apps that placed useful features behind a paywall. I built Splity both to solve that problem and to strengthen my understanding of full-stack development, software architecture, testing and deployment.

## Features

- Sign in securely with Google OAuth
- Create groups in a selected currency
- Join groups using a six-character invitation code
- Record which member paid for an expense
- Split expenses equally or assign custom amounts
- Edit and delete bills with ownership and membership checks
- Calculate each member's net balance
- Simplify debts into a smaller set of repayments
- Record repayments and let the receiving member confirm them
- Manage group details and membership safely
- Use a responsive redesigned interface on desktop and mobile

## Architecture

Splity uses an application-factory structure with Flask Blueprints and separates responsibilities across several layers:

- **Presentation:** Flask routes, Jinja2 templates, forms and JavaScript
- **Service:** validation, bill-splitting rules and settlement calculations
- **Domain:** users, groups, bills and repayment models
- **Data access:** repository classes and SQLAlchemy ORM
- **Persistence:** SQLite in the current deployment, configurable through `DATABASE_URL`

This structure keeps business rules separate from web routes and database operations, making the application easier to test and extend.

## Technology Stack

- **Backend:** Python, Flask, Flask-Login, Flask-WTF and Authlib
- **Database:** SQLAlchemy and SQLite
- **Frontend:** Jinja2, HTML, CSS and JavaScript
- **Authentication:** Google OAuth 2.0 / OpenID Connect
- **Testing:** pytest and pytest-cov
- **Deployment:** AWS Lightsail, Ubuntu, Gunicorn and Nginx
- **Security and networking:** HTTPS with Let's Encrypt, CSRF protection and secure server-side configuration

## Local Setup

### 1. Clone the redesign branch

```bash
git clone --branch redesign --single-branch https://github.com/Zelandini/Splity_flask.git
cd Splity_flask
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Splity reads the following values from the environment:

| Variable | Purpose | Required locally? |
| --- | --- | --- |
| `SECRET_KEY` | Signs Flask sessions and CSRF tokens | Recommended |
| `DATABASE_URL` | Overrides the default SQLite database | No |
| `GOOGLE_CLIENT_ID` | Identifies the Google OAuth application | Required for Google login |
| `GOOGLE_CLIENT_SECRET` | Authenticates the Google OAuth application | Required for Google login |

Never commit secrets or local environment files to Git.

Without Google credentials, the application retains its local authentication fallback for development and testing. The default database is created automatically as `splity.db` in Flask's instance directory.

### 5. Run the application

```bash
python wsgi.py
```

Open [http://127.0.0.1:5001](http://127.0.0.1:5001).

## Testing

Run the complete test suite:

```bash
python -m pytest -v
```

Generate a coverage report:

```bash
python -m pytest --cov=Splity tests/
```

The suite covers domain models, authentication, group management, access control, equal and custom bill splits, settlement calculations, repayments and currency-service fallback behaviour.

## Production Deployment

The redesign is deployed on an Ubuntu AWS Lightsail instance using:

- Gunicorn with a Unix socket for the Flask application
- Nginx as the public reverse proxy
- A Lightsail static IPv4 address
- HTTPS certificates issued by Let's Encrypt
- `systemd` for automatic startup and restart
- Protected environment variables stored outside the repository

The current production deployment uses SQLite and one Gunicorn worker to suit the application's small user base and lightweight Lightsail instance.

## Planned Improvements

- Move production persistence from SQLite to PostgreSQL as usage grows
- Add automated deployment and database-backup workflows
- Continue improving accessibility and mobile usability

## Security

- Google OAuth avoids storing Google passwords
- CSRF protection is enabled for forms
- SQLAlchemy provides parameterised database access
- Session cookies use `HttpOnly` and `SameSite=Lax`
- Credentials and the production database remain outside Git
- Nginx redirects public traffic to HTTPS

## Licence

MIT License. This is an educational portfolio project and should receive further infrastructure and security hardening before supporting a large public user base.
