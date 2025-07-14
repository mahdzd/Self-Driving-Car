
#calculate the optimal path using local reference(xk,yk,thetak)

#take a step to drive the motor

#Localize the robot interms of the old reference(xk,yk,thetak)
#localize the pillars with respect to the robot

#if there is a huge error,"" how much huge is huge??"" 
    #calculate a new path
    # else
    #continue on the old path

#-------------------needed libraries and Classes:-----------------------#
import numpy as np
import time
import keyboard
from scipy.optimize import minimize_scalar
from Mahdi_Codes_Python.CarController import CarController
from VSCode.sensors.sensors import Sensors


#-------------------Global state variables:-----------------------#

parking_exists=False # will store if we have parking on the map
parking_location=[0,0,0] # will be defined as section number relative to start,[x pos, y pos]
pillars=[] # will store the global positions of the pillars with respect to the robot as[x,y,color,section#]
distance_sensors=[] # will store the distances of the 5 distance sensors as [FR1,FR2,FL2,FL1,R]
color_sensor=""     # will store the colors as gsition with respect to the starting reference as[x,y,theta]
current_position=[0,0,0] # will store the robotrey, yellow, orange, blue
global_position=[0,0,0] # will store the robot po position with respect to the last used reference as[x,y,theta]
local_reference_pos=[] # will store the positionof the local reference used with respect to the global reference as[ox,oy,theta]
par_s=0 # this oduble will hold  a paremeter to drive the robot through the curve
time_t=time.time(); # saves the actual time at beginning
time_when_Section_updated=time.time()# will hold the time when a section is updated
new_Section=True # will tick true whenever we enter a section and false whenever in the corners
direction=0 # 0 for CW and 1 for CCW
lap_nb=1 # will hold the lap number the robot is in 
section_nb=1 # will hold the section number the robot is in starting with the first position
in_corner=False # will tell if we are in the corner section or not
final_section=False # will turn true when the robot enters the final section
start_button=False # this will hold the state of the push button and lathes whenever on
trajectory=None  # this will hold the trajectory equations
error_to_track=0 # this will hold the distance to trajectory

#-------------------Objects:-----------------------#

Motor_control=CarController() #This object will intialize the drive controller for the motors
traj_builder= trajectory_builder....#this object will hold the trajectory builder for the robot
EKF_estimator= Kalman_estimator.... #this object will be responsible of estimating the current position
sensor_set=Sensors()
cvobj




#-------------------Helping methods to be used-----------------------#

#This methop should park the car in the parking lot, it will be in the seciton where the parking is in
def park():
    


    return

#This method should make the 
def exit_parking():
    
    return

#this should calculate trajectory if there are pillars
def calculate_trajectory():
    global pillars, trajectory,traj_builder

    # 1. Filter: keep only visible objects with y_cm > 0 (in front of robot)
    forward_pillars = [p for p in pillars if p.x_cm is not None and p.x_cm > 0]

    if len(forward_pillars) < 1:
        print("No forward pillars.")
        return

    # 2. Sort by Euclidean distance from robot
    forward_pillars.sort(key=lambda p: np.hypot(p.x_cm, p.y_cm))

    # 3. Select 3 nearest
    selected = forward_pillars[:3]

    # 4. Build trajectory
    points, steering, speed, segment_lengths = traj_builder.bezier_curve_from_pillars(
        np.array(selected), g0=np.array([0, 0]), d0=np.array([0, 1]),
        df=calculate_final_direction(selected[-1])
    )

    # 5. Store trajectory as a list of segments
    trajectory = [points, steering, speed, segment_lengths]


#this should create a trajectory when no pillar onsight
def calculate_trajectory_no_pillar():
    trajectory=#trajectory builder should return a parametric equation x(t) and y(t) starting at t=0
    
    return

# this is to be used by the trajectory builder to calculate the best final direction for bezier curve based on the last known pillar      
def calculate_final_direction(pillar):
    global direction  # 0 = CW, 1 = CCW

    section_nb = pillar.section_nb  # from the TrafficSign object

    base = {
        1: np.array([1, 0]),
        2: [np.array([0, -1]), np.array([0, 1])],
        3: [np.array([-1, 0]), np.array([1, 0])],
        4: [np.array([0, 1]), np.array([0, -1])],
    }

    if section_nb == 1:
        return base[1]
    elif section_nb in (2, 3, 4):
        return base[section_nb][direction]
    else:
        return np.array([0, 0])


