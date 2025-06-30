function [x,y]= create_Pillar(xc,yc,s)

x=[xc-2.5,xc+2.5,xc+2.5,xc-2.5,xc-2.5];
y=[yc-2.5,yc-2.5,yc+2.5,yc+2.5,yc-2.5];
if s==0
figure(1);
plot(x,y,'Color',"r");
hold on;

else
figure(1);
plot(x,y,'Color',"g");
hold on;
end

end