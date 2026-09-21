import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="CryptoGuard AI | AML Detection", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    h1 { color: #00FFCC; }
    .stMetric { background-color: #1E2130; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("CryptoGuard AI")
    st.markdown("###  AML Engine")
    st.divider()
    selected_model = st.selectbox("Select Active Model", ["Isolation Forest", "DBSCAN", "Random Forest"])
    # Hum is threshold variable ko donut chart filter karne ke liye use karenge
    anomaly_threshold = st.slider("Anomaly Threshold", min_value=0.01, max_value=0.99, value=0.80, step=0.01)
    st.divider()

st.title("🛡️ Crypto Fraud & AML Detection Dashboard")

# 1. Generate dummy data (Replace this with your real df later)
np.random.seed(42) # Seed taake dots ajeeb tarhan jump na karein
df = pd.DataFrame({
    'time': range(100),
    'transaction_volume': np.random.normal(500, 100, 100),
    'risk_score': np.random.uniform(0, 1, 100)
})

# 2. Dynamic Calculations based on Slider Threshold
# Agar risk_score threshold se zyada hai toh Illicit, agar thora kam hai toh Suspicious
illicit_count = len(df[df['risk_score'] >= anomaly_threshold])
suspicious_count = len(df[(df['risk_score'] >= anomaly_threshold - 0.2) & (df['risk_score'] < anomaly_threshold)])
legitimate_count = len(df) - illicit_count - suspicious_count

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", len(df))
col2.metric("Illicit Nodes Detected", illicit_count, delta=f"Threshold > {anomaly_threshold}", delta_color="inverse")
col3.metric("Suspicious Nodes", suspicious_count)
col4.metric("Active Model", selected_model)

st.divider()

chart_col1, chart_col2 = st.columns([2, 1])

with chart_col1:
    st.subheader("Transaction Volume vs Risk Score")
    fig = px.scatter(
        df, x='time', y='transaction_volume', color='risk_score',
        color_continuous_scale='Reds', template='plotly_dark'
    )
    # Threshold ki line draw karein plot par
    fig.add_hline(y=anomaly_threshold * 1000, line_dash="dot", line_color="#00FFCC", annotation_text="Threshold")
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=400)
    st.plotly_chart(fig, use_container_width=True)

with chart_col2:
    st.subheader("Risk Distribution")
    # Ab donut chart slider ke data ke hisaab se update hoga
    labels = ['Legitimate', 'Suspicious', 'Illicit']
    values = [legitimate_count, suspicious_count, illicit_count]
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=['#4169E1', '#FF8C00', '#DC143C'])])
    fig_pie.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=30, b=0), height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

tab1, tab2, tab3 = st.tabs(["📋 Investigation Queue", "🕸️ Network Graph (NetworkX)", "⚙️ Model Explanations"])

with tab1:
    # Filtered table dikhayein jo illicit hain
    st.write("### High Risk Transactions")
    st.dataframe(df[df['risk_score'] >= anomaly_threshold], use_container_width=True)

with tab2:
    st.write("### Transaction Node Network")
    # NetworkX se ek basic graph bana kar render kar rahe hain
    G = nx.erdos_renyi_graph(n=25, p=0.1)
    fig_nx, ax = plt.subplots(figsize=(10, 4))
    fig_nx.patch.set_facecolor('#0E1117') # Match dark theme
    nx.draw(G, ax=ax, node_color='#00FFCC', edge_color='gray', node_size=300, with_labels=True)
    st.pyplot(fig_nx)

with tab3:
    st.write(f"### Feature Importance for {selected_model}")
    # Model explanation ke liye bar chart
    importance_df = pd.DataFrame({
        'Feature': ['Transaction Volume', 'Time Frequency', 'Node Degree', 'Velocity'],
        'Importance': [0.45, 0.25, 0.20, 0.10]
    })
    fig_bar = px.bar(importance_df, x='Importance', y='Feature', orientation='h', template='plotly_dark', color='Importance')
    st.plotly_chart(fig_bar, use_container_width=True)