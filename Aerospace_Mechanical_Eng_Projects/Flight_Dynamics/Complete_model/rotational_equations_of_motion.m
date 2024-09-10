syms Ixx Iyy Izz Ixz p q r p_dot q_dot r_dot

% Inertia Matrix
I = [Ixx, 0 -Ixz;
    0, Iyy, 0;
    -Ixz, 0, Izz];

% Angular velocity and acceleration
omega_dot = [p_dot; q_dot; r_dot];
omega = [p; q; r];

% Calculate external moments (x, y, z moment equations)
M_ext = I*omega_dot + cross(omega, I*omega);

% Display the moments
M_x = simplify(M_ext(1))
M_y = simplify(M_ext(2))
M_z = simplify(M_ext(3))