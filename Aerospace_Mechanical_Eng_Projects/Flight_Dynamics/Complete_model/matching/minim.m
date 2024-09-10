function erro = minim(K)
global opreport ut p_FT r_FT outr out_ind TF

% Modifica as variáveis do Simulink

assignin('base','Cn_r',K(1));
assignin('base','Cn_beta',K(2));
assignin('base','Cn_rud',K(3));

[tout,xout,yout]=sim('ACFT',TF,simset('InitialState',getstatestruct(opreport),'Solver','ode4','FixedStep',0.02),ut);

erro = sum(sqrt((yout(:,out_ind(logical(strcmp('ACFT/r_degps',outr))))-r_FT).^2) + sqrt((yout(:,out_ind(logical(strcmp('ACFT/p_degps',outr))))-p_FT).^2));
