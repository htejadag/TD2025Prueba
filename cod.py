import pygame as pg
from random import random
from collections import deque
import time

def get_rect(x,y):
    return ((x*TILE + 1), (y*TILE + 1), (TILE-2), (TILE-2))

def get_next_nodes(x,y):
    verificarSiguienteNodo = lambda x,y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    acciones = [(-1,0), (0,-1),  (1,0),  (0,1)]
    l = [(x + dx, y + dy) for dx, dy in acciones if verificarSiguienteNodo(x + dx, y + dy)]
    return l

cols, rows = 25,15
TILE = 45

pg.init()
sc = pg.display.set_mode([cols*TILE, rows*TILE])
clock = pg.time.Clock()

#crear malla
#grid = [[1 if random() < 0.3 else 0 for cols in range(cols)] for rows in range(rows)] 
grid = [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


#diccionario de lista de adyacencias
graph = {}      
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x,y)] = graph.get((x,y),[]) + get_next_nodes(x,y)

start = (0, 0)
final = (5,5)
cola = deque([start])
visitados = {start:None}
cur_node = start

run = True
antirun = False
while run:
    sc.fill(pg.Color('black'))
    #dibuja el grid
    [[pg.draw.rect(sc,pg.Color('darkorange'), get_rect(x,y), border_radius=TILE // 5)
      for x, cols in enumerate(fila) if cols] for y, fila in enumerate(grid)]
    
    [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x,y)) for x, y in visitados]
    [pg.draw.rect(sc, pg.Color('darkslategrey'), get_rect(x,y)) for x, y in cola]

    #logica del BFS
    if cola:
        nodoActual = cola.popleft()
        next_nodes = graph[nodoActual]
    
        if(nodoActual==final):
            clock = pg.time.delay
            print(clock)
        else:
            for next_node in next_nodes:
                if next_node not in visitados:
                    cola.append(next_node)
                    visitados[next_node] = nodoActual

    #-----------
    cabezaRuta, cuerpoRuta = nodoActual , nodoActual
    while cuerpoRuta:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*cuerpoRuta), TILE, border_radius=TILE // 3)
        cuerpoRuta = visitados[cuerpoRuta]
    pg.draw.rect(sc, pg.Color('blue'), get_rect(*start), TILE, border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('magenta'), get_rect(*cabezaRuta), TILE, border_radius=TILE // 3)

    #lineas -----------------
    [pg.quit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(20)

    