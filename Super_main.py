
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
from stopPIDClass import StopPID
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

drive_control = CarController() # This object will intialize the drive controller for the motors
traj_builder = trajectory_builder() # This object will hold the trajectory builder for the robot
EKF_estimator = EKFEstimator() # This object will be responsible of estimating the current position
sensor_set = Sensors()
vision_system = Vision()



#-------------------Helping methods to be used-----------------------#

# This methop should park the car in the parking lot, it will be in the seciton where the parking is in
def park():
    


    return

# This method should make the 
def exit_parking():
    
    return

# This should calculate trajectory if there are pillars
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

# This should create a trajectory when no pillar onsight
def calculate_trajectory_no_pillar():
    trajectory=#trajectory builder should return a parametric equation x(t) and y(t) starting at t=0
    
    return

# This is to be used by the trajectory builder to calculate the best final direction for bezier curve based on the last known pillar      
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

# This method should proscess every sensor data and record it
def process_data(): #TODO
    global parking_exists, parking_location, pillars, lap_nb, section_nb

    # Run vision detection for current frame
    detected_objects = vision.detect_obstacles(frame)

    # Sync lap and section numbers
    lap_nb = vision.lap_number
    section_nb = vision.side_number

    # Reset pillars list
    pillars = []

    for obj in detected_objects:
        if obj.color in ["red", "green"] and hasattr(obj, "x_robot") and hasattr(obj, "y_robot"):
            pillars.append([obj.x_robot, obj.y_robot, obj.color, section_nb])

        elif obj.color == "magenta" and vision.lap_number == 1 and section_nb == 1:
            parking_exists = True
            parking_location = [section_nb, obj.x_px, obj.y_px]

    # If no magenta was found in this call and lap/side matches, don't erase memory
    if vision.lap_number == 1 and section_nb == 1 and not any(o.color == "magenta" for o in detected_objects):
        parking_exists = False
        parking_location = [0, 0, 0]
    return
    
# This method increases the sections and request end if in the last round
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

# This method should stop the robot in the current section
def stop_in_this_section():
    stoppping=StopPID()
    t1=time.time()
    for _ in range(20):
        cmd=stoppping.compute(RWL_encoder,RWR_encoder,time.time()-t1)
        didi="f" if cmd>0 else "b"
        drive_control.setAll(didi,cmd,0)
        t1=time.time()
        if 0.5*(RWL_encoder+RWR_encoder)<0.1:
            break
    return

# This method should check if the start button has been pressed
def check_start():  #TODO
    
    return

# This method will update the local reference to the current position 
def update_reference():
    global global_position,local_reference_pos,current_position
    local_reference_pos=global_position
    current_position=[0,0,0]
    pillars=pillars_local_to_local_robot_FPV
    
# This method should drive the robot 1 step ccording to the saved trajectory
def take_step():
    global trajectory
    global drive_control
    global local_reference_pos
    robot_pos=local_reference_pos

    ix = find_nearest_point_bounded(radius=10)
    if ix is None or ix >= len(trajectory[0]) - 1:
        return  # No valid point or no next point

    pt_now = trajectory[0][ix]
    pt_next = trajectory[0][ix + 1]
    vec_traj = pt_next - pt_now
    vec_robot = pt_next - np.array(robot_pos[:2])

    # Check dot product to determine if robot is ahead or behind
    drive_direction = "f" if np.dot(vec_traj, vec_robot) > 0 else "b"

    steering_angle = trajectory[1][ix]
    drive_speed = trajectory[2][ix]

    drive_control.setAll(drive_direction, drive_speed/4.0, steering_angle)
    return drive_direction,drive_speed,steering_angle

# This method will convert the local position to global position
def local_to_global(local_point):
    ox, oy, theta = local_reference_pos
    R = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])
    return np.array([ox, oy]) + R @ local_point

# This method will convert the global position to local position
def global_to_local(global_point):
    ox, oy, theta = local_reference_pos
    R_inv = np.array([
        [ np.cos(theta),  np.sin(theta)],
        [-np.sin(theta),  np.cos(theta)]
    ])
    return R_inv @ (global_point - np.array([ox, oy]))

# This methpd will convert the coordinates of the pillar from the local reference to the robot FPV
def pillars_local_to_local_robot_FPV(pillars):
    """
    Returns a new list of pillars with x_cm, y_cm transformed to local coordinates.

    Args:
        pillars (list): List of TrafficSign or FieldObject with x_cm, y_cm attributes.
        ref_pose (tuple): (x0, y0, theta) reference global pose.

    Returns:
        list: New list of pillar objects with updated x_cm, y_cm
    """
    ref_pose=local_reference_pos
    x0, y0, theta = ref_pose
    R = np.array([[np.cos(-theta), -np.sin(-theta)],
                  [np.sin(-theta),  np.cos(-theta)]])

    new_pillars = []
    for p in pillars:
        dx, dy = p.x_cm - x0, p.y_cm - y0
        x_local, y_local = R @ np.array([dx, dy])
        new_p = TrafficSign(p.color, p.x_px, p.y_px, p.bbox, p.bbox_width_px)
        new_p.x_cm = x_local
        new_p.y_cm = y_local
        new_pillars.append(new_p)

    return new_pillars

