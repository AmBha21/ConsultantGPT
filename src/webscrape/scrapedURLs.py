import trafilatura
from urls import google_custom_search

def scrape_urls(urls):
  """
  Scrapes the information from the given URLs using Trafilatura.

  Args:
    urls: A list of URLs to scrape.

  Returns:
    A list of dictionaries containing the scraped information.
  """

  scraped_info = []
  for url in urls:
    print(url)
    
    soup = trafilatura.fetch_url(url)
    print(soup)

    result = trafilatura.extract(soup)
    scraped_info.append({
      "url": url,
    #   "text": result,
    })

  return scraped_info


if __name__ == "__main__":
  # Get the URLs from the Google Custom Search API
  results = google_custom_search("steps to enter the electric manufacturing industry")
  urls = [result["link"] for result in results]

  # Scrape the information from the URLs
  scraped_info = scrape_urls(urls)

  # Print the scraped information
  for info in scraped_info.keys():
    print(scraped_info[info])