# Splity - Bill Splitting App

A Flask-based web application for splitting bills and managing shared expenses among friends and groups.

## 💭 Why I Built This

I've known Python for quite some time. During this journey of learning, I've always created scripts and programs that help me with small tasks—a PDF merger, Spotify playlist downloader, and various problem-solving tools during university. But I never truly understood how software is **actually built**.

After taking a software methodologies course (CS235) where we relied heavily on AI, I wanted to challenge myself: **build something real, from scratch, without the AI crutch.** I wanted to truly understand software architecture, design patterns, and best practices—not just copy-paste solutions.

At the same time, my friends and I travelled quite a lot in 2025. We kept running into the same frustration: bill-splitting apps with too many features locked behind paywalls. So I thought, **why not solve both problems at once?**

This is Splity—a learning journey and a practical solution combined.

## 🎯 What This Project Demonstrates

- **Clean Architecture**: Proper separation of concerns across layers
- **Design Patterns**: Repository, Service Layer, Factory, and Blueprint patterns
- **Domain-Driven Design**: Rich domain models with proper encapsulation
- **Test-Driven Development**: Comprehensive test coverage with pytest
- **SOLID Principles**: Single responsibility, dependency inversion, and more
- **Secure Authentication**: Password hashing, CSRF protection, session management
- **Real-World Application**: Solving an actual problem my friends and I face

## ✨ Features

### Current Implementation ✅
- **User Authentication**
  - Secure registration and login system
  - Password hashing with Werkzeug (PBKDF2-SHA256)
  - Session management with Flask-Login
  - Protected routes and access control

- **Group Management**
  - Create expense-sharing groups with custom currencies
  - Generate unique 6-character invite codes
  - Join groups using invite codes
  - View group members and details
  - Support for 140+ currencies via external API

- **User Dashboard**
  - View all groups you're a member of
  - Quick access to group details and invite codes
  - Clean, intuitive interface

### In Development 🚧
- Bill creation and management
- Expense splitting algorithms
- Settlement calculations (who owes whom)
- Payment tracking and history
- Expense categories and reports

## 🏗️ Architecture & Design

### Layered Architecture

This project follows a **strict layered architecture** to ensure maintainability and testability:

```
┌─────────────────────────────────────┐
│   Presentation Layer                │  Flask Blueprints (routes)
│   • Handles HTTP requests/responses │
│   • Renders templates               │
│   • Form validation                 │
├─────────────────────────────────────┤
│   Service Layer                     │  Business logic
│   • Orchestrates operations         │
│   • Enforces business rules         │
│   • Transaction management          │
├─────────────────────────────────────┤
│   Domain Layer                      │  Domain models (entities)
│   • Core business entities          │
│   • Domain logic                    │
│   • No external dependencies        │
├─────────────────────────────────────┤
│   Data Access Layer                 │  Repository pattern
│   • Abstracts database operations   │
│   • Converts between ORM and Domain │
│   • Query logic                     │
├─────────────────────────────────────┤
│   Persistence Layer                 │  SQLAlchemy ORM
│   • Database schema                 │
│   • ORM mappings                    │
│   • Connection management           │
└─────────────────────────────────────┘
```

**Why this matters:**
- Each layer has a **single, well-defined responsibility**
- Changes in one layer don't cascade through the system
- Easy to test each layer in isolation
- Can swap out implementations (e.g., change database) without affecting business logic

### Design Patterns

#### 1. Repository Pattern
**Purpose**: Abstracts data access logic from business logic

```python
class GroupRepository:
    def add(self, group: Group):
        # Converts domain Group to ORM and saves
        
    def get_by_id(self, group_id: int) -> Group:
        # Fetches from DB and converts back to domain
```

**Benefits:**
- Business logic doesn't know about database details
- Easy to mock for testing
- Can change database implementation without touching business logic

#### 2. Service Layer Pattern
**Purpose**: Encapsulates business logic and orchestrates operations

```python
def create_group(name: str, description: str, currency: str, creator_id: int) -> Group:
    # Validates business rules
    # Orchestrates repository calls
    # Manages transactions
```

**Benefits:**
- Business rules centralized in one place
- Routes stay thin and focused on HTTP concerns
- Reusable across different interfaces (web, API, CLI)

#### 3. Factory Pattern
**Purpose**: Creates application instances with proper configuration

```python
def create_app():
    app = Flask(__name__)
    # Configure
    # Initialize extensions
    # Register blueprints
    return app
```

**Benefits:**
- Clean separation of creation and usage
- Easy to create different configurations (test, dev, prod)
- Supports multiple app instances

#### 4. Blueprint Pattern
**Purpose**: Modular organization of routes

```python
home_blueprint = Blueprint("home", __name__)
authentication_blueprint = Blueprint("authentication", __name__)
```

**Benefits:**
- Logical grouping of related routes
- Can be developed and tested independently
- Easy to enable/disable features

### Domain-Driven Design

Domain models are **rich objects** with behavior, not just data containers:

```python
class Group:
    def __init__(self, name: str, description: str, currency: str, ...):
        # Encapsulation: private attributes
        self.__name = name
        self.__invite_code = self._generate_invite_code()
    
    @property
    def name(self):
        return self.__name  # Controlled access
```

**Key principles:**
- **Encapsulation**: Private attributes, public properties
- **Validation**: Domain objects enforce their own invariants
- **Immutability**: Some properties can't be changed after creation
- **No database concerns**: Domain models know nothing about persistence

### SOLID Principles in Practice

