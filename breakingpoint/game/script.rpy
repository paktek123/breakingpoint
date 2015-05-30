
define e = Character('Eileen', color="#c8ffc8")


init python:
    class Rec:
        def __init__(self, bottom_left, bottom_right, top_left, top_right):
            self.bottom_left = bottom_left
            self.bottom_right = bottom_right
            self.top_left = top_left
            self.top_right = top_right
            self.width = bottom_right[0] - bottom_left[0]
            self.height = bottom_left[1] - top_left[1]
            
        def is_colliding(self, rectangle):
            # top left corner colliding
            if rectangle.top_left[0] in range(self.bottom_left[0], self.bottom_right[0]) and rectangle.top_left[1] in range(self.bottom_left[1], self.bottom_right[1]):
                return True
                
            # top right corner colliding
            if rectangle.top_right[0] in range(self.bottom_left[0], self.bottom_right[0]) and rectangle.top_right[1] in range(self.bottom_left[1], self.bottom_right[1]):
                return True
                
            # bottom left corner colliding
            if rectangle.bottom_left[0] in range(self.top_left[0], self.top_right[0]) and rectangle.bottom_left[1] in range(self.top_left[1], self.top_right[1]):
                return True
                
            # bottom right corner colliding
            if rectangle.bottom_right[0] in range(self.top_left[0], self.top_right[0]) and rectangle.bottom_right[1] in range(self.top_left[1], self.top_right[1]):
                return True
                
            return False
            
        def render(self):
            return Solid((0, 0, 0, 150), area=(self.top_left[0], self.top_left[1], self.width, self.height))
            
        def __repr__(self):
            return '<Rec>: {} {} {} {}'.format(self.top_left[0], self.top_left[1], self.width, self.height)
            
init:
    $ rec1 = Rec((250, 150), (300, 150), (250, 50), (300, 50)) 
    $ rec2 = Rec((250, 300), (300, 300), (250, 200), (300, 200)) 
    $ rec3 = Rec((250, 450), (300, 450), (250, 350), (300, 350))
    
    image rec1_image = rec1.render()
    image rec2_image = rec2.render()
    image rec3_image = rec3.render()
    
screen sample:
    add "rec1_image"
    add "rec2_image"
    add "rec3_image"

label start:

    e "You've created a new Ren'Py game."
    
    show screen sample

    e "Once you add a story, pictures, and music, you can release it to the world!"

    return
