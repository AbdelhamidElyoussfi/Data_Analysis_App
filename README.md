# Data Analysis Application

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Django](https://img.shields.io/badge/django-latest-green)

A Django-based web application for data analysis and visualization, providing an intuitive interface for users to upload, analyze, and visualize their datasets.

## Project Structure
```
data_analysis_app/
├── data_an_project/        # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                  # Media files storage
│   ├── plots/             # Generated visualization plots
│   └── uploads/           # Uploaded datasets
├── py_project/            # Main Django application
│   ├── migrations/        # Database migrations
│   ├── templates/         # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── statistics.html
│   │   ├── upload.html
│   │   └── visualization.html
│   ├── __init__.py
│   ├── admin.py          # Admin interface configuration
│   ├── apps.py           # App configuration
│   ├── forms.py          # Form definitions
│   ├── models.py         # Database models
│   ├── tests.py          # Unit tests
│   ├── urls.py           # URL routing
│   └── views.py          # View logic
└── requirements.txt       # Project dependencies
```

## Features
- **Dataset Management**
  - Upload and store datasets
  - Preview data contents
  - Basic data cleaning options

- **Statistical Analysis**
  - Descriptive statistics
  - Data distribution analysis
  - Correlation analysis

- **Data Visualization**
  - Various chart types (line, bar, scatter, etc.)
  - Customizable plot parameters
  - Export visualization as images

## Technology Stack
- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Database:** SQLite (default) / PostgreSQL (optional)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AbdelhamidElyoussfi/Data_Analysis_App.git
cd data_analysis_app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage
1. Log in to the application
2. Upload your dataset (CSV format supported)
3. Navigate through the available options:
   - View basic statistics
   - Generate visualizations
   - Export results

## Development

### Running Tests
```bash
python manage.py test
```

### Making Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
- Email: abdelhamidelyoussfii@gamil.com 
- GitHub: AbdelhamiElyoussfi