# -*- coding: utf-8 -*-

# Библиотеки для отправки запросов к апи вк и разботы с json строкой
import json
import requests

# Библиотеки для создания графа
import networkx as nx
from pyvis import network as net


from tkinter import *

# Граф networkx
G = nx.Graph()

# Токен для запроса к апи вк & используемая версия апи для запроса v=5.130
cmafk = '&access_token=a93eb5c1a93eb5c1a93eb5c19ea9493113aa93ea93eb5c1c9bea86d36d437768354ba62&v=5.130'

def draw_graph3(networkx_graph,notebook=False,output_filename='graph.html',show_buttons=True,only_physics_buttons=False):
    
    #
    pyvis_graph = net.Network(notebook=notebook)
    
    #
    for node,node_attrs in networkx_graph.nodes(data=True):
        pyvis_graph.add_node(str(node),**node_attrs)

    #   
    for source,target,edge_attrs in networkx_graph.edges(data=True):
        if not 'value' in edge_attrs and not 'width' in edge_attrs and 'weight' in edge_attrs:
            edge_attrs['value']=edge_attrs['weight']
        pyvis_graph.add_edge(str(source),str(target),**edge_attrs)
        
    # Отображение кнопок для настройки графа
    if show_buttons:
        if only_physics_buttons:
            pyvis_graph.show_buttons(filter_=['physics'])
        else:
            pyvis_graph.show_buttons()
    
    return pyvis_graph.show(output_filename)


def clicked():
    uid = uid_textbox.get()
    count = count_textbox.get()
    count_fr = count_fr_textbox.get()
    s = requests.get('https://api.vk.com/method/users.get?user_ids=' + uid + '&fields=uid,first_name,last_name' + cmafk).text
    p = json.loads(s)

    # Достаем из полученной строки имя пользователя
    for x in p['response']:
        # Проверяем есть ли в полученной строке имеется "first_name"
        if('first_name' in x):
            # Добавляем к графу networkx ноду пользлователя
            G.add_node(x['first_name'] + " " + x['last_name'])
            # Записываем имя пользователя
            name = x['first_name'] + " " + x['last_name']
        # Если в полученной строке нет "first_name", то произошла какая-то ошибка
        else:
            # Выводим строку что бы понять что случилось
            # print(p)
            pass

    s=requests.get('https://api.vk.com/method/friends.get?user_id=' + uid + '&fields=uid,%20first_name,%20last_name&count='+ count + cmafk).text
    p = json.loads(s)

    # Переменная для записи id друзей пользователя в виде списка
    fr=[]

    # Переменная для перебора всего списка друзей пользователя из листа fr[]
    i = 0

    # Достаем из полученной строки имена друзей пользователя
    for x in p['response']['items']:
        # Добовляем в лист fr[] id друзей
        fr.append(str(x['id']))
        # Проверяем есть ли в полученной строке имеется "first_name", а так же не содержит ли она в себе данные о удаленной странице
        if('first_name' in x) & (x['first_name'] != 'DELETED'):
            # Добавляем к графу networkx ноды друзей пользователя 
            G.add_node(x['first_name'] + " " + x['last_name'])
            # Добовляем к графу networkx связи между нодой пользователя и нодами его друзей
            G.add_edge(name, x['first_name'] + " " + x['last_name'],color='#4174ff')
        print("Друг №  " + str(i))

        s=requests.get('https://api.vk.com/method/friends.get?user_id=' + fr[i] + '&fields=uid,%20first_name,%20last_name' + cmafk).text
        p = json.loads(s)

        # Если полученная строка содержит ошибку, то выводим её, что бы понять что случилось
        if ('error' in p):
            # print(p)
            pass
        else:
            ii=0
            # Достаем из полученной строки имена друзей друзей
            for z in p['response']['items']:
                if ii < int(count_fr):
                    # Проверяем есть ли в полученной строке имеется "first_name", а так же не содержит ли она в себе данные о удаленной странице
                    if('first_name' in z) & (z['first_name'] != 'DELETED'):
                        # Добавляем к графу networkx ноды друзей друзей 
                        G.add_node(z['first_name'] + " " + z['last_name'])
                        # Добовляем к графу networkx связи между нодами друзей пользователя и нодами их друзей
                        G.add_edge(x['first_name'] + " " + x['last_name'], z['first_name'] + " " + z['last_name'], color='#8aa9ff')
                        ii=ii+1
    
        # Переходим к следующиму другу в листе fr[]
        i = i + 1

    # Передаем в функцию draw_graph3 сеть networkx под названием G
    draw_graph3(G)

clicks = 0

window = Tk()
window.title("Добро пожаловать")
window.geometry('400x250')

lbl = Label(window, text="Введите id пользователя Вконтакте:")  
lbl.grid(column=0, row=0)
uid_textbox = Entry(window,width=10)  
uid_textbox.grid(column=1, row=0)  

lbl1 = Label(window, text="Введите количество друзей:")  
lbl1.grid(column=0, row=1)
count_textbox = Entry(window,width=10)  
count_textbox.grid(column=1, row=1)  

lbl2 = Label(window, text="Введите количество друзей друзей:")  
lbl2.grid(column=0, row=2)
count_fr_textbox = Entry(window,width=10)  
count_fr_textbox.grid(column=1, row=2)  

btn = Button(window, text="Done", command=clicked)
btn.grid(column=0, row=3)


window.mainloop()
