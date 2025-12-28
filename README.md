# Splity - Bill Splitting App

A Flask-based web application for splitting bills and managing shared expenses among friends and groups. Built as a learning project to apply software engineering principles from CS235.

## 🎯 Project Purpose

This project was created to:
- Apply software methodologies and design patterns learned in CS235
- Build a practical alternative to paid bill-splitting apps
- Practice clean architecture and proper software development practices
- Create a tool that me and my friends can actually use for splitting expenses

## ✨ Features

### Current Features
- **User Authentication**
  - Secure registration and login
  - Password hashing with werkzeug
  - Session management with Flask-Login

- **Group Management**
  - Create expense-sharing groups
  - Join groups using 6-character invite codes
  - View group members and details
  - Support for multiple currencies

- **User Dashboard**
  - View all groups you're a member of
  - See group invite codes for sharing
  - Quick access to group details

### Coming Soon
- Bill creation and splitting
- Expense tracking per group
- Settlement calculations
- Payment history
- Bill notifications

## 🏗️ Architecture

This project follows **layered architecture** and software engineering best practices:

```
┌─────────────────────────────────────┐
│   Presentation Layer                │  Flask Blueprints (routes)
├─────────────────────────────────────┤
│   Service Layer                     │  Business logic
├─────────────────────────────────────┤
│   Domain Layer                      │  Domain models (entities)
├─────────────────────────────────────┤
│   Data Access Layer                 │  Repository pattern
├─────────────────────────────────────┤
│   Persistence Layer                 │  SQLAlchemy ORM
└─────────────────────────────────────┘
```

### Design Patterns Applied
- **Repository Pattern**: Abstracts data access logic
- **Service Layer Pattern**: Encapsulates business logic
- **Dependency Injection**: Loose coupling between layers
- **Blueprint Pattern**: Modular route organization
- **Factory Pattern**: Application creation with `create_app()`

### Key Principles
- **Separation of Concerns**: Clear boundaries between layers
- **Single Responsibility**: Each class has one job
- **DRY (Don't Repeat Yourself)**: Reusable components
- **Domain-Driven Design**: Rich domain models with encapsulation

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Splity_flask
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   ```bash
   export SECRET_KEY='your-secret-key'
   export DATABASE_URL='sqlite:///splity.db'
   ```

5. **Run the application**
   ```bash
   python wsgi.py
   ```

6. **Access the app**
   Open your browser and go to: `http://localhost:5000`

## 📁 Project Structure

```
Splity_flask/
├── Splity/
│   ├── __init__.py              # Application factory
│   ├── adapters/                # Data access layer
│   │   ├── database.py          # Database initialization
│   │   ├── orm.py               # SQLAlchemy ORM models
│   │   └── repository.py        # Repository implementations
│   ├── domainmodel/             # Domain layer
│   │   └── models.py            # Domain entities (User, Group, Bill)
│   ├── services/                # Service layer
│   │   ├── authentication_services.py
│   │   ├── groups_services.py
│   │   └── currency_service.py
│   ├── forms/                   # WTForms
│   │   └── forms.py
│   ├── home/                    # Home blueprint
│   │   └── routes.py
│   ├── authentication/          # Authentication blueprint
│   │   └── routes.py
│   ├── bills/                   # Bills blueprint (future)
│   │   └── routes.py
│   └── templates/               # HTML templates
│       ├── base.html
│       ├── home.html
│       ├── authentication.html
│       ├── register.html
│       ├── group_creation.html
│       ├── join_group.html
│       └── group_details.html
├── tests/                       # Test suite
│   ├── conftest.py             # Test fixtures
│   ├── unit/
│   │   └── test_services.py
│   └── functional/
│       └── test_routes.py
├── config.py                    # Configuration
├── wsgi.py                      # Application entry point
└── requirements.txt             # Python dependencies
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/functional/test_routes.py

# Run with coverage
pytest --cov=Splity tests/
```

## 🛠️ Technologies Used

- **Backend**: Flask 3.0+
- **Database**: SQLAlchemy with SQLite (development)
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Password Hashing**: Werkzeug Security
- **Testing**: pytest
- **External API**: Currency API for currency list

## 📚 What I Learned from CS235

### Software Methodologies Applied
1. **Test-Driven Development (TDD)**
   - Writing tests before implementation
   - Red-Green-Refactor cycle
   - Comprehensive test coverage

2. **Clean Architecture**
   - Separation of concerns
   - Dependency inversion
   - Domain-driven design

3. **Design Patterns**
   - Repository pattern for data access
   - Factory pattern for app creation
   - Service layer for business logic

4. **SOLID Principles**
   - Single Responsibility Principle
   - Open/Closed Principle
   - Dependency Inversion Principle

5. **Version Control & Collaboration**
   - Git workflow
   - Meaningful commit messages
   - Code organization

## 🔒 Security Features

- Password hashing with PBKDF2-SHA256
- CSRF protection on forms
- Session-based authentication
- SQL injection prevention (SQLAlchemy ORM)
- Secure secret key management

## 🐛 Known Issues & Limitations

- Bill splitting functionality not yet implemented
- No email verification on registration
- Limited currency conversion (display only)
- Single-database setup (no production deployment)

## 🚧 Future Enhancements

- [ ] Implement bill creation and splitting
- [ ] Add expense categories
- [ ] Calculate who owes whom (settlement algorithm)
- [ ] Email notifications for new bills
- [ ] Mobile-responsive design improvements
- [ ] Export expense reports (CSV/PDF)
- [ ] Group statistics and charts
- [ ] Bill payment tracking
- [ ] Split by percentage or custom amounts
- [ ] Recurring bills support

## 🤝 Contributing

This is a learning project, but suggestions and improvements are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## 📝 License

This project is for educational purposes. Feel free to use and modify as needed.

## 🙏 Acknowledgments

- CS235 Software Methodologies course for the foundation
- Flask documentation and community
- Friends who inspired this project by complaining about paid bill-splitting apps!

## 📧 Contact

For questions or feedback about this project, please open an issue on GitHub.

---

**Note**: This is a learning project built to apply software engineering principles. It's not intended for production use without additional security hardening and testing.
