model = 'ACFT';

linsys = linearize(model,opreport);                                         % Command to linearize the model around the trim point
clc
st_ind=num2cell((1:length(linsys.StateName))');                             % state names indicies

%Longitudinal States: x=[q;u;w;theta;Zdist]
ind_long = [st_ind{logical(strcmp('q_radps',linsys.StateName))};
           st_ind{logical(strcmp('u_mps',linsys.StateName))};
           st_ind{logical(strcmp('w_mps',linsys.StateName))};
           st_ind{logical(strcmp('THETA_rad',linsys.StateName))};
           st_ind{logical(strcmp('ZI_m',linsys.StateName))}];

for i=1:size(ind_long,1)
    for j=1:size(ind_long,1)
        Along(i,j) = linsys.A(ind_long(i),ind_long(j));                     % Reduced A matrix with long. states
    end
end

LONG_EIG = eig(Along);
LongData = LONG_EIG(1:end,:)                                                % Eigen values calculation to determine the relevant longitudinal modes

%Lateral States: x=[p;r;v;phi;psi]
ind_lat = [st_ind{logical(strcmp('p_radps',linsys.StateName))};
           st_ind{logical(strcmp('r_radps',linsys.StateName))};
           st_ind{logical(strcmp('v_mps',linsys.StateName))};
           st_ind{logical(strcmp('PHI_rad',linsys.StateName))};
           st_ind{logical(strcmp('PSI_rad',linsys.StateName))}];

for i=1:size(ind_lat,1)
    for j=1:size(ind_lat,1)
        Alat(i,j) = linsys.A(ind_lat(i),ind_lat(j));                        % Reduced A matrix with lat.dir. states
    end
end
LAT_EIG = eig(Alat);
% First eigen value is not relevant
LatData = LAT_EIG(2:end,:)                                                  % Eingen values calculation to determine the relevant lat.dir. modes
Wn=0; Z=0;
[Wn,Z] = damp(LongData);                                                    % Frequency (Wn) and damping (Z) calculation from eigen values.

disp(['Short Period Frequency: ',num2str(Wn(2)),' rad/s'])
disp(['Short Period Damping: ',num2str(Z(2))])
disp(['Phugoid Frequency: ',num2str(Wn(4)),' rad/s'])
disp(['Phugoid Damping: ',num2str(Z(4))])
Wn=0; Z=0;
[Wn,Z] = damp(LatData);                                                     % Frequency (Wn) and damping (Z) calculation from eigen values.
disp(['Dutch Roll Frequency: ',num2str(Wn(2)),' rad/s'])
disp(['Dutch Roll Damping: ',num2str(Z(2))])
if max(LatData(imag(LatData)==0))>0;
    disp(['Spiral Stability time to double: ',num2str(log(2)*abs(1/(Wn(max(LatData(imag(LatData)==0))==real(LatData))*Z(max(LatData(imag(LatData)==0))==real(LatData))))),' s'])
else
    disp(['Spiral Stability time to half: ',num2str(log(2)*abs(1/(Wn(max(LatData(imag(LatData)==0))==real(LatData))*Z(max(LatData(imag(LatData)==0))==real(LatData))))),' s'])
end
disp(['Roll Mode time to half: ',num2str(log(2)*abs(1/(Wn(min(real(LatData))==real(LatData))*Z(min(real(LatData))==real(LatData))))),' s'])

