# Quick Setup Guide

## Prerequisites
- Python 3.10+ installed
- pip package manager

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

**Required Packages**:
- Django 5.1.4
- pandas 2.2.0
- numpy 1.26.3
- matplotlib 3.8.2
- seaborn 0.13.1
- Pillow 10.2.0

### 2. Run Database Migrations
```bash
python manage.py migrate
```

This will create the necessary database tables.

### 3. Create Admin User (Optional)
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 4. Run Development Server
```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## Usage

### Upload Data
1. Navigate to http://127.0.0.1:8000/
2. Click "Start Upload"
3. Select a CSV file
4. Preview your data

### View Statistics
1. After uploading, click "Statistics" in the navigation
2. View descriptive statistics
3. Analyze specific columns or rows
4. Check correlation matrix and missing values

### Create Visualizations
1. Click "Visualization" in the navigation
2. Select chart type:
   - **Histogram**: Distribution of a single numeric column
   - **Boxplot**: Box plot for numeric columns
   - **Scatter**: Relationship between two numeric columns
   - **Bar**: Frequency of categorical data
   - **Pie**: Proportion of categorical data
   - **Pairplot**: Relationships between all numeric columns
   - **Heatmap**: Correlation heatmap
3. Select required columns
4. Click "Generate Plot"

## Troubleshooting

### Issue: Module not found
**Solution**: Make sure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Run migrations
```bash
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Collect static files
```bash
python manage.py collectstatic
```

### Issue: Port already in use
**Solution**: Use a different port
```bash
python manage.py runserver 8080
```

## File Structure
```
Data_Analysis_App/
├── data_an_project/      # Django project settings
│   ├── settings.py       # Configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI config
├── py_project/          # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View logic
│   ├── forms.py         # Forms
│   ├── templates/       # HTML templates
│   └── migrations/      # Database migrations
├── media/               # Uploaded files
│   ├── uploads/         # CSV files
│   └── plots/           # Generated plots
├── manage.py            # Django management script
├── db.sqlite3           # SQLite database
└── requirements.txt     # Python dependencies
```

## Next Steps
1. Upload a sample CSV file
2. Explore the statistics features
3. Generate various visualizations
4. Check the ANALYSIS_REPORT.md for detailed information

## Support
For issues or questions, refer to:
- ANALYSIS_REPORT.md - Comprehensive analysis
- README.md - Project overview
- Django documentation: https://docs.djangoproject.com/
