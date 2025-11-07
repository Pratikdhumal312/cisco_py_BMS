# Banking Management System (BMS)

A production-ready Banking Management System built with Python, featuring account management, batch processing, web scraping, and more.

## Features

- REST API for Account CRUD operations
- SQLite persistence using SQLAlchemy ORM
- Asynchronous email notifications
- Batch balance calculation using threads and asyncio
- Web scraping module for bank information
- Structured logging (JSON/text format)
- Comprehensive exception handling
- Unit tests with pytest
- PEP 8 compliant codebase

## Project Structure

```
bms/
├── app/
│   ├── __init__.py        # Flask app factory
│   ├── config.py          # Configurations
│   ├── models.py          # SQLAlchemy models
│   ├── db.py              # Database utilities
│   ├── crud.py            # CRUD operations
│   ├── routes.py          # API endpoints
│   ├── emailer.py         # Email service
│   ├── batch_calc.py      # Batch processing
│   ├── scraper.py         # Web scraping
│   ├── logger.py          # Logging setup
│   └── exceptions.py      # Custom exceptions
├── client/
│   ├── __init__.py
│   └── cli.py             # CLI client
├── tests/
│   ├── test_crud.py
│   └── test_batch_calc.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bms.git
   cd bms
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\\Scripts\\activate    # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///bms.db
   SMTP_SERVER=smtp.mailtrap.io
   SMTP_PORT=2525
   SMTP_USERNAME=your-username
   SMTP_PASSWORD=your-password
   NOTIFICATIONS_EMAIL=admin@bms.com
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python run.py
   ```

2. Use the CLI client:
   ```bash
   # Create an account
   python client/cli.py create --name "John Doe" --number "123456" --balance 1000.0

   # List all accounts
   python client/cli.py list

   # Get account details
   python client/cli.py get --id 1

   # Delete an account
   python client/cli.py delete --id 1
   ```

## Running Tests

```bash
pytest tests/
```

For test coverage report:
```bash
pytest --cov=app tests/
```

## API Endpoints

- `POST /api/accounts` - Create new account
- `GET /api/accounts` - List all accounts
- `GET /api/accounts/{id}` - Get account by ID
- `GET /api/accounts/number/{number}` - Get account by number
- `PUT /api/accounts/{id}` - Update account
- `DELETE /api/accounts/{id}` - Delete account
- `GET /api/health` - Health check

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.