#this class is responsible to drive the motor based on closed-loop feedback systems, mainly PID controllers
#the inputs for the units are the actual position and heading, and the trajectory
#the controller will calculated the nearest position and headig angle on the trajectory that the robot should have been at 
#then the controller will control the output to adjust the rear wheels speed accordingly


#the following function calculates the position error value
import time
import PID_Controller

class Driving_PID_Controller(PID_Controller):
    #construct the PID using the constant parameters, and the boundaries
    def __init__(self, Kp, Ki, Kd, output_limits, windup_limit):
        super().__init__(Kp, Ki, Kd, output_limits, windup_limit)

 
    def compute_Position_error(self,curr_x,curr_y,curr_theta,trajectory,par_s):

        



        pos_e=0
        return pos_e 


    def Compute(self,curr_x,curr_y,curr_theta,trajectory,par_s):     
        error= self.compute_Position_error(curr_x,curr_y,curr_theta,trajectory,par_s)
        
        current_time = time.time()
        dt = current_time - self.last_time if self.last_time else 0.01
        self.last_time = current_time

        P = self.Kp * error

        # Integral with windup guard
        self.integral += error * dt
        self.integral = max(min(self.integral, self.windup_limit), -self.windup_limit)
        I = self.Ki * self.integral

        # Derivative
        derivative = (error - self.last_error) / dt if dt > 0 else 0.0
        D = self.Kd * derivative
        self.last_error = error

        # Output
        output = P + I + D
        output = max(self.output_limits[0], min(output, self.output_limits[1]))
        return output
        