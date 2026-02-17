# Campus Lost & Found Platform - Python Flask Version

A comprehensive web application built with Python Flask for students, teachers, and staff to report and find lost items within a school campus. Features a full backend with SQLite database, RESTful API, and responsive frontend.

![Campus Lost & Found Platform](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-2.0+-red)
![License](https://img.shields.io/badge/license-MIT-green)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

This platform provides a centralized solution for educational institutions to manage lost and found items. Unlike the static HTML version, this Python Flask implementation offers:

- **Persistent storage** with SQLite database
- **RESTful API** for easy integration
- **Real-time updates** with database queries
- **Search functionality** across all items
- **Category filtering** (Lost/Found)
- **Statistics dashboard** with live counts
- **Contact information** for item claims

## Features

### Core Functionality
- **Multi-role Support**: Students, Teachers, Staff
- **Dual Report Types**: Lost items and Found items
- **Persistent Storage**: All reports saved in database
- **Role-based Filtering**: Filter by user role
- **Type-based Filtering**: Filter by Lost/Found
- **Full-text Search**: Search by name, description, location
- **Live Statistics**: Real-time dashboard counts
- **Item Details Page**: Detailed view for each item

### API Features
- **RESTful Endpoints**: Complete CRUD operations
- **JSON Responses**: Easy integration with frontend
- **Error Handling**: Proper HTTP status codes
- **Search Endpoint**: Advanced search capabilities

### User Interface
- **Clean, Modern Design**: Intuitive layout
- **Responsive**: Works on all devices
- **Real-time Updates**: Live data from database
- **Interactive Forms**: User-friendly submission
- **Success Notifications**: Visual feedback
- **Loading States**: Spinner during data fetch

## Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 2.0+** - Web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database (easily switchable to PostgreSQL)
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with Flexbox/Grid
- **JavaScript (ES6+)** - Dynamic interactions
- **Font Awesome 6** - Icons
- **Google Fonts (Inter)** - Typography

## Demo

![Screenshot_17-2-2026_224633_127 0 0 1](https://github.com/user-attachments/assets/154d022f-d7b8-4efd-8584-2987ffc27009)


**Live Demo**: [https://campus-lost-found-python.herokuapp.com](https://campus-lost-found-python.herokuapp.com)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/campus-lost-found-python.git
   cd campus-lost-found-python
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   ```bash
   # Create .env file
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "DATABASE_URL=sqlite:///instance/lost_found.db" >> .env
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   - Navigate to `http://localhost:5000`
   - Start reporting and finding items!

## Usage

### Reporting an Item

1. **Select your role** (Student/Teacher/Staff)
2. **Choose report type** (Lost/Found)
3. **Enter item details**:
   - Item name (required)
   - Description (optional)
   - Location (optional)
   - Contact info (optional)
4. **Click "Post Report"**

### Finding Items

1. **Use role tabs** to filter by user type
2. **Use type filter** to show only Lost or Found
3. **Search** for specific items using keywords
4. **Click on any item** to view details
5. **Contact the reporter** using provided info

### Managing Items

- **View Details**: Click on any item card
- **Mark as Returned**: Click "Claim Item" on detail page
- **Delete**: Remove outdated reports (admin feature)

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/items` | Get all items | `role`, `type` |
| GET | `/items/<id>` | Get single item | - |
| POST | `/items` | Create new item | JSON body |
| PUT | `/items/<id>` | Update item | JSON body |
| DELETE | `/items/<id>` | Delete item | - |
| GET | `/stats` | Get statistics | - |
| GET | `/search` | Search items | `q` (query) |
| POST | `/items/<id>/claim` | Mark as returned | - |

### Example Requests

**Get all items:**
```bash
curl http://localhost:5000/api/items
```

**Filter by role:**
```bash
curl http://localhost:5000/api/items?role=student
```

**Create new item:**
```bash
curl -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{
    "role": "student",
    "type": "lost",
    "name": "Blue Backpack",
    "description": "Nike backpack with laptop sleeve",
    "location": "Library 2nd Floor",
    "contact_info": "john@email.com"
  }'
```

**Search items:**
```bash
curl http://localhost:5000/api/search?q=laptop
```

### Response Format

```json
{
  "id": 1,
  "role": "student",
  "role_display": "Student",
  "type": "lost",
  "type_display": "LOST",
  "name": "Engineering Drawing Set",
  "description": "Includes compass, rulers",
  "location": "Drafting Room 302",
  "status": "active",
  "contact_info": "student@email.com",
  "created_at": "2024-01-15 10:30",
  "time_ago": "2 hours ago"
}
```

## Project Structure

```
campus-lost-found-python/
│
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── .gitignore            # Git ignore file
├── README.md             # This file
│
├── instance/
│   └── lost_found.db     # SQLite database (auto-generated)
│
├── static/
│   ├── css/
│   │   └── style.css     # CSS styles
│   └── js/
│       └── main.js       # JavaScript functionality
│
├── templates/
│   ├── index.html        # Main page
│   └── item_detail.html  # Item detail page
│
└── tests/                 # Unit tests
    ├── test_app.py
    └── test_api.py
```

## Database Schema

### Items Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| role | String(20) | student/teacher/staff |
| type | String(10) | lost/found |
| name | String(100) | Item name |
| description | Text | Detailed description |
| location | String(200) | Where found/lost |
| status | String(20) | active/returned |
| contact_info | String(100) | Contact details |
| created_at | DateTime | Timestamp |
| updated_at | DateTime | Last update |

### Users Table (for future auth)

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| username | String(80) | Unique username |
| email | String(120) | Unique email |
| role | String(20) | User role |
| department | String(100) | Department |
| created_at | DateTime | Timestamp |

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Flask settings
SECRET_KEY=your-super-secret-key-change-this
FLASK_ENV=development
FLASK_APP=app.py

# Database (default SQLite)
DATABASE_URL=sqlite:///instance/lost_found.db

# For production PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Configuration Classes

```python
# config.py
class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/lost_found.db'

class ProductionConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

## Deployment

### Deploy to Heroku

1. **Create a Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Add PostgreSQL database**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set FLASK_ENV=production
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Deploy to PythonAnywhere

1. **Upload files** via PythonAnywhere console
2. **Set up virtual environment**
3. **Configure WSGI file**
4. **Set up static files mapping**

### Deploy with Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
```

## Testing

Run tests with pytest:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app
```

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Use meaningful commit messages

### Ideas for Contributions
- User authentication system
- Image upload for items
- Email notifications
- Item matching algorithm
- Admin dashboard
- Export reports to CSV
- Mobile app integration
- Multi-language support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

##  Acknowledgments

- Flask community for excellent documentation
- Font Awesome for beautiful icons
- All contributors and users
- Educational institutions for inspiration

##  Contact

Om Gedam

GitHub: @itsomg134

Email: omgedam123098@gmail.com

Twitter (X): @omgedam

LinkedIn: Om Gedam

Portfolio: https://ogworks.lovable.app

## Project Status

- Current Version: 2.0.0
- Last Updated: January 2024
- Next Release: Coming Soon

## Features for Future Releases

- [ ] User authentication
- [ ] Image upload
- [ ] Email notifications
- [ ] Admin dashboard
- [ ] Item categories
- [ ] QR code generation
- [ ] Mobile app
- [ ] Real-time chat
- [ ] Location mapping
