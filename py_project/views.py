import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FileUploadForm
from .models import UploadedFile
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from django.conf import settings
from django.http import JsonResponse
import random
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import base64

def home(request):
    return render(request, 'home.html')

def upload_view(request):
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.FILES:
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    uploaded_file = form.save()
                    data = pd.read_csv(uploaded_file.file.path)
                    
                    # Store data in session as records
                    request.session['data'] = json.loads(data.to_json(orient='records'))
                    request.session['columns'] = data.columns.tolist()
                    
                    preview_data = data.head(10)
                    # Include index in the HTML table
                    preview_rows = preview_data.to_html(
                        classes='table table-striped',
                        index=True,
                        index_names=False,
                        border=0
                    )
                    
                    return render(request, 'upload.html', {
                        'form': form,
                        'preview': preview_rows,
                        'columns': data.columns.tolist(),
                        'total_rows': len(data)
                    })
                except Exception as e:
                    messages.error(request, f'Error processing file: {str(e)}')
                    return render(request, 'upload.html', {'form': form})
        
        # Handle AJAX data filtering requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                stored_data = request.session.get('data', [])
                stored_columns = request.session.get('columns', [])
                
                if not stored_data:
                    return JsonResponse({'error': 'No data available'}, status=400)
                
                data = pd.DataFrame(stored_data)
                
                # Get filter parameters
                start_row = int(request.POST.get('start_row', 0))
                num_rows = int(request.POST.get('num_rows', 10))
                specific_row = request.POST.get('specific_row')
                selected_columns = request.POST.getlist('columns[]', [])  # Default to empty list
                
                # Validate columns
                valid_columns = [col for col in selected_columns if col in stored_columns]
                
                # Filter data
                if specific_row is not None and specific_row.isdigit():
                    row_idx = int(specific_row)
                    if 0 <= row_idx < len(data):
                        filtered_data = data.iloc[[row_idx]]
                    else:
                        return JsonResponse({'error': 'Row index out of range'}, status=400)
                else:
                    filtered_data = data.iloc[start_row:start_row + num_rows]
                
                # Select columns if any are specified
                if valid_columns:
                    filtered_data = filtered_data[valid_columns]
                
                # Convert to HTML with index
                table_html = filtered_data.to_html(
                    classes='table table-striped',
                    index=True,
                    index_names=False,
                    border=0
                )
                
                return JsonResponse({
                    'data': table_html,
                    'total_rows': len(data)
                })
                
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    
    else:
        form = FileUploadForm()
    
    return render(request, 'upload.html', {'form': form})

import json
from django.http import JsonResponse
def statistics_view(request):
    """
    View function for generating statistical analysis of the uploaded dataset.
    Handles both initial page load and AJAX requests for specific analyses.
    """
    # Check if data exists in session
    if 'data' not in request.session:
        messages.warning(request, 'Please upload a dataset first')
        return redirect('upload')
    
    try:
        # Load the dataset
        full_data = pd.DataFrame(request.session['data'])
        
        # Separate numeric and categorical columns
        numeric_data = full_data.select_dtypes(include=['float64', 'int64'])
        categorical_data = full_data.select_dtypes(include=['object'])
        
        numeric_columns = numeric_data.columns.tolist()
        categorical_columns = categorical_data.columns.tolist()
        
        # Handle POST requests for dynamic analysis
        if request.method == 'POST':
            try:
                return handle_post_request(request, full_data)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        
        # Initial page load - calculate default statistics
        stats = calculate_initial_statistics(full_data, numeric_data, categorical_data)
        
        # Prepare context for template
        context = {
            **stats,
            'numeric_columns': numeric_columns,
            'categorical_columns': categorical_columns
        }
        
        return render(request, 'statistics.html', context)
        
    except Exception as e:
        messages.error(request, f'Error processing data: {str(e)}')
        return redirect('upload')

def calculate_initial_statistics(full_data, numeric_data, categorical_data):
    """
    Calculate initial statistics for the full dataset.
    """
    stats = {
        'numerical': get_numerical_stats(numeric_data),
        'categorical': get_categorical_stats(categorical_data),
        'correlation': get_correlation_stats(numeric_data),
        'missing_values': get_missing_values_stats(full_data)
    }
    return stats

def handle_post_request(request, full_data):
    """
    Handle POST requests for specific analyses.
    """
    data = json.loads(request.body)
    action = data.get('action')
    
    if action == 'analyze_columns':
        return analyze_columns(data, full_data)
    elif action == 'analyze_rows':
        return analyze_rows(data, full_data)
    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)

def analyze_columns(data, full_data):
    """
    Analyze specific columns of the dataset.
    """
    selected_columns = data.get('columns', [])
    if not selected_columns:
        return JsonResponse({
            'error': 'Please select at least one column'
        }, status=400)
    
    
    # Filter data for selected columns
    selected_data = full_data[selected_columns]
    
    # Separate numeric and categorical data
    numeric_data = selected_data.select_dtypes(include=['float64', 'int64'])
    categorical_data = selected_data.select_dtypes(include=['object'])
    
    return JsonResponse({
        'numerical': get_numerical_stats(numeric_data),
        'categorical': get_categorical_stats(categorical_data),
        'missing_values': get_missing_values_stats(selected_data)
    })

