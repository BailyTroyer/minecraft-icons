import os
import requests
from multiprocessing.pool import ThreadPool
import urllib.parse

from mc_assets.progress import printProgressBar


def download_url(bucket):
    url = bucket.get("url")
    path = bucket.get("path")

    # https://url/minecraft_gamepedia/images/_SOMETHING_/_SOMETHING_/___FILE_IS_HERE___.EXTENSION
    # we also decode the URL query string
    file_name = urllib.parse.unquote(url.split("/")[7])

    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        filename = f"./downloads/{path}/{file_name}"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            for data in r:
                f.write(data)

    return url


def download_batch(urls):
    prefix = 'Progress Pulling MC Swag:'
    suffix = 'Dank'
    total_downloads = len(urls)

    printProgressBar(0, total_downloads, prefix='Progress:',
                     suffix='Complete', length=50)

    # Run 5 multiple threads. Each call will take the next element in urls list
    results = ThreadPool(5).imap_unordered(download_url, urls)
    for i, _ in enumerate(results):
        printProgressBar(i + 1, total_downloads, prefix=prefix,
                         suffix=suffix, length=50)
