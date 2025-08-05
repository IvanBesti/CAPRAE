# Caprae Capital Lead Enrichment Tool

A lightweight data enrichment and lead scoring tool built with Streamlit for private equity lead generation.

## Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone or download the project files**
   ```bash
   # Ensure you have all these files in your directory:
   # - app.py
   # - enrich.py
   # - sample_companies.csv
   # - README.md
   ```

2. **Install required packages**
   ```bash
   pip install streamlit pandas
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL shown in your terminal

## Features

### Core Functionality
- **CSV Upload**: Upload company data with a `company_name` column
- **Data Enrichment**: Automatically adds domain, industry, employee size, LinkedIn URL, and lead score
- **Smart Filtering**: Filter results by industry or lead score
- **Export Options**: Download filtered or complete results as CSV
- **Sample Data**: Built-in sample data for testing

### Enrichment Logic
- **Industry Detection**: Based on company name keywords
- **Domain Generation**: Creates dummy domains with common extensions
- **Employee Size Estimation**: Industry-specific size ranges
- **LinkedIn URL Generation**: Dummy URLs based on company names
- **Lead Scoring**: High/Medium/Low based on industry and company size

### Lead Scoring Algorithm
| Industry | Base Weight | Typical Score |
|----------|-------------|---------------|
| Healthcare | 0.9 | High |
| Technology | 0.8 | High |
| Energy | 0.7 | High |
| Finance | 0.6 | Medium |
| Manufacturing | 0.6 | Medium |
| Retail | 0.5 | Medium |
| Education | 0.4 | Low |

## File Structure

```
├── app.py                 # Main Streamlit application
├── enrich.py              # Enrichment and scoring logic
├── sample_companies.csv   # Sample input data
├── README.md             # This file
└── report.md             # Technical approach summary
```

## Usage Guide

### Step 1: Upload Data
- Use the file uploader to select your CSV file
- Or check "Use sample data for testing" to try with built-in data
- Ensure your CSV has a `company_name` column

### Step 2: Enrich Data
- Click "Start Enrichment" to process your data
- View real-time metrics and statistics
- Monitor the enrichment progress

### Step 3: Filter & Analyze
- Filter by industry or lead score using the dropdown menus
- View industry breakdown charts
- Analyze lead score distribution

### Step 4: Export Results
- Download filtered results (CSV)
- Download complete enriched dataset (CSV)
- View detailed analysis in expandable sections

## Customization

### Adding New Industries
Edit `enrich.py` and add to `INDUSTRY_KEYWORDS`:
```python
'new_industry': ['keyword1', 'keyword2', 'keyword3']
```

### Modifying Lead Scoring
Adjust weights in `LEAD_SCORE_WEIGHTS`:
```python
'new_industry': 0.7  # 0.0 to 1.0 scale
```

### Changing Employee Size Ranges
Update `EMPLOYEE_RANGES` for industry-specific sizing:
```python
'new_industry': [(min1, max1), (min2, max2), (min3, max3)]
```

## Sample Output

The tool enriches data with these additional columns:

| Column | Description | Example |
|--------|-------------|---------|
| company_name | Original company name | TechFlow Solutions |
| domain | Generated domain | techflowsolutions.com |
| industry | Detected industry | tech |
| employee_size | Estimated size range | 100-500 |
| linkedin_url | Generated LinkedIn URL | https://linkedin.com/company/techflow-solutions |
| lead_score | Calculated score | High |

## Troubleshooting

### Common Issues

1. **"No module named 'streamlit'"**
   ```bash
   pip install streamlit
   ```

2. **CSV upload error**
   - Ensure your CSV has a `company_name` column
   - Check file format (should be UTF-8 encoded)

3. **Port already in use**
   ```bash
   streamlit run app.py --server.port 8502
   ```

### Performance Tips
- For large datasets (>1000 companies), processing may take a few seconds
- Use the sample data first to test functionality
- Export results in chunks if working with very large datasets

## Requirements

### Python Packages
```
streamlit>=1.28.0
pandas>=1.5.0
```

### System Requirements
- Python 3.7 or higher
- 4GB RAM (for large datasets)
- Modern web browser

## For Caprae Capital Internship

This tool demonstrates:
- **Data Processing**: Efficient CSV handling and enrichment
- **Business Logic**: Industry-specific lead scoring algorithms
- **User Interface**: Intuitive Streamlit-based web application
- **Export Functionality**: Professional data export capabilities
- **Modular Design**: Clean, maintainable code structure

The prototype showcases key skills in data science, web development, and business intelligence - perfect for private equity applications.

## Support

For technical issues or questions about the implementation, refer to the code comments in `enrich.py` and `app.py` for detailed explanations of the algorithms and logic. 