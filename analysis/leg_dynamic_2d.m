clc; clear; close all;
addpath('.\utils\');

% l1 = 300;
l1 = 200;
l2 = 50;
l3 = 40;
l4 = 25;
% l5 = 317;
l5 = 217;
l6 = 80;
% l7 = 300;
l7 = 245;
l8 = 50;
l9 = 73;

l11 = 31.5;
l12 = 20;
l13 = l12+l8;
l14 = 35;

% line type
bar_ground = 'k';
bar_act = 'b';
bar_dri = 'r';
joint_color = 'k';
joint_radius = 3;


%%
t1 = deg2rad(3); % deg
t2 = deg2rad(-90+10); % deg

P0 = [0, -l3];

J1 = [0, 0];
J2 = [-l4, -l3];
P1 = [l1 * cos(t1), l1 * sin(t1)];
P2 = [-l4 + l2*cos(t2), -l3 + l2 * sin(t2)];

% solve P3
K1 = l1 * cos(t1) + l4 - l2 * cos(t2);
K2 = l1 * sin(t1) + l4 - l2 * sin(t2);
K3 = (l5^2-K1^2 - K2^2 - l6^2) / (2*l6);
t3 = atan2(-sqrt(K1^2+K2^2-K3^2), K3) + atan2(K2, K1);
P3 = [l1*cos(t1) + l6*cos(t3), l1*sin(t1)+l6*sin(t3)];
P4 = [l1*cos(t1) + l7*cos(t3), l1*sin(t1)+l7*sin(t3)];


figure;
two_points_line(P0, J1, bar_ground); hold on;
two_points_line(P0, J2, bar_ground);
two_points_line(J1, P1, bar_act);
two_points_line(J2, P2, bar_act);
two_points_line(P2, P3, bar_dri);
two_points_line(P1, P3, bar_dri);
two_points_line(P1, P4, bar_dri);

axis equal;


