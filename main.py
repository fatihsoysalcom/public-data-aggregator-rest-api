import requests
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Define a simple endpoint for our aggregated public data
@app.route('/public-data', methods=['GET'])
def get_public_data():
    """
    Aggregates data from multiple public, registration-free APIs
    and returns a combined JSON response.
    """
    aggregated_data = {}

    # --- Source 1: Currency Exchange Rates (e.g., EUR to USD) ---
    # This API provides current exchange rates without requiring an API key.
    try:
        currency_api_url = "https://api.frankfurter.app/latest?from=EUR&to=USD"
        currency_response = requests.get(currency_api_url, timeout=5)
        currency_response.raise_for_status() # Raise an exception for HTTP errors
        currency_data = currency_response.json()
        
        # Extract relevant information
        if currency_data and 'rates' in currency_data and 'USD' in currency_data['rates']:
            aggregated_data['exchange_rate_eur_to_usd'] = currency_data['rates']['USD']
            aggregated_data['exchange_rate_source'] = currency_api_url
        else:
            aggregated_data['exchange_rate_error'] = "Could not retrieve EUR to USD rate."
            
    except requests.exceptions.RequestException as e:
        aggregated_data['exchange_rate_error'] = f"Failed to fetch currency data: {e}"
    except ValueError: # JSON decoding error
        aggregated_data['exchange_rate_error'] = "Failed to decode currency data JSON."

    # --- Source 2: Public Holidays in Turkey for current year ---
    # This API provides public holidays for a given country and year, no API key needed.
    try:
        # Allow overriding year for testing via environment variable, default to 2024
        current_year = os.getenv("CURRENT_YEAR", "2024") 
        holidays_api_url = f"https://date.nager.at/api/v3/PublicHolidays/{current_year}/TR"
        holidays_response = requests.get(holidays_api_url, timeout=5)
        holidays_response.raise_for_status()
        holidays_data = holidays_response.json()

        # Extract relevant information (e.g., first 3 holidays)
        if isinstance(holidays_data, list):
            aggregated_data['turkish_public_holidays'] = [
                {'date': h['date'], 'name': h['name']} for h in holidays_data[:3]
            ]
            aggregated_data['public_holidays_source'] = holidays_api_url
        else:
            aggregated_data['public_holidays_error'] = "Could not retrieve public holidays."

    except requests.exceptions.RequestException as e:
        aggregated_data['public_holidays_error'] = f"Failed to fetch public holidays data: {e}"
    except ValueError: # JSON decoding error
        aggregated_data['public_holidays_error'] = "Failed to decode public holidays JSON."

    # --- Return the aggregated data as a registration-free JSON response ---
    # This API endpoint requires no authentication or API keys, demonstrating the 'kayıtsız' concept.
    return jsonify(aggregated_data)

# Run the Flask application
if __name__ == '__main__':
    # For development, Flask's built-in server is sufficient.
    # host='0.0.0.0' makes the server accessible externally (e.g., from Docker or other machines)
    # debug=True enables reloader and debugger (should be False in production)
    app.run(host='0.0.0.0', port=5000, debug=True)
