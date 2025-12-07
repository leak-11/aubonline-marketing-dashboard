# ============================================================================
# SBE MARKETING INTELLIGENCE PLATFORM
# Professional Marketing Analytics Dashboard
# AUB MSBA Capstone Project
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="SBE Marketing Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - LIGHTER PROFESSIONAL THEME
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap');
    
    /* Lighter background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f3460 0%, #16213e 100%);
        border-right: 1px solid #3d5a80;
    }
    
    [data-testid="stSidebar"] * {
        color: #e8e8e8 !important;
    }
    
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        color: #ffffff !important;
    }
    
    /* Improved KPI Cards */
    .kpi-card {
        background: linear-gradient(145deg, #1e3a5f 0%, #0f3460 100%);
        border: 1px solid #3d5a80;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 212, 255, 0.2);
    }
    
    .kpi-value {
        font-family: 'Roboto Mono', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        color: #00d4ff;
        margin: 8px 0;
    }
    
    .kpi-label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.9rem;
        color: #b8c5d6;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .kpi-delta {
        font-size: 0.85rem;
        color: #00ff88;
    }
    
    /* Insight Cards */
    .insight-card {
        background: linear-gradient(145deg, #0f3460 0%, #1a1a2e 100%);
        border-left: 4px solid #00d4ff;
        border-radius: 8px;
        padding: 20px;
        margin: 16px 0;
    }
    
    .insight-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #00d4ff;
        margin-bottom: 8px;
    }
    
    .insight-text {
        font-family: 'Poppins', sans-serif;
        font-size: 0.95rem;
        color: #d0d8e4;
        line-height: 1.6;
    }
    
    .section-header {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        padding: 16px 0;
        border-bottom: 2px solid #3d5a80;
        margin-bottom: 24px;
    }
    
    .coming-soon {
        background: rgba(255, 193, 7, 0.15);
        border: 1px dashed rgba(255, 193, 7, 0.6);
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        color: #ffc107;
    }
    
    /* Better Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 52, 96, 0.5);
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(61, 90, 128, 0.4);
        border-radius: 8px;
        color: #b8c5d6 !important;
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00d4ff, #7b2cbf) !important;
        color: white !important;
    }
    
    /* Filter indicator */
    .filter-active {
        background: rgba(0, 212, 255, 0.2);
        border: 1px solid #00d4ff;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        color: #00d4ff;
        font-size: 0.85rem;
    }
    
    /* Improve selectbox visibility */
    .stSelectbox label, .stSlider label {
        color: #e8e8e8 !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: #1e3a5f !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# COLOR PALETTE - BRIGHTER
# ============================================================================

colors = {
    'primary': '#00d4ff',
    'secondary': '#a855f7',
    'success': '#22c55e',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'google': '#3b82f6',
    'social': '#10b981',
    'neutral': '#94a3b8',
    'bg_dark': '#1e3a5f',
    'bg_light': '#0f3460'
}

# Plotly layout template for better visibility
plotly_layout = dict(
    paper_bgcolor='rgba(30, 58, 95, 0.5)',
    plot_bgcolor='rgba(15, 52, 96, 0.8)',
    font=dict(family='Poppins, sans-serif', color='#e8e8e8', size=12)
)

# ============================================================================
# DATA LOADING - CHANGED TO RELATIVE PATH FOR CLOUD
# ============================================================================

@st.cache_data
def load_data():
    BASE_DIR = "data"  # Relative path for Streamlit Cloud
    
    try:
        channel_gs = pd.read_csv(f'{BASE_DIR}/channel_costs_GS.csv')
        channel_sm = pd.read_csv(f'{BASE_DIR}/channel_costs_SM.csv')
        country_attr = pd.read_csv(f'{BASE_DIR}/country_attributes.csv')
        master_leads = pd.read_csv(f'{BASE_DIR}/master_leads.csv')
        master_leads_weekly = pd.read_csv(f'{BASE_DIR}/master_leads_weekly.csv')
        post_perf_totals = pd.read_csv(f'{BASE_DIR}/post_performance_totals_clean.csv')
        post_perf_regional = pd.read_csv(f'{BASE_DIR}/post_performance_regional_clean.csv')
        weekly_channel_summary = pd.read_csv(f'{BASE_DIR}/weekly_channel_summary.csv')
        
        # Clean data
        channel_gs['cpl'] = pd.to_numeric(channel_gs['cpl'].replace('#DIV/0!', np.nan), errors='coerce')
        channel_gs_clean = channel_gs.dropna(subset=['channel']).reset_index(drop=True)
        channels_combined = pd.concat([channel_gs_clean, channel_sm], ignore_index=True)
        channels_combined['cpl'] = pd.to_numeric(channels_combined['cpl'], errors='coerce')
        
        master_leads_weekly['week_num'] = master_leads_weekly['week_number'].str.extract('(\d+)').astype(int)
        master_enriched = master_leads_weekly.merge(country_attr, on='country', how='left', suffixes=('', '_country'))
        
        return {
            'channel_gs': channel_gs_clean,
            'channel_sm': channel_sm,
            'channels_combined': channels_combined,
            'country_attr': country_attr,
            'master_leads': master_leads,
            'master_leads_weekly': master_leads_weekly,
            'master_enriched': master_enriched,
            'post_perf_totals': post_perf_totals,
            'post_perf_regional': post_perf_regional,
            'weekly_channel_summary': weekly_channel_summary
        }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# ============================================================================
# FILTER DATA FUNCTION
# ============================================================================

def apply_filters(data, filters):
    """Apply sidebar filters to the data"""
    leads = data['master_leads_weekly'].copy()
    master_enriched = data['master_enriched'].copy()
    
    if filters['channel'] != 'All':
        leads = leads[leads['channel'] == filters['channel']]
        master_enriched = master_enriched[master_enriched['channel'] == filters['channel']]
    
    if filters['country'] != 'All':
        leads = leads[leads['country'] == filters['country']]
        master_enriched = master_enriched[master_enriched['country'] == filters['country']]
    
    if filters['priority'] != 'All':
        leads_with_priority = leads.merge(
            data['country_attr'][['country', 'market_priority']], 
            on='country', 
            how='left'
        )
        leads = leads_with_priority[leads_with_priority['market_priority'] == filters['priority']]
        leads = leads.drop(columns=['market_priority'], errors='ignore')
        master_enriched = master_enriched[master_enriched['market_priority'] == filters['priority']]
    
    week_min, week_max = filters['week_range']
    leads = leads[(leads['week_num'] >= week_min) & (leads['week_num'] <= week_max)]
    master_enriched = master_enriched[(master_enriched['week_num'] >= week_min) & (master_enriched['week_num'] <= week_max)]
    
    filtered_data = data.copy()
    filtered_data['master_leads_weekly'] = leads
    filtered_data['master_enriched'] = master_enriched
    
    return filtered_data

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_kpi_card(label, value, delta=None):
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """

def create_insight_card(title, text, icon="💡"):
    return f"""
    <div class="insight-card">
        <div class="insight-title">{icon} {title}</div>
        <div class="insight-text">{text}</div>
    </div>
    """

def show_filter_status(filters):
    """Show active filters"""
    active = []
    if filters['channel'] != 'All':
        active.append(f"Channel: {filters['channel']}")
    if filters['country'] != 'All':
        active.append(f"Country: {filters['country']}")
    if filters['priority'] != 'All':
        active.append(f"Priority: {filters['priority']}")
    
    if active:
        st.markdown(f"""
        <div class="filter-active">
            🎛️ Active Filters: {' | '.join(active)}
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar(data):
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="background: linear-gradient(90deg, #00d4ff, #a855f7); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.8rem;">
            📊 SBE MIP
        </h2>
        <p style="color: #94a3b8; font-size: 0.85rem;">Marketing Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧭 Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["📊 Overview", "📈 Performance", "🤖 Models", "💡 Recommendations"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛️ Filters")
    
    channels = ['All'] + sorted(data['master_leads_weekly']['channel'].dropna().unique().tolist())
    selected_channel = st.sidebar.selectbox("📡 Channel", channels)
    
    countries = ['All'] + sorted(data['country_attr']['country'].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("🌍 Country", countries)
    
    priorities = ['All'] + sorted(data['country_attr']['market_priority'].dropna().unique().tolist())
    selected_priority = st.sidebar.selectbox("⭐ Market Priority", priorities)
    
    min_week = int(data['master_leads_weekly']['week_num'].min())
    max_week = int(data['master_leads_weekly']['week_num'].max())
    week_range = st.sidebar.slider("📅 Week Range", min_week, max_week, (min_week, max_week))
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 16px; background: rgba(34, 197, 94, 0.15); border-radius: 8px;">
        <div style="color: #22c55e; font-size: 0.75rem;">Data Status</div>
        <div style="color: #22c55e; font-weight: 600;">● Live</div>
        <div style="color: #94a3b8; font-size: 0.7rem;">AUB MSBA Capstone</div>
    </div>
    """, unsafe_allow_html=True)
    
    return page, {'channel': selected_channel, 'country': selected_country, 'priority': selected_priority, 'week_range': week_range}

# ============================================================================
# PAGE 1: OVERVIEW
# ============================================================================

def render_overview(data, filters):
    filtered_data = apply_filters(data, filters)
    leads = filtered_data['master_leads_weekly']
    channels = data['channels_combined']
    
    show_filter_status(filters)
    
    st.markdown("""
    <h1 style="text-align: center; margin-bottom: 8px;">Marketing Intelligence Platform</h1>
    <p style="text-align: center; color: #94a3b8; font-family: 'Poppins', sans-serif; margin-bottom: 32px;">
        SBE Masters Program • Student Acquisition Campaign Analytics
    </p>
    """, unsafe_allow_html=True)
    
    if len(leads) == 0:
        st.warning("⚠️ No data matches the current filters. Please adjust your selection.")
        return
    
    total_budget = channels['budget_usd'].sum()
    total_leads = len(leads)
    qualified_leads = leads['is_qualified'].sum()
    reachable_leads = leads['is_reachable'].sum()
    qualification_rate = qualified_leads / total_leads * 100 if total_leads > 0 else 0
    reachability_rate = reachable_leads / total_leads * 100 if total_leads > 0 else 0
    avg_cpl = total_budget / total_leads if total_leads > 0 else 0
    avg_cpql = total_budget / qualified_leads if qualified_leads > 0 else 0
    
    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(create_kpi_card("Total Investment", f"${total_budget:,.0f}"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_kpi_card("Total Leads", f"{total_leads:,}", f"Filtered"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_kpi_card("Qualified Leads", f"{int(qualified_leads)}", f"{qualification_rate:.1f}%"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_kpi_card("Reachable Leads", f"{int(reachable_leads)}", f"{reachability_rate:.1f}%"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(create_kpi_card("Average CPL", f"${avg_cpl:.2f}"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_kpi_card("Average CPQL", f"${avg_cpql:.2f}"), unsafe_allow_html=True)
    with col3:
        weeks_in_filter = leads['week_num'].nunique()
        st.markdown(create_kpi_card("Weeks in View", f"{weeks_in_filter}", "of 35 total"), unsafe_allow_html=True)
    with col4:
        countries_in_filter = leads['country'].nunique()
        st.markdown(create_kpi_card("Countries", f"{countries_in_filter}"), unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Channel Paradox
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-header">🔍 Channel Efficiency Paradox</div>', unsafe_allow_html=True)
        
        gs_data = channels[channels['channel'] == 'Google_Search']
        sm_data = channels[channels['channel'] == 'Social_Media']
        
        gs_budget = gs_data['budget_usd'].sum()
        sm_budget = sm_data['budget_usd'].sum()
        gs_leads = len(leads[leads['channel'] == 'Google Search'])
        sm_leads = len(leads[leads['channel'] == 'Social Media'])
        gs_qualified = leads[leads['channel'] == 'Google Search']['is_qualified'].sum()
        sm_qualified = leads[leads['channel'] == 'Social Media']['is_qualified'].sum()
        
        gs_cpl = gs_budget / gs_leads if gs_leads > 0 else 0
        sm_cpl = sm_budget / sm_leads if sm_leads > 0 else 0
        gs_cpql = gs_budget / gs_qualified if gs_qualified > 0 else 0
        sm_cpql = sm_budget / sm_qualified if sm_qualified > 0 else 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='CPL', x=['Google Search', 'Social Media'], y=[gs_cpl, sm_cpl],
                            marker_color=[colors['google'], colors['social']], 
                            text=[f'${gs_cpl:.0f}', f'${sm_cpl:.0f}'], textposition='outside',
                            textfont=dict(color='#e8e8e8', size=12)))
        fig.add_trace(go.Bar(name='CPQL', x=['Google Search', 'Social Media'], y=[gs_cpql, sm_cpql],
                            marker_color=[colors['primary'], colors['secondary']], 
                            text=[f'${gs_cpql:.0f}', f'${sm_cpql:.0f}'], textposition='outside',
                            textfont=dict(color='#e8e8e8', size=12)))
        
        fig.update_layout(**plotly_layout, barmode='group', height=350,
                         legend=dict(orientation='h', y=-0.15, font=dict(color='#e8e8e8', size=12)),
                         yaxis_title='Cost ($)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">💡 Key Insight</div>', unsafe_allow_html=True)
        efficiency_ratio = sm_cpql / gs_cpql if gs_cpql > 0 else 0
        
        st.markdown(create_insight_card(
            "The Channel Efficiency Paradox",
            f"<b>Social Media</b> appears cheaper at <b>${sm_cpl:.0f} CPL</b>, but delivers <b>${sm_cpql:.0f} CPQL</b>.<br><br>"
            f"<b>Google Search</b> seems expensive at <b>${gs_cpl:.0f} CPL</b>, but delivers <b>${gs_cpql:.0f} CPQL</b>.<br><br>"
            f"<span style='color: #22c55e;'>Google Search is {efficiency_ratio:.1f}x more cost-efficient!</span>",
            "🎯"
        ), unsafe_allow_html=True)
        
        st.markdown(create_insight_card(
            "Strategic Recommendation",
            "Consider reallocating <b>20% of Social Media budget</b> to Google Search to improve overall CPQL.",
            "💰"
        ), unsafe_allow_html=True)
    
    # Weekly Trend
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        st.markdown('<div class="section-header">📈 Weekly Lead Volume Trend</div>', unsafe_allow_html=True)
        
        weekly_data = leads.groupby('week_num').agg({'lead_id': 'count', 'is_qualified': 'sum'}).reset_index()
        weekly_data.columns = ['Week', 'Total Leads', 'Qualified']
        weekly_data['4-Week MA'] = weekly_data['Total Leads'].rolling(window=4).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weekly_data['Week'], y=weekly_data['Total Leads'], mode='lines+markers',
                                name='Weekly Leads', line=dict(color=colors['primary'], width=2),
                                marker=dict(size=8)))
        fig.add_trace(go.Scatter(x=weekly_data['Week'], y=weekly_data['4-Week MA'], mode='lines',
                                name='4-Week MA', line=dict(color=colors['warning'], width=3, dash='dash')))
        
        fig.update_layout(**plotly_layout, height=320,
                         legend=dict(orientation='h', y=-0.2, font=dict(color='#e8e8e8', size=11)),
                         xaxis_title='Week Number', yaxis_title='Number of Leads')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">🌍 Top Countries</div>', unsafe_allow_html=True)
        
        country_data = leads.groupby('country').agg({'lead_id': 'count'}).reset_index()
        country_data.columns = ['Country', 'Leads']
        country_data = country_data.sort_values('Leads', ascending=False).head(5)
        
        fig = go.Figure(go.Bar(x=country_data['Leads'], y=country_data['Country'], orientation='h',
                              marker_color=colors['primary'], 
                              text=country_data['Leads'], textposition='outside',
                              textfont=dict(color='#e8e8e8', size=11)))
        fig.update_layout(**plotly_layout, height=320, yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 2: PERFORMANCE (SIMPLIFIED)
# ============================================================================

def render_performance(data, filters):
    filtered_data = apply_filters(data, filters)
    leads = filtered_data['master_leads_weekly']
    
    st.markdown('<h1 style="text-align: center; margin-bottom: 32px;">📈 Performance Analytics</h1>', unsafe_allow_html=True)
    show_filter_status(filters)
    
    if len(leads) == 0:
        st.warning("⚠️ No data for current filters.")
        return
    
    tabs = st.tabs(["📡 Channel", "🌍 Geographic", "🎨 Creative", "⏱️ Temporal"])
    
    with tabs[0]:
        # Channel Performance
        st.markdown("### Channel Performance")
        col1, col2 = st.columns(2)
        
        with col1:
            channel_dist = leads['channel'].value_counts()
            fig = go.Figure(data=[go.Pie(labels=channel_dist.index, values=channel_dist.values, hole=0.5,
                                         marker_colors=[colors['google'], colors['social'], colors['warning'], colors['secondary']],
                                         textinfo='label+percent', textfont=dict(color='#e8e8e8', size=11))])
            fig.update_layout(**plotly_layout, height=350, title="Channel Mix")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            channel_qual = leads.groupby('channel').agg({'is_qualified': ['sum', 'count']}).reset_index()
            channel_qual.columns = ['Channel', 'Qualified', 'Total']
            channel_qual['Rate'] = (channel_qual['Qualified'] / channel_qual['Total'] * 100).round(2)
            channel_qual = channel_qual.sort_values('Rate', ascending=True)
            
            fig = go.Figure(go.Bar(x=channel_qual['Rate'], y=channel_qual['Channel'], orientation='h',
                                  marker_color=[colors['danger'] if x < 10 else colors['success'] for x in channel_qual['Rate']],
                                  text=[f'{x:.1f}%' for x in channel_qual['Rate']], textposition='outside',
                                  textfont=dict(color='#e8e8e8', size=11)))
            fig.update_layout(**plotly_layout, height=350, title="Qualification Rate by Channel")
            st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:
        # Geographic Performance
        st.markdown("### Geographic Performance")
        country_leads = leads.groupby('country').agg({'lead_id': 'count', 'is_qualified': 'sum'}).reset_index()
        country_leads.columns = ['Country', 'Leads', 'Qualified']
        country_leads['Rate'] = (country_leads['Qualified'] / country_leads['Leads'] * 100).round(1)
        country_leads = country_leads.sort_values('Leads', ascending=False).head(10)
        
        fig = go.Figure(go.Bar(x=country_leads['Leads'], y=country_leads['Country'], orientation='h',
                              marker_color=colors['primary'],
                              text=[f"{l} ({r:.0f}%)" for l, r in zip(country_leads['Leads'], country_leads['Rate'])], 
                              textposition='outside', textfont=dict(color='#e8e8e8', size=10)))
        fig.update_layout(**plotly_layout, height=450, title="Top 10 Countries", yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:
        # Creative Performance
        st.markdown("### Creative/Post Performance")
        post_perf = data['post_perf_totals'].copy()
        post_perf['roi_score'] = (post_perf['qualified_leads'] / post_perf['ad_spend_usd'] * 1000).round(3)
        post_perf = post_perf.dropna(subset=['roi_score']).sort_values('roi_score', ascending=True)
        
        fig = go.Figure(go.Bar(x=post_perf['roi_score'], y=post_perf['post_id'], orientation='h',
                              marker_color=[colors['success'] if x > post_perf['roi_score'].median() else colors['danger'] for x in post_perf['roi_score']],
                              text=[f'{x:.2f}' for x in post_perf['roi_score']], textposition='outside',
                              textfont=dict(color='#e8e8e8', size=10)))
        fig.update_layout(**plotly_layout, height=400, title="Post ROI Ranking", xaxis_title='ROI Score')
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[3]:
        # Temporal Performance
        st.markdown("### Weekly Trends")
        weekly_data = leads.groupby('week_num').agg({'lead_id': 'count', 'is_qualified': 'mean'}).reset_index()
        weekly_data.columns = ['Week', 'Leads', 'Qual Rate']
        weekly_data['Qual Rate'] = (weekly_data['Qual Rate'] * 100).round(2)
        weekly_data['4-Week MA'] = weekly_data['Leads'].rolling(window=4).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weekly_data['Week'], y=weekly_data['Leads'], mode='lines+markers',
                                name='Weekly Leads', line=dict(color=colors['primary'], width=2),
                                fill='tozeroy', fillcolor='rgba(0, 212, 255, 0.1)', marker=dict(size=8)))
        fig.add_trace(go.Scatter(x=weekly_data['Week'], y=weekly_data['4-Week MA'], mode='lines',
                                name='4-Week MA', line=dict(color=colors['warning'], width=3, dash='dash')))
        fig.update_layout(**plotly_layout, height=400, title="Weekly Lead Volume",
                         legend=dict(orientation='h', y=-0.2, font=dict(color='#e8e8e8')))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 3: MODELS
# ============================================================================

def render_models(data, filters):
    st.markdown('<h1 style="text-align: center; margin-bottom: 32px;">🤖 Predictive Models</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["🎯 Lead Qualification", "📈 Forecasting"])
    
    with tabs[0]:
        st.markdown("### Lead Qualification Model")
        st.markdown("**Best Model:** Random Forest + ADASYN")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("F1-Score", "0.40", "+6% vs baseline")
        with col2:
            st.metric("ROC-AUC", "0.76", "Good discrimination")
        with col3:
            st.metric("Recall", "57%", "Catches majority")
        
        st.markdown(create_insight_card(
            "Model Insights",
            "The model identifies <b>is_reachable</b> as the top predictor. "
            "Leads from <b>Google Search</b> and <b>Lebanon</b> have higher qualification probability.",
            "🎯"
        ), unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("### Lead Volume Forecasting")
        st.markdown("**Best Model:** Prophet + Regressors")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("MAPE", "54.2%", "Fair accuracy")
        with col2:
            st.metric("Improvement", "53.8%", "vs baseline")
        with col3:
            st.metric("8-Week Forecast", "235 leads", "~29/week")
        
        st.markdown(create_insight_card(
            "Forecast Note",
            "Limited by 35 weeks of data. Accuracy will improve with more historical data. "
            "Use for <b>directional planning</b>, not precise predictions.",
            "📈"
        ), unsafe_allow_html=True)

# ============================================================================
# PAGE 4: RECOMMENDATIONS
# ============================================================================

def render_recommendations(data, filters):
    st.markdown('<h1 style="text-align: center; margin-bottom: 32px;">💡 Strategic Recommendations</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(create_insight_card("💰 Budget Reallocation",
            "<b>Action:</b> Shift 20% of Social Media budget to Google Search<br><br>"
            "<b>Rationale:</b> Google Search delivers better CPQL<br><br>"
            "<b>Impact:</b> 25-30% reduction in overall CPQL", "💰"), unsafe_allow_html=True)
        
        st.markdown(create_insight_card("🌍 Geographic Diversification",
            "<b>Action:</b> Reduce Lebanon dependency to &lt;35%<br><br>"
            "<b>Rationale:</b> Lebanon = 43% of leads (concentration risk)<br><br>"
            "<b>Impact:</b> More stable lead flow", "🌍"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_insight_card("🎨 Creative Optimization",
            "<b>Action:</b> Scale Post1 & Post4, pause Post8<br><br>"
            "<b>Rationale:</b> Post1 has highest ROI (3.11)<br><br>"
            "<b>Impact:</b> 15-20% improvement in creative ROI", "🎨"), unsafe_allow_html=True)
        
        st.markdown(create_insight_card("📊 Quality Focus",
            "<b>Action:</b> Prioritize qualification rate over volume<br><br>"
            "<b>Rationale:</b> Current 11.3% rate needs improvement<br><br>"
            "<b>Impact:</b> Better ROI on marketing spend", "📊"), unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    data = load_data()
    
    if data is None:
        st.error("❌ Failed to load data. Please check that data files exist in the 'data' folder.")
        st.info("Required files: channel_costs_GS.csv, channel_costs_SM.csv, country_attributes.csv, master_leads.csv, master_leads_weekly.csv, post_performance_totals_clean.csv, post_performance_regional_clean.csv, weekly_channel_summary.csv")
        return
    
    page, filters = render_sidebar(data)
    
    if page == "📊 Overview":
        render_overview(data, filters)
    elif page == "📈 Performance":
        render_performance(data, filters)
    elif page == "🤖 Models":
        render_models(data, filters)
    elif page == "💡 Recommendations":
        render_recommendations(data, filters)
    
    st.markdown("""
    <div style="text-align: center; padding: 24px; color: #94a3b8; font-size: 0.85rem; border-top: 1px solid #3d5a80; margin-top: 48px;">
        SBE Marketing Intelligence Platform • AUB MSBA Capstone Project • December 2025
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