#### Single Responsibility Principle
Each class has **one reason to change**:
- `UserRepository` → only changes if data access logic changes
- `AuthenticationService` → only changes if authentication rules change
- `LoginForm` → only changes if login form requirements change

#### Open/Closed Principle
Open for extension, closed for modification:
- New repositories can be added without modifying existing ones
- New services can use existing repositories
- New blueprints don't affect existing ones

#### Dependency Inversion Principle
High-level modules don't depend on low-level modules:
- Services depend on repository **interfaces** (conceptually), not implementations
- Routes depend on services, not repositories directly
- Domain layer has **zero dependencies** on other layers

### Test-Driven Development

Tests are written **before** implementation following the Red-Green-Refactor cycle:

**Red**: Write a failing test
```python
def test_user_cannot_create_duplicate_group():
    # Test fails because feature doesn't exist yet
```

**Green**: Write minimal code to pass
```python
def create_group(...):
    if repo.get_by_name_and_creator(name, creator_id):
        raise GroupServiceException("Group already exists")
```

**Refactor**: Improve code while keeping tests passing

**Test Coverage:**
- ✅ Unit tests for service layer business logic
- ✅ Integration tests for routes and database
- ✅ Fixture-based setup for clean test isolation
- ✅ Edge cases and error conditions

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/splity-flask.git
   cd splity-flask
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   ```bash
   # On macOS/Linux:
   export SECRET_KEY='your-secret-key-here'
   export DATABASE_URL='sqlite:///splity.db'
   
   # On Windows:
   set SECRET_KEY=your-secret-key-here
   set DATABASE_URL=sqlite:///splity.db
   ```

5. **Run the application**
   ```bash
   python wsgi.py
   ```

6. **Access the app**
   Open your browser and navigate to: **http://localhost:5000**

### Quick Start
1. Register a new account
2. Create your first group (e.g., "Weekend Trip")
3. Share the 6-character invite code with friends
4. Friends join using the code
5. Start managing expenses together

## 📁 Project Structure

```
Splity_flask/
├── Splity/                      # Main application package
│   ├── __init__.py              # Application factory (create_app)
│   ├── adapters/                # Data Access Layer
│   │   ├── database.py          # Database initialization
│   │   ├── orm.py               # SQLAlchemy ORM models
│   │   └── repository.py        # Repository implementations
│   ├── domainmodel/             # Domain Layer
│   │   └── models.py            # Domain entities (User, Group, Bill)
│   ├── services/                # Service Layer (Business Logic)
│   │   ├── authentication_services.py
│   │   ├── groups_services.py
│   │   └── currency_service.py
│   ├── forms/                   # WTForms for validation
│   │   └── forms.py
│   ├── home/                    # Home blueprint
│   │   └── routes.py
│   ├── authentication/          # Authentication blueprint
│   │   └── routes.py
│   ├── bills/                   # Bills blueprint (in progress)
│   │   └── routes.py
│   └── templates/               # Jinja2 HTML templates
│       ├── base.html
│       ├── home.html
│       ├── authentication.html
│       ├── register.html
│       ├── group_creation.html
│       ├── join_group.html
│       └── group_details.html
├── tests/                       # Test suite
│   ├── conftest.py             # Pytest fixtures
│   ├── unit/                   # Unit tests
│   │   └── test_services.py
│   └── functional/             # Integration tests
│       └── test_routes.py
├── config.py                    # Configuration settings
├── wsgi.py                      # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🧪 Testing

Comprehensive test suite following TDD principles:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/functional/test_routes.py

# Run with coverage report
pytest --cov=Splity tests/

# Run a specific test
pytest tests/functional/test_routes.py::test_join_group_with_valid_code -v
```

### Test Organization
- **Unit Tests**: Test service layer logic in isolation
- **Functional Tests**: Test routes and full request/response cycle
- **Fixtures**: Reusable test setup (database, authenticated clients)
- **Coverage**: Aim for high coverage of critical paths

## 🛠️ Technologies & Tools

- **Backend**: Flask 3.0+ (lightweight WSGI framework)
- **Database**: SQLAlchemy ORM with SQLite (development)
- **Authentication**: Flask-Login (session management)
- **Forms**: Flask-WTF + WTForms (validation and CSRF protection)
- **Security**: Werkzeug (PBKDF2-SHA256 password hashing)
- **Testing**: pytest + pytest-flask (test framework)
- **External API**: fawazahmed0 Currency API (140+ currencies)

## 🔒 Security Considerations

- **Password Security**: PBKDF2-SHA256 hashing (100,000 iterations)
- **CSRF Protection**: Token-based protection on all forms
- **Session Security**: Secure cookie settings
- **SQL Injection Prevention**: Parameterized queries via ORM
- **Input Validation**: Server-side validation on all inputs
- **Secret Management**: Environment variables for sensitive data

## 🐛 Known Limitations

- Bill splitting functionality not yet implemented
- SQLite database (suitable for development, not production scale)
- No email verification or password reset
- Currency display only (no real-time conversion rates)
- No mobile app or responsive design optimizations

## 🚧 Next Steps

**Immediate priorities:**
- Implement bill creation within groups
- Add bill splitting algorithms (equal split initially)
- Build settlement calculation (who owes whom)
- Add payment tracking and history

**Future enhancements:**
- Custom split amounts (percentage, custom amounts)
- Expense categories and filtering
- Export reports (CSV, PDF)
- Mobile-responsive design
- Production deployment preparation

## 📝 License

MIT License - This project is open source and available for educational purposes.