# This methpd will convert the coordinates of the pillar from the robot FPV to the local reference 
def pillars_local_robot_FPV_to_local(pillars):
    """
    Returns a new list of pillars with x_cm, y_cm transformed to global coordinates.

    Args:
        pillars (list): List of TrafficSign or FieldObject with x_cm, y_cm attributes.

    Returns:
        list: New list of pillar objects with updated x_cm, y_cm
    """
    ref_pose=local_reference_pos
    x0, y0, theta = ref_pose
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])

    new_pillars = []
    for p in pillars:
        x_global, y_global = R @ np.array([p.x_cm, p.y_cm]) + np.array([x0, y0])
        new_p = TrafficSign(p.color, p.x_px, p.y_px, p.bbox, p.bbox_width_px)
        new_p.x_cm = x_global
        new_p.y_cm = y_global
        new_pillars.append(new_p)

    return new_pillars

# This method finds the nearest point on the trajectory to be used by the step taking method
def find_nearest_point_bounded(radius):
    """
    Efficient nearest point search using a circular bound.

    Args:
        trajectory (np.ndarray): Nx2 array of (x, y) points.
        robot_pos (tuple): (x, y) of the robot.
        radius (float): Search radius in same unit as trajectory.

    Returns:
        int or None, np.ndarray or None: index and coordinates of closest point, or None if none found.
    """
    global trajectory,local_reference_pos
    traj_points=trajectory[0]
    robot_pos = np.array(local_reference_pos)
    diffs = traj_points - robot_pos
    dists_sq = np.einsum('ij,ij->i', diffs, diffs)  # squared distances
    mask = dists_sq <= radius**2

    if not np.any(mask):
        return None, None

    filtered_indices = np.where(mask)[0]
    filtered_dists = dists_sq[mask]
    min_idx_in_filtered = np.argmin(filtered_dists)
    idx = filtered_indices[min_idx_in_filtered]

    return idx, traj_points[idx]

# This method calculates the neerest distance from the robot to the curve
def compute_tracking_error():
    """
    Computes tracking error between robot and nearest trajectory point.

    Returns:
        dict: {
            'lateral_error': float,
            'heading_error': float,
            'target_speed': float,
            'target_steer': float
        }
        or None if no valid target
    """
    global trajectory, local_reference_pos  # (x, y, theta)

    ix, target_point = find_nearest_point_bounded(radius=10)
    if ix is None or ix >= len(trajectory[0]) - 1:
        return None

    # Target pose
    pt_next = trajectory[0][ix + 1]
    traj_vec = pt_next - target_point
    traj_theta = np.arctan2(traj_vec[1], traj_vec[0])

    # Robot pose
    x, y, theta = local_reference_pos
    pos_vec = np.array([x, y])
    heading_vec = np.array([np.cos(theta), np.sin(theta)])

    # Lateral error (signed cross product)
    err_vec = target_point - pos_vec
    lateral_error = np.cross(heading_vec, err_vec)

    # Heading error
    heading_error = np.arctan2(np.sin(traj_theta - theta), np.cos(traj_theta - theta))

    return {
        'lateral_error': lateral_error,
        'heading_error': heading_error,
        'target_speed': trajectory[2][ix],
        'target_steer': trajectory[1][ix]
    }


#-------------------Code Starts Here-----------------------#

print("The code has started")     

#wait until the button is pressed
while not start_button:
    time.sleep(0.0001)
    check_start()

print("button pressed. The main loop will start now")

error_to_track_threshold=5
#the main loop
while True:     #TODO COMPATIBLE...
    
    #Process sensor and camera data
    process_data()
    
    drive_direction,drive_speed,steering_angle = take_step()# The robot should move a step according to the saved trajectory
    drive_speed=-1*drive_speed if drive_direction=="b" else drive_speed
    current_position=EKF_estimator.update(current_position,ms,drive_speed,steering_angle,RWR_encoder,RWL_encoder,steer_encoder,imu_z)

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
         error_to_track=compute_tracking_error()
         if error_to_track>error_to_track_threshold:
            if(not pillars):
              calculate_trajectory_no_pillar()

            else:
                calculate_trajectory()



   
    



    
    
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