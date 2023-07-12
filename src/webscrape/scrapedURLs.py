import trafilatura
from .getUrls import google_custom_search

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
    # print(url)
    
    soup = trafilatura.fetch_url(url)
    # print(soup)

    result = trafilatura.extract(soup)
    scraped_info.append({
      "url": url,
      "text": result,
    })
  return scraped_info


if __name__ == "__main__":
  # Get the URLs from the Google Custom Search API
  results = google_custom_search("""1. Electric vehicle market
2. Market trends
3. Target customer demographics""", 2)
  urls = [result["link"] for result in results]

  # Scrape the information from the URLs
  scraped_info = scrape_urls(urls)

  # print(scraped_info.keys())
  # Print the scraped information
  for info in scraped_info:
    print(info['url'])
    print(info['text'])