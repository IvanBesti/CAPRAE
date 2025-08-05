import streamlit as st
import pandas as pd
import io
from enrich import enrich_companies, get_industry_stats

# Page configuration
st.set_page_config(
    page_title="Caprae Capital - Lead Enrichment Tool",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: #2c3e50;
        padding: 1rem;
        border-radius: 5px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #34495e;
        padding: 1rem;
        border-radius: 5px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    .stDataFrame {
        border-radius: 5px;
        overflow: hidden;
    }
    .filter-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header"><h1>Caprae Capital Lead Enrichment Tool</h1><p>Data Enrichment & Lead Scoring Platform</p></div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Upload & Enrich", "About"]
    )
    
    if page == "Upload & Enrich":
        upload_and_enrich_page()
    elif page == "About":
        about_page()

def upload_and_enrich_page():
    st.header("Upload & Enrich Companies")
    
    # File upload section
    st.subheader("Step 1: Upload CSV File")
    uploaded_file = st.file_uploader(
        "Choose a CSV file with company names",
        type=['csv'],
        help="The CSV should have a 'company_name' column"
    )
    
    # Sample data option
    if st.checkbox("Use sample data for testing"):
        uploaded_file = "sample_companies.csv"
        st.success("Using sample data: sample_companies.csv")
    
    if uploaded_file is not None:
        try:
            # Load data
            if isinstance(uploaded_file, str):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            
            st.success(f"Successfully loaded {len(df)} companies")
            
            # Display original data
            with st.expander("Original Data Preview"):
                st.dataframe(df.head(), use_container_width=True)
            
            # Enrichment section
            st.subheader("Step 2: Enrich Data")
            if st.button("Start Enrichment", type="primary"):
                with st.spinner("Enriching company data..."):
                    enriched_df = enrich_companies(df)
                
                st.success("Enrichment completed!")
                
                # Display metrics
                stats = get_industry_stats(enriched_df)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f'<div class="metric-card"><h3>{stats["total_companies"]}</h3><p>Total Companies</p></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="metric-card"><h3>{len(stats["industries"])}</h3><p>Industries</p></div>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<div class="metric-card"><h3>{stats["avg_high_score_companies"]}</h3><p>High Score Leads</p></div>', unsafe_allow_html=True)
                with col4:
                    high_score_pct = round((stats["avg_high_score_companies"] / stats["total_companies"]) * 100, 1)
                    st.markdown(f'<div class="metric-card"><h3>{high_score_pct}%</h3><p>High Score Rate</p></div>', unsafe_allow_html=True)
                
                # Filtering section
                st.subheader("Step 3: Filter & Analyze")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Industry filter
                    industries = ["All"] + sorted(enriched_df['industry'].unique().tolist())
                    selected_industry = st.selectbox("Filter by Industry:", industries)
                
                with col2:
                    # Lead score filter
                    scores = ["All"] + sorted(enriched_df['lead_score'].unique().tolist())
                    selected_score = st.selectbox("Filter by Lead Score:", scores)
                
                # Apply filters
                filtered_df = enriched_df.copy()
                
                if selected_industry != "All":
                    filtered_df = filtered_df[filtered_df['industry'] == selected_industry]
                
                if selected_score != "All":
                    filtered_df = filtered_df[filtered_df['lead_score'] == selected_score]
                
                # Display filtered results
                st.subheader("Enriched Results")
                st.dataframe(filtered_df, use_container_width=True)
                
                # Industry breakdown
                if selected_industry == "All":
                    st.subheader("Industry Breakdown")
                    industry_counts = enriched_df['industry'].value_counts()
                    st.bar_chart(industry_counts)
                
                # Lead score distribution
                st.subheader("Lead Score Distribution")
                score_counts = enriched_df['lead_score'].value_counts()
                st.bar_chart(score_counts)
                
                # Export section
                st.subheader("Step 4: Export Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Export filtered data
                    csv_buffer = io.StringIO()
                    filtered_df.to_csv(csv_buffer, index=False)
                    csv_data = csv_buffer.getvalue()
                    
                    st.download_button(
                        label="Download Filtered Results (CSV)",
                        data=csv_data,
                        file_name="enriched_companies_filtered.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Export all data
                    csv_buffer_all = io.StringIO()
                    enriched_df.to_csv(csv_buffer_all, index=False)
                    csv_data_all = csv_buffer_all.getvalue()
                    
                    st.download_button(
                        label="Download All Results (CSV)",
                        data=csv_data_all,
                        file_name="enriched_companies_all.csv",
                        mime="text/csv"
                    )
                
                # Detailed analysis
                with st.expander("Detailed Analysis"):
                    st.write("**Industry Analysis:**")
                    for industry, count in stats["industries"].items():
                        st.write(f"- {industry.title()}: {count} companies")
                    
                    st.write("\n**Lead Score Analysis:**")
                    for score, count in stats["lead_scores"].items():
                        percentage = round((count / stats["total_companies"]) * 100, 1)
                        st.write(f"- {score}: {count} companies ({percentage}%)")
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.info("Please ensure your CSV file has a 'company_name' column.")

def about_page():
    st.header("About This Tool")
    
    st.markdown("""
    ## Caprae Capital Lead Enrichment Tool
    
    This tool is designed for private equity lead generation and scoring. It enriches company data with:
    
    ### Enrichment Features
    - **Domain Generation**: Creates dummy domains based on company names
    - **Industry Detection**: Automatically categorizes companies by industry
    - **Employee Size Estimation**: Estimates company size based on industry patterns
    - **LinkedIn URL Generation**: Creates dummy LinkedIn company URLs
    - **Lead Scoring**: Assigns High/Medium/Low scores based on industry and size
    
    ### Lead Scoring Logic
    - **High Score**: Healthcare (0.9), Tech (0.8), Energy (0.7)
    - **Medium Score**: Finance (0.6), Manufacturing (0.6), Retail (0.5)
    - **Low Score**: Education (0.4), Other industries (0.5)
    
    ### Company Size Multipliers
    - **1-100 employees**: 0.8x multiplier
    - **100-500 employees**: 1.0x multiplier
    - **500-1000 employees**: 1.2x multiplier
    - **1000-5000 employees**: 1.5x multiplier
    - **5000+ employees**: 1.8x multiplier
    
    ### Usage
    1. Upload a CSV with a `company_name` column
    2. Click "Start Enrichment" to process the data
    3. Filter results by industry or lead score
    4. Export the enriched data to CSV
    
    **Note**: This is a prototype tool using dummy data generation for demonstration purposes.
    """)

if __name__ == "__main__":
    main() 