import pandas as pd
import re
import random
from typing import Dict, List

# Industry mapping based on company name keywords
INDUSTRY_KEYWORDS = {
    'tech': ['tech', 'software', 'data', 'cloud', 'digital', 'ai', 'analytics', 'platform'],
    'energy': ['energy', 'green', 'solar', 'wind', 'renewable', 'power'],
    'healthcare': ['health', 'bio', 'medical', 'pharma', 'care'],
    'finance': ['fin', 'bank', 'capital', 'investment', 'financial'],
    'retail': ['retail', 'ecommerce', 'shop', 'store', 'commerce'],
    'education': ['edu', 'learn', 'school', 'academy', 'training'],
    'manufacturing': ['manufacturing', 'factory', 'industrial', 'production', 'plus']
}

# Employee size ranges for different company types
EMPLOYEE_RANGES = {
    'tech': [(10, 500), (50, 1000), (200, 5000)],
    'energy': [(50, 1000), (200, 5000), (1000, 10000)],
    'healthcare': [(20, 200), (100, 1000), (500, 5000)],
    'finance': [(50, 500), (200, 2000), (1000, 10000)],
    'retail': [(100, 1000), (500, 5000), (2000, 20000)],
    'education': [(10, 100), (50, 500), (200, 2000)],
    'manufacturing': [(100, 1000), (500, 5000), (2000, 20000)]
}

# Lead score weights by industry
LEAD_SCORE_WEIGHTS = {
    'tech': 0.8,
    'energy': 0.7,
    'healthcare': 0.9,
    'finance': 0.6,
    'retail': 0.5,
    'education': 0.4,
    'manufacturing': 0.6
}

def detect_industry(company_name: str) -> str:
    """
    Detect industry based on company name keywords.
    Returns 'other' if no match found.
    """
    company_lower = company_name.lower()
    
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in company_lower:
                return industry
    
    return 'other'

def generate_domain(company_name: str) -> str:
    """
    Generate a dummy domain based on company name.
    """
    # Clean company name for domain
    clean_name = re.sub(r'[^\w\s]', '', company_name)
    clean_name = clean_name.replace(' ', '').lower()
    
    # Add common domain extensions
    extensions = ['.com', '.net', '.org', '.io']
    return f"{clean_name}{random.choice(extensions)}"

def estimate_employee_size(company_name: str, industry: str) -> str:
    """
    Estimate employee size based on industry and company characteristics.
    """
    if industry == 'other':
        # Default ranges for unknown industries
        ranges = [(10, 500), (50, 1000), (200, 5000)]
    else:
        ranges = EMPLOYEE_RANGES.get(industry, [(10, 500), (50, 1000), (200, 5000)])
    
    # Choose a range based on company name length (simple heuristic)
    name_length = len(company_name)
    if name_length < 15:
        range_idx = 0  # Small company
    elif name_length < 25:
        range_idx = 1  # Medium company
    else:
        range_idx = 2  # Large company
    
    min_size, max_size = ranges[range_idx]
    size = random.randint(min_size, max_size)
    
    # Format size ranges
    if size < 100:
        return "1-100"
    elif size < 500:
        return "100-500"
    elif size < 1000:
        return "500-1000"
    elif size < 5000:
        return "1000-5000"
    else:
        return "5000+"

def generate_linkedin_url(company_name: str) -> str:
    """
    Generate a dummy LinkedIn URL based on company name.
    """
    clean_name = re.sub(r'[^\w\s]', '', company_name)
    clean_name = clean_name.replace(' ', '-').lower()
    return f"https://linkedin.com/company/{clean_name}"

def calculate_lead_score(industry: str, employee_size: str) -> str:
    """
    Calculate lead score based on industry and company size.
    """
    base_weight = LEAD_SCORE_WEIGHTS.get(industry, 0.5)
    
    # Size multiplier
    size_multipliers = {
        "1-100": 0.8,
        "100-500": 1.0,
        "500-1000": 1.2,
        "1000-5000": 1.5,
        "5000+": 1.8
    }
    size_multiplier = size_multipliers.get(employee_size, 1.0)
    
    # Calculate final score
    final_score = base_weight * size_multiplier
    
    # Add some randomness
    final_score += random.uniform(-0.1, 0.1)
    final_score = max(0, min(1, final_score))  # Clamp between 0 and 1
    
    # Convert to High/Medium/Low
    if final_score >= 0.7:
        return "High"
    elif final_score >= 0.4:
        return "Medium"
    else:
        return "Low"

def enrich_companies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich company data with additional fields.
    """
    enriched_data = []
    
    for _, row in df.iterrows():
        company_name = row['company_name']
        
        # Detect industry
        industry = detect_industry(company_name)
        
        # Generate domain
        domain = generate_domain(company_name)
        
        # Estimate employee size
        employee_size = estimate_employee_size(company_name, industry)
        
        # Generate LinkedIn URL
        linkedin_url = generate_linkedin_url(company_name)
        
        # Calculate lead score
        lead_score = calculate_lead_score(industry, employee_size)
        
        enriched_data.append({
            'company_name': company_name,
            'domain': domain,
            'industry': industry,
            'employee_size': employee_size,
            'linkedin_url': linkedin_url,
            'lead_score': lead_score
        })
    
    return pd.DataFrame(enriched_data)

def get_industry_stats(df: pd.DataFrame) -> Dict:
    """
    Get statistics about industries and lead scores.
    """
    stats = {
        'total_companies': len(df),
        'industries': df['industry'].value_counts().to_dict(),
        'lead_scores': df['lead_score'].value_counts().to_dict(),
        'avg_high_score_companies': len(df[df['lead_score'] == 'High'])
    }
    return stats 