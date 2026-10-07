import os
import time
import pandas as pd


def generate_pipeline_data():
  """Generates features and copilot advisory reports CSVs for local testing and deployment."""
  print("1. Generating merchant feature dataset...")

  data = [
      {
          "User_Name": "Ava Allen",
          "business_category": "Grocery",
          "country": "Bangladesh",
          "total_transactions": 340,
          "total_volume": 145000.0,
          "vol_last_30d": 12450.0,
          "avg_basket_size": 426.47,
          "digital_pay_ratio": 0.35,
          "volume_growth_30d": -0.374,
          "recency_days": 12,
          "is_churn_risk": 1,
          "churn_risk_probability": 0.974,
      },
      {
          "User_Name": "Farhan Ahmed",
          "business_category": "Electronics",
          "country": "Bangladesh",
          "total_transactions": 85,
          "total_volume": 89000.0,
          "vol_last_30d": 4200.0,
          "avg_basket_size": 1047.05,
          "digital_pay_ratio": 0.22,
          "volume_growth_30d": -0.521,
          "recency_days": 18,
          "is_churn_risk": 1,
          "churn_risk_probability": 0.928,
      },
      {
          "User_Name": "Rahima Begum",
          "business_category": "Clothing",
          "country": "Bangladesh",
          "total_transactions": 110,
          "total_volume": 45000.0,
          "vol_last_30d": 2100.0,
          "avg_basket_size": 409.09,
          "digital_pay_ratio": 0.15,
          "volume_growth_30d": -0.683,
          "recency_days": 21,
          "is_churn_risk": 1,
          "churn_risk_probability": 0.951,
      },
      {
          "User_Name": "Tanvir Hossain",
          "business_category": "Restaurant",
          "country": "Bangladesh",
          "total_transactions": 290,
          "total_volume": 98000.0,
          "vol_last_30d": 8900.0,
          "avg_basket_size": 337.93,
          "digital_pay_ratio": 0.40,
          "volume_growth_30d": -0.410,
          "recency_days": 14,
          "is_churn_risk": 1,
          "churn_risk_probability": 0.885,
      },
      {
          "User_Name": "Oliver Allen",
          "business_category": "Home & Kitchen",
          "country": "Bangladesh",
          "total_transactions": 210,
          "total_volume": 67000.0,
          "vol_last_30d": 8528.66,
          "avg_basket_size": 319.04,
          "digital_pay_ratio": 0.65,
          "volume_growth_30d": -0.312,
          "recency_days": 0,
          "is_churn_risk": 0,
          "churn_risk_probability": 0.182,
      },
  ]

  df_features = pd.DataFrame(data)
  df_features.to_csv("merchant_churn_growth_features.csv", index=False)
  print("   Saved -> merchant_churn_growth_features.csv")

  print("2. Generating AI Copilot advisory reports...")
  high_risk = df_features[df_features["is_churn_risk"] == 1]
  reports = []

  for idx, row in high_risk.iterrows():
    report_text = f"""### ⚠️ CRITICAL CHURN RISK DIAGNOSIS
**Merchant Name:** {row['User_Name']}
**Category:** {row['business_category']}
**Churn Probability Score:** {row['churn_risk_probability']*100:.1f}%

---

### 🔍 Key Root Cause Analysis
1. **Transaction Velocity Decline:** 30-day transaction volume dropped by **{abs(row['volume_growth_30d'])*100:.1f}%**.
2. **Inactivity Spells:** Merchant has zero digital transactions over the past **{row['recency_days']} consecutive days**.
3. **Digital Ratio Decay:** Digital payment conversion ratio stands low at **{row['digital_pay_ratio']*100:.1f}%**.

---

### 🛠️ Field Agent Action Plan
* **Immediate Contact:** Schedule an in-person field agent visit within 24 hours.
* **Incentive Deployment:** Activate targeted zero-fee P2M transaction promotion for 14 days.
* **Terminal Support:** Verify QR code standee placement and troubleshoot any Soundbox device issues.
"""
    reports.append({
        "Merchant_Name": row["User_Name"],
        "Category": row["business_category"],
        "Country": row["country"],
        "Recency_Days": row["recency_days"],
        "Volume_Growth_30d": row["volume_growth_30d"],
        "Churn_Probability": row["churn_risk_probability"],
        "AI_Copilot_Report": report_text,
    })

  df_reports = pd.DataFrame(reports)
  df_reports.to_csv("merchant_copilot_reports.csv", index=False)
  print("   Saved -> merchant_copilot_reports.csv")
  print("\nData pipeline completed successfully.")


if __name__ == "__main__":
  generate_pipeline_data()
