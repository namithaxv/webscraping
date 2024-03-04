import requests
from bs4 import BeautifulSoup
import csv
import os

#Testing requests function
req = requests.get("https://dataviz.vam.wfp.org/asia-and-the-pacific/india/climate-explorer")
url_content = req.content
csv_file = open('downloaded.csv', 'wb')
csv_file.write(url_content)
csv_file.close()


# Function to webscrape and download
def scrape_and_download_csv(url, output_folder, keywords):
   # Send an HTTP request to the URL
    response = requests.get(url)
    # Check if request was successful
    links_and_titles = []
    if response.status_code == 200:
        # Parse HTML content of page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract links and titles from the HTML

        for d_flex_div in soup.find_all('div', class_='ms-auto'):
            link_tag = d_flex_div.find('a', href=True)


            if link_tag:
                link = link_tag['href']
                title = link_tag.get_text(strip=True)

                if "csv" in link:

                # check if title contains specified keywords
                  if any(keyword.lower() in title.lower() for keyword in keywords):

                     links_and_titles.append((link, title))

        # Download CSV files
        for link, title in links_and_titles:
            csv_url = f"{url}/{link}"
            csv_response = requests.get(csv_url)

            if csv_response.status_code == 200:
                csv_path = os.path.join(output_folder, f"{title}.csv")
                with open(csv_path, 'wb') as csv_file:
                    csv_file.write(csv_response.content)
                print(f"CSV file saved successfully: {csv_path}")
            else:
                print(f"Failed to retrieve CSV file. Status code: {csv_response.status_code}")

    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")





# implementation
url_to_scrape = 'https://www.fao.org/giews/earthobservation/country/index.jsp?code=IND'
output_folder = 'downloaded_csv'
keywords = ['rainfall', 'NDVI']

# make output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

response = requests.get(url_to_scrape, allow_redirects=True)

soup = BeautifulSoup(response.text, 'html.parser')
links_and_titles = []
for link_tag in soup.find_all("a",href=True):
  if link_tag:
    link = link_tag['href']
    title = link_tag.get_text(strip=True)
    if "csv" in link:
      if any(keyword.lower() in link.lower() for keyword in keywords):
          links_and_titles.append((link, title))
for link, title in links_and_titles:
    csv_url = f"{'https://www.fao.org/giews/earthobservation/'}/{link}"
    csv_response = requests.get(csv_url)
    if csv_response.status_code == 200:
                csv_path = os.path.join(output_folder, f"{title}.csv")
                with open(csv_path, 'wb') as csv_file:
                    csv_file.write(csv_response.content)
                print(f"CSV file saved successfully: {csv_path}")
    else:
      print(f"Failed to retrieve CSV file. Status code: {csv_response.status_code}")

