function g=bezier_curve()
g0=[50 50]; %initial position
d0=[0 1]; %initial direction
df=[-1 0];%ending direction
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
   260, 150,  1;
   100, 40, 0

];

for i = 1:size(pillars,1)
    create_Pillar(pillars(i,1), pillars(i,2), pillars(i,3));
end
axis equal

%find the coordinates of the passage points
v=zeros(size(pillars,1)+1,2);
v(1,:)=g0; %assumed initail position
for i=2:size(v,1)
    if pillars(i-1,1)<=100 & pillars(i-1,2)<=200 & pillars(i-1,2)>=100
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


%figuring the direction vectors from passage points
dv=zeros(size(pillars,1)+1,2);
dv(1,:)=d0; %initial direction is assumed
dv(size(pillars,1)+1,:)=df; %final direction is assumed
kc=0.0085; %constatant used for direction contribution

%Computing the next direction:
for i=2:size(dv,1)-1 
    tdv=[v(i+1,1)-v(i,1), v(i+1,2)-v(i,2) ];
    dis_to_next=norm(tdv);
    dv(i,:)=tdv+kc*norm(tdv)*[v(i,1)-v(i-1,1), v(i,2)-v(i-1,2) ]; %taking the direction from the current to the next point adding to it a multiple proportional to the direction of the vector and the vector of the previuos direction to minimize curvature
end



%creating bezier curve using passage points and direction
for i=1:size(v,1)-1
    p0=[v(i,1) v(i,2)];
    p1=[v(i+1,1) v(i+1,2)];
    v0=dv(i,:);
    v3=dv(i+1,:);
create_bezier_curve(p0,p1,v0,v3,i);
hold on;
end

end
