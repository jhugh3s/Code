import os
import requests
import re

board_url = 'https://boards.4chan.org/pol/'
output_file = 'pol_url.txt'
desktop_path = os.path.expanduser('~/Desktop')

thread_urls = []

for page_num in range(10):  # Adjust the range to fetch threads from all 10 pages
    if page_num > 0:
        page_url = f'{board_url}{page_num + 1}'
    else:
        page_url = board_url
    response = requests.get(page_url)
    response.raise_for_status()

    thread_urls += re.findall(r'<a href="/pol/thread/(\d+)', response.text)

with open(os.path.join(desktop_path, output_file), 'w') as file:
    for url in thread_urls:
        file.write(f"'https://boards.4chan.org/pol/thread/{url}',\n")

print(f'URLs of {len(thread_urls)} threads saved to "{output_file}" on your desktop.')
