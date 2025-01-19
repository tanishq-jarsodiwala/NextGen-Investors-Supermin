import os
import requests
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "88bdc206-3a82-475e-94fd-543ed8a7cefc"
FLOW_ID = "e80b75ea-e2be-4990-b879-f47a18ec221a"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")  # Load the token from the environment
ENDPOINT = ""  # Optional endpoint name in the flow settings


def run_flow(message: str) -> dict:
    """
    Function to send a message to the API flow and retrieve a response.

    :param message: The input message to send to the API
    :return: Parsed JSON response from the API or None if an error occurs
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT or FLOW_ID}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def generate_mock_kundali(name, dob, tob, place, gender):
    """
    Generate mock Kundali data for demonstration purposes.
    """
    return {
        "Name": name,
        "Date of Birth": dob.strftime("%B %d, %Y"),
        "Time of Birth": tob.strftime("%I:%M %p"),
        "Place of Birth": place,
        "Gender": gender,
        "Planetary Positions": {
            "Sun": "Virgo",
            "Moon": "Capricorn",
            "Mars": "Libra",
            "Mercury": "Virgo",
        },
        "Ascendant": "Libra",
        "Nakshatra Details": {
            "Moon Nakshatra": "Shravana",
            "Nakshatra Ruler": "Moon",
        },
        "Dasha Information": "Jupiter Mahadasha (5 years remaining)",
        "Lucky Attributes": {
            "Lucky Color": "Blue, Green",
            "Lucky Gemstone": "Yellow Sapphire",
        },
        "Career Focus": "Financial growth and development",
        "Summary": "Strong analytical mind with a focus on financial growth.",
    }


def format_kundali_output(kundali):
    """
    Format the Kundali data into plain text for display.
    """
    output = f"""
    Kundali Details for {kundali['Name']}:
    -------------------------------------
    Date of Birth: {kundali['Date of Birth']}
    Time of Birth: {kundali['Time of Birth']}
    Place of Birth: {kundali['Place of Birth']}
    Gender: {kundali['Gender']}

    Planetary Positions:
    --------------------
    """
    for planet, position in kundali["Planetary Positions"].items():
        output += f"{planet}: {position}\n"

    output += "\nNakshatra Details:\n------------------\n"
    for key, value in kundali["Nakshatra Details"].items():
        output += f"{key}: {value}\n"

    output += f"""
    Dasha Information:
    ------------------
    {kundali['Dasha Information']}

    Lucky Attributes:
    -----------------
    """
    for attr, value in kundali["Lucky Attributes"].items():
        output += f"{attr}: {value}\n"

    output += f"""
    Career Focus:
    -------------
    {kundali['Career Focus']}

    Summary:
    --------
    {kundali['Summary']}
    """

    return output


def main():
    """
    Main function to handle the Streamlit UI and API interaction.
    """
    st.title("Astrology & Kundali Generator")

    # Sidebar Inputs
    with st.sidebar:
        st.header("Enter Your Details")
        name = st.text_input("Full Name", placeholder="e.g., Vihan Verma")
        dob = st.date_input("Date of Birth", min_value=datetime(1900, 1, 1), max_value=datetime.today())
        tob = st.time_input("Time of Birth")
        place_of_birth = st.text_input("Place of Birth", placeholder="e.g., Vadodara, Gujarat")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        api_integration = st.checkbox("Use API Integration")
        submit = st.button("Generate Kundali")

    if submit:
        if not all([name, dob, tob, place_of_birth, gender]):
            st.warning("Please fill out all fields.")
        else:
            st.info("Processing your request...")
            if api_integration:
                # Construct the API request message
                message = f"Generate Kundali for {name}, born on {dob} at {tob} in {place_of_birth}. Gender: {gender}."
                response = run_flow(message)

                if response:
                    st.success("Kundali Generated Successfully via API!")
                    st.text_area("Kundali Output", value=json.dumps(response, indent=4), height=300)
                else:
                    st.error("Failed to generate Kundali via API. Please try again.")
            else:
                # Generate mock Kundali data
                kundali = generate_mock_kundali(name, dob, tob, place_of_birth, gender)
                st.success("Kundali Generated Successfully!")
                output_text = format_kundali_output(kundali)
                st.text_area("Kundali Output", value=output_text, height=400)


if __name__ == "__main__":
    main()
