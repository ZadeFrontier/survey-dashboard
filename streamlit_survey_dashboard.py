import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Trademark Awareness Survey Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Trademark Awareness Survey - Vijayawada Traders")
st.markdown("### Comprehensive Analysis of Trademark Knowledge among Local Businesses")

# File uploader
st.sidebar.header("📤 Upload Survey Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=['csv'])

# Load data
@st.cache_data
def load_data(file):
    if file is not None:
        df = pd.read_csv(file)
    else:
        # Load default file if no upload - use relative path for cloud deployment
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        default_csv = os.path.join(current_dir, 'ravi_survey.csv')
        df = pd.read_csv(default_csv)

    # Clean column names
    df.columns = df.columns.str.strip()
    # Convert all string data to uppercase (not column names)
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.upper()
    return df

df = load_data(uploaded_file)

# Display dataset info
st.sidebar.header("Dataset Information")
st.sidebar.write(f"Total Responses: {len(df)}")
st.sidebar.write(f"Total Questions: {len(df.columns)}")

if uploaded_file is not None:
    st.sidebar.success(f"✅ File uploaded: {uploaded_file.name}")
else:
    st.sidebar.info("ℹ️ Using default CSV file")

# Show raw data option
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader("Raw Survey Data")
    st.dataframe(df)

# Data cleaning - remove NA entries where appropriate
df_clean = df.copy()

# Create tabs for different chart categories
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Demographics", 
    "🏢 Business Profile", 
    "⚖️ Trademark Awareness", 
    "📋 Registration Status",
    "💡 Opinions & Attitudes",
    "🔍 Deep Dive Analysis"
])

