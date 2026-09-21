import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="CryptoGuard AI | AML Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# Advanced CSS Styling
# -------------------------
st.markdown("""
<style>
    /* Main Background */
    .main { background-color: #0E1117; }
    
    /* Headers */
    h1, h2, h3 { color: #00FFCC !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #1E2130;
        border: 1px solid #2D3142;
        padding: 5% 10% 5% 10%;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Divider */
    hr { border-color: #2D3142; }
    
    /* Custom Badges for Explainability */
    .risk-badge {
        padding: 5px 12px;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        font-size: 0.9em;
    }
    .badge-high { background-color: #FF4B4B; }
    .badge-medium { background-color: #FFA500; }
    .badge-low { background-color: #00C853; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Color Palette Definition
# -------------------------
RISK_COLORS = {
    "HIGH": "#FF4B4B",
    "MEDIUM": "#FFA500",
    "LOW": "#00C853"
}

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/processed/final_risk_results.csv")
        return df
    except FileNotFoundError:
        st.error("Data file not found! Please check the path.")
        return pd.DataFrame()

df = load_data()

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/shield.png", width=60) # Placeholder logo
    st.title("CryptoGuard AI")
    st.markdown("### AML Monitoring Engine")
    st.caption("Real-time blockchain transaction screening.")
    st.divider()

    selected_level = st.selectbox(
        "⚡ Risk Filter",
        ["ALL", "HIGH", "MEDIUM", "LOW"]
    )
    st.divider()
    st.info("System Status: **Active** ✅")

# -------------------------
# Filter Data
# -------------------------
if selected_level == "ALL":
    filtered_df = df
else:
    filtered_df = df[df["final_risk_level"] == selected_level]

# -------------------------
# Header & Top Metrics
# -------------------------
st.title("🛡️ Crypto Fraud & AML Detection Dashboard")
st.markdown("Monitor, analyze, and investigate suspicious cryptocurrency transaction networks.")
st.write("") # Spacer

if not df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Transactions", f"{len(df):,}")
    col2.metric("High Risk Alerts", len(df[df["final_risk_level"]=="HIGH"]))
    col3.metric("Medium Risk Alerts", len(df[df["final_risk_level"]=="MEDIUM"]))
    col4.metric("Average Risk Score", f"{df['final_risk_score'].mean():.2f}")

    st.divider()

    # -------------------------
    # Visualizations Row
    # -------------------------
    chart1, chart2 = st.columns([1, 1.5])

    with chart1:
        st.subheader("Risk Level Distribution")
        risk_count = df["final_risk_level"].value_counts().reset_index()
        risk_count.columns = ['Risk Level', 'Count']
        
        fig1 = px.pie(
            risk_count, 
            values='Count', 
            names='Risk Level',
            hole=0.6,
            color='Risk Level',
            color_discrete_map=RISK_COLORS,
            template="plotly_dark"
        )
        fig1.update_layout(margin=dict(t=30, b=0, l=0, r=0), showlegend=True)
        st.plotly_chart(fig1, use_container_width=True)

    with chart2:
        st.subheader("Risk Score Distribution")
        fig2 = px.histogram(
            df, 
            x="final_risk_score", 
            nbins=40,
            color="final_risk_level",
            color_discrete_map=RISK_COLORS,
            template="plotly_dark",
            labels={'final_risk_score': 'Risk Score (0-100)'}
        )
        fig2.update_layout(margin=dict(t=30, b=0, l=0, r=0), barmode='stack')
        st.plotly_chart(fig2, use_container_width=True)

    # -------------------------
    # Main Investigation Tabs
    # -------------------------
    st.write("")
    tab1, tab2, tab3 = st.tabs(["📋 Investigation Queue", "🕸️ Network Analysis", "⚙️ AI Explainability"])

    # --- TAB 1: Data Queue ---
    with tab1:
        st.subheader("Suspicious Transactions Queue")
        
        # Function to color code dataframe rows
        def style_risk(val):
            color = RISK_COLORS.get(val, "white")
            return f'color: {color}; font-weight: bold'
            
        display_cols = ["txId", "final_risk_score", "final_risk_level", "priority"]
        styled_df = filtered_df[display_cols].style.map(style_risk, subset=['final_risk_level'])
        
        st.dataframe(styled_df, use_container_width=True, height=400)

    # --- TAB 2: Network Graph ---
    with tab2:
        st.subheader("Transaction Network View")
        
        if len(filtered_df) > 0:
            G = nx.Graph()
            sample = filtered_df.head(50)
            
            for _, row in sample.iterrows():
                G.add_node(row["txId"])
                
            nodes = list(G.nodes)
            for i in range(len(nodes)-1):
                G.add_edge(nodes[i], nodes[i+1])

            # Themed Matplotlib Graph
            fig_net, ax = plt.subplots(figsize=(10, 5))
            fig_net.patch.set_facecolor('#0E1117')
            ax.set_facecolor('#0E1117')
            
            # Styling nodes and edges
            nx.draw(
                G, ax=ax, 
                with_labels=False, 
                node_size=150, 
                node_color='#00FFCC', 
                edge_color='#2D3142', 
                linewidths=1,
                alpha=0.8
            )
            st.pyplot(fig_net)
        else:
            st.info("No data available for network visualization based on current filters.")

    # --- TAB 3: Explainability ---
    with tab3:
        st.subheader("Why was this transaction flagged?")
        
        if len(filtered_df) > 0:
            col_sel, col_det = st.columns([1, 2])
            
            with col_sel:
                selected_tx = st.selectbox("Search Transaction ID", filtered_df["txId"])
                row = filtered_df[filtered_df["txId"] == selected_tx].iloc[0]
                
                st.metric("Risk Score", f"{row['final_risk_score']:.2f}")
                
                # Custom HTML Badge for Risk Level
                badge_class = f"badge-{row['final_risk_level'].lower()}"
                st.markdown(f"**Risk Level:** <span class='risk-badge {badge_class}'>{row['final_risk_level']}</span>", unsafe_allow_html=True)
                st.write(f"**Priority Queue:** {row['priority']}")

            with col_det:
                st.markdown("#### 🚨 Flagged Suspicious Behaviors")
                
                reasons = []
                # Safely checking columns in case they don't exist in your specific CSV
                if "high_amount_flag" in row and row["high_amount_flag"] == 1:
                    reasons.append("High transaction amount anomaly detected.")
                if "night_transaction" in row and row["night_transaction"] == 1:
                    reasons.append("Unusual night-time transaction activity.")
                if "transaction_velocity" in row and row["transaction_velocity"] > 10:
                    reasons.append(f"High velocity ({row['transaction_velocity']} tx/hr).")
                if "degree" in row and row["degree"] > 20:
                    reasons.append("Excessive network connections (Hub Node).")
                    
                if not reasons:
                    st.success("No major suspicious indicators found.")
                else:
                    for reason in reasons:
                        st.error(f"⚠️ {reason}")
        else:
            st.warning("No transactions available to explain for this filter.")