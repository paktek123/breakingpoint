
define e = Character('Eileen', color="#c8ffc8")


init python:
    full_counter = 0
    full_movement = None
    
    class Rec:
        def __init__(self, bottom_left, bottom_right, top_left, top_right, property=None):
            self.bottom_left = list(bottom_left)
            self.bottom_right = list(bottom_right)
            self.top_left = list(top_left)
            self.top_right = list(top_right)
            self.width = bottom_right[0] - bottom_left[0]
            self.height = bottom_left[1] - top_left[1]
            self.dimensions = (self.width, self.height)
            self.points = [self.bottom_left, self.bottom_right, self.top_left, self.top_right]
            self.property = property
            
        def is_colliding(self, rectangle):
            # top left corner colliding
            if rectangle.top_left[0] in range(self.bottom_left[0], self.bottom_right[0]) and rectangle.top_left[1] in range(self.top_right[1], self.bottom_right[1]):
                return True
                
            # top right corner colliding
            if rectangle.top_right[0] in range(self.bottom_left[0], self.bottom_right[0]) and rectangle.top_right[1] in range(self.top_left[1], self.bottom_left[1]):
                return True
                
            # bottom left corner colliding
            if rectangle.bottom_left[0] in range(self.top_left[0], self.top_right[0]) and rectangle.bottom_left[1] in range(self.top_right[1], self.bottom_right[1]):
                return True
                
            # bottom right corner colliding
            if rectangle.bottom_right[0] in range(self.top_left[0], self.top_right[0]) and rectangle.bottom_right[1] in range(self.top_left[1], self.bottom_left[1]):
                return True
                
            return False
            
        def swerve(self):
            x_delta = renpy.random.randint(-5, 5)
            
            if self.property == "forward":
                y_delta = renpy.random.randint(-5, 1)
            elif self.property == "back":
                y_delta = renpy.random.randint(-1, 5)
            else:
                y_delta = 0
            
            for point in self.points:
                point[0] += x_delta
                point[1] += y_delta
            
            
        def forward(self):
            y_delta = -5
            
            for point in self.points:
                point[1] += y_delta
                
        def back(self):
            y_delta = 5
            
            for point in self.points:
                point[1] += y_delta
                
        def left(self):
            x_delta = -5
            
            for point in self.points:
                point[0] += x_delta
                
        def right(self):
            x_delta = 5
            
            for point in self.points:
                point[0] += x_delta
            
        def render(self):
            #return renpy.image
            return Solid((0, 0, 0, 150), area=(self.top_left[0], self.top_left[1], self.width, self.height))
            
        def __repr__(self):
            return '<Rec>: {} {} {} {}'.format(self.top_left[0], self.top_left[1], self.width, self.height)
            
init:
    $ start_x = 350
    $ start_y = 50
    $ car_width = 100
    $ car_height = 150
    $ car_gap = 30
    
    $ rec1 = Rec((start_x, start_y + car_height), (start_x + car_width, start_y + car_height), (start_x, start_y), (start_x + car_width, start_y), )#"back") 
    $ rec2 = Rec((start_x, start_y + car_gap + 2*car_height), (start_x + car_width, start_y + car_gap + 2*car_height), (start_x, start_y + car_gap + car_height), (start_x + car_width, start_y + car_gap + car_height)) 
    $ rec3 = Rec((start_x, start_y + 2*car_gap + 3*car_height), (start_x + car_width, start_y + 2*car_gap + 3*car_height), (start_x, start_y + 2*car_gap + 2*car_height), (start_x + car_width, start_y + 2*car_gap + 2*car_height),)# "forward")
    
    $ obs1 = Rec((150, 50), (230, 50), (150, 10), (230, 10))  
    
    image rec = "slot.png"
    image barricade = im.Scale("barricade.png", 50, 10)
    image road = im.Scale("road.png", 800, 600)
    image tree = im.Scale("tree.png", 100, 200)
    image tree2 = im.Scale("tree.png", 100, 200)
    image light = im.Scale("light.png", 100, 200)
    image light2 = im.Flip(im.Scale("light.png", 100, 200), horizontal=True)
    image traffic = im.Scale("trafficlight.png", 100, 200)
    image redcircle = im.Scale("redcircle.png", 80, 80)
    
    $ road_left = Position(xpos=100, ypos=-200)
    $ road_right = Position(xpos=600, ypos=-200)
    $ road_left_tree = Position(xpos=50, ypos=-200)
    $ road_right_tree = Position(xpos=650, ypos=-200)
    
    
