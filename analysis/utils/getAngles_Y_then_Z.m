function [theta_y, theta_z] = getAngles_Y_then_Z(v0, v, x, y)
    % Normalize local axes
    ex = x / norm(x);
    ey = y / norm(y);
    ez = cross(ex, ey);
    ez = ez / norm(ez);

    % Local basis matrix: columns are ex, ey, ez
    R = [ex ey ez];

    % Convert to local coordinates
    v0_loc = R' * v0
    v_loc  = R' * v;


    theta_y = atan2(-v_loc(3), sqrt(1-v_loc(3)));
    theta_z = atan2(v_loc(2) / cos(theta_y), v_loc(1) / cos(theta_y));

    % x0 = v0_loc(1);  y0 = v0_loc(2);  z0 = v0_loc(3);
    % x1 = v_loc(1);   y1 = v_loc(2);   z1 = v_loc(3);
    % 
    % % ---------------------------------------------
    % % 1) Solve for theta_y (rotation about local Y)
    % % ---------------------------------------------
    % % Y rotation affects the X-Z plane:
    % %   [x1; z1] = [ cos θy   0   sin θy;
    % %                0        1    0;
    % %               -sin θy   0   cos θy ] * [x'; z']
    % %
    % theta_y = atan2(-z1, x1);
    % 
    % % ---------------------------------------------
    % % 2) Undo Y rotation to isolate Z rotation
    % % ---------------------------------------------
    % cy = cos(theta_y);
    % sy = sin(theta_y);
    % 
    % Ry_inv = [ cy  0  -sy;
    %            0   1   0;
    %            sy  0   cy ];
    % 
    % v_prime = Ry_inv * v_loc;
    % 
    % % ---------------------------------------------
    % % 3) Solve for theta_z (rotation about Z)
    % % ---------------------------------------------
    % phi_after  = atan2(v_prime(2), v_prime(1));  % atan2(y', x')
    % phi_before = atan2(y0, x0);                 % initial angle in XY plane
    % 
    % theta_z = phi_after - phi_before;
    % 
    % % Wrap to (-pi, pi]
    % theta_y = wrapToPi(theta_y);
    % theta_z = wrapToPi(theta_z);
end
