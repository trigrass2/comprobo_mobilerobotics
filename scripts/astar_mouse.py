#!/usr/bin/python
from collections import deque
import math
from Queue import PriorityQueue
import numpy as np
import scipy.misc.pilutil as smp
import pickle
import rospy

map_vis = pickle.load( open( "starMapCut.p", "rb" ) )
map_info = pickle.load( open( "map_info.p", "rb" ) )

visited = set()
nodesToExplore = deque([])
start = (24,49)
#$goal = (80 ,84)
goal = (250, 200)


def mapBuffer(map_info, map_vis):
  for i in map_info

def isFree(pixel):
  if map_info[pixel[1]][pixel[0]] == 0:
    return True
  return False

class Node():
  def __init__(self, parent, pixels, value=None):
    self.pixels = pixels
    # self.coords = convert_to_m(pixels)
    self.parent = parent
    if self.parent != None:
      self.parent.assign_child(self)
    self.children = []
    self.value = value

  def set_value(self, distance):
    self.value = distance + self.parent.value

  def return_parent(self):
    return self.parent

  def return_full_path(self):
    path = []
    while self.parent != None:
      path.append(self.parent.pixels)
      self = self.parent
    return path

  def assign_child(self, child):
    self.children.append(child)

  def convert_to_m(self):
    constant = .05
    width = 102.4
    return (self.pixels[0] * constant - width, self.pixels[1] * constant - width)



"""

Priority Queue used for A* heuristic
Returns the node with the lowest value first

"""
# class MyPriorityQueue(PriorityQueue):
#     def __init__(self):
#         PriorityQueue.__init__(self)
#         self.counter = 0

#     def put(self, item, priority):
#         PriorityQueue.put(self, (priority, self.counter, item))
#         self.counter += 1

#     def get(self, *args, **kwargs):
#         _, _, item = PriorityQueue.get(self, *args, **kwargs)
#         return item

"""

A* Heuristic
Finds the "as the crow flies" distance between a given node and the goal node

"""
def manhattan_distance(node):

  current_x = node.pixels[0]
  current_y = node.pixels[1]

  goal_x = goal[0]
  goal_y = goal[1]

  distance = math.sqrt((goal_x - current_x)**2 + (goal_y - current_y)**2)

  return distance

"""

A* Heuristic2
Finds the "as the crow flies" distance between a given node and the goal node

"""
def edge_weight_distance(value):
  #print value
  current_value = value

  return current_value + 1


"""

Get surrounding pixels (+/- 1) for a given x, y
Return a list of tuples of (a tuple for coordinate, distance value)

"""

def get_surrounding_pixels(location):
  # Find the pixels of all the neighbors
  child_right = ((location[0] + 1, location[1]), 1)
  child_left = ((location[0] - 1, location[1]), 1)
  child_up = ((location[0], location[1] + 1), 1)
  child_down = ((location[0], location[1] - 1), 1)
  child_right_down = ((location[0] + 1, location[1] - 1), math.sqrt(2))
  child_right_up = ((location[0] + 1, location[1] + 1), math.sqrt(2))
  child_left_down = ((location[0] - 1, location[1] - 1), math.sqrt(2))
  child_left_up = ((location[0] - 1, location[1] + 1), math.sqrt(2) )

  return [child_right, child_left, child_up, child_down, child_right_down, child_right_up, child_left_up, child_left_down]



"""

BFS implementation using the Node object
Flattened - tested with goal 500 away x and y

"""

def expand_tree(node):

  priorityqueue = PriorityQueue()
  while True:
    # Check if current node is the goal node
    if node.pixels == goal:
      break

    surrounding_area = get_surrounding_pixels(node.pixels)
    
    # Iterate through the all 8 pixels around the current x, y point
    for current_pixel in surrounding_area:
      
      # Only add pixel is a child if it isn't visisted already
      if current_pixel[0] not in visited and isFree(current_pixel[0]):
        # Create new node
        #weight = edge_weight_distance(node.value)
        next = Node(node, current_pixel[0])
        next.set_value(current_pixel[1])
        visited.add(next.pixels)
        #nodesToExplore.append(next)
        next = priorityqueue.put((next, next.value))

    #node = nodesToExplore.popleft()
    node = priorityqueue.get()[0]

  # Once breaking, return the full path of the goal node
  return node.return_full_path()

    

def paint_point((x,y),data,color):
  for i in range(y-1, y+2):
    for k in range(x-1, x+2):
      data[i,k] = color
  return data


def make_tree(start_pixel):
  # Make star_pixel the root of the tree
  # start_pixels is a tuple (x, y)c
  root = Node(None, start_pixel, 1)

  # Recursively expand the tree 
  return expand_tree(root)


def mapflip(map_vis,map_info):
  map_vis2 = []
  map_info2 = []
  for i in map_vis:
    map_vis2.insert(0,i)
  for i in map_info:
    map_info2.insert(0,i)
  return map_vis2, map_info2

def setup_gui():
  root = Tk()

  #setting up a tkinter canvas ((((with scrollbars))))
  frame = Frame(root, bd=2, relief=SUNKEN)
  frame.grid_rowconfigure(0, weight=1)
  frame.grid_columnconfigure(0, weight=1)
  #xscroll = Scrollbar(frame, orient=HORIZONTAL)
  #xscroll.grid(row=1, column=0, sticky=E+W)
  #yscroll = Scrollbar(frame)
  #yscroll.grid(row=0, column=1, sticky=N+S)
  #canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
  canvas = Canvas(frame, bd=0)
  canvas.grid(row=0, column=0, sticky=N+S+E+W)
  #xscroll.config(command=canvas.xview)
  #yscroll.config(command=canvas.yview)
  frame.pack(fill=BOTH,expand=1)
  return root

def reset():
    img = ImageTk.PhotoImage(smp.toimage( map_vis ))
    #-------------------------------------------------
    canvas.create_image(0,0,image=img,anchor="nw")

def mouseClick(event):
  global goal
  goal = (event.x, event.y)
  resetGoal

if __name__ == '__main__':
  root = setup_gui()
  print 'calculating path...'
  path = make_tree(start)
  print 'done with search'
  print 'goal',goal
  print 'start',start
  #print path
  for i in path:
    map_info[i[1]][i[0]] = 2
    map_vis[i[1],i[0]] = [0,255,0]

  map_vis = paint_point(start, map_vis, [0,0,255])
  map_vis = paint_point(goal, map_vis, [255,0,0])
  map_vis, map_info = mapflip(map_vis, map_info)

  canvas.bind("<Button 1>",mouseClick)
  root.mainloop()

  # img = smp.toimage( map_vis )
  # img.show()
  # flag = True
  # while flag == True:
  #   continue
