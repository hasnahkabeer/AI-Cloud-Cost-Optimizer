
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Cloud Cost Optimisation Assistant",
    page_icon="☁️",
    layout="wide"
)

st.title("☁️ AI Cloud Cost Optimisation Assistant")
st.write("Analyse cloud expenditure and identify optimisation opportunities.")

uploaded_file = st.file_uploader(
    "Upload your cloud billing CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    required_columns = [
        "Month",
        "Service",
        "Usage_Hours",
        "Monthly_Cost_USD",
        "Utilisation_Percent"
    ]

    if not all(col in df.columns for col in required_columns):
        st.error("Your CSV is missing required columns.")
    else:
        st.success("Billing data uploaded successfully!")

        total_cost = df["Monthly_Cost_USD"].sum()
        service_cost = df.groupby("Service")["Monthly_Cost_USD"].sum()
        low_utilisation = df[df["Utilisation_Percent"] < 20]

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Cloud Cost", f"${total_cost:,.2f}")
        col2.metric("Highest Spending Service", service_cost.idxmax())
        col3.metric("Low Utilisation Records", len(low_utilisation))

        st.subheader("Billing Data")
        st.dataframe(df, use_container_width=True)

        st.subheader("Spending by Service")
        fig, ax = plt.subplots()
        service_cost.plot(kind="bar", ax=ax)
        ax.set_ylabel("Cost (USD)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Monthly Expenditure")
        monthly_cost = df.groupby("Month")["Monthly_Cost_USD"].sum()

        fig, ax = plt.subplots()
        monthly_cost.plot(kind="line", marker="o", ax=ax)
        ax.set_ylabel("Cost (USD)")
        ax.grid(True)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Underutilised Resources")
        st.dataframe(low_utilisation, use_container_width=True)

else:
    st.info("Upload your cloud billing CSV to begin.")
