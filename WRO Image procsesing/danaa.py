
#-------------------needed libraries and Classes:-----------------------#
import numpy as np
import time
import keyboard
from vision_system import Vision

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
RWL_encoder=0
RWR_encoder=1


#-------------------Objects:-----------------------#

vision_system = Vision()



def process_data(vision):
    global parking_exists, parking_location, pillars, lap_nb, section_nb

    # Capture and process frame inside Vision
    vision.init_camera_and_detect()

    # Use processed vision data
    lap_nb = vision.lap_number
    section_nb = vision.side_number

    pillars = []
    for obj in vision.current_side_registry:
        if obj.color in ["red", "green"] and hasattr(obj, "x_robot") and hasattr(obj, "y_robot"):
            pillars.append([obj.x_robot, obj.y_robot, obj.color, section_nb])

    if vision.parking_marker and vision.side_number == 1:
        parking_exists = True
        pos=[vision.parking_marker.x_cm, vision.parking_marker.y_cm]
        parking_location = [section_nb, pillars_local_robot_FPV_to_local(pos)[0], pillars_local_robot_FPV_to_local(pos)[1]]
        
        
print("The code has started")     

process_data(vision_system)
print(parking_exists, parking_location, pillars, lap_nb, section_nb)
