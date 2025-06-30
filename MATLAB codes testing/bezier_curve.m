function g=bezier_curve()
x=[40 80 25 60 120 190 ];
y=[30 80 170 220 250 220];
d=[[0 1] ;[-1 1]; [1 3];[1 1];[1 -0.6]; [0 -1]];
figure(1);
clf;
figure(2);
clf;

%ploting the map outlines
draw_outline()

% Define pillars as a matrix where each row is [xc, yc, s]
pillars = [
    60,  100,  0;
    40, 200,  1;
    100, 260,  0;
   200, 260,  1;
   260, 150,  0
];

for i = 1:size(pillars,1)
    create_Pillar(pillars(i,1), pillars(i,2), pillars(i,3));
end
axis equal

%find the coordinates of the passage points
v=zeros(length(pillars)+1,2);
v(1,:)=[50 0];
for i=2:size(v,1)
    if pillars(i-1,1)<=100 & pillars(i-1,2)<=200
        if pillars(i-1,3)==0
            v(i,:)=[pillars(i-1,1)+20,pillars(i-1,2)];
        else
            v(i,:)=[pillars(i-1,1)-20,pillars(i-1,2)];
        end
    elseif pillars(i-1,1)<=200 & pillars(i-1,2)>=200
         if pillars(i-1,3)==0
            v(i,:)=[pillars(i-1,1),pillars(i-1,2)-20];
        else
            v(i,:)=[pillars(i-1,1),pillars(i-1,2)+20];
        end

    elseif pillars(i-1,1)>=200 & pillars(i-1,2)>=100
        if pillars(i-1,3)==0
            v(i,:)=[pillars(i-1,1)-20,pillars(i-1,2)];
        else
            v(i,:)=[pillars(i-1,1)+20,pillars(i-1,2)];
        end
    else
        if pillars(i-1,3)==0
            v(i,:)=[pillars(i-1,1),pillars(i-1,2)+20];
        else
            v(i,:)=[pillars(i-1,1),pillars(i-1,2)-20];
        end
    end

end


for i=1:size(v,1)-1
    p0=[v(i,1) v(i,2)];
    p1=[v(i+1,1) v(i+1,2)];
    v0=d(i,:)
    v3=d(i+1,:)
create_bezier_curve(p0,p1,v0,v3,i);
hold on;
end

end
