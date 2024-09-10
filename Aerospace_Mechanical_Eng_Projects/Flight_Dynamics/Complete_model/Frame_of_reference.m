
% Project: Definition od Rotation of Frame of Reference


%==========================================================================
% Define the variables that will be needed
syms psi theta phi u v w i j k p q r u_dot v_dot w_dot m

%% ROTATION AND VEL
% DEFINE MATRICES
% Yaw Angle Frame
Lpsi = [cos(psi) sin(psi) 0; -sin(psi) cos(psi) 0; 0 0 1]

%Pitch Angle Rotation
Ltheta = [cos(theta) 0 -sin(theta); 0 1 0; sin(theta) 0 cos(theta)]

% Bank Angle Rotation
Lphi = [1 0 0; 0 cos(phi) sin(phi); 0 -sin(phi) cos(phi)]

%COMPLETE ROTATION - EARTH TO BODY
LEB = Lphi * Ltheta * Lpsi

% COMPLETE ROTATION V- BODY TO EARTH
LBE = transpose(Abody)

% CONVERT BODY VELOCITY INTO EARTH'S VELOCITY
VE = LBE*[u;v;w]

% Angular Velocity
k_1 = simplify((Ltheta^-1)*(Lphi^-1)*[i;j;k])
j_2 = simplify((Lphi*^-1)*[0;j;k])


%% Derivation of Equations of Motion (EOM)
% Translational Motion - External Forces (x, y, z)
F_external = m*([u_dot + v_dot] + cross([p;q;r], [u;v;w]))

% Rotational Motion - valid for an inertial frame

% Aircraft States Vector - Conditions that define the Aircraft at a given
% time