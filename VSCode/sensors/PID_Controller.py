#this class is responsible to drive the motor based on closed-loop feedback systems, mainly PID controllers
#the inputs for the units are the actual position and heading, and the trajectory
#the controller will calculated the nearest position and headig angle on the trajectory that the robot should have been at 
#then the controller will control the output to adjust the rear wheels speed accordingly


#the following function calculates the position error value
import time

class PID_Controller:
    #construct the PID using the constant parameters, and the boundaries
    def __init__(self, Kp, Ki, Kd, output_limits, windup_limit):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.integral = 0.0
        self.last_error = 0.0
        self.last_time = None

        self.output_limits = output_limits
        self.windup_limit = windup_limit

    def reset_Controller(self):
         self.integral = 0.0
         self.last_error = 0.0

    #the following function computes the nearest point on the trajectory that the car should be on, it is based on...
    def compute_Nearest_on_Trajectory(self,curr_x,curr_y,curr_theta,trajectory,par_s):

        nearest_x=0
        nearest_y=0
        nearest_theta=0
        return nearest_x,nearest_y,nearest_theta

        