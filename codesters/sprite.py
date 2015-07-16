import math
from PIL import Image, ImageTk
from .manager import Manager

class SpriteClass(object):

    ## PIVOTAL FUNCTIONS ##
    def __init__(self, image):
        self.canvas = Manager.canvas
        Manager.elements.append(self)

        # Default values
        self.type = Sprite

        self.xcor = 0
        self.ycor = 0
        self.xspeed = 0
        self.yspeed = 0
        self.speed = 1
        self.modes=[]
        self.size = 1
        self.color = 'white'
        self.heading = 0

        self.photo = Image.open("./codesters/sprites/codestersLogo.gif")
        self.base_photo = Image.open("./codesters/sprites/codestersLogo.gif")

        self.hidden = False

        self.future_heading = 0
        self.animation_duration = 1000
        self.animation_x_coords = []
        self.animation_y_coords = []
        self.animation_rotation_degrees = []
        self.animation_index = 0
        self.rotation_direction=1
        self.future_x = 0
        self.future_y = 0
        self.angle = 0
        self.step_size = 0

        self.wait_list = []
        self.total_wait_time = 0
        self.future_most_recent_wait_time = 0

        self.say_text = ""
        self.say_color = ""
        self.say_size = 0
        self.say_time = 0
        self.say_font = ""

        self.paused = False

        self.gravity = 1
        self.gravity_true = False
        self.physics_true = False

        self.goal = False
        self.hazard = False
        self.collision = False
        self.drag = False

        self.opacity = 255

        self.x_flip_plans = []
        self.y_flip_plans = []
        self.x_flipped = False
        self.y_flipped = False

        self.scale_plans = []

        self.pen = False
        self.pen_color_var = "green"
        self.pen_size_var = 1
        self.lines = []

        self.pen_plans = []
        self.pen_color_plans = []
        self.pen_size_plans = []

        self.fill = False
        self.fill_color_var = self.pen_color_var
        self.fill_color_plans = []
        self.fill_plans = []
        self.polygons = []

        if image != '':
            self.base_photo = Image.open("./codesters/sprites/"+image+".gif")
            self.photo = Image.open("./codesters/sprites/"+image+".gif")
            im2 = self.photo.convert('RGBA')
            rot = im2.rotate(self.heading, expand=1)
            fff =  Image.new("RGBA", rot.size, (0,)*4)
            self.photo = Image.composite(rot,fff,rot)

        self.base_photo_width = self.photo.size[0]
        self.base_photo_height = self.photo.size[1]
        self.height = self.base_photo_height
        self.width = self.base_photo_width
        self.image_name = image
        self.name = image

    def draw(self):
        if self.photo != None and self.hidden == False:
            # im2 = self.photo.convert('RGBA')
            # self.photo.close()
            # rot = im2.rotate(self.heading, expand=1)
            # fff =  Image.new("RGBA", rot.size, (0,)*4)
            # self.photo = Image.composite(rot,fff,rot)
            # rot.close()
            # fff.close()
            # im2.close()
            #  im2 = self.photo.convert('RGBA')
            # self.photo.close()
            # rot = im2.rotate(self.heading, expand=1)
            # fff =  Image.new("RGBA", rot.size, (0,)*4)
            # self.photo = Image.composite(rot,fff,rot)
            # rot.close()
            # fff.close()
            # im2.close()
            self.bg_photoimg = ImageTk.PhotoImage(self.photo)
            self.canvas.create_image((self.xcor + self.canvas.winfo_reqwidth()/2, self.canvas.winfo_reqheight()/2 - self.ycor), image = self.bg_photoimg)
            if self.say_time != 0:
                self.canvas.create_text(self.xcor + self.canvas.winfo_reqwidth()/2,self.canvas.winfo_reqheight()/2 - self.ycor - 100,text=self.say_text, font=(self.say_font,self.say_size),fill=self.say_color)
                self.say_time = self.say_time-1
        elif self.hidden == False:
            self.canvas.create_oval((self.xcor-(self.size/2),self.ycor-(self.size/2),self.xcor+(self.size/2),self.ycor+(self.size/2)), fill=self.color)
        for p in self.polygons:
            self.canvas.create_polygon(tuple(p[0]), fill = p[1])
        for l in self.lines:
            self.canvas.create_line(l[0], fill = l[1], width = l[2])

    def update_physics(self):
        prevx = self.xcor
        prevy = self.ycor
        self.xcor += self.xspeed
        self.ycor -= self.yspeed
        if self.gravity_true:
            self.yspeed += self.gravity

        if  self.pen:
            newline = []
            newline.append((self.canvas.winfo_reqwidth()/2 + prevx,self.canvas.winfo_reqheight()/2 - prevy,self.canvas.winfo_reqwidth()/2 + self.xcor,self.canvas.winfo_reqheight()/2 - self.ycor))
            newline.append(self.pen_color_var)
            newline.append(self.pen_size_var)
            self.lines.append(newline)
        if self.fill and self.pen:
           self.polygons[-1][0].append(self.canvas.winfo_reqwidth()/2 + self.xcor)
           self.polygons[-1][0].append(self.canvas.winfo_reqheight()/2 - self.ycor)

        if self.drag:
            def drag(event):
                ex = event.x - self.canvas.winfo_reqwidth()/2
                ey = self.canvas.winfo_reqheight()/2 - event.y
                if ex < self.xcor + self.width/2 and ex > self.xcor - self.width and ey < self.ycor + self.height/2 and ey > self.ycor - self.height/2:
                    self.set_x(ex)
                    self.set_y(ey)
                    self.set_x_speed(0)
                    self.set_y_speed(0)
            self.canvas.bind("<B1-Motion>", drag)

        if Manager.stage.wall_bottom_on:
            if self.ycor - (self.size*self.height/2) <= -self.canvas.winfo_reqheight()/2:
                self.ycor = -self.canvas.winfo_reqheight()/2 + (self.size*self.height/2)
                self.jump(abs(self.yspeed * Manager.stage.bounce))

        if Manager.stage.wall_top_on:
            if self.ycor + (self.size*self.height/2) >= self.canvas.winfo_reqheight()/2:
                self.ycor = self.canvas.winfo_reqheight()/2 - (self.size*self.height/2)
                self.jump(-abs(self.yspeed * Manager.stage.bounce))

        if Manager.stage.wall_left_on:
            if self.xcor - (self.size*self.width/2)<= -self.canvas.winfo_reqwidth()/2:
                self.xcor = -self.canvas.winfo_reqwidth()/2 + (self.size*self.width/2)
                self.xspeed = abs(self.xspeed * Manager.stage.bounce)

        if Manager.stage.wall_right_on:
            if self.xcor + self.size*self.width/2 >= self.canvas.winfo_reqwidth()/2:
                self.xcor  = self.canvas.winfo_reqwidth()/2 - (self.size*self.width/2)
                self.xspeed = -abs(self.xspeed * Manager.stage.bounce)


    def update_image(self):
        im2 = self.base_photo.convert('RGBA')
        if self.x_flipped:
            im2=im2.transpose(Image.FLIP_LEFT_RIGHT)
        if self.y_flipped:
            im2=im2.transpose(Image.FLIP_TOP_BOTTOM)
        #self.base_photo.close()
        if self.opacity < 255:
            print self.opacity
            im2.putalpha(self.opacity)
        scale = im2.resize((int(self.size * self.width), int(self.size*self.height)), Image.ANTIALIAS)
        rot = scale.rotate(self.heading, expand=1)
        fff = Image.new("RGBA", rot.size, (0,)*4)
        self.photo = Image.composite(rot,fff,rot)
        #self.photo.save("check.gif")

    def update_animation(self):
        #print self.future_x, "yao"
        if len(self.modes) > 0 and not self.paused:
            #print self.modes
            if self.modes[0] == "wait":
                if len(self.wait_list)> 0:
                    if self.wait_list[0] == 0:
                        print self.wait_list.pop(0)
                        print self.wait_list.pop(0)
                        print self.modes.pop(0)
                    else:
                        self.wait_list[0] = self.wait_list[0] - 1

            else:
                if self.modes[0] == "translate":
                    if len(self.animation_y_coords)>0 and len(self.animation_x_coords)>0:
                        if isinstance(self.animation_x_coords[0],basestring) and isinstance(self.animation_y_coords[0],basestring):
                            print self.animation_x_coords.pop(0)
                            print self.animation_y_coords.pop(0)
                            print self.modes.pop(0)
                        else:
                            prevx = self.xcor
                            prevy = self.ycor
                            self.xcor = (self.animation_x_coords.pop(0))
                            self.ycor = (self.animation_y_coords.pop(0))
                            if  self.pen:
                                newline = []
                                newline.append((self.canvas.winfo_reqwidth()/2 + prevx,self.canvas.winfo_reqheight()/2 - prevy,self.canvas.winfo_reqwidth()/2 + self.xcor,self.canvas.winfo_reqheight()/2 - self.ycor))
                                newline.append(self.pen_color_var)
                                newline.append(self.pen_size_var)
                                self.lines.append(newline)
                            if self.fill and self.pen:
                                self.polygons[-1][0].append(self.canvas.winfo_reqwidth()/2 + self.xcor)
                                self.polygons[-1][0].append(self.canvas.winfo_reqheight()/2 - self.ycor)
                            if len(self.animation_x_coords)>1:
                                self.future_x = self.animation_x_coords[-2]
                            if len(self.animation_y_coords)>1:
                                self.future_y = self.animation_y_coords[-2]
                elif self.modes[0] == "rotate":
                    if len(self.animation_rotation_degrees)>0 :
                        if isinstance(self.animation_rotation_degrees[0],basestring):
                            print self.animation_rotation_degrees.pop(0)
                            print self.modes.pop(0)
                        else:
                            self.heading = self.animation_rotation_degrees.pop(0)
                            self.update_image()
                elif self.modes[0] == "xflip":
                    if len(self.x_flip_plans) > 0:
                        state = self.x_flip_plans.pop(0)
                        self.x_flipped = not self.x_flipped
                        print self.x_flipped
                        self.update_image()
                        self.modes.pop(0)
                elif self.modes[0] == "yflip":
                    if len(self.y_flip_plans) > 0:
                        state = self.y_flip_plans.pop(0)
                        self.y_flipped = state
                        self.update_image()
                        self.modes.pop(0)
                elif self.modes[0] == "scale":
                    if len(self.scale_plans) > 0:
                        if isinstance(self.scale_plans[0],basestring):
                            print self.modes.pop(0)
                            self.scale_plans.pop(0)
                        else:
                            self.size = self.scale_plans.pop(0)
                            self.update_image()
                elif self.modes[0] == "pen":
                    if len(self.pen_plans) > 0:
                        self.pen = self.pen_plans.pop(0)
                        self.modes.pop(0)
                elif self.modes[0] == "pen_color":
                    if len(self.pen_color_plans) > 0:
                        self.pen_color_var = self.pen_color_plans.pop(0)
                        self.modes.pop(0)
                elif self.modes[0] == "pen_size":
                    if len(self.pen_size_plans) > 0:
                        self.pen_size_var = self.pen_size_plans.pop(0)
                        self.modes.pop(0)
                elif self.modes[0] == "pen_clear":
                    self.lines = []
                    self.polygons = []
                    self.modes.pop(0)
                elif self.modes[0] == "fill":
                    if len(self.fill_plans) > 0:
                        state = self.fill_plans.pop(0)
                        self.modes.pop(0)
                        if state and not self.fill:
                            color = self.fill_color_var
                            #if len(self.fill_color_plans) > 0:
                             #   print 'yes', color
                              #  color = self.fill_color_plans[-1]
                            print color
                            self.polygons.append([[self.canvas.winfo_reqwidth()/2 + self.xcor, self.canvas.winfo_reqheight()/2 - self.ycor], color])
                        self.fill = state
                elif self.modes[0] == "fill_color":
                    if len(self.fill_color_plans) > 0:
                        self.fill_color_var = self.fill_color_plans.pop(0)
                        self.modes.pop(0)




    ## END OF PIVOTAL FUNCTIONS ##

    def hide(self):
        self.hidden=True

    def show(self):
        self.hidden=False

    # Basic motion
    def move_right(self, amount):
        self.glide_to(self.future_x+amount, self.future_y)

    def move_left(self, amount):
        self.glide_to(self.future_x-amount,self.future_y)

    def move_down(self, amount):
        self.glide_to(self.future_x,self.future_y-amount)

    def move_up(self, amount):
        self.glide_to(self.future_x,self.future_y+amount)
#    def move_forward(self, amount):
#        desired_x = amount * math.cos(self.future_heading * (math.pi/180)) + self.future_x
#        desired_y = amount * math.sin(self.future_heading * (math.pi/180)) + self.future_y
#        self.glide_to(desired_x,desired_y)

    def forward(self, amount):
        self.move_forward(amount)

    def move_backward(self, amount):
        self.move_forward(-amount)

    def backward(self, amount):
        self.move_forward(-amount)

    def move_back(self, amount):
        desired_x = (-1*(amount * math.cos(self.heading * (math.pi/180)))) +self.future_x
        desired_y = (-1*(amount * math.sin(self.heading * (math.pi/180)))) + self.future_y

    def move_forward(self,amount):
        if len(self.x_flip_plans) >= 1 and not self.x_flip_plans[-1]:
            desired_x = amount * math.cos(self.future_heading * (math.pi/180)) + self.future_x
            desired_y = amount * math.sin(self.future_heading * (math.pi/180)) + self.future_y
        elif not self.x_flipped and len(self.x_flip_plans) < 1:
            desired_x = amount * math.cos(self.future_heading * (math.pi/180)) + self.future_x
            desired_y = amount * math.sin(self.future_heading * (math.pi/180)) + self.future_y
        else:
            desired_x = -amount * math.cos(self.future_heading * (math.pi/180)) + self.future_x
            desired_y = -amount * math.sin(self.future_heading * (math.pi/180)) + self.future_y
        self.glide_to(desired_x,desired_y)
    def forward(self,amount):
        self.move_forward(amount)
    def move_backward(self,amount):
        self.move_forward(-1 * amount)
    def backward(self,amount):
        self.move_backward(amount)
    def move_back(self,amount):
        self.move_backward(amount)
    def back(self,amount):
        self.move_backward(amount)
    def movex(self, amount):
        self.glide_to(self.future_x+amount, self.future_y)

    def move_x(self, amount):
        self.glide_to(self.future_x+amount, self.future_y)

    def movey(self, amount):
        self.glide_to(self.future_x,self.future_y+amount)

    def move_y(self, amount):
        self.glide_to(self.future_x,self.future_y+amount)

    def translate_y(self, amount):
        self.glide_to(self.future_x,self.future_y+amount)

    def translate_x(self, amount):
        self.glide_to(self.future_x+amount, self.future_y)

    # More complex motion
    def go_to(self, newx, newy):
        self.animation_x_coords.append(newx)
        self.animation_x_coords.append("Finished current animation")
        self.animation_y_coords.append(newy)
        self.animation_y_coords.append("Finished current animation")
        self.modes.append("translate")
        self.future_x = newx
        self.future_y = newy

    def goto(self, newx, newy):
        self.go_to(newx,newy)

    def glide_to(self, newx, newy):
        print self.future_x, " ", self.future_y
        xdist = float(newx - self.future_x)
        ydist = float(newy - self.future_y)
        dist = math.sqrt(xdist**2 + ydist**2)
        frames_needed = ((dist/self.speed) / 22)
        if frames_needed == 0:
            frames_needed = 1
        x_step_size = xdist/frames_needed
        y_step_size = ydist/frames_needed
        tempx = self.future_x
        tempy = self.future_y
        self.future_x = newx
        self.future_y = newy
        for n in range(int(frames_needed)):
            self.animation_x_coords.append(tempx+(x_step_size+(x_step_size * n)))
            self.animation_y_coords.append(tempy+(y_step_size+(y_step_size * n)))
            #print self.animation_x_coords, self.animation_y_coords
        print self.future_x, " ", self.future_y
        self.future_x = self.animation_x_coords[-1]
        self.future_y = self.animation_y_coords[-1]
        self.animation_x_coords.append("Finished current animation")
        self.animation_y_coords.append("Finished current animation")
        self.modes.append("translate")
        print '###########'


        # tempheading = self.heading
        # self.heading = math.atan(ydist/xdist)
        # #Trig stuff
        # while dist > self.speed:
        #     if xdist > 0:
        #         self.set_x(self.xcor + self.speed*math.cos(self.heading))
        #     else:
        #         self.set_x(self.xcor - self.speed*math.cos(self.heading))
        #     if ydist > 0:
        #         self.set_y(self.future_y + self.speed*math.sin(self.heading))
        #     else:
        #         self.set_y(self.ycor - self.speed*math.sin(self.heading))
        #     xdist = newx - self.xcor
        #     ydist = newy - self.ycor
        #     dist = math.sqrt(xdist**2 + ydist**2)
        # #Just to make sure it does end up in the right spot
        # self.set_x(newx)
        # self.set_y(newy)
        # self.heading = tempheading
        # self.canvas.delete("all")

    #
    def set_direction(self, tox, toy):
        if (tox==0):
            tox=.000001
        destination = math.atan(float(toy - self.future_y)/float(tox - self.future_x))*(180/math.pi)
        if tox - self.future_x < 0:
            destination += 180
        frames_needed = (self.animation_duration / 22)
        if frames_needed == 0:
            frames_needed = 1
        degree_rot = destination - self.future_heading
        self.step_size = float(degree_rot)/float(frames_needed)
        for n in range(int(frames_needed)):
            self.animation_rotation_degrees.append(self.step_size+(self.step_size*n)+self.future_heading)
        self.animation_rotation_degrees[-1] = destination
        self.animation_rotation_degrees.append("Finished current animation")
        self.modes.append("rotate")
        self.future_heading = destination

    def point_towards(self, tox, toy):
        self.set_direction(tox, toy)

    def turn_clockwise(self, degrees):
        destination = self.future_heading - degrees
        frames_needed = (self.animation_duration / 22)
        degree_rot = destination - self.future_heading
        self.step_size = float(degree_rot)/float(frames_needed)
        for n in range(int(frames_needed)):
            self.animation_rotation_degrees.append(self.step_size+(self.step_size*n)+self.future_heading)
        self.animation_rotation_degrees[-1] = destination
        self.animation_rotation_degrees.append("Finished current animation")
        #print self.animation_rotation_degrees
        self.modes.append("rotate")
        self.future_heading = destination

    def turn_right(self, degrees):
        self.turn_clockwise(degrees)

    def right(self, degrees):
        self.turn_clockwise(degrees)

    def turn_counterclockwise(self,degrees):
        destination = self.future_heading + degrees
        frames_needed = (self.animation_duration / 22)
        degree_rot = destination - self.future_heading
        self.step_size = float(degree_rot)/float(frames_needed)
        for n in range(int(frames_needed)):
            self.animation_rotation_degrees.append(self.step_size+(self.step_size*n)+self.future_heading)
        self.animation_rotation_degrees[-1] = destination
        self.animation_rotation_degrees.append("Finished current animation")
        self.modes.append("rotate")
        self.future_heading = destination

    def turn_left(self,degrees):
        self.turn_counterclockwise(degrees)

    def left(self,degrees):
        self.turn_counterclockwise(degrees)

    #
    def wait(self, seconds):
        self.modes.append("wait")
        self.wait_list.append(seconds*10)
        self.wait_list.append("Finished current animation")
        print self.wait_list
        self.total_wait_time += seconds
        self.future_most_recent_wait_time = seconds

    def get_wait_time(self):
        return self.future_most_recent_wait_time

    def get_total_wait_time(self):
        return self.total_wait_time

    def say(self, text,seconds=-1,color="#000000", size=12, font="Purisa"):
        self.say_text = text
        self.say_time = seconds
        self.say_color = color
        self.say_size = size
        self.say_font = font

    def ask(self, text):
        return raw_input(text)

    def reset_animation(self):
        self.animation_rotation_degrees = []
        self.animation_x_coords = []
        self.animation_y_coords = []
        self.modes = []

    def pause(self):
        self.paused = True

    def stop(self):
        self.reset_animation()

    def reset(self):
        self.reset_animation()

    def play(self):
        self.paused = False

    #Physics

    def jump(self, newspeed):
        self.yspeed = -newspeed

    def gravity_on(self):
        self.gravity_true = True

    def gravity_off(self):
        self.gravity_true = False

    def physics_on(self):
        self.physics_true = True
        self.gravity_on()

    def physics_off(self):
        self.physics_true = False
        self.gravity_off()

    def set_gravity_on(self):
        self.gravity_on()

    def set_gravity_off(self):
        self.gravity_off()

    def set_physics_on(self):
        self.physics_on()

    def set_physics_off(self):
        self.physics_off()

    def is_goal(self):
        self.goal = True

    def collision_goal_on(self):
        self.goal = True

    def collision_goal_off(self):
        self.goal = False

    def is_hazard(self):
        self.hazard = True

    def collision_hazard_on(self):
        self.hazard = True

    def collision_hazard_off(self):
        self.hazard = False

    def cannot_collide(self):
        self.collision = False

    def collision_on(self):
        self.collision = True

    def collision_off(self):
        self.collision = False

    def set_drag_on(self):
        self.drag = True

    def set_drag_off(self):
        self.drag = False

    # the speed in the following functions refers to animations, NOT physics

    def set_speed(self, newspeed):
        self.speed = newspeed
        self.animation_duration = 1000/newspeed
    def speed(self, newspeed):
        self.set_speed(newspeed)
    def get_speed(self):
        return self.speed

    # Setters
    def set_width(self, newsize):
        # self.width = int(self.base_photo.size[0] * newsize)
        # self.update_image()
        self.width = newsize
        self.update_image()
    def set_height(self, newsize):
        # self.height = int(self.base_photo.size[1] * newsize)
        # self.update_image()
        self.height = newsize
        self.update_image()
    # Old setters
    def set_velx(self, amount):
        self.set_x_speed(amount)
    def set_vely(self, amount):
        self.set_y_speed(amount)
    def set_x_speed(self, newspeed):
        self.xspeed = newspeed
    def set_y_speed(self, newspeed):
        self.yspeed = newspeed
    def set_y(self, newy):
        self.animation_y_coords.append(newy)
        self.animation_y_coords.append("Finished current animation")
        self.animation_x_coords.append(self.future_x)
        self.animation_x_coords.append("Finished current animation")
        self.modes.append("translate")
        self.future_y = newy
    def set_x(self, newx):
        self.animation_x_coords.append(newx)
        self.animation_x_coords.append("Finished current animation")
        self.animation_y_coords.append(self.future_y)
        self.animation_y_coords.append("Finished current animation")
        self.modes.append("translate")
        self.future_x = newx
    def set_position(self, to_x, to_y):
        self.set_x(to_x)
        self.set_y(to_y)
    def set_rotation(self, rot):
        self.animation_rotation_degrees.append(rot)
        self.modes.append("rotate")
        self.animation_rotation_degrees.append("Finished current animation")
    def set_heading(self, rot):
        self.set_rotation(rot)
    def set_opacity(self, opacity):
        self.opacity = int(opacity * 255)
        self.update_image()
    def set_left(self, amount):
        self.set_x(self.width/2+amount)
    def set_right(self, amount):
        self.set_x(-self.width/2+amount)
    def set_top(self, amount):
        self.set_y(-self.height/2+amount)
    def set_bottom(self, amount):
        self.set_y(self.height/2+amount)

    # Old getters

    def velx(self):
        return self.xspeed
    def vely(self):
        return self.yspeed
    def y(self):
        return self.ycor
    def x(self):
        return self.xcor
    def rotation(self):
        return self.heading
    def direction(self):
        return self.heading

    # Getters

    def get_x_speed(self):
        return self.xspeed
    def get_y_speed(self):
        return self.yspeed
    def get_composite_speed(self):
        return math.sqrt(self.xspeed**2 + self.yspeed**2)
    def get_y(self):
        return self.future_y
    def get_x(self):
        return self.future_x
    def get_rotation(self):
        return self.future_heading
    def get_direction(self):
        return self.future_heading
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_left(self):
        return self.future_x-self.width/2
    def get_right(self):
        return self.future_x+self.width/2
    def get_top(self):
        return self.future_y+self.height/2
    def get_bottom(self):
        return self.future_y-self.height/2
    def get_sides(self):
        return 0
    def get_x_scale(self):
        pass
    def get_size(self):
        return self.size
    def get_scale(self):
        return self.size
    def get_y_scale(self):
        pass
    def get_type(self):
        print self.type
    def get_text(self):
        pass
    def get_name(self):
        print self.name
    def get_image_name(self):
        print self.image_name


    def set_size(self, newsize):
        self.scale_plans.append(newsize)
        self.modes.append("scale")
        self.scale_plans.append("Finished current animatoin")

    # flippers
    def flip_horizontal(self):
        if len(self.x_flip_plans) == 0:
            self.x_flip_plans.append(not self.x_flipped)
        else:
            print len(self.x_flip_plans), self.x_flip_plans, "helpppp"
            self.x_flip_plans.append(not self.x_flip_plans[-1])
        self.modes.append("xflip")
    def flip_right_left(self):
        self.flip_horizontal()
    def flip_left_right(self):
        self.flip_horizontal()
    def flip_vertical(self):
        if len(self.y_flip_plans) == 0:
            self.y_flip_plans.append(not self.y_flipped)
        else:
            self.y_flip_plans.append(not self.y_flip_plans[-1])
        self.modes.append("yflip")
    def flip_up_down(self):
        self.flip_vertical()
    def flip_down_up(self):
        self.flip_vertical()
    def face_forward(self):
        self.x_flip_plans.append(False)
        self.modes.append("xflip")
    def face_backward(self):
        self.x_flip_plans.append(True)
        self.modes.append("xflip")
    def face_upside_down(self):
        self.y_flip_plans.append(True)
        self.modes.append("yflip")
    def face_rightside_up(self):
        self.y_flip_plans.append(False)
        self.modes.append("yflip")

    def set_color(self, newcolor):
        self.color = newcolor
        self.pen_color(newcolor)

    def pen_color(self, newcolor):
        self.pen_color_plans.append(newcolor)
        self.modes.append("pen_color")
        self.fill_toggle()
        self.fill_toggle()

    def fill_color(self, newcolor):
        self.fill_color_plans.append(newcolor)
        self.modes.append("fill_color")
        self.fill_toggle()
        self.fill_toggle()

    def pen_down(self):
        self.pen_plans.append(True)
        self.modes.append("pen")
    def pen_up(self):
        self.pen_plans.append(False)
        self.modes.append("pen")
    def pen_toggle(self):
        if len(self.pen_plans)>=1:
            self.pen_plans.append(not self.pen_plans[-1])
        else:
            self.pen_plans.append(not self.pen)
        self.modes.append("pen")

    def pen_size(self, newsize):
        self.pen_size_plans.append(newsize)
        self.modes.append("pen_size")

    def pen_clear(self):
        self.modes.append("pen_clear")

    def fill_on(self):
        self.fill_plans.append(True)
        self.modes.append("fill")
    def fill_off(self):
        self.fill_plans.append(False)
        self.modes.append("fill")
    def fill_toggle(self):
        if len(self.fill_plans)>=1:
            self.fill_plans.append(not self.fill_plans[-1])
        else:
            self.fill_plans.append(not self.fill)
        self.modes.append("fill")


    #Basic motion
    #Step functions to build other functions
    # def step_forward(self):
    #     self.set_x(self.xcor + self.speed*math.cos(self.heading))
    #     self.set_y(self.ycor + self.speed*math.sin(self.heading))
    # def step_backward(self):
    #     self.set_x(self.xcor - self.speed*math.cos(self.heading))
    #     self.set_y(self.ycor - self.speed*math.sin(self.heading))
    # def move_forward(self, amount):
    #     dist = amount
    #     while dist > 0:
    #         self.step_forward()
    #         dist -= self.speed
    #         time.sleep(0.01)
    # def move_backward(self, amount):
    #     dist = amount
    #     while dist > 0:
    #         self.step_backward()
    #         dist -= self.speed
    #         time.sleep(0.01)


class Sprite(SpriteClass):

    def __init__(self, image):
        super(Sprite, self).__init__(image)