import os
from dotenv import load_dotenv
import googleapiclient.discovery
import pprint
load_dotenv()

def google_custom_search(search_term, num_results=1):
    """
    Performs a Google Custom Search and returns the first `num_results` results.

    Args:
    search_term: The search term to search for.
    num_results: The number of results to return.

    Returns:
    A list of the first `num_results` search results.
    """

    # Get your API key and cse key from the Google Developers Console
    google_search_api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
    cse_key = os.environ.get("CSE_ID")

    # Create the API client
    service = googleapiclient.discovery.build("customsearch", "v1", developerKey=google_search_api_key)

    # Search for the string `search_term` and limit the results to `num_results` URLs
    result = service.cse().list(q=search_term, cx=cse_key, num=num_results).execute()

    # Return the list of search results
    return result["items"]

if __name__ == "__main__":
    # Search for the string "batteries" and print the first 5 results
    results = google_custom_search("batteries")
    for result in results:
        print(result["link"])