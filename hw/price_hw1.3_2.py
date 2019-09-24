class particle2(object):
    
    def __init__(self, mass=1., x=0., y=0., vx=0., vy=0.):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
       
    def euler(self, fx, fy, dt):
        self.vx = self.vx + fx/self.mass*dt
        self.vy = self.vy + fy/self.mass*dt
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt

import numpy as np
from matplotlib import pyplot
from matplotlib.colors import ColorConverter as cc
import math

g = 9.8            # g acceleration
v0 = 30.           # initial velocity
k2 = 0.1       # Drag Coefficient

dt = 0.1           # time step

xmax = [0]
angled = [0]
colors = ['red','orange','yellow','green','magenta','cyan','blue','purple','black']

for angle in range(1,9):
    x = [0]                                  # we need to initialize the arrays for each value of the angle
    y = [0]
    vx = [math.cos(angle*0.1*math.pi/2.)*v0]
    vy = [math.sin(angle*0.1*math.pi/2.)*v0]
    t = [0.]

    angled.append(int(angle*0.1*90))
    
    p = particle2(1., 0., 0., vx[0], vy[0])
    while p.y >= 0.:
        v = math.sqrt(p.vx**2 + p.vy**2)
        fy = -g-k2*abs(v)*p.vy
        fx = -k2*p.vx*abs(v)
        p.euler(fx, fy, dt)
        x.append(p.x)
        y.append(p.y)
        vx.append(p.vx)
        vy.append(p.vy)
        t.append(t[-1]+dt)

    t_data = np.array(t) # we convert the list into a numpy array for plotting
    x_data = np.array(x)
    y_data = np.array(y)
    vx_data = np.array(vx)
    vy_data = np.array(vy)
    
    xmax.append(x[-1])
    
    my_plot = pyplot.plot(x_data, y_data, color=(colors[angle]), ls='-', lw=3, label = str(angle*0.1))
    pyplot.legend()

xmost = max(xmax)
index = xmax.index(max(xmax))
ang = angled[index]
print("Given the initial angle ",ang,"deg, the particle will achieve the max distance: ",xmost)

pyplot.xlabel('position x(m)')
pyplot.ylabel('position y(m)');
pyplot.show()