# ==================== TAB 1: DEMOGRAPHICS ====================
with tab1:
    st.header("Demographic Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender Distribution - Pie Chart
        st.subheader("Gender Distribution")
        gender_counts = df_clean['Gender'].value_counts()
        fig_gender_pie = px.pie(
            values=gender_counts.values, 
            names=gender_counts.index,
            title="Survey Respondents by Gender",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_gender_pie, use_container_width=True)
        
    with col2:
        # Gender Distribution - Bar Chart
        st.subheader("Gender Count")
        fig_gender_bar = px.bar(
            df_clean['Gender'].value_counts().reset_index(),
            x='Gender', 
            y='count',
            title="Gender Distribution (Bar Chart)",
            color='Gender',
            text='count'
        )
        fig_gender_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_gender_bar, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Age Group Distribution
        st.subheader("Age Group Distribution")
        age_counts = df_clean['Age Group'].value_counts()
        fig_age = px.bar(
            age_counts.reset_index(),
            x='Age Group',
            y='count',
            title="Respondents by Age Group",
            color='Age Group',
            text='count'
        )
        fig_age.update_traces(textposition='outside')
        st.plotly_chart(fig_age, use_container_width=True)
        
    with col4:
        # Age Group - Donut Chart
        st.subheader("Age Group Split")
        fig_age_donut = px.pie(
            values=age_counts.values,
            names=age_counts.index,
            title="Age Group Distribution (Donut)",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_age_donut, use_container_width=True)

# ==================== TAB 2: BUSINESS PROFILE ====================
with tab2:
    st.header("Business Profile Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Business Type Distribution
        st.subheader("Business Types")
        business_counts = df_clean['Business Type / Trade'].value_counts()
        fig_business = px.bar(
            business_counts.reset_index(),
            x='count',
            y='Business Type / Trade',
            orientation='h',
            title="Distribution of Business Types",
            color='count',
            text='count'
        )
        fig_business.update_traces(textposition='outside')
        st.plotly_chart(fig_business, use_container_width=True)
        
    with col2:
        # Location Distribution
        st.subheader("Location Distribution")
        location_counts = df_clean['Location (Area in Vijayawada)'].value_counts()
        fig_location = px.bar(
            location_counts.reset_index(),
            x='count',
            y='Location (Area in Vijayawada)',
            orientation='h',
            title="Respondents by Location",
            color='count',
            text='count',
            color_continuous_scale='Blues'
        )
        fig_location.update_traces(textposition='outside')
        st.plotly_chart(fig_location, use_container_width=True)
    
    # Years in Business
    st.subheader("Business Experience")
    years_counts = df_clean['Number of years in business'].value_counts()
    fig_years = px.histogram(
        df_clean,
        x='Number of years in business',
        title="Distribution of Years in Business",
        color='Number of years in business',
        text_auto=True
    )
    st.plotly_chart(fig_years, use_container_width=True)
    
    # Treemap: Business Type by Experience
    st.subheader("Business Type & Experience (Treemap)")
    fig_treemap = px.treemap(
        df_clean,
        path=['Business Type / Trade', 'Number of years in business'],
        title="Business Type by Years of Experience"
    )
    st.plotly_chart(fig_treemap, use_container_width=True)
    
    # Sunburst: Gender → Business Type → Experience
    st.subheader("Multi-dimensional View: Gender → Business → Experience")
    # Clean data for sunburst - remove rows with any NaN in the path columns
    df_sunburst = df_clean[['Gender', 'Business Type / Trade', 'Number of years in business']].dropna()
    if not df_sunburst.empty:
        fig_sunburst = px.sunburst(
            df_sunburst,
            path=['Gender', 'Business Type / Trade', 'Number of years in business'],
            title="Hierarchical View of Demographics and Business"
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)
    else:
        st.warning("No complete data available for sunburst chart")

# ==================== TAB 3: TRADEMARK AWARENESS ====================
with tab3:
    st.header("Trademark Awareness & Knowledge")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Heard of Trademark
        st.subheader("Trademark Term Awareness")
        heard_counts = df_clean['Have you heard of the term Trademark?'].value_counts()
        fig_heard = px.pie(
            values=heard_counts.values,
            names=heard_counts.index,
            title='Have you heard of Trademark?',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_heard, use_container_width=True)
        
    with col2:
        # Knowledge of Legal Protection
        st.subheader("Legal Protection Awareness")
        protection_counts = df_clean['Do you know that registering a trademark gives legal protection to your brand name or logo?'].value_counts()
        fig_protection = px.pie(
            values=protection_counts.values,
            names=protection_counts.index,
            title="Knowledge of Legal Protection",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_protection, use_container_width=True)
    
    # Trademark Protection Belief
    st.subheader("Belief in Trademark Protection")
    belief_counts = df_clean['Do you think trademark registration helps protect your business identity?'].value_counts()
    fig_belief = px.bar(
        belief_counts.reset_index(),
        x='Do you think trademark registration helps protect your business identity?',
        y='count',
        title="Do you think trademark registration protects business identity?",
        color='count',
        text='count'
    )
    fig_belief.update_traces(textposition='outside')
    st.plotly_chart(fig_belief, use_container_width=True)
    
    # Law Enforcement Opinion
    st.subheader("Law Enforcement Opinion")
    enforcement_counts = df_clean['Do you believe trademark law is adequately enforced in India?'].value_counts()
    fig_enforcement = px.bar(
        enforcement_counts.reset_index(),
        x='Do you believe trademark law is adequately enforced in India?',
        y='count',
        title="Is trademark law adequately enforced in India?",
        color='count',
        text='count',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_enforcement.update_traces(textposition='outside')
    st.plotly_chart(fig_enforcement, use_container_width=True)

# ==================== TAB 4: REGISTRATION STATUS ====================
with tab4:
    st.header("Trademark Registration Status & Barriers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Registration Status
        st.subheader("Registration Status")
        registered_counts = df_clean['Have you ever registered a trademark for your business?'].value_counts()
        fig_registered = px.pie(
            values=registered_counts.values,
            names=registered_counts.index,
            title="Trademark Registration Status",
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_registered, use_container_width=True)
        
    with col2:
        # Willingness to Register
        st.subheader("Willingness to Register")
        willingness_counts = df_clean['Would you be willing to register your business trademark if you get proper guidance?'].value_counts()
        fig_willingness = px.bar(
            willingness_counts.reset_index(),
            x='Would you be willing to register your business trademark if you get proper guidance?',
            y='count',
            title="Willingness to Register with Guidance",
            color='count',
            text='count'
        )
        fig_willingness.update_traces(textposition='outside')
        st.plotly_chart(fig_willingness, use_container_width=True)
    
    # Reasons for Not Registering
    st.subheader("Barriers to Registration")
    reasons_counts = df_clean['If No; what is the main reason for not registering?'].value_counts()
    fig_reasons = px.bar(
        reasons_counts.reset_index(),
        x='count',
        y='If No; what is the main reason for not registering?',
        orientation='h',
        title="Main Reasons for Not Registering Trademark",
        color='count',
        text='count',
        color_continuous_scale='Reds'
    )
    fig_reasons.update_traces(textposition='outside')
    st.plotly_chart(fig_reasons, use_container_width=True)
    
    # Registration by Business Type
    st.subheader("Registration Status by Business Type")
    reg_business = pd.crosstab(
        df_clean['Business Type / Trade'],
        df_clean['Have you ever registered a trademark for your business?']
    )
    fig_reg_business = px.bar(
        reg_business.reset_index(),
        x='Business Type / Trade',
        y=reg_business.columns.tolist(),
        title="Registration Status across Business Types",
        barmode='group'
    )
    st.plotly_chart(fig_reg_business, use_container_width=True)

# ==================== TAB 5: OPINIONS & ATTITUDES ====================
with tab5:
    st.header("Opinions & Attitudes")
    
    # Importance Rating
    importance_col = 'How important do you think trademarks are for promoting fair trade and competition? (1 = Not important; 5-very important)'
    st.subheader("Importance Rating for Fair Trade (1-5 Scale)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution of ratings
        importance_counts = df_clean[importance_col].value_counts().sort_index()
        fig_importance = px.bar(
            importance_counts.reset_index(),
            x=importance_col,
            y='count',
            title="Distribution of Importance Ratings",
            color='count',
            text='count',
            labels={importance_col: 'Rating (1-5)'}
        )
        fig_importance.update_traces(textposition='outside')
        st.plotly_chart(fig_importance, use_container_width=True)
        
    with col2:
        # Box plot
        fig_box = px.box(
            df_clean,
            y=importance_col,
            title="Importance Rating Statistics (Box Plot)",
            color_discrete_sequence=['#FF6692']
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Violin Plot
    st.subheader("Rating Distribution (Violin Plot)")
    fig_violin = px.violin(
        df_clean,
        y=importance_col,
        box=True,
        title="Importance Rating Distribution",
        color_discrete_sequence=['#00CC96']
    )
    st.plotly_chart(fig_violin, use_container_width=True)
    
    # Government Suggestions Word Cloud (Text Analysis)
    st.subheader("Government & Legal Authority Suggestions")
    govt_suggestions = df_clean['In your opinion;  what can the government or legal authorities do to make trademark law more accessible for small traders?'].dropna()
    
    # Display as text list
    st.write("**Key Suggestions:**")
    for idx, suggestion in enumerate(govt_suggestions.unique(), 1):
        if suggestion != 'NA':
            st.write(f"{idx}. {suggestion}")

# ==================== TAB 6: DEEP DIVE ANALYSIS ====================
with tab6:
    st.header("Deep Dive Analysis")
    
    # Heatmap: Gender vs Business Type
    st.subheader("Gender vs Business Type (Heatmap)")
    pivot_gender_business = pd.crosstab(df_clean['Gender'], df_clean['Business Type / Trade'])
    fig_heatmap = px.imshow(
        pivot_gender_business,
        text_auto=True,
        title="Heatmap: Gender vs Business Type",
        color_continuous_scale='Blues',
        labels=dict(x="Business Type", y="Gender", color="Count")
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Parallel Categories
    st.subheader("Parallel Categories: Multi-dimensional Flow")
    df_parallel = df_clean[['Gender', 'Age Group', 'Business Type / Trade', 'Number of years in business']].dropna()
    # Create a color dimension based on gender
    df_parallel['Color'] = pd.factorize(df_parallel['Gender'])[0]
    fig_parallel = px.parallel_categories(
        df_parallel,
        dimensions=['Gender', 'Age Group', 'Business Type / Trade', 'Number of years in business'],
        color='Color',
        title="<b>Flow Analysis: Gender → Age → Business Type → Experience</b>",
        color_continuous_scale=px.colors.diverging.Spectral,
        labels={'Gender': 'Gender', 'Age Group': 'Age Group', 
                'Business Type / Trade': 'Business Type', 
                'Number of years in business': 'Years in Business'}
    )
    fig_parallel.update_layout(
        font=dict(size=14, family="Arial, sans-serif", color="#000000"),
        title_font=dict(size=18, family="Arial, sans-serif", color="#000000")
    )
    st.plotly_chart(fig_parallel, use_container_width=True)
    
    # Awareness by Demographics
    st.subheader("Trademark Awareness by Age Group")
    awareness_age = pd.crosstab(
        df_clean['Age Group'],
        df_clean['Have you heard of the term Trademark?']
    )
    fig_awareness_age = px.bar(
        awareness_age.reset_index(),
        x='Age Group',
        y=awareness_age.columns.tolist(),
        title="Trademark Awareness across Age Groups",
        barmode='group'
    )
    st.plotly_chart(fig_awareness_age, use_container_width=True)
    
    # Knowledge vs Registration
    st.subheader("Legal Protection Knowledge vs Registration Status")
    knowledge_reg = pd.crosstab(
        df_clean['Do you know that registering a trademark gives legal protection to your brand name or logo?'],
        df_clean['Have you ever registered a trademark for your business?']
    )
    fig_knowledge_reg = px.bar(
        knowledge_reg.reset_index(),
        x='Do you know that registering a trademark gives legal protection to your brand name or logo?',
        y=knowledge_reg.columns.tolist(),
        title="Protection Knowledge vs Actual Registration",
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    st.plotly_chart(fig_knowledge_reg, use_container_width=True)
    
    # Scatter Plot: Importance Rating vs Years in Business
    st.subheader("Rating vs Business Experience")
    # Create numeric mapping for years (UPPERCASE keys)
    years_mapping = {
        'LESS THAN 2 YEARS': 1,
        '2-5 YEARS': 3.5,
        '5 YEARS': 5,
        '6-10 YEARS': 8,
        'ABOVE 10 YEARS': 12
    }
    df_clean['Years_Numeric'] = df_clean['Number of years in business'].map(years_mapping)
    
    # Convert importance to numeric
    df_clean[importance_col] = pd.to_numeric(df_clean[importance_col], errors='coerce')
    
    # Filter out rows with NaN values
    df_scatter = df_clean.dropna(subset=['Years_Numeric', importance_col])
    
    if not df_scatter.empty:
        fig_scatter = px.scatter(
            df_scatter,
            x='Years_Numeric',
            y=importance_col,
            color='Gender',
            size=[30]*len(df_scatter),
            title="<b>Importance Rating vs Years in Business</b>",
            labels={'Years_Numeric': 'Years in Business (approx)', importance_col: 'Importance Rating'},
            hover_data=['Business Type / Trade']
        )
        fig_scatter.update_layout(
            font=dict(size=14, family="Arial, sans-serif", color="#000000"),
            title_font=dict(size=18, family="Arial, sans-serif", color="#000000")
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("No data available for scatter plot")
    
    # Correlation Analysis
    st.subheader("Statistical Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Importance Rating", f"{df_clean[importance_col].mean():.2f}")
    with col2:
        registration_rate = (df_clean['Have you ever registered a trademark for your business?'] == 'Yes').sum() / len(df_clean) * 100
        st.metric("Registration Rate", f"{registration_rate:.1f}%")
    with col3:
        awareness_rate = (df_clean['Have you heard of the term Trademark?'] == 'Yes').sum() / len(df_clean) * 100
        st.metric("Awareness Rate", f"{awareness_rate:.1f}%")
    with col4:
        willingness_rate = (df_clean['Would you be willing to register your business trademark if you get proper guidance?'] == 'Yes').sum() / len(df_clean) * 100
        st.metric("Willingness Rate", f"{willingness_rate:.1f}%")

# Footer
st.markdown("---")
st.markdown("### 📝 Survey Insights Dashboard | Data-driven Analysis for Trademark Awareness in Vijayawada")
