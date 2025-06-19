import os
from dotenv import load_dotenv
import streamlit as st

# import azure libraries
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# loading variables from .env file
load_dotenv() 

# accessing vision key and endpoint
subscription_key = os.getenv("LANGUAGE_KEY")
endpoint = os.getenv("LANGUAGE_ENDPOINT")

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(subscription_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

def analyse_health_text(client, health_text):
    documents = [health_text]
    poller = client.begin_analyze_healthcare_entities(documents)
    result = poller.result()
    docs = [doc for doc in result if not doc.is_error]
    st.markdown("---")
    for idx, doc in enumerate(docs):
        for entity in doc.entities:
            st.text(f"Entity: {entity.text}")
            st.text(f"...Normalized Text: {entity.normalized_text}")
            st.text(f"...Category: {entity.category}")
            st.text(f"...Subcategory: {entity.subcategory}")
            st.text(f"...Offset: {entity.offset}")
            st.text(f"...Confidence score: {entity.confidence_score}")
        for relation in doc.entity_relations:
            st.text(f"Relation of type: {relation.relation_type} has the following roles")
            for role in relation.roles:
                st.text(f"...Role '{role.name}' with entity '{role.entity.text}'")
        st.markdown("------------------------------------------")

# this is the main function in which we define our webpage  
def main():
    st.markdown("# Text Analytics App ✍️📝")
    st.markdown("### This app allows you to analyse Health Texts.")

    # Authenticate the client
    client = authenticate_client()

    # Get Medical Text from user after authentication
    health_text = st.text_input("Enter a medical text", "Patient needs to take 50 mg of ibuprofen.")

    # Add a button to trigger analysis
    if st.button("Analyse Text"):
        analyse_health_text(client, health_text)

# Init code
if __name__=='__main__': 
    main()
