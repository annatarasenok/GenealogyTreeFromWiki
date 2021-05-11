#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install pyvis')
from bs4 import BeautifulSoup
import requests
import networkx as nx
from pyvis.network import Network


G = nx.Graph()
listifwas = []
listlinkifwas = []
nt = Network()
def f(url, state, name, koleno):
  if (koleno > 0):
    urladded = list(url)
    urladded.insert(0,"https://ru.wikipedia.org")
    urladded = "".join(urladded)
    try:
      page = requests.get(urladded)
      soup = BeautifulSoup(page.text, 'html.parser')
      everything = []
      relatives = []
      everything = soup.find_all('tr')
      for i in everything:
          if str(i).find('Отец') >0:
            relatives.append(i)
            
          if str(i).find('Мать') >0:
            relatives.append(i)
          
          if str(i).find('Супруг') >0:
            relatives.append(i)
          
          if str(i).find('Дети') >0:
            relatives.append(i)

      links = []
      relativesnames = []

      for i in relatives:
        a = list(i.text)

        b = 2
        while b!=len(a):
          if (a[b].isupper() and a[b-1] != ('-') and a[b-1] != (' ') and a[b]!= "I" and a[b]!= "V") or (a[b] =="и" and a[b-1]==" ") or a[b]==",":
            a.insert(b,"$")
            b = b + 1
          b = b + 1

        while True:
          try:
            a.remove('\n')
          except:
            break
        a = ''.join(a)
        a = a.split('$')
        relativesnames.append(a)

        position = str(i).find("/wiki/")
        if(position == -1):
          links.append("\nNone")
        b = 0
        while position > 0:
          if b == 0:
            links.append("\n")
          else:
            links.append("^^^")
          while list(str(i))[position] != '"' :
                      links.append(list(str(i))[position])
                      position = position + 1
          position = str(i).find("/wiki/",position)
          b = b + 1


      links = ''.join(links)
      links = links.split('\n')
      b = 1
      while b!= len(links):
        links[b] = links[b].split('^^^')
        b = b + 1
      try:
        links.remove("")
      except:
        0
      b = 1
      for i in links:
        if b == -1:
          break
        if b != state:
          c = 2
          for j in i:
            G.add_edge(name,relativesnames[b-1][c-1])
            if (relativesnames[b-1][c-1] in listifwas) or (links[b-1][c-2] in listlinkifwas) : 0
            else:
              listifwas.append(relativesnames[b-1][c-1])
              listlinkifwas.append(links[b-1][c-2])
              f(links[b-1][c-2], b, relativesnames[b-1][c-1], koleno-1)
            c = c + 1
        b = b + 1
    except: 0
f("/wiki/%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B0_II", 0, "Екатерина II", 12)

print(len(listlinkifwas))
nt.from_nx(G)
nt.show('net2.html')


# In[ ]:




