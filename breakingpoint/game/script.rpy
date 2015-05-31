
define e = Character('Eileen', color="#c8ffc8")


init python:
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
    
    $ rec1 = Rec((start_x, start_y + car_height), (start_x + car_width, start_y + car_height), (start_x, start_y), (start_x + car_width, start_y), "back") 
    $ rec2 = Rec((start_x, start_y + car_gap + 2*car_height), (start_x + car_width, start_y + car_gap + 2*car_height), (start_x, start_y + car_gap + car_height), (start_x + car_width, start_y + car_gap + car_height)) 
    $ rec3 = Rec((start_x, start_y + 2*car_gap + 3*car_height), (start_x + car_width, start_y + 2*car_gap + 3*car_height), (start_x, start_y + 2*car_gap + 2*car_height), (start_x + car_width, start_y + 2*car_gap + 2*car_height), "forward")
    
    image rec = "slot.png"
    image road = im.Scale("road.png", 800, 600)
    
    #image rec1_image = rec1.render()
    #image rec2_image = rec2.render()
    #image rec3_image = rec3.render()
    
    #$ rec1_image = rec1.render()
    #$ rec2_image = rec2.render()
    #$ rec3_image = rec3.render()
    
screen sample:
    
    #$ renpy.image("rec1_image", rec1.render())
    #$ renpy.image("rec2_image", rec2.render())
    #$ renpy.image("rec3_image", rec3.render())
    
    add "rec" pos rec1.top_left size rec1.dimensions
    #add "rec" pos rec2.top_left size rec2.dimensions
    add "rec" pos rec3.top_left size rec3.dimensions
    
screen control:
    $ rec1_status = rec2.is_colliding(rec1)
    $ rec3_status = rec2.is_colliding(rec3)
    
    textbutton "Forward" action Jump('forward_control')
    textbutton "Back" action Jump('back_control') ypos 0.1
    text "[rec1_status]" xpos 0.8
    text "[rec3_status]" xpos 0.9
    add "rec" pos rec2.top_left size rec2.dimensions
    
label forward_control:
    hide screen control
    $ rec2.forward()
    jump start
    #show screen control
    
label back_control:
    hide screen control
    $ rec2.back()
    jump start
    #show screen control
    

label start:
    scene road #with dissolve

    #e "You've created a new Ren'Py game."
    #$ renpy.transition(dissolve)
    show screen control #with dissolve
    
    python:
        def swerve(limit):
            counter = 0
            
            while counter < limit:
                renpy.hide_screen('sample')
                rec1.swerve()
                rec3.swerve()
                renpy.show_screen('sample')
                renpy.pause(1)
                counter += 1

    $ swerve(100)
    #$ swerve()
    #$ swerve()
    #$ swerve()
    #$ swerve()
    #$ swerve()
    
    
    e "Once you add a story, pictures, and music, you can release it to the world!"

    return
