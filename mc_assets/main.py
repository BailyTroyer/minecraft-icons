from re import S
import requests
import re
from bs4 import BeautifulSoup

from mc_assets.downloader import download_batch

BASE_ICONS_URL = "https://minecraft.fandom.com"
LINK_CLASSES = "CategoryTreeLabel CategoryTreeLabelNs14 CategoryTreeLabelCategory"
IMAGE_LABEL_RE = r"^(.*\.(png|gif|svg|jpg|PNG))(\d[\d,.]*\b × \d[\d,.]*\b); (?P<size>\b\d[\d,.]*\b) (?P<unit>KB|MB|GB|bytes)$"

B = 1
KB = 1e3
MB = 1e6
GB = 1e9


def format_bytes(size):
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'kilo', 2: 'mega', 3: 'giga'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'bytes'


def convert_size(size, unit):
    """Converts a size label to a valid byte float."""

    if unit == "bytes":
        return size * B
    elif unit == "KB":
        return size * KB
    elif unit == "MB":
        return size * MB
    elif unit == "GB":
        return size * GB


def fetch_remote_fandom(prefix="/wiki/Category:Icons"):
    """Fetches root fandom HTML."""
    response = requests.get(BASE_ICONS_URL+prefix)
    # This will check the topmost DOCTYPE is set to html => `response.text[:90]``
    return response.text


def build_soup(html):
    return BeautifulSoup(html, 'html.parser')


def scrape_size(image):
    label_text = image.parent.parent.parent.find(
        'div', class_='gallerytext').text.replace('\n', '')

    regex_match = re.search(IMAGE_LABEL_RE, label_text)

    size = float(regex_match.group("size").replace(",", ""))
    unit = regex_match.group("unit")

    size = convert_size(size, unit)

    return size


def scrape_image(image, path):

    return {
        "url": image.get('href'),
        "size": scrape_size(image),
        "path": path
    }


def total_size(list_):
    return sum(float(x.get('size', 0)) for x in list_)


def parse_images(soup, link, path, level=1):

    soup = build_soup(fetch_remote_fandom(link))
    links = [x.get("href") for x in soup.find_all("a", class_=LINK_CLASSES)]
    images = [scrape_image(x, path)
              for x in soup.find_all("a", class_="image")]

    if not links:
        size_ = total_size(images)
        print(f"{' ' * level}>{path}")
        return images, size_

    total_links = []
    size = 0
    for link in links:
        link_name = link.split(":")[1]
        img, sz = parse_images(soup, link, f"{path}/{link_name}", level+1)
        total_links.extend(img)
        size += sz

    return total_links, size


def kickoff():
    html = fetch_remote_fandom()
    soup = build_soup(html)

    links = [x.get("href") for x in soup.find_all("a", class_=LINK_CLASSES)]
    images = []
    size = 0

    # For each link fetch images, check links
    for link in links:
        link_name = link.split(":")[1]
        images_, size_ = parse_images(soup, link, link_name)
        images.extend(images_)
        size += size_

    download_batch(images)
    bytes_, unit = format_bytes(size)
    print(f"💦 Scraped 😩 {len(images)} images totalling {int(bytes_)} {unit}")


if __name__ == "__main__":
    kickoff()
