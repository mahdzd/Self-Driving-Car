% this code crates a bezier curve based on a starting and ending point and
% based on a starting and ending vector that represent the direction of the
% car on each position
% Define start and end points
P0 = [10 10];
P3 = [15 20];

% Define direction vectors at start and end points
v0 = [-2 1]; % Direction vector at start point
v3 = [1 0]; % Direction vector at end point

% Normalize direction vectors
v0 = v0 / norm(v0);
v3 = v3 / norm(v3);

% Calculate control points P1 and P2
d = norm(P3 - P0) / 3; % Distance from P0 to P1 and P2 to P3
P1 = P0 + d * v0;
P2 = P3 - d * v3;

% Create a finer grid for interpolation
t = linspace(0, 1, 100);

% Calculate the Bézier curve
x = (1-t).^3 * P0(1) + 3*(1-t).^2 .* t * P1(1) + 3*(1-t) .* t.^2 * P2(1) + t.^3 * P3(1);
y = (1-t).^3 * P0(2) + 3*(1-t).^2 .* t * P1(2) + 3*(1-t) .* t.^2 * P2(2) + t.^3 * P3(2);

% Plot the result
plot(x, y);
hold on;
plot(P0(1), P0(2), 'ro');
plot(P1(1), P1(2), 'go');
plot(P2(1), P2(2), 'go');
plot(P3(1), P3(2), 'ro');
legend('Bézier Curve', 'Start/End Points', 'Control Points');