from Tkinter import Tk, Canvas


class Manager(object):
    root = Tk()
    canvas = Canvas(root, width=500, height=500)
    elements = []
    stage = None

    mouse_x = 0
    mouse_y = 0
    prev_x = 0
    prev_y = 0
    frame_number = 1
    mouse_down = False

    default_gravity = False

    def __init__(self):
        #Keeping here essentially global variables to get the mouse position and whether it's pressed at any given moment.
        def global_mouse(event):
            Manager.prev_x, Manager.prev_y = Manager.mouse_x, Manager.mouse_y
            Manager.mouse_x, Manager.mouse_y = event.x - Manager.canvas.winfo_reqwidth()/2, Manager.canvas.winfo_reqheight()/2 - event.y
            #print " MOUSE LOCS", Manager.mouse_x, Manager.mouse_y
        Manager.canvas.bind('<Motion>', global_mouse, add="+")

        def mouse_press(event):
            Manager.mouse_down = True
        def mouse_release(event):
            Manager.mouse_down = False
        self.canvas.bind("<Button-1>", mouse_press, add="+")
        self.canvas.bind("<ButtonRelease-1>", mouse_release, add="+")

    ## THE FRAME MANAGER, THE MOST IMPORTANT FUNCTION. ##

    def run(self):
        Manager.frame_number += 1
        self.canvas.delete("all")
        ## THIS IS WHERE THE CHECKS FOR GRAVITY AND SPEED WOULD GO ##
        self.update_animation()
        self.update_physics()
        self.update_collision()
        self.update_events()
        ## THIS IS THE END OF THE UPDATES FOR SPEED AND GRAVITY ##

        for e in self.elements:
            e.draw()
        self.canvas.update()

    ## ^ THE ABOVE FUNCTION RUNS EVERYTHING ^ ##

    def update_physics(self):
        for e in self.elements:
            if e.physics_true:
                e.update_physics()

    def update_animation(self):
        for e in self.elements:
            e.update_animation()

    def update_collision(self):
        for e in self.elements:
            e.update_collision()

    def update_events(self):
        for e in self.elements:
            e.update_events()

