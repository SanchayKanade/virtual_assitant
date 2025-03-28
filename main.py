# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token
import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a75942c7-6a21-4dc6-a228-936249005e2d"
FLOW_ID = "9552fb46-7f4c-4ab9-9480-648300514980"
APPLICATION_TOKEN = os.environ.get("API_TOKEN")
ENDPOINT = "customer" # The endpoint name of the flow


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)

    # Debug logs
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    # Check before parsing JSON
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            raise Exception("Response is not valid JSON.")
    else:
        raise Exception(f"API call failed with status {response.status_code}: {response.text}")


def main():
    st.title("Chat Interface")
    
    message = st.text_area("Message", placeholder="Ask something...")
    print(message)
    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return
    
        try:
            with st.spinner("Running flow..."):
                print("Calling api function")
                response = run_flow(message)
                print(response)

            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            print(response)
            st.markdown(response)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()

# Simple testing
# result = run_flow("What are the shipment times?")
# print(result["outputs"][0]["outputs"][0]["results"]["message"]["text"])
