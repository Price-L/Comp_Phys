class particle(object):
    
    def __init__(self, mass=1., y=0., v=0.):
        self.mass = mass
        self.y = y
        self.v = v

    def euler(self, f, dt):
        self.y = self.y + self.v*dt
        self.v = self.v + f/self.mass*dt

    def euler_cromer(self, f, dt):
        self.v = self.v + f/self.mass*dt
        self.y = self.y + self.v*dt

import numpy as np
from matplotlib import pyplot

g = 9.8            # g acceleration
mass =  0.01        # mass of the particle
y0 = 10000.          # initial position
y0max = 1000000.
y0min = 10000.
v0 = 0.            # initial velocity
vt = 30.           # terminal velocity
gforce = g*mass
k2 = 0 #gforce/vt**2  # drag coeff.
R = 6370000.       # Radius of the Earth

dy = 10000        
dt = 0.1           # time step

p = particle(mass, y0, v0)

p_d = particle(mass, y0, v0)

y = [y0] # since we do not know the size of the arrays, we define first a python list
v = [v0] # the append method is more efficient for lists than arrays
t = [0.]

y_d = [y0]
v_d = [v0]
t_d = [0.]

def dist_calc(y0, p_d, p):
        
    y_d = [y0]
    v_d = [v0]
    t_d = [0.]

    while p_d.y > 0.:
        dist = 1.+(y_d[-1]/R)
        gforce_d = g*mass/(dist**2)
        # k2_d = gforce_d/vt**2
        fy_d = -gforce_d
        p_d.euler(fy_d, dt)
        y_d.append(p_d.y)
        v_d.append(p_d.v)
        t_d.append(t_d[-1]+dt)
        
    y = [y0]
    v = [v0]
    t = [0.]

    while p.y > 0.:
        fy = -gforce
        p.euler(fy, dt)
        y.append(p.y)
        v.append(p.v)
        t.append(t[-1]+dt)
    
    diff = abs((v_d[-1]-v[-1])/v[-1])

    return (y,v,t,y_d,v_d,t_d,diff)

y,v,t,y_d,v_d,t_d,differ = dist_calc(y0, p_d, p)

while True:    
    
    if (abs(differ - 0.01) < 0.0001) and (differ > 0.01):
        break

    if (differ < 0.01):
        y0min = y0
        y0 = (y0+y0max)/2.
        p_d = particle(mass, y0, v0)
        p = particle(mass, y0, v0)
        y,v,t,y_d,v_d,t_d,differ = dist_calc(y0, p_d, p)

    if (differ > 0.01):
        y0max = y0
        y0 = (y0min+y0)/2.
        p_d = particle(mass, y0, v0)
        p = particle(mass, y0, v0)
        y,v,t,y_d,v_d,t_d,differ = dist_calc(y0, p_d, p)


t_data = np.array(t) # we convert the list into a numpy array for plotting
y_data = np.array(y)
v_data = np.array(v)

td_data = np.array(t_d)
yd_data = np.array(y_d)
vd_data = np.array(v_d)

#for i in range(0,t_data.size):
#    print (i,t_data[i], y_data[i], v_data[i])

pyplot.figure(1)
pyplot.plot(t_data, v_data, color="#0000FF", ls='-', lw=3)
pyplot.plot(td_data, vd_data, color="#FF0000", ls='-', lw=3)
pyplot.xlabel('time(s)')
pyplot.ylabel('velocity(m/s)');

pyplot.figure(2)
pyplot.plot(t_data, y_data, color="#0000FF", ls='-', lw=3)
pyplot.plot(td_data, yd_data, color="#FF0000", ls='-', lw=3)
pyplot.ylabel('position(m)');
pyplot.show()

print("Given the initial height: ", y[0], "The impact velocities will have a ", differ*100., "difference")
