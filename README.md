# Portfolio Backend

A production-ready Django backend for an AI-powered developer portfolio.

## Features

- **Portfolio Content Management**: Dynamic home, about, profile, and projects sections
- **AI Chatbot**: Groq-powered chatbot that answers questions about the portfolio
- **User Authentication**: JWT-based authentication with custom user model
- **Admin Dashboard**: Full-featured admin panel for content management
- **Image Upload**: Support for profile, about, project, and hero images
- **RESTful API**: Clean API endpoints for frontend integration
- **Scalable Architecture**: Modular app structure ready for growth

## Tech Stack

- **Backend**: Django 5.0
- **API**: Django REST Framework
- **Database**: SQLite (default) or PostgreSQL (production)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **AI**: Groq API (Llama 3.3)
- **CORS**: django-cors-headers
- **Deployment**: WhiteNoise, Gunicorn

## Quick Start

### Prerequisites

- Python 3.10+
- pip and virtualenv
- **Database**: SQLite (default, no installation needed) OR PostgreSQL 14+ (optional)

### Installation

1. **Clone the repository**
   ```bash
   cd My_Portfoloi
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example env file
   cp .env.example .env

   # Edit .env with your settings:
   # - SECRET_KEY
   # - OPENAI_API_KEY
   # - FRONTEND_URL
   # - USE_POSTGRES=False (default, uses SQLite)
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Windows-Specific Setup (No Docker Required)

This project works natively on Windows without Docker:

1. **No PostgreSQL?** No problem! The project uses SQLite by default.
2. **Just run:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
3. **Access the admin:** http://localhost:8000/admin/

If you want to use PostgreSQL later:
- Install PostgreSQL from https://www.postgresql.org/download/windows/
- Set `USE_POSTGRES=True` in your `.env` file
- Update your database credentials

## API Endpoints

### Portfolio Content

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/core/home/` | Get home page content | Public |
| GET | `/api/core/about/` | Get about page content | Public |
| GET | `/api/core/profile/` | Get profile information | Public |
| GET | `/api/core/projects/` | List all projects | Public |
| GET | `/api/core/projects/<id>/` | Get project details | Public |

### Chatbot

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/chatbot/chat/` | Send message to AI | Public |
| GET | `/api/chatbot/sessions/<id>/` | Get chat session | Public |
| GET | `/api/chatbot/sessions/` | List all sessions | Public |

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/users/register/` | Register new user | Public |
| POST | `/api/users/login/` | Login (get JWT tokens) | Public |
| POST | `/api/users/token/refresh/` | Refresh access token | Public |
| GET | `/api/users/me/` | Get current user | Required |
| PUT | `/api/users/me/` | Update current user | Required |
| POST | `/api/users/change-password/` | Change password | Required |

### Admin Content Management

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET/PUT | `/api/core/admin/profile/` | Manage profile | Admin |
| GET/PUT | `/api/core/admin/home/` | Manage home content | Admin |
| GET/PUT | `/api/core/admin/about/` | Manage about content | Admin |
| GET/POST | `/api/core/admin/projects/` | List/Create projects | Admin |
| GET/PUT/DELETE | `/api/core/admin/projects/<id>/` | Project CRUD | Admin |

## Admin Dashboard

Access the admin dashboard at `/admin/` with your superuser credentials.

The admin panel allows you to:
- Manage profile information
- Update home page hero section
- Edit about page content
- Create, edit, and delete projects
- View chat sessions and messages
- Manage users

## Project Structure

```
My_Portfoloi/
├── portfolio_backend/      # Main Django project
│   ├── settings/           # Modular settings
│   │   ├── base.py         # Base settings
│   │   ├── development.py  # Dev settings
│   │   └── production.py   # Prod settings
│   ├── urls.py             # Main URL config
│   └── admin.py            # Admin customization
├── core/                   # Portfolio content app
│   ├── models.py           # Profile, Home, About, Project
│   ├── serializers.py      # API serializers
│   ├── views.py            # API views
│   └── admin.py            # Admin config
├── chatbot/                # AI chatbot app
│   ├── models.py           # ChatSession, ChatMessage
│   ├── serializers.py      # API serializers
│   ├── views.py            # API views
│   ├── services/           # Business logic
│   │   └── openai_service.py
│   └── utils/              # Utilities
│       └── context_engine.py
├── users/                  # Authentication app
│   ├── models.py           # CustomUser
│   ├── serializers.py      # API serializers
│   ├── views.py            # API views
│   └── admin.py            # Admin config
├── media/                  # User uploads
├── .env                    # Environment variables
├── .env.example            # Example env file
├── requirements.txt        # Python dependencies
└── manage.py               # Django CLI
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | True |
| `DB_NAME` | PostgreSQL database name | portfolio_db |
| `DB_USER` | PostgreSQL username | postgres |
| `DB_PASSWORD` | PostgreSQL password | Required |
| `DB_HOST` | PostgreSQL host | localhost |
| `DB_PORT` | PostgreSQL port | 5432 |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `FRONTEND_URL` | Frontend URL for CORS | http://localhost:3000 |
| `JWT_SECRET_KEY` | JWT signing key | Required |
| `CHATBOT_RATE_LIMIT` | Chatbot rate limit | 10 |
| `CHATBOT_RATE_LIMIT_PERIOD` | Rate limit period (seconds) | 60 |

## Development

### Running Tests

```bash
python manage.py test
```

### Code Formatting

This project follows Django's coding standards. Use `black` and `flake8` for formatting.

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## Security Considerations

- All passwords are hashed using Django's PBKDF2
- JWT tokens for API authentication
- Rate limiting on chatbot endpoint
- CORS configured for specific origins
- Environment variables for sensitive data

## License

MIT License
