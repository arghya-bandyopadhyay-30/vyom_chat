import requests
from bs4 import BeautifulSoup


def load_the_content_from_link(link: str) -> str:
    try:
        response = requests.get(link, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, features="lxml")
        paragraphs = soup.find_all('p')
        return ' '.join([paragraph.get_text(strip=True) for paragraph in paragraphs])

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch content from the link: {link}. Error: {e}")
    except Exception as e:
        raise ValueError(f"Error occurred while extracting content: {e}")
