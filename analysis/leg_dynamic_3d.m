clc; clear; close all;
addpath('.\utils\');

l1 = 300;
l2 = 50;
l3 = 40;
l4 = 25;
l5 = 317;
l6 = 80;
l7 = 300;
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
t1 = deg2rad(5);        % deg
t2 = deg2rad(-90+3);   % deg
t4 = deg2rad(-5);                 % deg
t1_d = deg2rad(7);        % deg
t2_d = deg2rad(-90+5);   % deg
t7 = deg2rad(-90);

t = 0:0.001:15;


P00 = [0; -l3; l11];
J10 = [0; 0; l11];
J20 = [-l4; -l3; l11];
P10 = [l1 * cos(t1); l1 * sin(t1); l11];
P20 = [-l4 + l2*cos(t2); -l3 + l2 * sin(t2); l11];

% solve P3, P3
K1 = l1 * cos(t1) + l4 - l2 * cos(t2);
K2 = l1 * sin(t1) + l4 - l2 * sin(t2);
K3 = (l5^2-K1^2 - K2^2 - l6^2) / (2*l6);
t3 = atan2(-sqrt(K1^2+K2^2-K3^2), K3) + atan2(K2, K1);
P30 = [l1*cos(t1) + l6*cos(t3); l1*sin(t1)+l6*sin(t3); l11];
P40 = [l1*cos(t1) + l7*cos(t3); l1*sin(t1)+l7*sin(t3); l11];
P50 = [l1*cos(t1) + l7*cos(t3); l1*sin(t1)+l7*sin(t3); l11 - l12];

trans = rotx(rad2deg(t4));
P0 = trans * P00;
J1 = trans * J10;
J2 = trans * J20;
P1 = trans * P10;
P2 = trans * P20;
P3 = trans * P30;
P4 = trans * P40;
P5 = trans * P50;



% second group
P00_d = [0; -l3; -l11];

J10_d = [0; 0; -l11];
J20_d = [-l4; -l3; -l11];
P10_d = [l1 * cos(t1_d); l1 * sin(t1_d); -l11];
P20_d = [-l4 + l2*cos(t2_d); -l3 + l2 * sin(t2_d); -l11];

% solve P3_d, P4_d
K1_d = l1 * cos(t1_d) + l4 - l2 * cos(t2_d);
K2_d = l1 * sin(t1_d) + l4 - l2 * sin(t2_d);
K3_d = (l5^2-K1_d^2 - K2_d^2 - l6^2) / (2*l6);
t3_d = atan2(-sqrt(K1_d^2+K2_d^2-K3_d^2), K3_d) + atan2(K2_d, K1_d);


P30_d = [l1*cos(t1_d) + l6*cos(t3_d); l1*sin(t1_d)+l6*sin(t3_d); -l11];
P40_d = [l1*cos(t1_d) + l7*cos(t3_d); l1*sin(t1_d)+l7*sin(t3_d); -l11];
P50_d = [l1*cos(t1_d) + l7*cos(t3_d); l1*sin(t1_d)+l7*sin(t3_d); -l11+l12];

% solve t4_d
x50 = P50(1); y50 = P50(2); z50 = P50(3);
x5 = P5(1); y5 = P5(2); z5 = P5(3);
x50_d = P50_d(1); y50_d = P50_d(2); z50_d = P50_d(3);

x5_d = x50_d;
dx = (x5 - x5_d);
T3 = dx^2 + y5^2 + (z5+l8)^2 + y50_d^2 + z50_d^2 - l9^2;
T2 = 2 * (z5+l8) * y50_d - 2 * y5 * z50_d;
T1 = 2 * y5 * y50_d + 2 * (z5+l8) * z50_d;

t4_d = atan2(sqrt(T1^2+T2^2-T3^2), T3) + atan2(T2, T1);


l_trans = [0; 0; -l8];

% t4_d = deg2rad(3);
trans_d = rotx(rad2deg(t4_d));
% trans_d = rotx(6)
P0_d = trans_d * P00_d + l_trans;
J1_d = trans_d * J10_d + l_trans;
J2_d = trans_d * J20_d + l_trans;
P1_d = trans_d * P10_d + l_trans;
P2_d = trans_d * P20_d + l_trans;
P3_d = trans_d * P30_d + l_trans;
P4_d = trans_d * P40_d + l_trans;
P5_d = trans_d * P50_d + l_trans;

P6 = (P5+P5_d) / 2;

%%
v = P5_d - P5;
v = v / norm(v);
vy = P3 - P4;
vy = vy / norm(vy);
vx = P5 - P4;
vx = vx / norm(vx);
vz = cross(vx, vy);

R = [vx vy vz];
v_loc  = R' * v;

t5 = atan2(-v_loc(3), sqrt(1-v_loc(3)^2));
t6 = -atan2(v_loc(2) / cos(t5), v_loc(1) / cos(t5));

Rx = [1, 0, 0;
      0, cos(t7), -sin(t7);
      0, sin(t7),  cos(t7);];

vec_per = R * Rx * [0; -1; 0];
P7 = l14 * vec_per + P6;


% vec_per = [0; v(3); v(2)];
% vec_per = vec_per / norm(vec_per);
% P7 = l14 * vec_per  + P6;


%%

figure('Position',[200, 200, 600, 600]);
two_points_line3(P0, J1, bar_ground); hold on;
two_points_line3(P0, J2, bar_ground);
two_points_line3(J1, P1, bar_act);
two_points_line3(J2, P2, bar_act);
two_points_line3(P2, P3, bar_dri);
two_points_line3(P1, P3, bar_dri);
two_points_line3(P3, P4, bar_dri);
two_points_line3(P4, P5, bar_dri);

two_points_line3(P0_d, J1_d, bar_ground); hold on;
two_points_line3(P0_d, J2_d, bar_ground);
two_points_line3(J1_d, P1_d, bar_act);
two_points_line3(J2_d, P2_d, bar_act);
two_points_line3(P2_d, P3_d, bar_dri);
two_points_line3(P1_d, P3_d, bar_dri);
two_points_line3(P3_d, P4_d, bar_dri);
two_points_line3(P4_d, P5_d, bar_dri);

two_points_line3(P5, P6, bar_act);
two_points_line3(P6, P5_d, bar_act);

two_points_line3(P6, P7, bar_dri);


axis equal;
view_vec = [1.1420   -0.0039   -2.1299];
view(view_vec)


rad2deg(t5)
rad2deg(t6)
