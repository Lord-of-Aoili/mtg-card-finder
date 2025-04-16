import argparse
import requests
import time
import json
import os
from functools import lru_cache

# Optional: import OpenAI for LLM capabilities
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

SCRYFALL_API_URL = "https://api.scryfall.com/cards/search"

def query_llm(natural_query):
    """Use an LLM to translate natural language into Scryfall search parameters."""
    if not OPENAI_AVAILABLE:
        print("OpenAI library not available. Install with: pip install openai")
        return None
    
    # Check for API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        return None
    
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    # Create prompt for translating query
    prompt = f"""
    You are a Magic: The Gathering expert who translates user queries into Scryfall syntax.
    
    Translate the following request into a Scryfall search query:
    
    "{natural_query}"
    
    Return ONLY the Scryfall search query with proper syntax and operators.
    """
    
    # Call the OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You convert MTG card requests into Scryfall search syntax."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        scryfall_query = response.choices[0].message.content.strip()
        print(f"Translated query: {scryfall_query}")
        return scryfall_query
    except Exception as e:
        print(f"Error querying LLM: {e}")
        return None

def query_scryfall(query, use_llm=False):
    """Query the Scryfall API with a search query."""
    # Use LLM to translate the query if requested
    if use_llm:
        translated_query = query_llm(query)
        if translated_query:
            query = translated_query
    
    params = {"q": query}
    headers = {
        "User-Agent": "MTGCardFinder/1.0",
        "Accept": "application/json"
    }
    
    response = requests.get(SCRYFALL_API_URL, params=params, headers=headers)
    if response.status_code == 200:
        cards = response.json().get("data", [])
        if not cards:
            print("No cards found matching your query.")
            return
            
        for card in cards:
            print(f"Name: {card['name']}")
            print(f"Mana Cost: {card.get('mana_cost', 'N/A')}")
            print(f"Type: {card['type_line']}")
            print(f"Rarity: {card['rarity']}")
            print(f"Text: {card.get('oracle_text', 'N/A')}")
            print("-" * 40)
            time.sleep(0.1)  # Add a 100ms delay between processing cards
    elif response.status_code == 429:
        print("Rate limit exceeded. Please wait and try again.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

@lru_cache(maxsize=128)
def query_scryfall_cached(query):
    """Query the Scryfall API with caching."""
    params = {"q": query}
    headers = {
        "User-Agent": "MTGCardFinder/1.0",
        "Accept": "application/json"
    }
    response = requests.get(SCRYFALL_API_URL, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        print("Rate limit exceeded. Retrying in 1 second...")
        time.sleep(1)  # Wait before retrying
        return query_scryfall_cached(query)  # Retry the query
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def download_bulk_data():
    """Download bulk data from Scryfall."""
    bulk_data_url = "https://api.scryfall.com/bulk-data"
    response = requests.get(bulk_data_url)
    if response.status_code == 200:
        bulk_data = response.json()
        for item in bulk_data["data"]:
            if item["type"] == "default_cards":
                download_url = item["download_uri"]
                print(f"Downloading bulk data from {download_url}...")
                bulk_response = requests.get(download_url)
                with open("scryfall_bulk_data.json", "wb") as f:
                    f.write(bulk_response.content)
                print("Bulk data downloaded and saved as scryfall_bulk_data.json")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main():
    parser = argparse.ArgumentParser(description="MTG Card Finder")
    parser.add_argument("--query", type=str, help="Natural language search query for MTG cards")
    parser.add_argument("--llm", action="store_true", help="Use LLM to translate the query")
    parser.add_argument("--bulk", action="store_true", help="Download bulk data from Scryfall")
    args = parser.parse_args()

    if args.bulk:
        download_bulk_data()
    elif args.query:
        query_scryfall(args.query, use_llm=args.llm)
    else:
        print("Please provide a query using --query")
        print("Add --llm to use language model for natural language search")

if __name__ == "__main__":
    main()