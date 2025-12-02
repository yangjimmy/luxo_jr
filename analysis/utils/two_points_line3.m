function two_points_line3(p1, p2, linetype, joint_color, joint_size)
arguments
    p1
    p2
    linetype = 'k'
    joint_color = 'k'
    joint_size = 12
end
plot3([p1(1),p2(1)], [p1(2),p2(2)], [p1(3),p2(3)], '-o', 'Color',linetype, 'MarkerEdgeColor',joint_color, 'MarkerSize',joint_size); hold on;

end
