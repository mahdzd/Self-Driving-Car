
#calculate the optimal path using local reference(xk,yk,thetak)

#take a step to drive the motor

#Localize the robot interms of the old reference(xk,yk,thetak)
#localize the pillars with respect to the robot

#if there is a huge error,"" how much huge is huge??"" 
    #calculate a new path
    # else
    #continue on the old path


import numpy as np
import time
import keyboard

#Global state variables:
parking_exists=False #will store if we have parking on the map
parking_location=[0,0,0] #will be defined as[section number relative to start, x pos, y pos]
pillars=[] #will store the global positions of the pillars with respect to the robot as[x,y,color]
distance_sensors=[] #will store the distances of the 5 distance sensors as [FR1,FR2,FL2,FL1,R]
color_sensor=""     #will store the colors as grey,yeloow, orange, blue
global_position=[0,0,0] #will store the robot position with respect to the starting reference as[x,y,theta]
current_position=[0,0,0] #will store the robot position with respect to the last used reference as[x,y,theta]
par_s=0 #this oduble will hold  a paremeter to drive the robot through the curve
time_t=time.time(); #saves the actual time at beginning
time_when_Section_updated=time.time()#will hold the time when a section is updated
new_Section=True #will tick true whenever we enter a section and false whenever in the corners
direction=0 #0 for CW and 1 for CCW
lap_nb=1 #will hold the lap number the robot is in 
section_nb=1 #will hold the section number the robot is in starting with the first position
in_corner=False #will tell if we are in the corner section or not
final_section=False #will turn true when the robot enters the final section
print("Press 'q' to quit.")


#Helping methods to be used:
def park():
    


    return

def exit_parking():
    
    return

def calculate_trajectory():
    #first sort the pillars according to the nearst to the robot
    distances = np.linalg.norm(pillars[:, :2], axis=1)
    sorted_indices = np.argsort(distances)
    sorted_pillars = pillars[sorted_indices]
    
    #call the trajectory builder
    tra_x,tra_y=bezier_curve_trajectoy_calculator(sorted_pillars[:2],0,0,0)#trajectory builder should return a parametric equation x(t) and y(t) starting at t=0
    
    return tra_x,tra_y

def process_data():


    return

def add_Section():
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

while True:
    parking_exists,parking_location,pillars,distance_sensors,color_sensor=process_data()
    #check if we are in the parking:
    if parking_exists and distance_sensors[1]<10 and distance_sensors[4]<10:
        exit_parking()
    
    #stop in the reached section
    if True:
        if(final_section and parking_exists):
            park()
        elif(final_section):
            stop_in_this_section()
            break
        
        


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







    time_t=time.time
    if keyboard.is_pressed('q'):
        print("Quitting...")
        break

repeat{
    proccces_Data()
    Decide_what_action_to_tak()
    if(action==get out of the parking)
        get_out_of_the_parking()
    else if(action== turnleft)
        turn_left
    else if(action== turnright)
        turn_right   
    else if(action== no pillar,continue straight)
        calculate_trajectory()

    else if(pillers detected)
        calculate_trajectory with pillars()
        drive_the_car_to_move_on_track()
        calculate_the_error_to_the_curve()
        if(error>threshold)
            calculate_trajectory()
            drive.....
    if(3 laps and parking_detected)
        park()
    if(3 laps and no parking)
        stop()
}



