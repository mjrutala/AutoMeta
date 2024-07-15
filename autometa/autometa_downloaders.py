"""
Created on Mon Jul 15 14:57:13 2024

@author: mrutala
"""

import urllib.request
link = 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls'
urllib.request.urlretrieve(link, 'naif0012.tls')


def run_urllibForSPICE(url, savedir, namepattern, show_progress=True, force_update=False):
    
    #  In case savedir is being handled as a pathlib Path, which subprocess
    #  doesn't like
    savedir = str(savedir)
    
    html_url = url
    with urllib.request.urlopen(url) as response:
        html_body = response.read().decode('utf-8')
    soup = BeautifulSoup(html_body, 'html.parser')
    
    href_link_list = list()
    for a in soup.find_all('a', href=True):
        href_link_list.append(a['href'])
    
    #  Check if namepattern occurs in href_link_list
    
    #  Construct new urls including above matches
    
    #  url request complete url names
    
    
    with file as urllib.request.URLopener():
        file.retreive(url)