def analyze_rows(data, full_data):
    """
    Analyze specific rows of the dataset.
    """
    row_range = data.get('row_range', 'all')
    
    # Select rows based on range
    if row_range == 'first_10':
        selected_data = full_data.head(10)
    elif row_range == 'last_10':
        selected_data = full_data.tail(10)
    else:  # 'all'
        selected_data = full_data
    
    # Separate numeric and categorical data
    numeric_data = selected_data.select_dtypes(include=['float64', 'int64'])
    categorical_data = selected_data.select_dtypes(include=['object'])
    
    return JsonResponse({
        'numerical': get_numerical_stats(numeric_data),
        'categorical': get_categorical_stats(categorical_data),
        'missing_values': get_missing_values_stats(selected_data)
    })

def get_numerical_stats(data):
    """
    Generate HTML table with numerical statistics.
    """
    if data.empty:
        return '<p>No numerical columns to analyze</p>'
    return data.describe().round(2).to_html(
        classes='table table-striped table-hover',
        border=0
    )

def get_categorical_stats(data):
    """
    Generate HTML table with categorical statistics.
    """
    if data.empty:
        return '<p>No categorical columns to analyze</p>'
    return data.describe().to_html(
        classes='table table-striped table-hover',
        border=0
    )

def get_correlation_stats(data):
    """
    Generate HTML table with correlation statistics.
    """
    if data.empty:
        return '<p>No numerical columns to analyze correlations</p>'
    return data.corr().round(2).to_html(
        classes='table table-striped table-hover',
        border=0
    )

def get_missing_values_stats(data):
    """
    Generate HTML table with missing values statistics.
    """
    return data.isnull().sum().to_frame('Missing Values').to_html(
        classes='table table-striped table-hover',
        border=0
    )

def visualization_view(request):
    if 'data' not in request.session:
        messages.warning(request, 'Please upload a dataset first')
        return redirect('upload')

    data = pd.DataFrame(request.session.get('data'))
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_columns = data.select_dtypes(include=['object']).columns.tolist()

    NUMERIC_PLOTS = ['histogram', 'boxplot', 'scatter']
    CATEGORICAL_PLOTS = ['bar', 'pie'] 
    AUTO_PLOTS = ['pairplot', 'heatmap']

    if request.method == 'POST':
        plot_type = request.POST.get('plot_type')
        columns = request.POST.getlist('columns')

        if plot_type not in AUTO_PLOTS and not columns:
            return JsonResponse({'error': 'Please select columns'}, status=400)

        try:
            sns.set_theme(style="whitegrid", palette="deep")
            buffer = BytesIO()

            if plot_type in AUTO_PLOTS:
                if plot_type == 'pairplot':
                    sns_plot = sns.pairplot(data[numeric_columns], diag_kind='kde')
                    sns_plot.fig.savefig(buffer, format='png', bbox_inches='tight')
                elif plot_type == 'heatmap':
                    plt.figure(figsize=(12, 8))
                    corr = data[numeric_columns].corr()
                    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
                    plt.title('Correlation Heatmap')
                    plt.tight_layout()
                    plt.savefig(buffer, format='png', bbox_inches='tight')
            else:
                plt.figure(figsize=(12, 8))

                if plot_type == 'scatter':
                    if len(columns) != 2:
                        return JsonResponse({'error': 'Scatter plot requires exactly 2 columns'}, status=400)
                    sns.scatterplot(data=data, x=columns[0], y=columns[1])
                    plt.title(f'{columns[0]} vs {columns[1]}')

                elif plot_type == 'histogram':
                    if len(columns) != 1:
                        return JsonResponse({'error': 'Histogram requires exactly 1 column'}, status=400)
                    sns.histplot(data=data[columns[0]], kde=True, bins=30)
                    plt.title(f'Distribution of {columns[0]}')

                elif plot_type == 'boxplot':
                    sns.boxplot(data=data[columns])
                    plt.title('Box Plot')
                    plt.xticks(rotation=45)

                elif plot_type == 'bar':
                    if len(columns) != 1:
                        return JsonResponse({'error': 'Bar plot requires exactly 1 column'}, status=400)
                    value_counts = data[columns[0]].value_counts()
                    sns.barplot(x=value_counts.index, y=value_counts.values)
                    plt.title(f'Bar Plot of {columns[0]}')
                    plt.xticks(rotation=45)

                elif plot_type == 'pie':
                    if len(columns) != 1:
                        return JsonResponse({'error': 'Pie chart requires exactly 1 column'}, status=400)
                    value_counts = data[columns[0]].value_counts()
                    plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%')
                    plt.title(f'Pie Chart of {columns[0]}')

                plt.tight_layout()
                plt.savefig(buffer, format='png', bbox_inches='tight')

            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            plt.close('all')

            # Encode image to base64
            image_base64 = base64.b64encode(image_png).decode('utf-8')

            return JsonResponse({
                'success': True,
                'plot_base64': image_base64
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'visualization.html', {
        'numeric_columns': numeric_columns,
        'categorical_columns': categorical_columns,
        'numeric_plots': NUMERIC_PLOTS,
        'categorical_plots': CATEGORICAL_PLOTS,
        'auto_plots': AUTO_PLOTS
    })