#this method should proscess every sensor data and record it
def process_data(): #TODO


    return
    
#this method increases the sections and request end if in the last round
def add_Section():
    global section_nb,lap_nb,final_section
    if(section_nb==4 and lap_nb<3):
        section_nb=0
        lap_nb+=1
    elif(lap_nb<3):
        section_nb+=1
    else:
        final_section=True

    return

#This method should stop the robot in the current section
def stop_in_this_section():


    return

#this method should check if the start button has been pressed
def check_start():  #TODO
    
    return

#this method is used by the error method
def distance_squared(t):
    xt, yt = trajectory(t)
    return (xt - current_position[0])**2 + (yt - current_position[1])**2

#this method calculates the neerest distance from the robot to the curve
def compute_error_to_track():
    res = minimize_scalar(distance_squared, bounds=(par_s-0.5, par_s+0.5), method='bounded')
    return res

#this method will update the local reference to the current position 
def update_reference():
    global global_position,local_reference_pos,current_position
    local_reference_pos=global_position
    current_position=[0,0,0]
    pillars.change_pos
    
#this method should drive the robot 1 step ccording to the saved trajectory
def take_step():
    return

#this method will convert the local position to global position
def local_to_global(local_point):
    ox, oy, theta = local_reference_pos
    R = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])
    return np.array([ox, oy]) + R @ local_point

#this method will convert the global position to local position
def global_to_local(global_point):
    ox, oy, theta = local_reference_pos
    R_inv = np.array([
        [ np.cos(theta),  np.sin(theta)],
        [-np.sin(theta),  np.cos(theta)]
    ])
    return R_inv @ (global_point - np.array([ox, oy]))

print("The code has started")

#wait until the button is pressed
while not start_button:
    time.sleep(0.0001)
    check_start()

print("button pressed. The main loop will start now")

#the main loop
while True:     #TODO COMPATIBLE...
    
    #Process sensor and camera data
    parking_exists,parking_location,pillars,distance_sensors,color_sensor=process_data()


    #check if we are in the parking:
    if parking_exists and distance_sensors[1]<10 and distance_sensors[4]<10 and lap_nb==1 and section_nb==1:
        exit_parking()
        continue
    #check if it is the first time to assign trajectory
    if trajectory is None:
        if(not pillars):
            calculate_trajectory_no_pillar()
            update_reference()
        else:
            calculate_trajectory()
            update_reference()
    else: #if there is already a trajectory decide wether to create new one or stick with the old depending on the error
         error_to_track=compute_error_to_track()
         if error_to_track>3:
            if(not pillars):
              calculate_trajectory_no_pillar()

            else:
                calculate_trajectory()



    take_step()#the robot should move a step according to the trajectory

    current_position=kalman_estimation()



    
    
    #check if we entered or exited the corner and update the direction
    if True:
        if(color_sensor=="blue" and new_Section and time.time()-time_when_Section_updated > 1):
            direction=1
            new_Section=False
            in_corner=True
            time_when_Section_updated=time.time()
        elif(color_sensor=="blue" and (not new_Section ) and time.time()-time_when_Section_updated > 1 ):
            new_Section=True
            in_corner=False
            add_Section()
            time_when_Section_updated=time.time()
        elif(color_sensor=="orange" and new_Section and time.time()-time_when_Section_updated > 1):
            direction=0
            new_Section=False 
            in_corner=True
            time_when_Section_updated=time.time()       
        elif(color_sensor=="orange" and (not new_Section) and time.time()-time_when_Section_updated > 1):
            new_Section=True
            add_Section()
            in_corner=False
            time_when_Section_updated=time.time()


    #stop in the reached section if this is the fina section
    if True:
        if(final_section and parking_exists):
            park()
        elif(final_section):
            stop_in_this_section()
            break
        
    #update the time
    time_t=time.time

    #exit the loop if q is pressed on the keyboard
    if keyboard.is_pressed('q'):
        print("Quitting...")
        break




