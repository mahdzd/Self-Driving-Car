
#calculate the optimal path using local reference(xk,yk,thetak)

#take a step to drive the motor

#Localize the robot interms of the old reference(xk,yk,thetak)
#localize the pillars with respect to the robot

#if there is a huge error,"" how much huge is huge??"" 
    #calculate a new path
    # else
    #continue on the old path
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
        calculate_trajectory_if_no pillars()

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