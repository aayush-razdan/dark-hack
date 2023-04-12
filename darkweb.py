#!/usr/bin/env python
# coding: utf-8
import socks
import socket
import requests
import re
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

def getaddrinfo(*args):
    # It is necessary to use Tor for DNS resolution of Onion websites
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

def crawl(url):
    # Configuring Socks to use Tor
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
    socket.socket = socks.socksocket
    socket.getaddrinfo = getaddrinfo
    # Using requests package to read in the Hidden Wiki Onion Website on the Darknet
    res = requests.get(url)
    # Using beautifulsoup to get the website content into a nice format
    soup = BeautifulSoup(res.content, 'html.parser')
    # Having a look at the Website content
    # Checking the Websites title
    # Getting all links out of the soup and deleting None's
    links = [link.get('href') for link in soup.find_all('a')]
    links = list(filter(None, links)) 
    # Saving all onion links into a list
    found_nodes = []
    p = re.compile('http\S+onion')
    for l in links:
      nodes = p.findall(l)
      found_nodes.append(nodes)
    unique_nodes= set()
    for node in found_nodes:
        for link in node:
            unique_nodes.add(link)
    print(unique_nodes)
    return unique_nodes

if __name__ == "__main__":
    print("Links :")
    print(crawl(sys.argv[1]))

# print(len(unique_nodes))
# print(len(found_nodes))
# 
# 
# # In[32]:
# 
# 
# onion_body={}
# cnt=0
# for link in unique_nodes:
#     if cnt < 5:
#         res=requests.get(link)
#         soup=BeautifulSoup(res.content,'html.parser')
#         body=soup.find('body')
#         text=body.text
#         text_lines=text.split('\n')
#         clean_text=''.join(text_lines)
#         onion_body[link]=clean_text
#         cnt+=1
#     else:
#         break
# 
# 
# # In[33]:
# 
# 
# onion_body
# 
# 
# # In[ ]:




