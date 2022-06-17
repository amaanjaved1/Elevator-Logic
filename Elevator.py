import pygame
from pygame.locals import *
import random
import time 
from time import process_time 
import datetime
from datetime import datetime
import timer 

time_buffer = 4
reset = False
action_dictionary = {}

#______________________________________________________________________
class person(): #create a class for passengers
  def __init__(self, direction, current_floor):
    self.direction = direction #Up or Down
    self.current_floor = current_floor #the current floor their on
    
  def find_passenger_destination_floor(self):
    if self.direction == "Up":
      self.destination_floor = random.randint(elevator_object.currentdirfloors[-1] + 1,10) 
    elif self.direction == "Down":
      self.destination_floor = random.randint(1,elevator_object.currentdirfloors[-1]- 1) 
    return self.destination_floor 
#______________________________________________________________________

class elevator():
  def __init__(self, direction, current_floor, destination_floor):
    self.queue = [] #queue for all passengers (regadless of direction)
    self.samedirqueue = [] #queue for all passengers travelling in the same direction
    self.finaldestqueue = [] #list to find the highest destination for all the passengers in same direction
    self.currentdirfloors = [] #list to find the floor numbers of all the people riding 
    self.ridingelevator = []
    self.direction = direction #direction which the elevator is travelling 
    self.current_floor = current_floor #the current floor the elevator is on
    self.state = "Idle"
    self.destination_floor = 0
    self.door = "Closed"

  def find_same_direction(self): #don't call - append passengers into list if direction is the same as elevator 
    for each in self.queue:
      if each.direction == self.direction:
        self.samedirqueue.append(each)

  def reset_elevator_queue(self): #dont call - resets self.samedirqueue and empties common passengers from self.queue
    global reset
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"The doors are opening")
    self.door = "Middle1"
    display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
    pygame.display.update()
    time.sleep(1)
    self.door = "Middle2"
    display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
    pygame.display.update()
    time.sleep(1)
    self.door = "Middle3"
    display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
    pygame.display.update()
    time.sleep(1)
    self.door = "Middle4"
    display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
    pygame.display.update()
    time.sleep(1)
    #time.sleep(time_buffer)
    self.door = "Offloading"
    t0 = time.time()
    while True:
      t1 = time.time()
      t = t1 - t0
      pygame.event.get()
      display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
      if hold.draw_button():
        t0 = time.time()
        t1 = time.time()
        add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"The door is being held")
      if t > time_buffer: 
        break
      exitingtext = buttonfont.render(f"Passenger(s) Exiting", False, black)
      screen.blit(exitingtext, (460, 510))
      pygame.display.update()
    display(elevator_object.door, self.current_floor, self.state, self.destination_floor)
    pygame.display.update()
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"The passenger(s) have gotten off")
    #time.sleep(time_buffer)
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"The doors are now closing")
    self.door = "Middle4"
    display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
    pygame.display.update()
    time.sleep(1)
    self.door = "Middle3"
    display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
    pygame.display.update()
    time.sleep(1)
    self.door = "Middle2"
    display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
    pygame.display.update()
    time.sleep(1)
    self.door = "Middle1"
    display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
    pygame.display.update()
    time.sleep(1)
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"The doors have now closed")
    self.door = "Closed"
    display(elevator_object.door, self.current_floor, self.state, self.destination_floor)
    pygame.display.update()
    if len(self.finaldestqueue) == 0:
      for i in self.queue[:]:
        if i in self.samedirqueue:
          self.queue.remove(i)
      self.samedirqueue.clear()
      self.ridingelevator.clear()
      
  def reset_elevator_direction(self): #dont call - changes elevator direction
    #this changes the direction of the elevator
    if self.direction == "Up":
      self.direction = "Down"
    elif self.direction == "Down": 
      self.direction = "Up"
    elif self.direction == "Idle":
      self.direction = self.queue[0].direction

  def find_stopping_floors(self, listarr): #if Up - ascending, if Down - descending
    if listarr == "stopping":
      if self.direction == "Up":
        self.currentdirfloors.sort()
      elif self.direction == "Down":
        self.currentdirfloors.sort(reverse = True)
    elif listarr == "destination":
      self.finaldestqueue = list(set(self.finaldestqueue))
      if self.direction == "Up":
        self.finaldestqueue.sort()
      elif self.direction == "Down":
        self.finaldestqueue.sort(reverse = True)

  def find_destination_floor(self): #callable - this to find the common drop off floor for all Up/Down passengers 
    self.find_same_direction()
    if len(self.samedirqueue) == 0:
      self.reset_elevator_direction()
      self.find_same_direction()
    for each in self.samedirqueue:
      self.currentdirfloors.append(each.current_floor)
    self.find_stopping_floors("stopping")
    for each in self.samedirqueue:
      self.finaldestqueue.append(each.find_passenger_destination_floor())
    self.find_stopping_floors("destination")
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"The passengers are getting off at floors -  {self.finaldestqueue}")

    
  def move_elevator_mechanics(self, first_passenger_floor):
    distance = abs(first_passenger_floor - self.current_floor)
    display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
    pygame.display.update()
    if first_passenger_floor > self.current_floor:
      self.state = "Up"
      while distance != 0:
        distance -= 1
        self.current_floor += 1
        display(elevator_object.door, self.current_floor, self.state, self.destination_floor)
        pygame.display.update()
        time.sleep(time_buffer)
    elif first_passenger_floor < self.current_floor:
      self.state = "Down"
      while distance != 0:
        distance -= 1
        self.current_floor -= 1
        display(elevator_object.door, self.current_floor, self.state, self.destination_floor)
        pygame.display.update()
        time.sleep(time_buffer)
    self.state = "Idle"
    display(elevator_object.door, self.current_floor, self.state, self.destination_floor)
    pygame.display.update()

  def animate_elevator(self, lists):
    if lists == self.currentdirfloors:
      self.move_elevator_mechanics(lists[0]) #move elevator to first passengers floor
      self.unpress_buttons(self.direction, self.current_floor)
      add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"The doors are opening to pick Up a passenger")
      self.door = "Middle1"
      display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
      pygame.display.update()
      time.sleep(1)
      self.door = "Middle2"
      display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
      pygame.display.update()
      time.sleep(1)
      self.door = "Middle3"
      display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
      pygame.display.update()
      time.sleep(1)
      self.door = "Middle4"
      display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
      pygame.display.update()
      time.sleep(1)
      add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"The doors are open...Passenger(s) are boarding")
      self.door = "Open"
      t0 = time.time()
      while True:
        t1 = time.time()
        t = t1 - t0
        pygame.event.get()
        display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
        if hold.draw_button():
          t0 = time.time()
          t1 = time.time()
        if t > time_buffer: 
          break
        loadingtext = buttonfont.render(f"Passenger(s) Loading", False, black)
        screen.blit(loadingtext, (460, 510))
        pygame.display.update()
      self.ridingelevator.append(lists[0]) #load passenger onto riding elevator list 
      lists.pop(0) #once boarded, remove passenger from list
      self.door = "Boarding"
      display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
      liststext = buttonfont.render(str(elevator_object.finaldestqueue), False, white)
      screen.blit(liststext, (530,590))
      pygame.display.update()
      time.sleep(time_buffer)
      add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"The passengers have boarded...The door is now closing")
      self.door = "Middle4"
      display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
      pygame.display.update()
      time.sleep(1)
      self.door = "Middle3"
      display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
      pygame.display.update()
      time.sleep(1)
      self.door = "Middle2"
      display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
      pygame.display.update()
      time.sleep(1)
      self.door = "Middle1"
      display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
      pygame.display.update()
      time.sleep(1)
      pygame.display.update()
      time.sleep(time_buffer)
      self.door = "Closed"
      display(elevator_object.door, self.current_floor,self.state, self.destination_floor)
      pygame.display.update()
      add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"The doors has now closed")
    elif lists == self.finaldestqueue:
      self.move_elevator_mechanics(self.finaldestqueue[0])
      self.finaldestqueue.pop(0)
      self.reset_elevator_queue()

  def move_elevator(self):
    while len(self.currentdirfloors) != 0:
      self.animate_elevator(self.currentdirfloors) 
    while len(self.finaldestqueue) != 0: 
      self.animate_elevator(self.finaldestqueue)
    time.sleep(time_buffer)

  def unpress_buttons(self, direction, level):
    global button_list
    for each in button_list:
      if each.text == direction and each.level == level: 
        each.unpress()
        display(elevator_object.door, self.current_floor, self.direction, self.destination_floor)
        pygame.display.update()
  
  def start_elevator(self):
    self.find_destination_floor()
    self.move_elevator()
    self.direction = "Idle"

#______________________________________________________________________
def add_to_queue(elevator, passenger):
  if len(elevator.queue) == 0:
    elevator.queue.append(passenger)
    elevator.direction = passenger.direction
  else:
    if passenger.direction == elevator.direction:
      elevator.queue.insert(0, passenger) #add to the beginning of the list 
    else:
      elevator.queue.append(passenger) #add to the end of the list 

def add_to_dictionary(time, command):
  global action_dictionary
  action_dictionary[time] = command
  
#_________________________________________________________________________

elevator_object = elevator("Idle", 1, None)
  
#____________
pygame.init()
screen_width = 750
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Elevator')
buttonfont = pygame.font.SysFont('Georgia', 20, italic = True)
textfont = pygame.font.SysFont('Georgia', 30, bold = True)
titlefont = pygame.font.SysFont('Georgia', 28, bold = True, italic = True)
instructionfont = pygame.font.SysFont('Georgia', 14, italic = True)
floorfont = pygame.font.SysFont('Georgia', 10)

#define colours
bg = (51, 36, 33)
gray = (220,220,220)
dark_gray = (169,169,169)
gold = (156,124,56)
dark_red = (128, 11, 25)
light_red = (249, 139, 133)
dark_green = (0,100,0)
light_green = (144,238,144)
black = (0, 0, 0)
white = (255, 255, 255)
clicked = False

class button():
  #colours for button and text
  button_col = gold
  hover_col = light_red
  click_col = dark_red
  text_col = black
  width = 80
  height = 45

  def __init__(self, x, y, text, type, level):
    self.x = x
    self.y = y
    self.text = text
    self.pressed = False
    self.type = type 
    self.level = level

  def draw_button(self):
    global clicked
    action = False

		#get mouse position
    pos = pygame.mouse.get_pos()

		#create pygame Rect object for the button
    button_rect = Rect(self.x, self.y, self.width, self.height)

    if self.type == "normal":
      #check mouseover and clicked conditions
      if button_rect.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] == 1:
          clicked = True
          self.pressed = True 
          pygame.draw.rect(screen, self.click_col, button_rect)
        elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
          clicked = False
          action = True
        else:
          pygame.draw.rect(screen, self.hover_col, button_rect)
      elif self.pressed == True:
        pygame.draw.rect(screen, self.click_col, button_rect)
      else:
        pygame.draw.rect(screen, self.button_col, button_rect)
    elif self.type == "hold":
      if button_rect.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] == 1:
          clicked = True
          pygame.draw.rect(screen, self.click_col, button_rect)
        elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
          clicked = False
          action = True
        else:
          pygame.draw.rect(screen, self.hover_col, button_rect)
      else:
        pygame.draw.rect(screen, self.button_col, button_rect)
		
		#add shading to button
    pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
    pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
    pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
    pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

    #add text to button
    text_img = buttonfont.render(self.text, True, self.text_col)
    text_len = text_img.get_width()
    screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 10))
    return action

  def unpress(self):
    self.pressed = False 


def display(door, current_floor, state, destination):
  global open
  draw()
  rect12 = Rect(420, 162, 297, 61)
  pygame.draw.rect(screen, dark_gray, rect12)
  pygame.draw.line(screen, white, (415, 160), (720, 160), 3) #line below the instructions
  destinationtext = buttonfont.render(f"Passenger(s) Selected: ", False, white)
  screen.blit(destinationtext, (448,554))
  floortext = buttonfont.render("Floor(s): ", False, white)
  screen.blit(floortext, (435,590))
  #display vertical floor position
  x = 283
  if current_floor == 1:  
    y = 723
  if current_floor == 2:  
    y = 648
  if current_floor == 3:  
    y = 571
  if current_floor == 4:  
    y = 494
  if current_floor == 5:  
    y = 417
  if current_floor == 6:  
    y = 340
  if current_floor == 7:  
    y = 263
  if current_floor == 8:  
    y = 186
  if current_floor == 9:  
    y = 109
  if current_floor == 10:  
    y = 32
  rect = Rect(x, y, 80, 45)
  pygame.draw.rect(screen, (192,192,192), rect)
  text_img = buttonfont.render(state, True, black)
  text_len = text_img.get_width()
  screen.blit(text_img, (x + int(80 / 2) - int(text_len / 2), y + 10))
  pygame.draw.line(screen, white, (320, 25), (320, y), 2)
  #display floor number
  rect2 = Rect(525, 170, 80, 45)
  pygame.draw.rect(screen, gold, rect2)
  text_img2 = buttonfont.render(str(current_floor), True, dark_red)
  text_len2 = text_img2.get_width()
  screen.blit(text_img2, (525 + int(80 / 2) - int(text_len2 / 2), 170 + 10))
  rect3 = Rect(283, 15, 80, 10)
  pygame.draw.rect(screen, (192,192,192), rect3)
  #door animations 
  if door == "Closed":
    rect4 = Rect(420, 229, 147, 320)
    pygame.draw.rect(screen, dark_gray, rect4)
    rect5 = Rect(570, 229, 147, 320)
    pygame.draw.rect(screen, dark_gray, rect5)
    pygame.draw.line(screen, black, (567, 229), (567, 548), 4)  
    pygame.draw.rect(screen, black, pygame.Rect(420, 229, 297, 320), 4)
  elif door == "Middle1":
    rect13 = Rect(420, 229, 295, 320)
    pygame.draw.rect(screen, dark_gray, rect13)
    rect14 = Rect(560, 229, 12, 320)
    pygame.draw.rect(screen, white, rect14)
    pygame.draw.line(screen, black, (560, 229), (560, 548), 4) 
    pygame.draw.line(screen, black, (572, 229), (572, 548), 4)
    pygame.draw.rect(screen, black, pygame.Rect(420, 229, 297, 320), 4)
  elif door == "Middle2":
    rect15 = Rect(420, 229, 295, 320)
    pygame.draw.rect(screen, dark_gray, rect15)
    rect16 = Rect(535, 229, 60, 320)
    pygame.draw.rect(screen, white, rect16)
    pygame.draw.line(screen, black, (532, 229), (532, 548), 4) 
    pygame.draw.line(screen, black, (592, 229), (592, 548), 4)
    pygame.draw.rect(screen, black, pygame.Rect(420, 229, 297, 320), 4)
  elif door == "Middle3":
    rect17 = Rect(420, 229, 80, 320)
    pygame.draw.rect(screen, dark_gray, rect17)
    rect18 = Rect(630, 229, 87, 320)
    pygame.draw.rect(screen, dark_gray, rect18)
    rect19 = Rect(501, 229, 130, 320)
    pygame.draw.rect(screen, white, rect19)
    pygame.draw.line(screen, black, (500, 229), (500, 548), 4) 
    pygame.draw.line(screen, black, (630, 229), (630, 548), 4)
    pygame.draw.rect(screen, black, pygame.Rect(420, 229, 297, 320), 4)
  elif door == "Middle4":
    rect20 = Rect(420, 229, 80, 320)
    pygame.draw.rect(screen, dark_gray, rect20)
    rect21 = Rect(630, 229, 87, 320)
    pygame.draw.rect(screen, dark_gray, rect21)
    rect22 = Rect(475, 229, 190, 320)
    pygame.draw.rect(screen, white, rect22)
    pygame.draw.line(screen, black, (475, 229), (475, 548), 4) 
    pygame.draw.line(screen, black, (665, 229), (665, 548), 4)
    pygame.draw.rect(screen, black, pygame.Rect(420, 229, 297, 320), 4)
  else:
    rect6 = Rect(420, 229, 15, 320)
    pygame.draw.rect(screen, dark_gray, rect6)
    rect7 = Rect(699, 229, 15, 320)
    pygame.draw.rect(screen, dark_gray, rect7)
    pygame.draw.line(screen, black, (435, 229), (435, 548), 4) 
    pygame.draw.line(screen, black, (699, 229), (699, 548), 4)
    rect8 = Rect(440, 229, 255, 320)
    pygame.draw.rect(screen, white, rect8)
    pygame.draw.rect(screen, black, pygame.Rect(420, 229, 297, 320), 4)
    #person
    pygame.draw.circle(screen, black, (560,300), 35) #head
    pygame.draw.line(screen, black, (560, 300), (560, 460), 7) #spine
    pygame.draw.line(screen, black, (560, 360), (510, 395), 7) #left arm
    pygame.draw.line(screen, black, (560, 360), (610, 395), 7) #right arm
    pygame.draw.line(screen, black, (560, 460), (510, 495), 7) #left leg
    pygame.draw.line(screen, black, (560, 460), (610, 495), 7) #right leg
    
  #display arrows
  if state == "Up":
    up_color = dark_green
    down_color = light_red
  elif state == "Down":
    up_color = light_green
    down_color = dark_red
  elif state == "Idle":
    up_color = light_green
    down_color = light_red
  pygame.draw.polygon(screen, up_color, ((450,215), (465,215), (465,190), (480, 190), (458,171), (435,190), (450,190)))
  pygame.draw.polygon(screen, down_color, ((680,171),(665,171), (665,196), (650,196), (672,215), (695,196), (680,196)))

    
level1up = button(70, 723, 'Up', "normal", 1)
level2up = button(70, 648, 'Up', "normal", 2)
level2down = button(165, 648, 'Down', "normal", 2)
level3up = button(70, 571, 'Up', "normal", 3)
level3down = button(165, 571, 'Down', "normal", 3)
level4up = button(70, 494, 'Up', "normal", 4)
level4down = button(165, 494, 'Down', "normal", 4)
level5up = button(70, 417, 'Up', "normal", 5)
level5down = button(165, 417, 'Down', "normal", 5)
level6up = button(70, 340, 'Up', "normal", 6)
level6down = button(165, 340, 'Down', "normal", 6)
level7up = button(70, 263, 'Up', "normal", 7)
level7down = button(165, 263, 'Down', "normal", 7)
level8up = button(70, 186, 'Up', "normal", 8)
level8down = button(165, 186, 'Down', "normal", 8)
level9up = button(70, 109, 'Up', "normal", 9)
level9down = button(165, 109, 'Down', "normal", 9)
level10down = button(165, 32, 'Down', "normal", 10)
button_list = [level1up,level2up,level2down,level3up,level3down, level4up,level4down, level5up,level5down, level6up,level6down, level7up,level7down, level8up,level8down, level9up, level9down, level10down]
start = button(600, 686, "Start", "hold", 1)
hold = button(450, 686, "Hold", "hold", 1)
elevator_floor1 = textfont.render('1', False, white)
elevator_floor2 = textfont.render('2', False, white)
elevator_floor3 = textfont.render('3', False, white)
elevator_floor4 = textfont.render('4', False, white)
elevator_floor5 = textfont.render('5', False, white)
elevator_floor6 = textfont.render('6', False, white)
elevator_floor7 = textfont.render('7', False, white)
elevator_floor8 = textfont.render('8', False, white)
elevator_floor9 = textfont.render('9', False, white)
elevator_floor10 = textfont.render('10', False, white)
elevator_title = titlefont.render("The Smith Machine", False, white)
instructions1 = instructionfont.render("Press buttons to register all of the", False, white)
instructions2 = instructionfont.render("passengers, then click the start button", False, white)


def draw():
  screen.fill(bg)
  screen.blit(elevator_floor1, (25,725))
  screen.blit(elevator_floor2, (25,648))
  screen.blit(elevator_floor3, (25,571))
  screen.blit(elevator_floor4, (25,494))
  screen.blit(elevator_floor5, (25,417))
  screen.blit(elevator_floor6, (25,340))
  screen.blit(elevator_floor7, (25,263))
  screen.blit(elevator_floor8, (25,186))
  screen.blit(elevator_floor9, (25,109))
  screen.blit(elevator_floor10, (25,32))
  screen.blit(elevator_title, (415,15))
  screen.blit(instructions1, (450,90))
  screen.blit(instructions2, (430,120))
  pygame.draw.line(screen, white, (415, 160), (720, 160), 3) #line below the instructions
  pygame.draw.rect(screen, white, (10, 25, 250, 760), 3) #rectangle around Up/Down buttons
  pygame.draw.line(screen, white, (415, 55), (720, 55), 4) #line underneath "The Smith Machine"
  pygame.draw.rect(screen, white, (260, 25, 125, 760), 3) #Rectangle for elevator position
  pygame.draw.rect(screen, white, (415, 70, 307, 715), 5) #Rectangle for the box underneath title
  pygame.draw.line(screen, white, (415, 550), (720, 550), 6) #line above hold button
  pygame.draw.line(screen, white, (415, 640), (720, 640), 6) #line above arrows and floor number
  pygame.draw.line(screen, white, (415, 225), (720, 225), 6) #line below Destination Floor 
  
  #________
  if level1up.draw_button():
    add_to_queue(elevator_object, person("Up", 1))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 1 Up")
  if level2up.draw_button():
    add_to_queue(elevator_object, person("Up", 2))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 2 Up")
  if level3up.draw_button():
    add_to_queue(elevator_object, person("Up", 3))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 3 Up")
  if level4up.draw_button():
    add_to_queue(elevator_object, person("Up", 4))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 4 Up")
  if level5up.draw_button():
    add_to_queue(elevator_object, person("Up", 5))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 5 Up")
  if level6up.draw_button():
    add_to_queue(elevator_object, person("Up", 6))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 6 Up")
  if level7up.draw_button():
    add_to_queue(elevator_object, person("Up", 7))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 7 Up")
  if level8up.draw_button():
    add_to_queue(elevator_object, person("Up", 8))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 8 Up")
  if level9up.draw_button():
    add_to_queue(elevator_object, person("Up", 9))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 9 Up")
  if level2down.draw_button():
    add_to_queue(elevator_object, person("Down", 2))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 2 Down")
  if level3down.draw_button():
    add_to_queue(elevator_object, person("Down", 3))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 3 Down")
  if level4down.draw_button():
    add_to_queue(elevator_object, person("Down", 4))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 4 Down")
  if level5down.draw_button():
    add_to_queue(elevator_object, person("Down", 5))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 5 Down")
  if level6down.draw_button():
    add_to_queue(elevator_object, person("Down", 6))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 6 Down")
  if level7down.draw_button():
    add_to_queue(elevator_object, person("Down", 7))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 7 Down")
  if level8down.draw_button():
    add_to_queue(elevator_object, person("Down", 8))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 8 Down")
  if level9down.draw_button():
    add_to_queue(elevator_object, person("Down", 9))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 9 Down")
  if level10down.draw_button():
    add_to_queue(elevator_object, person("Down", 10))
    add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Button Pressed: Level 10 Down")
run = True

t0 = datetime.now()
while run:
  t1 = datetime.now()
  t = t1 - t0
  display(elevator_object.door, elevator_object.current_floor, elevator_object.state, elevator_object.destination_floor) #updates screen
  if start.draw_button(): #if start is clicked 
    while len(elevator_object.queue) != 0: #as long as there are passengers in the elevator
      elevator_object.start_elevator() #this single line picks/drops everyone
      t0 = datetime.now()
  if t.seconds > 59:
    if elevator_object.current_floor != 1:
      elevator_object.move_elevator_mechanics(1)
      add_to_dictionary(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "60 Seconds Idle: Returning to Ground Floor")
    t0 = datetime.now()
  pygame.display.update()
                      
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      with open('file.txt','w') as x: 
        x.write(str(action_dictionary))

pygame.quit()
