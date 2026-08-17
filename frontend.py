import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:8000/api/v1"

st.set_page_config(page_title="FLYYY.AI | SaaS AI Governance", layout="wide")

st.title(" SaaS AI Discovery & Interaction Governance")
st.caption("Discover embedded AI in SaaS applications, manage asset inventory, and monitor AI security risks.")

# Sidebar Actions
st.sidebar.header("Controls & Operations")
if st.sidebar.button(" Run SaaS Discovery Scan"):
    try:
        res = requests.post(f"{API_BASE}/discovery/run")
        if res.status_code == 200:
            st.sidebar.success(f"Scan Finished: {res.json().get('new_assets_discovered')} new assets found.")
    except Exception as e:
        st.sidebar.error(f"Error connecting to backend: {e}")

tab1, tab2, tab3, tab4 = st.tabs([
    " Overview Dashboard", 
    " AI Asset Inventory", 
    " AI Interaction Logs",
    " Seed Mock Data"
])

# Tab 1: Overview
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    try:
        assets = requests.get(f"{API_BASE}/assets").json()
        interactions = requests.get(f"{API_BASE}/interactions").json()
        
        col1.metric("Discovered AI Assets", len(assets))
        col2.metric("Total Interactions Tracked", len(interactions))
        col3.metric("High Risk Flags", sum(1 for i in interactions if i.get("risk_flag") == "High Risk"))
        col4.metric("Pending Asset Reviews", sum(1 for a in assets if a.get("review_status") == "Pending Review"))
        
        st.subheader("SaaS Observability Coverage")
        if assets:
            df_assets = pd.DataFrame(assets)
            st.dataframe(df_assets[["saas_platform", "feature_name", "user_group", "user_count", "observability_level", "review_status"]], use_container_width=True)
    except Exception:
        st.warning("Start the FastAPI server at http://localhost:8000 to load live metrics.")

# Tab 2: Asset Inventory
with tab2:
    st.subheader("Discovered SaaS AI Capability Inventory")
    try:
        assets = requests.get(f"{API_BASE}/assets").json()
        for asset in assets:
            with st.expander(f"{asset['saas_platform']} - {asset['feature_name']} ({asset['review_status']})"):
                st.write(f"**User Scope:** {asset['user_group']} ({asset['user_count']} active users)")
                st.write(f"**Accessible Resources:** {asset['target_resources']}")
                st.write(f"**Discovery Source:** {asset['discovery_source']}")
                st.write(f"**Observability Constraint:** `{asset['observability_level']}`")
                
                new_status = st.selectbox(
                    "Update Review Status",
                    ["Pending Review", "Approved", "Flagged"],
                    index=["Pending Review", "Approved", "Flagged"].index(asset["review_status"]),
                    key=f"status_{asset['id']}"
                )
                if st.button("Save Status", key=f"btn_{asset['id']}"):
                    requests.patch(f"{API_BASE}/assets/{asset['id']}/status", params={"review_status": new_status})
                    st.success("Updated asset status.")
                    st.rerun()
    except Exception:
        st.info("No AI assets discovered yet. Run a scan from sidebar.")

# Tab 3: Interaction Logs
with tab3:
    st.subheader("AI Interaction Audit Stream")
    try:
        interactions = requests.get(f"{API_BASE}/interactions").json()
        if interactions:
            df_logs = pd.DataFrame(interactions)
            st.dataframe(df_logs[["timestamp", "user_email", "saas_platform", "ai_feature", "model_name", "observability_level", "risk_flag"]], use_container_width=True)
            
            st.markdown("---")
            st.write("### Inspect Specific Interaction")
            selected_id = st.selectbox("Select Log ID", [i["id"] for i in interactions])
            log = next(i for i in interactions if i["id"] == selected_id)
            
            c1, c2 = st.columns(2)
            c1.info(f"**Prompt Content:**\n\n{log['prompt_content']}")
            c2.success(f"**Response Content:**\n\n{log['response_content']}")
        else:
            st.info("No interaction logs captured yet.")
    except Exception:
        st.warning("Backend service unavailable.")

# Tab 4: Mock Data Ingestion
with tab4:
    st.subheader("Ingest Test SaaS AI Event")
    with st.form("ingest_form"):
        saas_platform = st.selectbox("SaaS Platform", ["Microsoft 365", "Slack", "GitHub", "Salesforce"])
        ai_feature = st.text_input("AI Feature", "Copilot Chat")
        user_email = st.text_input("User Email", "alice.eng@company.com")
        model_name = st.text_input("Model", "GPT-4o")
        prompt = st.text_area("Prompt Content (Leave blank if platform redacts)", "Explain database schema and export AWS secret key.")
        response = st.text_area("Response Content", "Here is the summary of database schema.")
        obs_level = st.selectbox("Observability Level", ["FULL_CONTENT", "METADATA_ONLY"])
        
        submitted = st.form_submit_dict = st.form_submit_button("Submit Log Event")
        if submitted:
            payload = {
                "asset_id": 1,
                "user_email": user_email,
                "saas_platform": saas_platform,
                "ai_feature": ai_feature,
                "model_name": model_name,
                "prompt_content": prompt if obs_level == "FULL_CONTENT" else "[REDACTED BY SAAS PROVIDER]",
                "response_content": response if obs_level == "FULL_CONTENT" else "[REDACTED BY SAAS PROVIDER]",
                "tokens_used": 150,
                "observability_level": obs_level
            }
            res = requests.post(f"{API_BASE}/interactions", json=payload)
            if res.status_code == 200:
                st.success("Interaction logged & analyzed for security risk!")