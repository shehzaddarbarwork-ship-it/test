# Python CRM Project

A modern Customer Relationship Management (CRM) system built with Python, Flask, SQLAlchemy, and MySQL.

## 🐍 Python Version

This project is built with **Python 3.13.3** and uses modern Python features.

## 🚀 Features

- **User Management**: Registration, authentication, and session management
- **Company Management**: Add, edit, delete, and view companies
- **Interaction Tracking**: Log interactions with companies (calls, emails, meetings)
- **Email System**: Send emails and manage email templates
- **Modern UI**: Responsive web interface with AJAX functionality
- **RESTful API**: Well-structured API endpoints for all operations

## 📁 Project Structure

```
python_crm/
├── app/
│   ├── controllers/          # API endpoints and business logic
│   │   ├── company_controller.py
│   │   ├── user_controller.py
│   │   ├── interaction_controller.py
│   │   └── mail_controller.py
│   ├── models/              # Database models
│   │   ├── company.py
│   │   ├── user.py
│   │   ├── interaction.py
│   │   └── mail.py
│   └── views/               # Web page routes
│       └── main_views.py
├── config/                  # Configuration files
│   └── database.py
├── static/                  # CSS, JavaScript, and images
│   ├── css/
│   ├── js/
│   └── img/
├── templates/               # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── send_mail.html
│   ├── learn_python.html
│   └── see_interaction.html
├── venv/                    # Virtual environment
├── app.py                   # Main application file
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

## 🛠 Setup Instructions

### 1. Prerequisites

- Python 3.13.3 or higher
- MySQL server
- Git (optional)

### 2. Clone or Download

```bash
# If using git
git clone <repository-url>
cd python_crm

# Or extract the project files to python_crm directory
```

### 3. Set up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Database Setup

1. Create a MySQL database named `my_db`
2. Update database credentials in `.env` file:

```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=my_db
```

### 6. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and update the values:

- `DB_HOST`: Database host (default: localhost)
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name
- `SECRET_KEY`: Flask secret key for sessions
- `FLASK_DEBUG`: Enable/disable debug mode
- `PORT`: Application port (default: 5000)

## 📚 API Endpoints

### User Management
- `POST /api/user/signup` - Register new user
- `POST /api/user/login` - User login
- `POST /api/user/logout` - User logout
- `GET /api/user/profile` - Get user profile
- `GET /api/user/check-auth` - Check authentication status

### Company Management
- `GET /api/company/` - Get user's companies
- `POST /api/company/` - Create new company
- `GET /api/company/<id>` - Get specific company
- `PUT /api/company/<id>` - Update company
- `DELETE /api/company/<id>` - Delete company

### Interactions
- `GET /api/interaction/company/<id>` - Get company interactions
- `GET /api/interaction/user/<id>` - Get user interactions
- `POST /api/interaction/` - Create new interaction
- `PUT /api/interaction/<id>` - Update interaction
- `DELETE /api/interaction/<id>` - Delete interaction

### Email Management
- `GET /api/mail/templates/<user_id>` - Get email templates
- `GET /api/mail/sent/<user_id>` - Get sent emails
- `POST /api/mail/` - Create email/template
- `POST /api/mail/<id>/send` - Send email
- `PUT /api/mail/<id>` - Update email
- `DELETE /api/mail/<id>` - Delete email

## 🎨 Frontend Features

- **Responsive Design**: Works on desktop and mobile devices
- **AJAX Integration**: Dynamic content loading without page refresh
- **Modern UI**: Clean and intuitive user interface
- **Interactive Tables**: Sortable and filterable data tables
- **Modal Dialogs**: User-friendly popup forms
- **Flash Messages**: User feedback for actions

## 🔒 Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Secure user sessions
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **CSRF Protection**: Built-in Flask security features

## 🚀 Deployment

### Production Setup

1. Set `FLASK_DEBUG=False` in `.env`
2. Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. Set up a reverse proxy with Nginx
4. Use environment variables for sensitive configuration
5. Set up SSL/TLS certificates

## 🧪 Testing

To test the application:

1. Start the server: `python app.py`
2. Open `http://localhost:5000` in your browser
3. Create a new account or login
4. Test all features:
   - Add companies
   - Create interactions
   - Send emails
   - View data tables

## 🔄 Migration from PHP

This Python CRM is a complete rewrite of the original PHP CRM with the following improvements:

- **Modern Python 3.13**: Latest Python features and performance
- **Flask Framework**: Lightweight and flexible web framework
- **SQLAlchemy ORM**: Type-safe database operations
- **Better Architecture**: Clean separation of concerns
- **Enhanced Security**: Modern security practices
- **Improved UI/UX**: Better user experience and responsiveness

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review the code comments
3. Test with the provided examples
4. Create an issue with detailed information

## 🔮 Future Enhancements

- [ ] Real email sending integration
- [ ] File upload for company documents
- [ ] Advanced reporting and analytics
- [ ] Calendar integration for meetings
- [ ] Mobile app API
- [ ] Multi-language support
- [ ] Advanced user roles and permissions
- [ ] Data export/import functionality