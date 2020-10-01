def paragraphFinder(url):
    page = (scraper.get(url,proxies = proxies).text)
    soup = BeautifulSoup(page, 'html.parser')

    links = []
    for link in soup.find_all('p'):
        links.append(str(link.text))

    return str(links[0])
