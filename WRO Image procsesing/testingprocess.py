from vision_system import Vision


parking_exists=False # will store if we have parking on the map
parking_location=[0,0,0] # will be defined as section number relative to start,[x pos, y pos]
pillars=[] # will store the global positions of the pillars with respect to the robot as[x,y,color,section#]
distance_sensors=[] # will store the distances of the 5 distance sensors as [FR1,FR2,FL2,FL1,R]
color_sensor=""     # will store the colors as gsition with respect to the starting reference as[x,y,theta]
current_position=[0,0,0] # will store the robotrey, yellow, orange, blue
global_position=[0,0,0] 

lap_nb = 1
section_nb = 1

# Temporary dummy function for testing
def pillars_local_robot_FPV_to_local(pos):
    # Replace this later with the actual transformation logic
    return pos

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
    
vision = Vision(debug=True)

if __name__ == "__main__":
    vision = Vision(debug=True)
    while True:
        process_data(vision)
        print(...)
        key = input("Press Enter to continue or 'q' to quit: ")
        if key == 'q':
            break
