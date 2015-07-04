
define e = Character('Eileen', color="#c8ffc8")


init python:
    import copy
    
    full_counter = 0
    full_movement = None
    
    class Rec:
        def __init__(self, img, bottom_left, bottom_right, top_left, top_right, property=None):
            self.bottom_left = list(bottom_left)
            self.bottom_right = list(bottom_right)
            self.top_left = list(top_left)
            self.top_right = list(top_right)
            self.width = bottom_right[0] - bottom_left[0]
            self.height = bottom_left[1] - top_left[1]
            self.dimensions = (self.width, self.height)
            self.points = [self.bottom_left, self.bottom_right, self.top_left, self.top_right]
            self.original_points = [tuple(point) for point in self.points]
            self.original_top_left = tuple(self.top_left)
            self.property = property
            self.hidden = False
            self.img = img
            
        def __eq__(self, other):
            return self.top_left == other.top_left
            
        def respawn(self):
            self.points = [list(point) for point in self.original_points]
            self.bottom_left, self.bottom_right, self.top_left, self.top_right = list(self.points[0]), list(self.points[1]), list(self.points[2]), list(self.points[3])
            self.hidden = False
            
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
            
            
        def forward(self, extra=0):
            y_delta = -5 - extra
            
            for point in self.points:
                point[1] += y_delta
                
        def back(self, extra=0):
            y_delta = 5 + extra
            
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
                
        def is_off_screen(self):
            if not self.top_left[0] in range(0, config.screen_width):
                return True
                
            if not self.top_left[1] in range(0, config.screen_height):
                return True
                
            if not self.bottom_left[0] in range(0, config.screen_width):
                return True
                
            if not self.bottom_left[1] in range(0, config.screen_height):
                return True
                
            return False
            
        def render(self):
            #return renpy.image
            return Solid((0, 0, 0, 150), area=(self.top_left[0], self.top_left[1], self.width, self.height))
            
        def __repr__(self):
            return '<Rec>: {} {} {} {}'.format(self.top_left[0], self.top_left[1], self.width, self.height)
            
init:
    $ start_x = 140 #/ config.screen_width
    $ start_y = 50 #/ config.screen_height
    $ car_width = 70 #/ config.screen_width
    $ car_height = 120 #/ config.screen_height
    $ car_gap = 50 #/ config.screen_height
    
    image rec = "slot.png"
    image barricade = im.Scale("barricade.png", 50, 10)
    image road = im.Scale("road.png", config.screen_width, config.screen_height)
    image tree = im.Scale("tree.png", 60, 160)
    image tree2 = im.Scale("tree.png", 60, 160)
    image light = im.Scale("light.png", 60, 160)
    image light2 = im.Flip(im.Scale("light.png", 60, 160), horizontal=True)
    image traffic = im.Scale("trafficlight.png", 100, 200)
    image redcircle = im.Scale("redcircle.png", 80, 80)
    #image up_arrow = im.Scale("up.png", 40, 40)
    #image down_arrow = im.Flip(im.Scale("up.png", 40, 40), vertical=True)
    
    image up_arrow:
        "up.png"
        size (40, 40) alpha 0.5
    
    image down_arrow:
        "up.png"
        size (40, 40) rotate 180 alpha 0.5
        
    image left_arrow:
        "up.png"
        size (40, 40) rotate 270 alpha 0.5
        
    image right_arrow:
        "up.png"
        size (40, 40) rotate 90 alpha 0.5
    
    $ road_left = Position(xpos=30, ypos=-200)
    $ road_right = Position(xpos=280, ypos=-200)
    $ road_left_tree = Position(xpos=30, ypos=-200)
    $ road_right_tree = Position(xpos=280, ypos=-200)
    
label load_resources:
    
    $ rec1 = Rec("rec", (start_x, start_y + car_height), (start_x + car_width, start_y + car_height), (start_x, start_y), (start_x + car_width, start_y), )#"back") 
    $ rec2 = Rec("rec", (start_x, start_y + car_gap + 2*car_height), (start_x + car_width, start_y + car_gap + 2*car_height), (start_x, start_y + car_gap + car_height), (start_x + car_width, start_y + car_gap + car_height)) 
    $ rec3 = Rec("rec", (start_x, start_y + 2*car_gap + 3*car_height), (start_x + car_width, start_y + 2*car_gap + 3*car_height), (start_x, start_y + 2*car_gap + 2*car_height), (start_x + car_width, start_y + 2*car_gap + 2*car_height),)# "forward")
    
    $ obs1 = Rec("barricade", (40, 50), (90, 50), (40, 10), (90, 10))  
    $ obs2 = Rec("barricade", (250, 50), (300, 50), (250, 10), (300, 10)) 
    
    $ truck = Rec("rec", (200, 590), (250, 590), (200, 470), (250, 470)) 
    
    $ other_objects = [store.rec1, store.rec3, store.obs1, store.obs2] # store.truck]
    
    return

screen sample:
    
    add "rec" pos rec2.top_left size rec2.dimensions
    
    for obj in other_objects:
        if not obj.hidden:
            add obj.img pos obj.top_left size obj.dimensions
        
    #add "rec" pos rec1.top_left size rec1.dimensions
    #add "rec" pos rec2.top_left size rec2.dimensions
    #add "rec" pos rec3.top_left size rec3.dimensions
    #add "barricade" pos obs1.top_left size obs1.dimensions
    #add "barricade" pos obs2.top_left size obs2.dimensions
    
screen control:
    $ rec1_status = rec2.is_colliding(rec1)
    $ obs1_status = obs1.is_colliding(rec1)
    
    imagebutton idle "up_arrow" hover "up_arrow" action Jump('forward_control') hovered Jump('forward_control') alternate Jump('forward_control') xpos 280 ypos 0.5
    imagebutton idle "down_arrow" hover "down_arrow" action Jump('back_control') hovered Jump('back_control') alternate Jump('back_control') xpos 272 ypos 0.61
    imagebutton idle "right_arrow" hover "right_arrow" action Jump('right_control') hovered Jump('right_control') alternate Jump('right_control') xpos 295 ypos 0.55
    imagebutton idle "left_arrow" hover "left_arrow" action Jump('left_control') hovered Jump('left_control') alternate Jump('left_control') xpos 250 ypos 0.55
    
    #text "[rec1_status]" xpos 0.8
    #text "[obs1_status]" xpos 0.9
    text "[full_counter]" xpos 0.7
    #add "rec" pos rec2.top_left size rec2.dimensions
    #add "redcircle" xpos 0.85 ypos 0.4
    #text "{color=#000}[speed_limit]{/color}" xpos 0.88 ypos 0.45
    
label forward_control:
    hide screen control
    python:
        full_counter += 1
    $ rec2.forward(5)
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
    
    call load_resources
    
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
        
        def move_recs(movement, off_screen=True):
            
            if off_screen:
                movement = 'apart'
            
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
        
        def clean_items(items):
            for item in items:
                if item.is_off_screen():
                    item.hidden = True
                    items.remove(item)
                    
                if rec2.is_colliding(item):
                    renpy.jump('gameover')
            
        
        def normal_movement():
            rec1.swerve()
            rec3.swerve()
            rec2.back(-2)
            
            if not store.obs1.hidden:
                store.obs1.back(10)
                
            if not store.obs2.hidden:
                store.obs2.back(5)
                
        def truck_movement():
                
            if not store.truck.hidden:
                store.truck.forward(10)
        
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
                
                if 20 < full_counter < 120:
                    move_recs(full_movement, off_screen=True)
                    
                    if store.truck in other_objects:
                        truck_movement()
                    
                    if store.rec1 in other_objects or store.rec3 in other_objects:
                        pass
                    else:
                        other_objects.append(store.truck)
                    
                else:
                    move_recs(full_movement)
                
                normal_movement()
                
                clean_items(other_objects)
                        
                
                # respawn
                if obs1.is_off_screen():
                    store.obs1.respawn()
                    #store.obs1 = Rec((40, 50), (90, 50), (40, 10), (90, 10), property="back")
                    
                if obs2.is_off_screen():
                    store.obs2.respawn()
                    #store.obs2 = Rec((250, 50), (300, 50), (250, 10), (300, 10), property="back") 
                
                renpy.show_screen('sample')
                renpy.pause(0.5)
                full_counter += 1

    #$ rec2.back()
    $ swerve(1000)
    
    e "Once you add a story, pictures, and music, you can release it to the world!"

    return
    
label gameover:
    hide screen control
    hide screen sample
    hide tree
    hide tree2
    hide light
    hide light2
    "GAMEOVER"
    "Your score is [full_counter]"
    $ full_counter = 0
    return
    #$ renpy.full_restart()
