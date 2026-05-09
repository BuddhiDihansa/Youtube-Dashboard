import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard_shared import load_data, apply_filters

# PAGE CONFIG
st.set_page_config(
    page_title=" YouTube Creator Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# ULTRA MODERN DESIGN WITH CREATIVE STYLING
st.markdown("""
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    .stApp { 
        background: linear-gradient(135deg, #0a0e27 0%, #16213e 50%, #0f3460 100%);
        color: #ecf0f1;
    }

    /* Animated Background */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Header with Gradient and Animation */
    .header-container {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        padding: 3rem 2.5rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        margin-bottom: 2.5rem;
        position: relative;
        overflow: hidden;
    }

    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: float 20s linear infinite;
    }

    @keyframes float {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }

    .header-title {
        font-size: 3rem;
        font-weight: 900;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
        letter-spacing: -1px;
    }

    .header-subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.95);
        font-weight: 300;
        letter-spacing: 0.08em;
        position: relative;
        z-index: 1;
    }

    /* KPI Cards with Colored Variants */
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 2px solid rgba(59, 130, 246, 0.4);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 1px, transparent 1px);
        background-size: 30px 30px;
    }

    .kpi-card:hover {
        border-color: rgba(59, 130, 246, 0.8);
        box-shadow: 0 25px 80px rgba(59, 130, 246, 0.2);
        transform: translateY(-8px) scale(1.02);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
    }

    .kpi-card.views {
        border-left: 5px solid #ff6b6b;
    }

    .kpi-card.likes {
        border-left: 5px solid #4ecdc4;
    }

    .kpi-card.comments {
        border-left: 5px solid #ffd93d;
    }

    .kpi-card.engagement {
        border-left: 5px solid #a8e6cf;
    }

    .kpi-emoji {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
        display: inline-block;
    }

    .kpi-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.8rem;
        font-weight: 700;
    }

    .kpi-value {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    .kpi-change {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 500;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0a0e27 0%, #1e3a8a 100%) !important;
        border-right: 3px solid rgba(59, 130, 246, 0.3);
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #93c5fd !important;
    }

    /* Section Headers */
    h2 {
        color: #f1f5f9 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 1rem !important;
        border-bottom: 3px solid rgba(59, 130, 246, 0.4) !important;
        letter-spacing: -0.5px !important;
    }

    h3 {
        color: #e2e8f0 !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin-top: 1.2rem !important;
        margin-bottom: 1rem !important;
    }

    /* Tabs - Modern Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(15, 23, 42, 0.5);
        padding: 0.5rem;
        border-radius: 15px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(30, 41, 59, 0.4);
        border-radius: 12px;
        padding: 0.9rem 1.8rem;
        color: #94a3b8;
        border: 1px solid rgba(59, 130, 246, 0.2);
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(30, 41, 59, 0.6);
        border-color: rgba(59, 130, 246, 0.4);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: #fff;
        border-color: #3b82f6;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
    }

    /* Data Table */
    .stDataFrame {
        background-color: rgba(30, 41, 59, 0.2) !important;
        border-radius: 15px !important;
    }

    /* Metric Cards */
    .stMetric {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
        border: 2px solid rgba(59, 130, 246, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .stMetric:hover {
        border-color: rgba(59, 130, 246, 0.6);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.1);
    }

    /* Success/Info Boxes */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.15) !important;
        border: 2px solid rgba(16, 185, 129, 0.4) !important;
        border-radius: 15px !important;
        color: #a7f3d0 !important;
        font-weight: 500 !important;
        padding: 1.2rem !important;
    }

    .stInfo {
        background-color: rgba(59, 130, 246, 0.15) !important;
        border: 2px solid rgba(59, 130, 246, 0.4) !important;
        border-radius: 15px !important;
    }

    .stWarning {
        background-color: rgba(251, 146, 60, 0.15) !important;
        border: 2px solid rgba(251, 146, 60, 0.4) !important;
        border-radius: 15px !important;
    }

    /* Divider */
    hr {
        border: 0 !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent) !important;
        margin: 2rem 0 !important;
    }

    /* Creative Section Separator */
    .section-divider {
        text-align: center;
        margin: 2rem 0;
        color: #3b82f6;
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: 0.2em;
    }

    @media (max-width: 900px) {
        .header-title {
            font-size: 2rem;
        }
        .kpi-value {
            font-size: 1.8rem;
        }
        .header-container {
            padding: 2rem 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# LOAD DATA
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ANIMATED HEADER
st.markdown("""
<div class="header-container">
    <div class="header-title">YOUTUBE ANALYTICS HUB</div>
    <div class="header-subtitle"> Real-time Creator Performance Intelligence & Advanced Content Analytics </div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR FILTERS WITH ENHANCED STYLING
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;"></div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #93c5fd;">SMART FILTERS</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    category = st.multiselect(
        " **Video Category**",
        options=sorted(df["category"].unique()),
        default=None,
        placeholder=" Select categories..."
    )
    
    region = st.multiselect(
        " **Geographic Region**",
        options=sorted(df["region"].unique()),
        default=None,
        placeholder=" Select regions..."
    )
    
    language = st.multiselect(
        " **Language**",
        options=sorted(df["language"].unique()),
        default=None,
        placeholder=" Select languages..."
    )
    
    st.markdown("---")
    
    st.markdown("""
    <div style="color: #93c5fd; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.8rem;">
    DATE RANGE SELECTOR
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            " Start",
            value=df["timestamp"].min(),
            min_value=df["timestamp"].min(),
            max_value=df["timestamp"].max(),
            label_visibility="collapsed"
        )
    with col2:
        end_date = st.date_input(
            " End",
            value=df["timestamp"].max(),
            min_value=df["timestamp"].min(),
            max_value=df["timestamp"].max(),
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 2rem;">
    Pro Tip: Combine filters for deeper insights!
    </div>
    """, unsafe_allow_html=True)

# FILTER DATA
filtered = apply_filters(df, category, region, language)
filtered = filtered[
    (filtered["timestamp"] >= pd.to_datetime(start_date)) &
    (filtered["timestamp"] <= pd.to_datetime(end_date))
]

has_data = not filtered.empty

if has_data:
    engagement_by_category = (
        filtered.groupby("category", observed=True)["engagement"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    engagement_by_region = (
        filtered.groupby("region", observed=True)["engagement"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    views_by_month = (
        filtered.groupby("month", observed=True)["views"]
        .sum()
        .reset_index()
        .sort_values("month")
    )
    views_by_category = filtered.groupby("category", observed=True)["views"].sum()
    views_by_region = filtered.groupby("region", observed=True)["views"].sum()
    engagement_by_hour = filtered.groupby("hour", observed=True)["engagement"].mean()
    engagement_by_language = filtered.groupby("language", observed=True)["engagement"].mean()

# KPI SECTION WITH ENHANCED STYLING
st.markdown("##  KEY PERFORMANCE INDICATORS")

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4, gap="medium")

# Views Card
with kpi_col1:
    views_count = int(filtered['views'].sum())
    st.markdown(f"""
    <div class="kpi-card views">
        <div class="kpi-emoji"></div>
        <div class="kpi-label">Total Views</div>
        <div class="kpi-value">{views_count:,}</div>
        <div class="kpi-change">Reach Metric</div>
    </div>
    """, unsafe_allow_html=True)

# Likes Card
with kpi_col2:
    likes_count = int(filtered['likes'].sum())
    st.markdown(f"""
    <div class="kpi-card likes">
        <div class="kpi-emoji"></div>
        <div class="kpi-label">Total Likes</div>
        <div class="kpi-value">{likes_count:,}</div>
        <div class="kpi-change"> Audience Love</div>
    </div>
    """, unsafe_allow_html=True)

# Comments Card
with kpi_col3:
    comments_count = int(filtered['comments'].sum())
    st.markdown(f"""
    <div class="kpi-card comments">
        <div class="kpi-emoji"></div>
        <div class="kpi-label">Total Comments</div>
        <div class="kpi-value">{comments_count:,}</div>
        <div class="kpi-change"> Community Voice</div>
    </div>
    """, unsafe_allow_html=True)

# Engagement Card
with kpi_col4:
    engagement_rate = filtered['engagement'].mean()
    st.markdown(f"""
    <div class="kpi-card engagement">
        <div class="kpi-emoji"></div>
        <div class="kpi-label">Avg Engagement</div>
        <div class="kpi-value">{engagement_rate:.4f}</div>
        <div class="kpi-change"> Interaction Rate</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# CREATIVE SECTION DIVIDER
st.markdown("""
<div class="section-divider">
    ★ ░ ★ ░ ★ ░ ADVANCED ANALYTICS ░ ★ ░ ★ ░ ★
</div>
""", unsafe_allow_html=True)

# MAIN ANALYTICS TABS
tab1, tab2, tab3, tab4 = st.tabs([
    " Interactive Charts",
    " Data Explorer",
    " Performance Summary",
    " AI Insights"
])

# TAB 1: CHARTS
with tab1:
    chart_row1_col1, chart_row1_col2 = st.columns(2, gap="large")
    
    with chart_row1_col1:
        st.markdown("###  Engagement by Category")
        if has_data and len(engagement_by_category) > 0:
            fig = px.bar(
                engagement_by_category, x="category", y="engagement",
                color="engagement", color_continuous_scale="Viridis",
                labels={"engagement": "Engagement Rate", "category": "Category"},
                text="engagement"
            )
            fig.update_traces(textposition='outside', texttemplate='%{text:.4f}')
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(15,23,42,0.3)",
                paper_bgcolor="rgba(30,41,59,0.2)",
                font=dict(color="#f1f5f9", size=11),
                hovermode="x unified",
                showlegend=False,
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(" Select categories to view insights")
    
    with chart_row1_col2:
        st.markdown("###  Engagement by Region")
        if has_data and len(engagement_by_region) > 0:
            fig = px.bar(
                engagement_by_region, x="region", y="engagement",
                color="engagement", color_continuous_scale="Plasma",
                labels={"engagement": "Engagement Rate", "region": "Region"},
                text="engagement"
            )
            fig.update_traces(textposition='outside', texttemplate='%{text:.4f}')
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(15,23,42,0.3)",
                paper_bgcolor="rgba(30,41,59,0.2)",
                font=dict(color="#f1f5f9", size=11),
                hovermode="x unified",
                showlegend=False,
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(" Select regions to view insights")
    
    st.markdown("###  Monthly Views Trend Analysis")
    if has_data and len(views_by_month) > 0:
        fig = px.line(
            views_by_month, x="month", y="views",
            markers=True, line_shape="spline",
            labels={"views": "Total Views", "month": "Month"},
            title="Views Performance Over Time"
        )
        fig.update_traces(
            line_color="#3b82f6",
            marker=dict(size=12, color="#60a5fa", line=dict(color="#1e3a8a", width=2)),
            fill="tozeroy",
            fillcolor="rgba(59, 130, 246, 0.1)"
        )
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(15,23,42,0.3)",
            paper_bgcolor="rgba(30,41,59,0.2)",
            font=dict(color="#f1f5f9", size=11),
            hovermode="x unified",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(" No data available for trend analysis")
    
    col_scatter1, col_scatter2 = st.columns(2, gap="large")
    
    with col_scatter1:
        st.markdown("###  Views vs Engagement Correlation")
        if has_data and len(filtered) > 50:
            scatter_cols = ["views", "engagement", "likes", "category", "comments", "video_id"]
            sample = filtered[scatter_cols].sample(min(1500, len(filtered)))
            fig = px.scatter(
                sample, x="views", y="engagement",
                size="likes", color="category",
                hover_data=["comments", "video_id"],
                labels={"views": "Total Views", "engagement": "Engagement Rate"}
            )
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(15,23,42,0.3)",
                paper_bgcolor="rgba(30,41,59,0.2)",
                font=dict(color="#f1f5f9"),
                hovermode="closest",
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(" Insufficient data for scatter plot")
    
    with col_scatter2:
        st.markdown("###  Engagement Distribution")
        if len(filtered) > 0:
            pie_data = pd.DataFrame({
                "Type": [" Likes", " Comments", " Shares"],
                "Value": [
                    filtered["likes"].sum(),
                    filtered["comments"].sum(),
                    filtered["shares"].sum()
                ]
            })
            fig = px.pie(
                pie_data, names="Type", values="Value", hole=0.5,
                color_discrete_sequence=["#3b82f6", "#60a5fa", "#93c5fd"]
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(30,41,59,0.2)",
                font=dict(color="#f1f5f9"),
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(" No data available")

# TAB 2: DATA TABLE
with tab2:
    st.markdown("###  Top 15 High-Performing Videos")
    if has_data:
        top_videos = filtered.nlargest(15, "views")
        display_cols = ["video_id", "category", "region", "views", "likes", "comments", "engagement"]
        
        # Format for better display
        display_df = top_videos[display_cols].reset_index(drop=True).copy()
        display_df.index = display_df.index + 1
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=600,
            column_config={
                "views": st.column_config.NumberColumn(" Views", format="%.0f"),
                "likes": st.column_config.NumberColumn(" Likes", format="%.0f"),
                "comments": st.column_config.NumberColumn(" Comments", format="%.0f"),
                "engagement": st.column_config.NumberColumn(" Engagement", format="%.6f")
            }
        )
        
        st.markdown(f"""
         **Summary**: {len(filtered)} videos analyzed | 
         **Total Views**: {filtered['views'].sum():,} | 
         **Total Engagement**: {filtered['engagement'].sum():.4f}
        """)
    else:
        st.warning(" No data to display. Adjust your filters.")

# TAB 3: SUMMARY
with tab3:
    summary_col1, summary_col2 = st.columns(2, gap="large")
    
    with summary_col1:
        st.markdown("###  Performance Leaders")
        if has_data:
            try:
                top_category = engagement_by_category.iloc[0]["category"]
                top_region = engagement_by_region.iloc[0]["region"]
                best_hour = int(engagement_by_hour.idxmax())
                
                st.metric(
                    " Top Category",
                    top_category,
                    delta="Highest engagement",
                    delta_color="normal"
                )
                st.metric(
                    " Top Region",
                    top_region,
                    delta="Best performer",
                    delta_color="normal"
                )
                st.metric(
                    " Peak Hour",
                    f"{best_hour:02d}:00",
                    delta="Maximum traffic",
                    delta_color="normal"
                )
                st.metric(
                    " Total Videos",
                    f"{len(filtered):,}",
                    delta="In selection",
                    delta_color="normal"
                )
            except:
                st.warning(" Insufficient data for analysis")
        else:
            st.warning(" No data available for selected filters")
    
    with summary_col2:
        st.markdown("###  Statistical Metrics")
        if len(filtered) > 0:
            st.metric(
                " Avg Views/Video",
                f"{filtered['views'].mean():,.0f}",
                delta="Per video average",
                delta_color="normal"
            )
            st.metric(
                " Avg Likes/Video",
                f"{filtered['likes'].mean():,.0f}",
                delta="Per video average",
                delta_color="normal"
            )
            st.metric(
                " Avg Comments/Video",
                f"{filtered['comments'].mean():,.0f}",
                delta="Per video average",
                delta_color="normal"
            )
            st.metric(
                " Peak Engagement",
                f"{filtered['engagement'].max():.6f}",
                delta="Maximum rate",
                delta_color="normal"
            )
        else:
            st.warning(" No data available")

# TAB 4: AI INSIGHTS
with tab4:
    st.markdown("###  Intelligent Data Insights")
    
    if len(filtered) > 0:
        col_insight1, col_insight2 = st.columns(2, gap="large")
        
        with col_insight1:
            st.markdown("####  Strategic Recommendations")
            
            try:
                # Insight 1: Best Category
                top_cat = views_by_category.idxmax()
                top_cat_views = views_by_category.max()
                st.success(f" **{top_cat}** dominates with {top_cat_views:,.0f} total views")
                
                # Insight 2: Best Region
                top_reg = views_by_region.idxmax()
                top_reg_views = views_by_region.max()
                st.success(f" **{top_reg}** is your strongest market ({top_reg_views:,.0f} views)")
                
                # Insight 3: Engagement Performance
                avg_eng = filtered['engagement'].mean()
                st.success(f" Your average engagement rate is **{avg_eng:.4f}** - Strong performance!")
                
                # Insight 4: Best Hour
                best_hr = int(engagement_by_hour.idxmax())
                st.success(f" Post content at **{best_hr:02d}:00** for maximum engagement")
                
            except Exception as e:
                st.warning(f" Some insights unavailable: {str(e)}")
        
        with col_insight2:
            st.markdown("####  Content Performance")
            
            try:
                # Top Video
                top_video = filtered.loc[filtered["views"].idxmax()]
                st.success(f" Top video ID: **{top_video['video_id']}** ({top_video['views']:,.0f} views)")
                
                # Language Performance
                if len(engagement_by_language) > 0:
                    top_lang = engagement_by_language.idxmax()
                    st.success(f" Language **{top_lang}** has the best engagement rate")
                
                # Growth Metric
                total_engagement = filtered['engagement'].sum()
                st.success(f" Total engagement score: **{total_engagement:,.2f}**")
                
                # Coverage
                coverage = len(filtered) / len(df) * 100
                st.success(f" Analyzing **{coverage:.1f}%** of your dataset")
                
            except Exception as e:
                st.warning(f" Some insights unavailable")
    else:
        st.warning(" No data available. Please adjust your filters to see AI-powered insights!")

# FOOTER
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; margin-top: 2rem;">
    <div> Powered by Advanced Analytics Engine </div>
    <div style="margin-top: 0.5rem;"> YouTube Creator Analytics v2.0 |  Real-time Data Processing</div>
</div>
""", unsafe_allow_html=True)