screen sample:
    
    add "rec" pos rec1.top_left size rec1.dimensions
    #add "rec" pos rec2.top_left size rec2.dimensions
    add "rec" pos rec3.top_left size rec3.dimensions
    add "barricade" pos obs1.top_left size obs1.dimensions
    
screen control:
    $ rec1_status = rec2.is_colliding(rec1)
    $ obs1_status = rec2.is_colliding(obs1)
    
    textbutton "Forward" action Jump('forward_control')
    textbutton "Back" action Jump('back_control') ypos 0.1
    textbutton "Right" action Jump('right_control') ypos 0.2
    textbutton "Left" action Jump('left_control') ypos 0.3
    text "[rec1_status]" xpos 0.8
    text "[obs1_status]" xpos 0.9
    text "[full_counter]" xpos 0.7
    add "rec" pos rec2.top_left size rec2.dimensions
    add "redcircle" xpos 0.85 ypos 0.4
    text "{color=#000}[speed_limit]{/color}" xpos 0.88 ypos 0.45
    
label forward_control:
    hide screen control
    python:
        full_counter += 1
    $ rec2.forward()
    jump main_loop
    
label back_control:
    hide screen control
    python:
        full_counter += 1
    $ rec2.back()
    jump main_loop
    
label left_control:
    hide screen control
    python:
        full_counter += 1
    $ rec2.left()
    jump main_loop
    
label right_control:
    hide screen control
    python:
        full_counter += 1
    $ rec2.right()
    jump main_loop
    

label start:
    scene road #with dissolve
    $ speed_limit = 30
    
    show tree at road_left_tree:
        linear 4.0 yalign 3.0
        linear 0.0 yalign 0.0
        repeat
        
    show tree2 at road_right_tree:
        linear 4.0 yalign 3.0
        linear 0.0 yalign 0.0
        repeat
        
    show light at road_left:
        linear 5.0 yalign 3.0
        linear 0.0 yalign 0.0
        repeat
        
    show light2 at road_right:
        linear 5.0 yalign 3.0
        linear 0.0 yalign 0.0
        repeat

label main_loop:

    show screen control #with dissolve
    
    python:
        import random
        
        def move_recs(movement):
            if movement == "back":
                store.speed_limit = 20
            elif movement == "forward":
                store.speed_limit = 40
            else:
                store.speed_limit = 30
                
            if movement == "apart":
                rec1.property = "forward"
                rec3.property = "back"
            elif movement == "squeeze":
                rec1.property = "back"
                rec3.property = "forward"
            else:
                rec1.property = movement
                rec3.property = movement
        
        def swerve(limit):
            move_choice = ["back", "forward", "apart", "squeeze", None]
            global full_counter
            global full_movement
            
            while full_counter < limit:
                renpy.hide_screen('sample')
                
                if full_counter in range(1, 10) and not full_movement:
                    move_choice = ["back", "forward"]
                
                if not full_counter % 10:
                    full_movement = random.choice(move_choice)
                
                move_recs(full_movement)
                
                rec1.swerve()
                rec3.swerve()
                obs1.back()
                renpy.show_screen('sample')
                renpy.pause(0.5)
                full_counter += 1

    $ swerve(1000)
    
    e "Once you add a story, pictures, and music, you can release it to the world!"

    return
