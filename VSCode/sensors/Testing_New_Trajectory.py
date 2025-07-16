import numpy as np
import matplotlib.pyplot as plt

manual_clicks = []

def draw_outline():
    plt.plot([0, 300, 300, 0, 0], [0, 0, 300, 300, 0], 'k')
    plt.plot([110, 190, 190, 110, 110], [110, 110, 190, 190, 110], 'k')
    plt.axis("equal")
    plt.title("Click: 1st = start point, 2nd = direction")
    plt.grid(True)

    # Grids and lines
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

def create_pillar(xc, yc, s):
    x = [xc-2.5, xc+2.5, xc+2.5, xc-2.5, xc-2.5]
    y = [yc-2.5, yc-2.5, yc+2.5, yc+2.5, yc-2.5]
    plt.plot(x, y, color='r' if s == 0 else 'g')

def create_bezier_curve(P0, P3, v0, v3, nb, label=None, color=None):
    v0 = v0 / np.linalg.norm(v0)
    v3 = v3 / np.linalg.norm(v3)
    d = np.linalg.norm(P3 - P0) / 3
    P1 = P0 + d * v0
    P2 = P3 - d * v3

    t = np.linspace(0, 1, 50)
    x = (1 - t)**3 * P0[0] + 3*(1 - t)**2 * t * P1[0] + 3*(1 - t) * t**2 * P2[0] + t**3 * P3[0]
    y = (1 - t)**3 * P0[1] + 3*(1 - t)**2 * t * P1[1] + 3*(1 - t) * t**2 * P2[1] + t**3 * P3[1]

    dx_dt = np.gradient(x, t)
    dy_dt = np.gradient(y, t)
    d2x_dt2 = np.gradient(dx_dt, t)
    d2y_dt2 = np.gradient(dy_dt, t)

    curvature = np.abs(dx_dt * d2y_dt2 - dy_dt * d2x_dt2) / (dx_dt**2 + dy_dt**2)**1.5
    l = 13
    radius = 1 / curvature
    sign_curvature = np.sign(dx_dt * d2y_dt2 - dy_dt * d2x_dt2)
    steering_angle = -sign_curvature * np.degrees(np.arctan(l / radius))

    plt.figure(1)
    plt.plot(x, y, color=color if color else 'b', label=label)
    plt.plot([P0[0], P3[0]], [P0[1], P3[1]], 'ro')
    plt.legend()

    plt.figure(2)
    t_plot = t + nb - 1
    plt.plot(t_plot, steering_angle, label=f"Steering {label}", color=color)
    plt.xlabel('t')
    plt.ylabel('Steering Angle (deg)')
    plt.title('Steering Angle')
    plt.axhline(0, color='k', linestyle='--')
    plt.grid(True)
    plt.legend()

# Main setup
pillars = np.array([
    [60, 100, 0],
    [40, 200, 1],
])
g0 = np.array([50, 50])
d0 = np.array([0, 1])
df = np.array([0, 1])

def plot_static_path():
    plt.figure(1)
    draw_outline()
    for p in pillars:
        create_pillar(p[0], p[1], int(p[2]))

    v = np.zeros((pillars.shape[0] + 1, 2))
    v[0, :] = g0
    for i in range(1, v.shape[0]):
        x, y, s = pillars[i-1]
        if x <= 100 and 100 <= y <= 200:
            v[i, :] = [x + 20, y] if s == 0 else [x - 20, y]
        elif x <= 200 and y >= 200:
            v[i, :] = [x, y - 20] if s == 0 else [x, y + 20]
        elif x >= 200 and y >= 100:
            v[i, :] = [x - 20, y] if s == 0 else [x + 20, y]
        else:
            v[i, :] = [x, y + 20] if s == 0 else [x, y - 20]

    dv = np.zeros_like(v)
    dv[0, :] = d0
    dv[-1, :] = df
    kc = 0.0085
    for i in range(1, dv.shape[0]-1):
        tdv = v[i+1] - v[i]
        dv[i, :] = tdv + kc * np.linalg.norm(tdv) * (v[i] - v[i-1])

    for i in range(len(v) - 1):
        create_bezier_curve(v[i], v[i+1], dv[i], dv[i+1], i+1)
def on_click(event):
    if event.inaxes is None or event.button != 1:
        return
    global manual_clicks
    manual_clicks.append(np.array([event.xdata, event.ydata]))
    plt.figure(1)
    plt.plot(event.xdata, event.ydata, 'bx')
    plt.draw()

    if len(manual_clicks) == 2:
        start = manual_clicks[0]
        direction = manual_clicks[1] - manual_clicks[0]
        if np.linalg.norm(direction) == 0:
            print("Direction vector cannot be zero.")
            manual_clicks.clear()
            return

        # Build new path starting from manually clicked point
        v = np.zeros((pillars.shape[0] + 1, 2))
        v[0, :] = start
        for i in range(1, v.shape[0]):
            x, y, s = pillars[i-1]
            if x <= 100 and 100 <= y <= 200:
                v[i, :] = [x + 20, y] if s == 0 else [x - 20, y]
            elif x <= 200 and y >= 200:
                v[i, :] = [x, y - 20] if s == 0 else [x, y + 20]
            elif x >= 200 and y >= 100:
                v[i, :] = [x - 20, y] if s == 0 else [x + 20, y]
            else:
                v[i, :] = [x, y + 20] if s == 0 else [x, y - 20]

        # Create direction vectors
        dv = np.zeros_like(v)
        dv[0, :] = direction
        dv[-1, :] = df
        kc = 0.0085
        for i in range(1, dv.shape[0]-1):
            tdv = v[i+1] - v[i]
            dv[i, :] = tdv + kc * np.linalg.norm(tdv) * (v[i] - v[i-1])

        # Draw updated path
        for i in range(len(v) - 1):
            create_bezier_curve(v[i], v[i+1], dv[i], dv[i+1], i+1, label=f"Manual Curve {i+1}", color='m')

        plt.figure(1)
        plt.legend()
        plt.draw()
        plt.figure(2)
        plt.draw()
        manual_clicks.clear()


# Call the base plot
plot_static_path()

# Connect the click handler
fig1 = plt.figure(1)
fig1.canvas.mpl_connect('button_press_event', on_click)

# Show plots
plt.figure(2)
plt.grid(True)
plt.show()
