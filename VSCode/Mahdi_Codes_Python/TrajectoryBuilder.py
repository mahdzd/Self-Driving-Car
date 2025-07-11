import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


class Trajectory_Builder:
    last_calculated_trajectory=None

    def __init__(self):




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

    def create_pillar(self,xc, yc, s):
        x = [xc-2.5, xc+2.5, xc+2.5, xc-2.5, xc-2.5]
        y = [yc-2.5, yc-2.5, yc+2.5, yc+2.5, yc-2.5]
        plt.figure(1)
        plt.plot(x, y, color='r' if s == "red" else 'g')
        plt.axis("equal")

    def bezier_curve_x(self,t, P0, P1, P2, P3):
        return ((1 - t)**3) * P0[0] + 3 * ((1 - t)**2) * t * P1[0] + 3 * (1 - t) * (t**2) * P2[0] + (t**3) * P3[0]

    def bezier_curve_y(self,t, P0, P1, P2, P3):
        return ((1 - t)**3) * P0[1] + 3 * ((1 - t)**2) * t * P1[1] + 3 * (1 - t) * (t**2) * P2[1] + (t**3) * P3[1]

    def create_bezier_curve(self,P0, P3, v0, v3, nb):

        v0 = v0 / np.linalg.norm(v0)
        v3 = v3 / np.linalg.norm(v3)
        d = np.linalg.norm(P3 - P0) / 3
        P1 = P0 + d * v0
        P2 = P3 - d * v3

        t = np.linspace(0, 1, 100)
        x = self.bezier_curve_x(t, P0, P1, P2, P3)
        y = self.bezier_curve_y(t, P0, P1, P2, P3)

        dx_dt = np.gradient(x, t)
        dy_dt = np.gradient(y, t)
        d2x_dt2 = np.gradient(dx_dt, t)
        d2y_dt2 = np.gradient(dy_dt, t)

        curvature = np.abs(dx_dt * d2y_dt2 - dy_dt * d2x_dt2) / (dx_dt**2 + dy_dt**2)**1.5
        l = 13
        radius = 1 / curvature
        sign_curvature = np.sign(dx_dt * d2y_dt2 - dy_dt * d2x_dt2)
        steering_angle = -sign_curvature * np.degrees(np.arctan(l / radius))

        #smoothout the steering angle curve
        #steering_angle = gaussian_filter1d(steering_angle, sigma=3)

        a_y_max = 2.0  # max lateral acceleration in m/s^2 (safety assumption )
        max_speed=3
        safe_speed =np.minimum(
        np.sqrt(a_y_max *( l/100) / np.tan(np.radians(np.abs(steering_angle)))), max_speed
    )
        safe_speed = np.clip(safe_speed, 0.5, max_speed)

        #safe_speed = gaussian_filter1d(safe_speed, sigma=3)

        # Save trajectory (x, y, angle, speed) to class variable
        Trajectory_Builder.last_calculated_trajectory = {
            "x": x.tolist(),
            "y": y.tolist(),
            "steering_angle": steering_angle.tolist(),
            "safe_speed": safe_speed.tolist()
        }

        plt.figure(1)
        plt.plot(x, y)
        plt.plot(P0[0], P0[1], 'ro')
        plt.plot(P3[0], P3[1], 'ro')
        plt.legend(['Bézier Curve', 'Start/End Points'])

        plt.figure(2)
        t_plot = t + nb - 1
        plt.plot(t_plot, steering_angle)
        plt.xlabel('t')
        plt.ylabel('Steering Angle (deg)')
        plt.title('Steering Angle')
        plt.axhline(0, color='k', linestyle='--')
        plt.axvline(0, color='k', linestyle='--')

        plt.figure(3)
        plt.plot(t_plot, safe_speed)
        plt.xlabel('t')
        plt.ylabel('Safe Speed (m/s)')
        plt.title('Safe Speed')
        plt.axhline(0, color='k', linestyle='--')
        plt.axvline(0, color='k', linestyle='--')

    def bezier_curve(self,pillars,g0,d0,df):        
        self.draw_outline()
        for p in pillars:
            self.create_pillar(p.x_cm, p.y_cm, p.color)

        v = np.zeros((pillars.shape[0] + 1, 2))
        v[0, :] = g0
        for i in range(1, v.shape[0]):
            x, y, s = pillars[i-1].x_cm,pillars[i-1].y_cm,pillars[i-1].color
            if x <= 100 and 100 <= y <= 200:
                v[i, :] = [x + 20, y] if s == "red" else [x - 20, y]
            elif x <= 200 and y >= 200:
                v[i, :] = [x, y - 20] if s == "red" else [x, y + 20]
            elif x >= 200 and y >= 100:
                v[i, :] = [x - 20, y] if s == "red" else [x + 20, y]
            else:
                v[i, :] = [x, y + 20] if s == "red  " else [x, y - 20]

        dv = np.zeros_like(v)
        dv[0, :] = d0
        dv[-1, :] = df
        kc = 0.0085
        for i in range(1, dv.shape[0]-1):
            tdv = v[i+1] - v[i]
            dv[i, :] = tdv + kc * np.linalg.norm(tdv) * (v[i] - v[i-1])

        for i in range(len(v) - 1):
            self.create_bezier_curve(v[i], v[i+1], dv[i], dv[i+1], i+1)

        plt.show()

    def sample_bezier_by_arclength(self, P0, P1, P2, P3, num_points=100):
        def bezier(t):
            return ((1 - t)**3) * P0 + 3 * ((1 - t)**2) * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3

        # Step 1: Fine sampling
        t_dense = np.linspace(0, 1, 1000)
        curve = np.array([bezier(t) for t in t_dense])

        # Step 2: Compute arc length
        deltas = np.diff(curve, axis=0)
        dists = np.sqrt((deltas**2).sum(axis=1))
        cumulative_lengths = np.insert(np.cumsum(dists), 0, 0)
        total_length = cumulative_lengths[-1]

        # Step 3: Find new t values for equally spaced points
        desired_lengths = np.linspace(0, total_length, num_points)
        t_equally_spaced = np.interp(desired_lengths, cumulative_lengths, t_dense)

        # Step 4: Get positions on the curve
        points = np.array([bezier(t) for t in t_equally_spaced])
        return points, t_equally_spaced




P0 = np.array([0, 0])
P1 = np.array([30, 60])
P2 = np.array([70, 60])
P3 = np.array([100, 0])

tb = Trajectory_Builder()
points, t_values = tb.sample_bezier_by_arclength(P0, P1, P2, P3, num_points=50)

# Plot it
plt.plot(points[:, 0], points[:, 1], 'bo-')
plt.axis("equal")
plt.title("Equally spaced points along Bézier curve")
plt.show()
