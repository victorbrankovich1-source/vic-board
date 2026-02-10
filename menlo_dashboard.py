import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

# ============================================================================
# PAGE CONFIG & THEME
# ============================================================================
st.set_page_config(
    page_title="Menlo College Sports Performance Dashboard",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Menlo College branding
st.markdown("""
<style>
    /* Primary Colors: Navy Blue (#002855), Gold (#F3C363) */
    .main {
        background-color: #FFFFFF;
    }
    
    h1, h2, h3 {
        color: #002855;
        font-weight: 700;
    }
    
    .stSelectbox label, .stMultiSelect label {
        color: #002855;
        font-weight: 600;
    }
    
    .metric-card {
        background-color: #F8F9FA;
        border-left: 4px solid #F3C363;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Print styles for Player Card */
    @media print {
        .stSidebar, .stButton, .no-print {
            display: none !important;
        }
        .print-card {
            page-break-inside: avoid;
            background: white;
            padding: 20px;
        }
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(135deg, #002855 0%, #003366 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .gold-accent {
        color: #F3C363;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE ROSTER DATA
# ============================================================================
ROSTER_DATA = [
    ("Acevedo, Joshua", "Line"),
    ("Ahonala, Kasper", "Big Skill"),
    ("Allen-Jackson, Daniel", "Skill"),
    ("Alonso, Fabian", "Line"),
    ("Ama Jr., Spencer", "Skill"),
    ("Andara, Aidan", "Big Skill"),
    ("Anderson, Jaylin", "Skill"),
    ("Anguiano, Damian", "Line"),
    ("Barajas, Julian", "Line"),
    ("Barden, Michael", "Skill"),
    ("Barklow, Dalton", "Big Skill"),
    ("Barklow, Neil", "Line"),
    ("Barron, Oscar", "Big Skill"),
    ("Bautista, Moises", "Skill"),
    ("Bedolla, Xavier", "Skill"),
    ("Benkis, Jordan", "Big Skill"),
    ("Birk, Griffin", "Big Skill"),
    ("Bivins, Josiah", "Line"),
    ("Bradshaw, Declan", "Skill"),
    ("Burke, Ethan", "Skill"),
    ("Busse, Jack", "Big Skill"),
    ("Cardenas, Emiliano", "Line"),
    ("Chipres, Edgar (Alex)", "Big Skill"),
    ("Clark, Jack", "Skill"),
    ("Correa, Elian", "Big Skill"),
    ("Courson, Dylan", "Skill"),
    ("Danielewicz, Blake", "Skill"),
    ("Diaz Orozco, Sebastian", "Skill"),
    ("DiCarlo Guzman, Vito", "Skill"),
    ("Dolan, Gabriel", "Big Skill"),
    ("Doss, Hunter", "Skill"),
    ("Evaimalo, Kini", "Big Skill"),
    ("Fakapelea, Joshua", "Skill"),
    ("Fifita, Malachai", "Line"),
    ("Fisiihoi, Liviu", "Line"),
    ("Flores Arteaga, Jayden", "Skill"),
    ("Franco, Anthony", "Skill"),
    ("Fusimalohi, Sione", "Line"),
    ("Gabriel, Kyle", "Skill"),
    ("Gonzalez, Eber", "Line"),
    ("Gonzalez, Julian", "Big Skill"),
    ("Granville, Noah", "Skill"),
    ("Groenewald, Martin", "Skill"),
    ("Guzman, Leo", "Line"),
    ("Henriquez-Sagrero, Jose", "Big Skill"),
    ("Ho, Bryant", "Big Skill"),
    ("Honerkamp, Teddy", "Big Skill"),
    ("Jackson, Jamario", "Skill"),
    ("James, Hayden", "Line"),
    ("Jaramillo-López, Tomás", "Big Skill"),
    ("Jimenez Ayala, Carlos", "Big Skill"),
    ("Jimenez, Poco", "Line"),
    ("Joslin-Davis, Elliott", "Big Skill"),
    ("Joya, Damon", "Skill"),
    ("Keighery, Lucca", "Skill"),
    ("Kline, George [Sonny]", "Skill"),
    ("Kryger, Dylan", "Skill"),
    ("Latu, Lawrence", "Line"),
    ("Lazare, Milo", "Big Skill"),
    ("Leafa, Nase", "Big Skill"),
    ("Lolohea, Folau", "Line"),
    ("Lomangino, Bennett", "Big Skill"),
    ("Lopez, Mark", "Line"),
    ("Lua, Joseph", "Big Skill"),
    ("Maciel, Juan Pablo", "Big Skill"),
    ("Madrid, Diego", "Skill"),
    ("Manumaleuna, Bishop", "Big Skill"),
    ("Martinez, Bryan", "Line"),
    ("Martinez, Hector", "Line"),
    ("Massoudi, Cyrus", "Big Skill"),
    ("Monroe, Kennedy", "Big Skill"),
    ("Mora, Isiah", "Line"),
    ("Munguia, Isaiah", "Line"),
    ("Munguia, Naim", "Skill"),
    ("Nava, Luis", "Line"),
    ("Neal, Rashod (Chris)", "Line"),
    ("Ochoa, Daniel", "Big Skill"),
    ("Ohtaki, Peter", "Big Skill"),
    ("Opetaia, Jonathan", "Big Skill"),
    ("Orrego Mayen, Alvin", "Line"),
    ("Page Ramirez, Jayden", "Skill"),
    ("Pahulu, Sione", "Line"),
    ("Parada Hernandez, Jaime", "Line"),
    ("Pasallo, Adrian", "Skill"),
    ("Pellican, Jake", "Line"),
    ("Raass, Edward", "Line"),
    ("Rakivnenko, Felix", "Line"),
    ("Ramos, Vicente", "Skill"),
    ("Rueda Franco, Ared", "Line"),
    ("Salas, Xavier", "Big Skill"),
    ("Sanft, Joseph", "Line"),
    ("Scott, George", "Big Skill"),
    ("Sokol, Zachary", "Skill"),
    ("Stephens, Terrance", "Skill"),
    ("Tahaafe, Sione", "Line"),
    ("Talamoa, Cameron", "Line"),
    ("Talamoa, Panapa", "Big Skill"),
    ("Tau, Kini", "Big Skill"),
    ("Taufa, Soane", "Line"),
    ("Toilolo, Justice", "Line"),
    ("Vainikolo, Michael", "Line"),
    ("Valdes, Eddie", "Line"),
    ("Van der Laan, Connor", "Big Skill"),
    ("Vele, Isiah", "Line"),
    ("Villegas-Maldonado, Angel", "Line"),
    ("Vuchic, Alex", "Line"),
    ("Weintz, Leif", "Big Skill"),
    ("Xocua, Armando", "Big Skill"),
    ("Yoshida, Kaito", "Skill"),
    ("Zaldana, Nirmal", "Line")
]

METRICS = [
    "Body Weight (lbs)",
    "Bench Press (lbs)",
    "Back Squat (lbs)",
    "Hex Bar Deadlift (lbs)",
    "Flying 10 Sprint (seconds)",
    "Vertical Jump (inches)",
    "Power Clean (lbs)"
]

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'master_data' not in st.session_state:
    roster_df = pd.DataFrame(ROSTER_DATA, columns=['Name', 'Position'])
    st.session_state.master_data = roster_df

if 'weekly_data' not in st.session_state:
    st.session_state.weekly_data = {}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def normalize_metric(value, metric_name, df_col):
    """Normalize metrics to 0-100 scale. Invert for Sprint (lower is better)."""
    if pd.isna(value):
        return 0
    
    col_values = df_col.dropna()
    if len(col_values) == 0:
        return 0
    
    min_val = col_values.min()
    max_val = col_values.max()
    
    if max_val == min_val:
        return 50
    
    # For Sprint times, lower is better, so invert the scale
    if "Sprint" in metric_name:
        normalized = 100 - ((value - min_val) / (max_val - min_val) * 100)
    else:
        normalized = ((value - min_val) / (max_val - min_val) * 100)
    
    return round(normalized, 1)

def get_athlete_data_for_week(athlete_name, week_num):
    """Get athlete metrics for a specific week."""
    if week_num not in st.session_state.weekly_data:
        return None
    
    week_df = st.session_state.weekly_data[week_num]
    athlete_row = week_df[week_df['Name'] == athlete_name]
    
    if athlete_row.empty:
        return None
    
    return athlete_row.iloc[0]

def calculate_body_weight_change(athlete_name, current_week):
    """Calculate % change in body weight from Week 1 to current week."""
    if 1 not in st.session_state.weekly_data or current_week not in st.session_state.weekly_data:
        return None
    
    week1_data = get_athlete_data_for_week(athlete_name, 1)
    current_data = get_athlete_data_for_week(athlete_name, current_week)
    
    if week1_data is None or current_data is None:
        return None
    
    if 'Body Weight (lbs)' not in week1_data or 'Body Weight (lbs)' not in current_data:
        return None
    
    week1_weight = week1_data['Body Weight (lbs)']
    current_weight = current_data['Body Weight (lbs)']
    
    if pd.isna(week1_weight) or pd.isna(current_weight) or week1_weight == 0:
        return None
    
    pct_change = ((current_weight - week1_weight) / week1_weight) * 100
    return round(pct_change, 2)

def get_position_average(position, week_num, metric):
    """Calculate average metric for a position group."""
    if week_num not in st.session_state.weekly_data:
        return None
    
    week_df = st.session_state.weekly_data[week_num]
    master_df = st.session_state.master_data
    
    # Get athletes in this position
    position_athletes = master_df[master_df['Position'] == position]['Name'].tolist()
    
    # Filter week data for these athletes
    position_data = week_df[week_df['Name'].isin(position_athletes)]
    
    if metric in position_data.columns:
        return position_data[metric].mean()
    
    return None

def get_team_best(week_num, metric):
    """Get team best for a metric."""
    if week_num not in st.session_state.weekly_data:
        return None
    
    week_df = st.session_state.weekly_data[week_num]
    
    if metric in week_df.columns:
        # For Sprint, best is minimum (fastest time)
        if "Sprint" in metric:
            return week_df[metric].min()
        else:
            return week_df[metric].max()
    
    return None

# ============================================================================
# MAIN APP HEADER
# ============================================================================
st.markdown("""
<div class="dashboard-header">
    <h1>🏈 Menlo College</h1>
    <h2 class="gold-accent">Student-Athlete Health, Wellness & Performance</h2>
    <p style="font-size: 14px; margin-top: 10px;">NCAA Division II • Football Performance Tracking</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
st.sidebar.image("https://via.placeholder.com/300x100/002855/F3C363?text=MENLO+OAKS", use_container_width=True)
st.sidebar.markdown("### 📊 Navigation")

page = st.sidebar.radio(
    "Select Page:",
    ["📋 Data Input & Roster", "📈 Progress Tracker", "🕸️ Spider Graph", "🎴 Player Card"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Athletes:** {len(ROSTER_DATA)}")
st.sidebar.markdown(f"**Weeks Tracked:** {len(st.session_state.weekly_data)}/12")
st.sidebar.markdown("---")
st.sidebar.markdown("*Developed for Menlo College Athletics*")

# ============================================================================
# TAB A: DATA INPUT & ROSTER
# ============================================================================
if page == "📋 Data Input & Roster":
    st.header("📋 Data Input & Roster Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📤 Upload Weekly Performance Data")
        
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel file with athlete performance data",
            type=['csv', 'xlsx'],
            help="File should contain columns: Name, Body Weight (lbs), Bench Press (lbs), etc."
        )
        
        week_number = st.selectbox(
            "Select Week Number",
            options=list(range(1, 13)),
            help="Choose which week this data represents (Week 1-12)"
        )
        
        if uploaded_file is not None:
            try:
                # Read the uploaded file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ File loaded successfully! {len(df)} records found.")
                
                # Preview the data
                with st.expander("👀 Preview Uploaded Data"):
                    st.dataframe(df.head(10), use_container_width=True)
                
                # Validate required columns
                required_cols = ['Name']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                else:
                    if st.button(f"✅ Confirm & Save Week {week_number} Data", type="primary"):
                        # Store in session state
                        st.session_state.weekly_data[week_number] = df
                        st.success(f"🎉 Week {week_number} data saved successfully!")
                        st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
    
    with col2:
        st.subheader("📊 Data Upload Status")
        
        for week in range(1, 13):
            if week in st.session_state.weekly_data:
                st.markdown(f"✅ **Week {week}** - {len(st.session_state.weekly_data[week])} records")
            else:
                st.markdown(f"⬜ **Week {week}** - No data")
    
    st.markdown("---")
    
    # Display Master Roster
    st.subheader("👥 Master Roster (110 Athletes)")
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        position_filter = st.multiselect(
            "Filter by Position",
            options=["Line", "Big Skill", "Skill"],
            default=["Line", "Big Skill", "Skill"]
        )
    
    with col2:
        search_name = st.text_input("🔍 Search by Name", "")
    
    roster_df = st.session_state.master_data.copy()
    
    # Apply filters
    roster_df = roster_df[roster_df['Position'].isin(position_filter)]
    if search_name:
        roster_df = roster_df[roster_df['Name'].str.contains(search_name, case=False, na=False)]
    
    # Display counts by position
    st.markdown("**Position Distribution:**")
    pos_counts = st.session_state.master_data['Position'].value_counts()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Line", pos_counts.get('Line', 0))
    with col2:
        st.metric("Big Skill", pos_counts.get('Big Skill', 0))
    with col3:
        st.metric("Skill", pos_counts.get('Skill', 0))
    
    st.dataframe(
        roster_df.reset_index(drop=True),
        use_container_width=True,
        height=400
    )
    
    # Download template
    st.markdown("---")
    st.subheader("📥 Download Data Entry Template")
    
    template_df = pd.DataFrame({
        'Name': [name for name, _ in ROSTER_DATA],
        'Body Weight (lbs)': [''] * len(ROSTER_DATA),
        'Bench Press (lbs)': [''] * len(ROSTER_DATA),
        'Back Squat (lbs)': [''] * len(ROSTER_DATA),
        'Hex Bar Deadlift (lbs)': [''] * len(ROSTER_DATA),
        'Flying 10 Sprint (seconds)': [''] * len(ROSTER_DATA),
        'Vertical Jump (inches)': [''] * len(ROSTER_DATA),
        'Power Clean (lbs)': [''] * len(ROSTER_DATA)
    })
    
    csv = template_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV Template",
        data=csv,
        file_name="menlo_performance_template.csv",
        mime="text/csv"
    )

# ============================================================================
# TAB B: PROGRESS TRACKER
# ============================================================================
elif page == "📈 Progress Tracker":
    st.header("📈 Individual Progress Tracker")
    
    if not st.session_state.weekly_data:
        st.warning("⚠️ No weekly data available. Please upload data in the 'Data Input & Roster' tab.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            selected_athlete = st.selectbox(
                "🔍 Select Athlete",
                options=sorted([name for name, _ in ROSTER_DATA]),
                help="Search and select an athlete to view their progress"
            )
        
        with col2:
            selected_metric = st.selectbox(
                "📊 Select Metric",
                options=METRICS,
                help="Choose which performance metric to track"
            )
        
        # Get athlete's position
        athlete_position = st.session_state.master_data[
            st.session_state.master_data['Name'] == selected_athlete
        ]['Position'].values[0]
        
        st.markdown(f"**Position:** {athlete_position}")
        
        # Gather data across weeks
        weeks = sorted(st.session_state.weekly_data.keys())
        values = []
        week_labels = []
        
        for week in weeks:
            data = get_athlete_data_for_week(selected_athlete, week)
            if data is not None and selected_metric in data:
                value = data[selected_metric]
                if not pd.isna(value):
                    values.append(value)
                    week_labels.append(f"Week {week}")
        
        if not values:
            st.info(f"ℹ️ No data available for {selected_athlete} - {selected_metric}")
        else:
            # Create line chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=week_labels,
                y=values,
                mode='lines+markers',
                name=selected_athlete,
                line=dict(color='#002855', width=3),
                marker=dict(size=10, color='#F3C363', line=dict(width=2, color='#002855'))
            ))
            
            fig.update_layout(
                title=f"{selected_athlete} - {selected_metric} Progress",
                xaxis_title="Week",
                yaxis_title=selected_metric,
                hovermode='x unified',
                plot_bgcolor='white',
                height=500,
                font=dict(size=14),
                xaxis=dict(showgrid=True, gridcolor='#E5E5E5'),
                yaxis=dict(showgrid=True, gridcolor='#E5E5E5')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Stats summary
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Starting Value", f"{values[0]:.2f}")
            with col2:
                st.metric("Current Value", f"{values[-1]:.2f}")
            with col3:
                change = values[-1] - values[0]
                st.metric("Change", f"{change:+.2f}")
            with col4:
                pct_change = ((values[-1] - values[0]) / values[0] * 100) if values[0] != 0 else 0
                st.metric("% Change", f"{pct_change:+.1f}%")
            
            # Special handling for Body Weight
            if selected_metric == "Body Weight (lbs)":
                st.markdown("---")
                st.subheader("💪 Body Weight Analysis")
                
                if 1 in st.session_state.weekly_data:
                    latest_week = max(weeks)
                    bw_change = calculate_body_weight_change(selected_athlete, latest_week)
                    
                    if bw_change is not None:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric(
                                "Body Weight Change from Week 1",
                                f"{bw_change:+.2f}%",
                                delta=f"{values[-1] - values[0]:+.1f} lbs"
                            )
                        
                        with col2:
                            if abs(bw_change) < 2:
                                status = "✅ Stable"
                                color = "green"
                            elif bw_change > 0:
                                status = "📈 Gaining"
                                color = "blue"
                            else:
                                status = "📉 Losing"
                                color = "orange"
                            
                            st.markdown(f"**Status:** <span style='color:{color}; font-size:18px;'>{status}</span>", unsafe_allow_html=True)

# ============================================================================
# TAB C: SPIDER GRAPH
# ============================================================================
elif page == "🕸️ Spider Graph":
    st.header("🕸️ Performance Spider Graph")
    
    if not st.session_state.weekly_data:
        st.warning("⚠️ No weekly data available. Please upload data in the 'Data Input & Roster' tab.")
    else:
        # Select week for comparison
        available_weeks = sorted(st.session_state.weekly_data.keys())
        selected_week = st.selectbox("📅 Select Week for Comparison", options=available_weeks)
        
        # Comparison mode toggle
        comparison_mode = st.radio(
            "Comparison Mode",
            ["Individual vs. Group", "Head-to-Head"],
            horizontal=True
        )
        
        st.markdown("---")
        
        if comparison_mode == "Individual vs. Group":
            selected_athlete = st.selectbox(
                "🔍 Select Athlete",
                options=sorted([name for name, _ in ROSTER_DATA])
            )
            
            # Get athlete's position
            athlete_position = st.session_state.master_data[
                st.session_state.master_data['Name'] == selected_athlete
            ]['Position'].values[0]
            
            st.markdown(f"**Position:** {athlete_position}")
            
            # Get data
            athlete_data = get_athlete_data_for_week(selected_athlete, selected_week)
            
            if athlete_data is None:
                st.info(f"ℹ️ No data available for {selected_athlete} in Week {selected_week}")
            else:
                week_df = st.session_state.weekly_data[selected_week]
                
                # Prepare data for radar chart
                categories = []
                athlete_values = []
                position_avg_values = []
                team_best_values = []
                
                for metric in METRICS:
                    if metric in athlete_data and not pd.isna(athlete_data[metric]):
                        categories.append(metric.replace(' (lbs)', '').replace(' (seconds)', '').replace(' (inches)', ''))
                        
                        # Normalize values
                        athlete_norm = normalize_metric(athlete_data[metric], metric, week_df[metric])
                        athlete_values.append(athlete_norm)
                        
                        # Position average
                        pos_avg = get_position_average(athlete_position, selected_week, metric)
                        if pos_avg is not None:
                            pos_avg_norm = normalize_metric(pos_avg, metric, week_df[metric])
                            position_avg_values.append(pos_avg_norm)
                        else:
                            position_avg_values.append(0)
                        
                        # Team best
                        team_best = get_team_best(selected_week, metric)
                        if team_best is not None:
                            team_best_norm = normalize_metric(team_best, metric, week_df[metric])
                            team_best_values.append(team_best_norm)
                        else:
                            team_best_values.append(0)
                
                if not categories:
                    st.info("ℹ️ No metrics available for comparison")
                else:
                    # Create radar chart
                    fig = go.Figure()
                    
                    # Athlete
                    fig.add_trace(go.Scatterpolar(
                        r=athlete_values,
                        theta=categories,
                        fill='toself',
                        name=selected_athlete,
                        line=dict(color='#002855', width=2),
                        fillcolor='rgba(0, 40, 85, 0.3)'
                    ))
                    
                    # Position Average
                    fig.add_trace(go.Scatterpolar(
                        r=position_avg_values,
                        theta=categories,
                        fill='toself',
                        name=f'{athlete_position} Average',
                        line=dict(color='#F3C363', width=2, dash='dash'),
                        fillcolor='rgba(243, 195, 99, 0.2)'
                    ))
                    
                    # Team Best
                    fig.add_trace(go.Scatterpolar(
                        r=team_best_values,
                        theta=categories,
                        fill='toself',
                        name='Team Best',
                        line=dict(color='#28A745', width=2, dash='dot'),
                        fillcolor='rgba(40, 167, 69, 0.1)'
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 100],
                                tickfont=dict(size=12)
                            )
                        ),
                        showlegend=True,
                        title=f"{selected_athlete} Performance Profile - Week {selected_week}",
                        height=600,
                        font=dict(size=14)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display raw values
                    with st.expander("📊 View Normalized Scores (0-100)"):
                        comparison_df = pd.DataFrame({
                            'Metric': categories,
                            selected_athlete: athlete_values,
                            f'{athlete_position} Avg': position_avg_values,
                            'Team Best': team_best_values
                        })
                        st.dataframe(comparison_df, use_container_width=True)
        
        else:  # Head-to-Head
            st.markdown("### Select Athletes to Compare (2-4 athletes)")
            
            selected_athletes = st.multiselect(
                "🔍 Select Athletes",
                options=sorted([name for name, _ in ROSTER_DATA]),
                max_selections=4,
                default=[]
            )
            
            if len(selected_athletes) < 2:
                st.info("ℹ️ Please select at least 2 athletes for head-to-head comparison")
            else:
                # Color palette for multiple athletes
                colors = ['#002855', '#F3C363', '#DC3545', '#28A745']
                
                fig = go.Figure()
                
                all_categories = []
                
                for idx, athlete in enumerate(selected_athletes):
                    athlete_data = get_athlete_data_for_week(athlete, selected_week)
                    
                    if athlete_data is not None:
                        week_df = st.session_state.weekly_data[selected_week]
                        categories = []
                        values = []
                        
                        for metric in METRICS:
                            if metric in athlete_data and not pd.isna(athlete_data[metric]):
                                cat_name = metric.replace(' (lbs)', '').replace(' (seconds)', '').replace(' (inches)', '')
                                categories.append(cat_name)
                                
                                # Normalize
                                norm_value = normalize_metric(athlete_data[metric], metric, week_df[metric])
                                values.append(norm_value)
                        
                        if categories:
                            all_categories = categories
                            
                            fig.add_trace(go.Scatterpolar(
                                r=values,
                                theta=categories,
                                fill='toself',
                                name=athlete,
                                line=dict(color=colors[idx % len(colors)], width=2),
                                fillcolor=f'rgba({int(colors[idx % len(colors)][1:3], 16)}, {int(colors[idx % len(colors)][3:5], 16)}, {int(colors[idx % len(colors)][5:7], 16)}, 0.2)'
                            ))
                
                if all_categories:
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 100],
                                tickfont=dict(size=12)
                            )
                        ),
                        showlegend=True,
                        title=f"Head-to-Head Comparison - Week {selected_week}",
                        height=600,
                        font=dict(size=14)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("ℹ️ No comparable data available for selected athletes")

