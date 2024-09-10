
%% SIMULATION
% Writing initial inputs vector.
inputs = getinputstruct(opreport);                                          % Reads the model inputs
utin = zeros(size(inputs.signals,2),1);                                     % initialize with zeros the inputs vector - this is optional but reduces computational time of the code.
for i = 1:size(inputs.signals,2)
    utin(i,:) = inputs.signals(i).values;                                   % Creates a vector with the trimmed values for the inputs.
end

% Total simulation time - [s];
TF=100;
% Time data for the input;
t = [0 5 6 7 8 9.0 10 TF];                                          % This vector can be any kind of time vector to create the input.

% Create an input vector of the same size as t;
%First line is the time stamp itself (simulink coding!)
ut = zeros(size(t,2),size(inputs.signals,2));                               % initialize with zeros the inputs vector - this is optional but reducis computational time of the code.
for i=1:size(t,2)
    ut(i,1) = t(i);                                                         % Simulink default. The first line is the time vector.
    for j=1:size(inputs.signals,2)
        ut(i,j+1) = utin(j);                                                % Initial input vectors with the same size as t.
    end
end

% ELEVATOR DOUBLET
delta = 5;                                                                   %amplitude [deg]
%Control Surface index
for i=1:size(opreport.Inputs,1)
    intr{i,1} = opreport.Inputs(i).Block;                                   % Create a structure with the names of the inputs
end
in_ind = [1:size(opreport.Inputs,1)];                                       % Create a vector with the indices of the inputs.
ind_control = in_ind(logical(strcmp('ACFT/Elevator_deg',intr)));            % Finds the position of the Elevator input.

% input command with the same size as t; You can draw anything here.
ut(:,ind_control+1) = [ut(1,ind_control+1) ut(1,ind_control+1) (ut(1,ind_control+1)-delta) (ut(1,ind_control+1)-delta) (ut(1,ind_control+1)+delta) (ut(1,ind_control+1)+delta) ut(1,ind_control+1) ut(1,ind_control+1)]' ;

%Simulation command
[tout,xout,yout]=sim('ACFT',TF,simset('InitialState',getstatestruct(opreport),'Solver','ode4','FixedStep',0.01),ut);

% Plot 
% Read Outputs
for i=1:size(opreport.Outputs,1)
    outr{i,1} = opreport.Outputs(i).Block;                                   % Create a structure with the names of the outputs.
end
out_ind = [1:size(opreport.Outputs,1)];                                      % Create a vector with the indices of the outputs.

grid;
subplot(421);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/Alpha_deg',outr))))); xlabel('Time - [s]');ylabel('Alpha - [deg]')
subplot(422);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/KCAS',outr))))); xlabel('Time - [s]');ylabel('KCAS')
subplot(423);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/Theta_deg',outr))))); xlabel('Time - [s]');ylabel('Theta - [deg]')
subplot(424);plot(t,ut(:,ind_control+1)); xlabel('Time - [s]');ylabel('Elevator - [deg]')
subplot(425);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/q_degps',outr))))); xlabel('Time - [s]');ylabel('Pitch Rate - [deg/s]')
subplot(426);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/Thrust_N',outr))))); xlabel('Time - [s]');ylabel('Thrust - [N]')
subplot(427);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/PresAlt_ft',outr))))); xlabel('Time - [s]');ylabel('Altitude - [ft]')
subplot(428);plot(tout,yout(:,out_ind(logical(strcmp('ACFT/nz',outr))))); xlabel('Time - [s]');ylabel('Load Factor (Nz) - [g]')