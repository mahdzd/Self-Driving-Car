import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import sys
sys.path.append(r"D:\Data Files\Projects\WRO\Self-Driving-Car\WRO Image procsesing")

from traffic_sign import TrafficSign 


class Trajectory_Builder:
    last_calculated_trajectory=None

    def __init__(self,resolution_cm=5.0):
        self.resolution_cm = resolution_cm
        return

    def draw_outline(self):
        plt.figure(1)
        plt.clf()
        plt.axis("equal")

        # Outer Grid
        plt.plot([0, 300, 300, 0, 0], [0, 0, 300, 300, 0], 'k')
        plt.plot([110, 190, 190, 110, 110], [110, 110, 190, 190, 110], 'k')

        # Draw internal grids (section 1 to 4)
        grids = [
            ([0, 100, 100, 0, 0], [100, 100, 200, 200, 100], 0, 0),
            ([0, 100, 100, 0, 0], [100, 100, 200, 200, 100], 100, 100),
            ([0, 100, 100, 0, 0], [100, 100, 200, 200, 100], 200, 0),
            ([0, 100, 100, 0, 0], [100, 100, 200, 200, 100], 100, -100)
        ]
        lines = [
            ([0, 100], [150, 150]), ([40, 40], [100, 200]), ([60, 60], [100, 200]),
            ([150, 150], [200, 300]), ([100, 200], [240, 240]), ([100, 200], [260, 260]),
            ([150, 150], [0, 100]), ([100, 200], [40, 40]), ([100, 200], [60, 60])
        ]

        for sx, sy, dx, dy in grids:
            plt.plot(np.array(sx) + dx, np.array(sy) + dy, '--', color=[0.8]*3, linewidth=0.2)

        for x, y in lines:
            plt.plot(x, y, '--', color=[0.6]*3, linewidth=0.1)

    def create_pillar(self,xc, yc, s, label=None):
        x = [xc-2.5, xc+2.5, xc+2.5, xc-2.5, xc-2.5]
        y = [yc-2.5, yc-2.5, yc+2.5, yc+2.5, yc-2.5]
        plt.figure(1)
        plt.plot(x, y, color='r' if s == "red" else 'g')
        if label is not None:
            plt.text(xc + 3, yc + 3, label, fontsize=8, color='blue')
        plt.axis("equal")

    def bezier_curve_from_pillars(self, pillars, g0, d0, df,theta):
        v = np.zeros((pillars.shape[0] + 1, 2)) #this vector holds the passing-through points
        v[0, :] = g0
        for i in range(1, v.shape[0]):
            x, y, s, sectionnb = pillars[i-1].x_cm, pillars[i-1].y_cm, pillars[i-1].color, pillars[i-1].section_nb
            if sectionnb==1:
                v[i, :] = [x - 20*np.sin(theta), y-20*np.cos(theta)] if s == "red" else [x + 20*np.sin(theta), y+20*np.cos(theta)] 
            elif sectionnb==2:
                v[i, :] = [x - 20*np.cos(theta), y+20*np.sin(theta)] if s == "red" else [x +20*np.cos(theta), y-20*np.sin(theta)]
            elif sectionnb==3:
                v[i, :] = [x + 20*np.sin(theta), y+20*np.cos(theta)] if s == "red" else [x - 20*np.sin(theta), y-20*np.cos(theta)] 
            else:
                v[i, :] = [x + 20*np.cos(theta), y-20*np.sin(theta)] if s == "red" else [x-20*np.cos(theta), y+20*np.sin(theta)]

        dv = np.zeros_like(v) #this vector holdes the direction @ passing through points
        dv[0, :] = d0
        dv[-1, :] = df
        kc = 0.0085 #this constant is used to optimize for minimum steering angle
        for i in range(1, dv.shape[0]-1):
            tdv = v[i+1] - v[i]
            dv[i, :] = tdv + kc * np.linalg.norm(tdv) * (v[i] - v[i-1])

        all_points = []
        all_steering = []
        all_speed = []
        segment_lengths = []

        for i in range(len(v) - 1):
            segment_points, steering, speed = self.sample_segment_by_arclength(v[i], v[i+1], dv[i], dv[i+1])
            all_points.append(segment_points)
            all_steering.append(steering)
            all_speed.append(speed)
            segment_lengths.append(len(segment_points))

        points = np.vstack(all_points)
        steering = np.concatenate(all_steering)
        speed = np.concatenate(all_speed)

        Trajectory_Builder.last_calculated_trajectory = {
            "x": [round(xi, 2) for xi in points[:, 0]],
            "y": [round(yi, 2) for yi in points[:, 1]],
            "steering_angle": [round(a, 2) for a in steering],
            "safe_speed": [round(s, 2) for s in speed]
    }
        
        #round the results to 2 decimal points for convenience
        points = np.round(points, 2)
        steering = np.round(steering, 2)
        speed = np.round(speed, 2)
        return points, steering, speed, segment_lengths

    def sample_segment_by_arclength(self, P0, P3, v0, v3):
        v0 = v0 / np.linalg.norm(v0)
        v3 = v3 / np.linalg.norm(v3)
        d = np.linalg.norm(P3 - P0) / 3
        P1 = P0 + d * v0
        P2 = P3 - d * v3

        def bezier(t):
            return ((1 - t)**3) * P0 + 3 * ((1 - t)**2) * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3

        t_dense = np.linspace(0, 1, 1000)
        curve = np.array([bezier(t) for t in t_dense])

        deltas = np.diff(curve, axis=0)
        dists = np.sqrt((deltas**2).sum(axis=1))
        cumulative_lengths = np.insert(np.cumsum(dists), 0, 0)
        total_length = cumulative_lengths[-1]

        num_points = max(int(total_length / self.resolution_cm), 2)
        desired_lengths = np.linspace(0, total_length, num_points)
        t_samples = np.interp(desired_lengths, cumulative_lengths, t_dense)
        points = np.array([bezier(t) for t in t_samples])

        dx_dt = np.gradient(points[:, 0], t_samples)
        dy_dt = np.gradient(points[:, 1], t_samples)
        d2x_dt2 = np.gradient(dx_dt, t_samples)
        d2y_dt2 = np.gradient(dy_dt, t_samples)

        curvature = np.abs(dx_dt * d2y_dt2 - dy_dt * d2x_dt2) / (dx_dt**2 + dy_dt**2)**1.5
        l = 13
        radius = 1 / curvature
        sign_curvature = np.sign(dx_dt * d2y_dt2 - dy_dt * d2x_dt2)
        steering_angle = -sign_curvature * np.degrees(np.arctan(l / radius))

        a_y_max = 2.0
        max_speed = 3.0
        safe_speed = np.minimum(np.sqrt(a_y_max * (l / 100) / np.tan(np.radians(np.abs(steering_angle)))), max_speed)
        safe_speed = np.clip(safe_speed, 0.5, max_speed)

        return points, steering_angle, safe_speed