# ============================================================================
# TAB D: PLAYER CARD
# ============================================================================
elif page == "🎴 Player Card":
    st.header("🎴 Printable Player Card")
    
    if not st.session_state.weekly_data:
        st.warning("⚠️ No weekly data available. Please upload data in the 'Data Input & Roster' tab.")
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_athlete = st.selectbox(
                "🔍 Select Athlete",
                options=sorted([name for name, _ in ROSTER_DATA])
            )
        
        available_weeks = sorted(st.session_state.weekly_data.keys())
        
        with col2:
            start_week = st.selectbox("📅 Start Week", options=available_weeks, index=0)
        
        with col3:
            end_week = st.selectbox(
                "📅 End Week",
                options=[w for w in available_weeks if w >= start_week],
                index=len([w for w in available_weeks if w >= start_week]) - 1
            )
        
        # Get athlete info
        athlete_position = st.session_state.master_data[
            st.session_state.master_data['Name'] == selected_athlete
        ]['Position'].values[0]
        
        start_data = get_athlete_data_for_week(selected_athlete, start_week)
        end_data = get_athlete_data_for_week(selected_athlete, end_week)
        
        if start_data is None or end_data is None:
            st.info(f"ℹ️ Data not available for selected week range")
        else:
            # Print button
            st.markdown('<div class="no-print">', unsafe_allow_html=True)
            if st.button("🖨️ Print Player Card", type="primary"):
                st.info("💡 Use your browser's Print function (Ctrl+P or Cmd+P) to print or save as PDF")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Player Card Layout
            st.markdown('<div class="print-card">', unsafe_allow_html=True)
            
            # Header
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #002855 0%, #003366 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px;">
                <h1 style="color: white; margin: 0;">{selected_athlete}</h1>
                <p style="font-size: 20px; color: #F3C363; margin: 5px 0;">Position: {athlete_position}</p>
                <p style="font-size: 16px; margin: 5px 0;">Performance Report: Week {start_week} to Week {end_week}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Current stats
            if 'Body Weight (lbs)' in end_data and not pd.isna(end_data['Body Weight (lbs)']):
                st.markdown(f"**Current Weight (Week {end_week}):** {end_data['Body Weight (lbs)']} lbs")
            
            st.markdown("### 📊 Performance Metrics")
            
            # Progress table
            progress_data = []
            
            for metric in METRICS:
                if metric in start_data and metric in end_data:
                    start_val = start_data[metric]
                    end_val = end_data[metric]
                    
                    if not pd.isna(start_val) and not pd.isna(end_val):
                        diff = end_val - start_val
                        pct_change = (diff / start_val * 100) if start_val != 0 else 0
                        
                        progress_data.append({
                            'Metric': metric,
                            f'Week {start_week}': f"{start_val:.2f}",
                            f'Week {end_week}': f"{end_val:.2f}",
                            'Change': f"{diff:+.2f}",
                            '% Change': f"{pct_change:+.1f}%"
                        })
            
            if progress_data:
                progress_df = pd.DataFrame(progress_data)
                st.dataframe(progress_df, use_container_width=True, hide_index=True)
            else:
                st.info("No comparable metrics available")
            
            # Body weight trend
            if 'Body Weight (lbs)' in start_data:
                st.markdown("### 💪 Body Weight Trend")
                
                # Gather body weight data
                weeks_range = [w for w in available_weeks if start_week <= w <= end_week]
                bw_values = []
                bw_weeks = []
                
                for week in weeks_range:
                    data = get_athlete_data_for_week(selected_athlete, week)
                    if data is not None and 'Body Weight (lbs)' in data:
                        bw = data['Body Weight (lbs)']
                        if not pd.isna(bw):
                            bw_values.append(bw)
                            bw_weeks.append(f"Week {week}")
                
                if bw_values:
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=bw_weeks,
                        y=bw_values,
                        mode='lines+markers',
                        line=dict(color='#002855', width=2),
                        marker=dict(size=8, color='#F3C363')
                    ))
                    
                    fig.update_layout(
                        title="Body Weight Progress",
                        xaxis_title="Week",
                        yaxis_title="Weight (lbs)",
                        height=300,
                        plot_bgcolor='white',
                        xaxis=dict(showgrid=True, gridcolor='#E5E5E5'),
                        yaxis=dict(showgrid=True, gridcolor='#E5E5E5')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            # Footer
            st.markdown("---")
            st.markdown(f"""
            <div style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
                <p>Menlo College Athletics • Student-Athlete Health, Wellness & Performance</p>
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px; padding: 20px;">
    <p><strong>Menlo College Oaks Football</strong> • NCAA Division II</p>
    <p>Assistant Director of Athletics for Student Athlete Health, Wellness and Performance</p>
    <p style="color: #002855;">🏈 Building Champions On and Off the Field 🏈</p>
</div>
""", unsafe_allow_html=True)
