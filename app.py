import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="upay Merchant Copilot", page_icon="💳", layout="wide"
)

st.title("💳 upay Merchant Growth & Churn Copilot")
st.caption("AI-Powered Predictive Risk & Field Agent Action Advisor")


# Load Datasets
@st.cache_data
def load_data():
  df_feat = pd.read_csv("merchant_churn_growth_features.csv")
  try:
    df_copilot = pd.read_csv("merchant_copilot_reports.csv")
  except Exception:
    df_copilot = pd.DataFrame()
  return df_feat, df_copilot


df_feat, df_copilot = load_data()

# Sidebar Directory & Filtering
st.sidebar.header("Merchant Search & Filters")
categories = sorted(df_feat["business_category"].dropna().unique().tolist())
category_filter = st.sidebar.multiselect(
    "Filter by Category", options=categories
)

filtered_df = df_feat.copy()
if category_filter:
  filtered_df = filtered_df[
      filtered_df["business_category"].isin(category_filter)
  ]

merchant_names = sorted(filtered_df["User_Name"].dropna().unique().tolist())
if not merchant_names:
  st.warning("No merchants match the selected filters.")
  st.stop()

selected_merchant_name = st.sidebar.selectbox(
    "Select Merchant Account", options=merchant_names
)

# Fetch Selected Merchant Metrics
merchant = df_feat[df_feat["User_Name"] == selected_merchant_name].iloc[0]

# High-Level Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Category", str(merchant["business_category"]))
col2.metric("30D Revenue", f"BDT {merchant['vol_last_30d']:,.2f}")
col3.metric("30D Growth Rate", f"{merchant['volume_growth_30d']*100:.1f}%")
col4.metric("Inactivity Recency", f"{int(merchant['recency_days'])} days")

st.divider()

# Main Display Tabs
tab1, tab2 = st.tabs(
    ["🤖 AI Copilot Advisory Report", "📊 Detailed Feature Profile"]
)

with tab1:
  st.subheader(f"Field Agent Copilot Report: {selected_merchant_name}")

  has_report = False
  if not df_copilot.empty and "Merchant_Name" in df_copilot.columns:
    matched_report = df_copilot[
        df_copilot["Merchant_Name"] == selected_merchant_name
    ]
    if not matched_report.empty:
      report_text = matched_report["AI_Copilot_Report"].values[0]
      st.markdown(report_text)
      has_report = True

  if not has_report:
    st.success("🟢 Stable Merchant Health")
    st.write(
        "This merchant is performing within healthy limits. No critical field"
        " interventions required."
    )

with tab2:
  st.subheader("Engineered Feature Breakdown")
  st.json({
      "Merchant Name": str(merchant["User_Name"]),
      "Business Category": str(merchant["business_category"]),
      "Country": str(merchant["country"]),
      "Total Lifetime Transactions": int(merchant["total_transactions"]),
      "Total Volume (BDT)": float(merchant["total_volume"]),
      "Average Basket Size (BDT)": float(merchant["avg_basket_size"]),
      "Digital Payment Usage Ratio": (
          f"{merchant['digital_pay_ratio']*100:.1f}%"
      ),
      "30-Day Volume Growth": f"{merchant['volume_growth_30d']*100:.1f}%",
      "Inactivity Recency (Days)": int(merchant["recency_days"]),
      "Churn Risk Flag": int(merchant["is_churn_risk"]),
      "Churn Probability Score": (
          f"{merchant['churn_risk_probability']*100:.1f}%"
      ),
  })