#region testing_main
if __name__ == "__main__":
    class Pillar:
        def __init__(self, x_cm, y_cm, color,section_nb):
            self.x_cm = x_cm
            self.y_cm = y_cm
            self.color = color
            self.section_nb=section_nb
    # CCW direction: left of red, right of green
    pillars = np.array([
        Pillar(60, 100, "red",1),
        Pillar(40, 200, "green",1),
        Pillar(100, 260, "red",2),
        Pillar(100, 260, "red",2),
        Pillar(260, 150, "green",3),
        Pillar(100, 40, "red",4)
    ])
    

    g0 = np.array([50, 50])       # Start position
    d0 = np.array([1, 0])         # Facing right
    df = np.array([0, -1])        # End pointing down (CCW)

    tb = Trajectory_Builder(3.0)
    tb.draw_outline()

    for i, p in enumerate(pillars):
        tb.create_pillar(p.x_cm, p.y_cm, p.color, label=f"P{i+1}")

    points, steering, speed, _ = tb.bezier_curve_from_pillars(pillars, g0, d0, df,0)

    plt.figure(1)
    plt.plot(points[:, 0], points[:, 1], label="Trajectory", color="blue")
    plt.scatter(points[:, 0], points[:, 1], s=10, color='black')
    plt.axis("equal")
    plt.title("Trajectory Path")
    plt.legend()

    plt.figure(2)
    plt.plot(steering, 'r-')
    plt.title("Steering Angle")
    plt.xlabel("Step")
    plt.ylabel("Angle (deg)")

    plt.figure(3)
    plt.plot(speed, 'g-')
    plt.title("Safe Speed")
    plt.xlabel("Step")
    plt.ylabel("Speed (m/s)")

    plt.show()

#endregion