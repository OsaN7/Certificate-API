# Certificate Issuing Service

A FastAPI-based service for generating certificates from PDF templates and CSV data, with PostgreSQL database support.

## Features

- **Folder Upload API**: Upload ZIP files containing certificate templates and CSV data
- **Certificate Generation**: Automatically generate certificates from uploaded templates
- **PostgreSQL Database**: Store upload history and certificate metadata
- **RESTful API**: Complete API for managing certificate generation
- **Status Tracking**: Track the status of certificate generation jobs

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pgAdmin 4 (for database management)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd certificate-issuing-service
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL Database**
   ```bash
   # Create database
   createdb certificate_service
   
   # Or using psql
   psql -U postgres
   CREATE DATABASE certificate_service;
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   # Database Configuration
   DATABASE_URL=postgresql://username:password@localhost:5432/certificate_service
   
   # Logging
   LOG_LEVEL=INFO
   
   # Email Configuration (Optional)
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password
   RECIPIENT_EMAILS=recipient1@example.com,recipient2@example.com
   ENABLE_EMAIL_SERVICE=False
   ```

## Running the Application

1. **Start the API server**
   ```bash
   uvicorn api_main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Folder Upload Endpoints

- `POST /folder-uploads/upload` - Upload a folder containing certificate template and CSV data
- `GET /folder-uploads/{upload_id}` - Get upload details by ID
- `GET /folder-uploads/{upload_id}/status` - Get upload status only
- `GET /folder-uploads/` - List all uploads
- `DELETE /folder-uploads/{upload_id}` - Delete an upload

### Certificate Endpoints

- `GET /certificates/{certificate_id}` - Get certificate by ID
- `GET /certificates/` - List all certificates

### User Endpoints

- User management endpoints (from existing user_routes.py)

## Folder Upload Format

The ZIP file should contain the following structure:

```
your-folder-name/
├── Template/
│   └── certificate-template.pdf
└── csv/
    └── participant-data.csv
```

### CSV File Requirements

The CSV file must contain at least these columns:
- `name` - Participant's name
- `email` - Participant's email address

Example CSV format:
```csv
name,email,additional_field
John Doe,john@example.com,value1
Jane Smith,jane@example.com,value2
```

## Database Schema

The application creates the following tables:

- `folder_uploads` - Stores upload history and metadata
- `template` - Stores certificate templates
- `user_record` - User information (from existing schema)

## Development

### Project Structure

```
certificate-issuing-service/
├── api_main.py                 # FastAPI application entry point
├── main.py                     # Command-line certificate generation
├── requirements.txt            # Python dependencies
├── certificateservice/         # Main application package
│   ├── api/                    # API layer
│   │   └── Routers/           # API route definitions
│   ├── domain/                # Domain models and schemas
│   ├── model/                 # Database models
│   ├── repo/                  # Data access layer
│   ├── service/               # Business logic layer
│   ├── utils/                 # Utility functions
│   └── settings.py            # Configuration
├── data/                      # Data storage
│   ├── certificates/          # Generated certificates
│   ├── templates/             # Certificate templates
│   └── csv/                   # CSV data files
└── resources/                 # Static resources
    └── fonts/                 # Font files
```

### Adding New Features

1. **Database Models**: Add new models in `certificateservice/model/`
2. **Domain Schemas**: Add Pydantic schemas in `certificateservice/domain/`
3. **Repository Layer**: Add data access logic in `certificateservice/repo/`
4. **Service Layer**: Add business logic in `certificateservice/service/`
5. **API Routes**: Add endpoints in `certificateservice/api/Routers/`

## Testing

To test the API:

1. **Start the server**
   ```bash
   uvicorn api_main:app --reload
   ```

2. **Use the Swagger UI**
   - Go to http://localhost:8000/docs
   - Test the endpoints interactively

3. **Test folder upload**
   - Create a ZIP file with the required structure
   - Use the `/folder-uploads/upload` endpoint
   - Monitor the status using `/folder-uploads/{upload_id}/status`

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check your `DATABASE_URL` in `.env`
   - Ensure PostgreSQL is running
   - Verify database exists

2. **File Upload Errors**
   - Ensure ZIP file has correct structure
   - Check file permissions
   - Verify CSV format

3. **Certificate Generation Errors**
   - Check PDF template format
   - Verify CSV column names
   - Check font file paths

## License

[Add your license information here] 