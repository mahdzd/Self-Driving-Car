function g=bezier_curve()
x=[40 80 25 60 120 190 ];
y=[30 80 170 220 250 220];
d=[[0 1] ;[-0 1]; [1 3];[1 1];[1 -0.6]; [1 0]];
figure(1);
hold off;
figure(2);
hold off;

figure(1);
sx=[0 300 300 0 0]
sy=[0 0 300 300 0]
plot(sx,sy);
hold on
sxi=[110 190 190 110 110]
syi=[110 110 190 190 110]
plot(sxi,syi);

create_Pillar(50,80,0);
create_Pillar(40,170,1);
create_Pillar(60,240,0);
create_Pillar(120,230,1);
create_Pillar(190,240,0);

for i=1:length(x)-1
    p0=[x(i) y(i)];
    p1=[x(i+1) y(i+1)];
    v0=d(i,:)
    v3=d(i+1,:)
create_bezier_curve(p0,p1,v0,v3,i);
hold on;
end

end
