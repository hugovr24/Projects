clear ut
global opreport ut rud_FT p_FT r_FT outr out_ind TF
%% FLIGHT DATA (mass = 10886 / cg = 0.34 / KCAS = 240 / Alt = 35000ft - init_high)

[NUM,TXT,RAW] = xlsread('ft_data2');
time_FT = NUM(:,1);
rud_FT = NUM(:,2);
p_FT = NUM(:,4);
r_FT = NUM(:,5);
beta_FT = NUM(:,3);
Ixx = 50400;
Ixz = 16400;
Iyy = 180000;
Izz = 210000;
Inertia = [Ixx 0 -Ixz; 0 Iyy 0; -Ixz 0 Izz]; 
%% SIMULATION
% Writing initial inputs vector.
inputs = getinputstruct(opreport);                                          % Reads the model inputs
utin = zeros(size(inputs.signals,2),1);                                     % initialize with zeros the inputs vector - this is optional but reduces computational time of the code.
for i = 1:size(inputs.signals,2)
    utin(i,:) = inputs.signals(i).values;                                   % Creates a vector with the trimmed values for the inputs.
end

% Total simulation time - [s];
TF=max(time_FT);
% Time data for the input;
t = time_FT';                                          % This vector can be any kind of time vector to create the input.

% Create an input vector of the same size as t;
%First line is the time stamp itself (simulink coding!)
ut = zeros(size(t,2),size(inputs.signals,2));                               % initialize with zeros the inputs vector - this is optional but reducis computational time of the code.
for i=1:size(t,2)
    ut(i,1) = t(i);                                                         % Simulink default. The first line is the time vector.
    for j=1:size(inputs.signals,2)
        ut(i,j+1) = utin(j);                                                % Initial input vectors with the same size as t.
    end
end

% RUDDER INPUT                                                                 %amplitude [deg]
%Control Surface index
for i=1:size(opreport.Inputs,1)
    intr{i,1} = opreport.Inputs(i).Block;                                   % Create a structure with the names of the inputs
end
in_ind = [1:size(opreport.Inputs,1)];                                       % Create a vector with the indices of the inputs.
ind_control = in_ind(logical(strcmp('ACFT/Rudder_deg',intr)));            % Finds the position of the Elevator input.

% input command with the same size as t; You can draw anything here.
ut(:,ind_control+1) = rud_FT;

%Simulation command
[tout,xout,yout]=sim('ACFT',TF,simset('InitialState',getstatestruct(opreport),'Solver','ode4','FixedStep',0.02),ut);

%Plot
%Read Outputs
for i=1:size(opreport.Outputs,1)
    outr{i,1} = opreport.Outputs(i).Block;                                   % Create a structure with the names of the outputs.
end
out_ind = [1:size(opreport.Outputs,1)];                                      % Create a vector with the indices of the outputs.

grid;
figure(1);
subplot(421);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/Beta_deg',outr)))),t,beta_FT,'--'); xlabel('Time - [s]');ylabel('Beta - [deg]')
subplot(422);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/KCAS',outr))))); xlabel('Time - [s]');ylabel('KCAS')
subplot(423);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/Phi_deg',outr))))); xlabel('Time - [s]');ylabel('Phi - [deg]')
subplot(424);plot(t,ut(:,ind_control+1)); xlabel('Time - [s]');ylabel('Rudder - [deg]')
subplot(425);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/p_degps',outr)))),t,p_FT,'--'); xlabel('Time - [s]');ylabel('Roll Rate - [deg/s]')
subplot(426);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/r_degps',outr)))),t,r_FT,'--'); xlabel('Time - [s]');ylabel('Yaw Rate - [deg/s]')
subplot(427);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/PresAlt_ft',outr))))); xlabel('Time - [s]');ylabel('Altitude - [ft]')
subplot(428);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/ny',outr))))); xlabel('Time - [s]');ylabel('Load Factor (Ny) - [g]')
figure(2);
plot(yout(:,out_ind(logical(strcmp('ACFT/Beta_deg',outr)))),yout(:,out_ind(logical(strcmp('ACFT/Phi_deg',outr))))); xlabel('Beta - [deg]');ylabel('Phi - [deg]')


%% OPTIMIZER

 options = optimset('Display','iter','MaxIter',300);


[K,FVAL] = fmincon(@minim2,[Cn_r,Cn_beta,Cn_rud],[],[],[],[],[-1,0,-0.15],[0,0.9,-0.03],[],options);

% [K,FVAL] = fminsearch(@minim,[Cn_r,Cn_beta,Cn_rud],options);

assignin('base','Cn_beta',K(2));
assignin('base','Cn_r',K(1));
assignin('base','Cn_rud',K(3));
K
%% FINAL RUN
% Run for 40s
ut = [ut; 21 ut(end,2:end-1) 0; 40 ut(end,2:end-1) 0];

[tout,xout,yout]=sim('ACFT',40,simset('InitialState',getstatestruct(opreport),'Solver','ode4','FixedStep',0.02),ut);

figure(3);
subplot(421);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/Beta_deg',outr)))),t,beta_FT,'--'); xlabel('Time - [s]');ylabel('Beta - [deg]')
subplot(422);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/KCAS',outr))))); xlabel('Time - [s]');ylabel('KCAS')
subplot(423);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/Phi_deg',outr))))); xlabel('Time - [s]');ylabel('Phi - [deg]')
subplot(424);plot(ut(:,1),ut(:,ind_control+1)); xlabel('Time - [s]');ylabel('Rudder - [deg]')
subplot(425);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/p_degps',outr)))),t,p_FT,'--'); xlabel('Time - [s]');ylabel('Roll Rate - [deg/s]')
subplot(426);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/r_degps',outr)))),t,r_FT,'--'); xlabel('Time - [s]');ylabel('Yaw Rate - [deg/s]')
subplot(427);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/PresAlt_ft',outr))))); xlabel('Time - [s]');ylabel('Altitude - [ft]')
subplot(428);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/ny',outr))))); xlabel('Time - [s]');ylabel('Load Factor (Ny) - [g]')
figure(4);
plot(yout(:,out_ind(logical(strcmp('ACFT/Beta_deg',outr)))),yout(:,out_ind(logical(strcmp('ACFT/Phi_deg',outr))))); xlabel('Beta - [deg]');ylabel('Phi - [deg]')