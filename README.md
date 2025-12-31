# Splity - Bill Splitting App

A Flask-based web application for splitting bills and managing shared expenses among friends and groups.

## 💭 Why I Built This

I've been familiar with Python for quite some time, having created scripts and small tools during my university studies. However, I never truly understood how software is **actually built**—the architecture, patterns, and principles that underlie it.

After taking a software methodologies course (CS235) where we relied heavily on AI, I challenged myself: **build something real, from scratch, without the AI crutch.** 

Meanwhile, my friends and I travelled a lot in 2025, constantly frustrated by bill-splitting apps with paywalled features. So I decided to solve both problems: learn proper software engineering **and** build a tool we actually need.

## 🎓 What I Learned

Building Splity without AI taught me that **understanding beats copying**. Debugging, refactoring, and watching tests pass—that's where real learning happens. This project significantly accelerated my learning progress in web development.

## 🎯 What This Demonstrates

- **Clean Architecture**: Strict separation of concerns across layers
- **Design Patterns**: Repository, Service Layer, Factory, Blueprint patterns
- **Domain-Driven Design**: Rich domain models with proper encapsulation
- **Test-Driven Development**: Comprehensive test coverage with pytest
- **SOLID Principles**: Single responsibility, dependency inversion
- **Secure Authentication**: Password hashing, CSRF protection, session management

## ✨ Features

- **User Authentication**: Secure registration, login, password hashing
- **Group Management**: Create groups, invite members with codes, manage memberships
- **Bill Splitting**: Create bills, split expenses equally, track who owes whom
- **Settlement Calculation**: Smart algorithm to minimise the number of transactions
- **Multi-Currency Support**: 140+ currencies via external API
- **Dashboard**: View all groups, bills, and balances at a glance

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Presentation Layer                │  Routes, Templates, Forms
├─────────────────────────────────────┤
│   Service Layer                     │  Business Logic, Validation
├─────────────────────────────────────┤
│   Domain Layer                      │  Entities (User, Group, Bill)
├─────────────────────────────────────┤
│   Data Access Layer                 │  Repository Pattern
├─────────────────────────────────────┤
│   Persistence Layer                 │  SQLAlchemy ORM, Database
└─────────────────────────────────────┘
```

**Key principles:**
- Each layer has a single, well-defined responsibility
- Business logic is independent of database and UI
- Domain models know nothing about persistence
- Easy to test, maintain, and extend


## 🚀 Getting Started

### Installation

```bash
# Clone and setup
git clone https://github.com/yourusername/splity-flask.git
cd splity-flask
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python wsgi.py
```

Visit **http://localhost:5000**

### Quick Start
1. Register an account
2. Create a group (e.g., "Weekend Trip")
3. Share the 6-character invite code with friends
4. Create bills and split expenses
5. View who owes whom

## 🧪 Testing

```bash
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest --cov=Splity tests/      # With coverage
```

**Test coverage:**
- User authentication and authorisation
- Group creation and management
- Bill splitting and calculations
- Settlement algorithms
- Access control and security

## 🛠️ Technologies

- **Flask 3.0+**: Web framework
- **SQLAlchemy**: ORM and database
- **Flask-Login**: Session management
- **Flask-WTF**: Forms and CSRF protection
- **Werkzeug**: Password hashing (PBKDF2-SHA256)
- **pytest**: Testing framework
- **Currency API**: https://github.com/fawazahmed0/exchange-api

## 🔒 Security

- Password hashing with PBKDF2-SHA256
- CSRF protection on all forms
- SQL injection prevention via ORM
- Session-based authentication
- Server-side input validation


## 📝 License

MIT License - Open source and available for educational purposes.

---

**Note**: This is a learning project demonstrating software engineering principles. Not intended for production use without additional hardening and infrastructure.
