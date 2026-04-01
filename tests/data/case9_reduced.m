function mpc = case9_reduced
%CASE9_REDUCED  6-bus reduced of power flow data from 9 bus, 3 generator case.
%   Derived from the standard CASE9 test case data from Joe H. Chow's book, p. 70.
%   by removing the three branch without BR_R and move the generator.
%
%   Original Bus 1 (Gen 1) merged into Bus 4  (slack)
%   Original Bus 2 (Gen 2) merged into Bus 8  (PV)
%   Original Bus 3 (Gen 3) merged into Bus 6  (PV)

mpc.version = '2';
mpc.baseMVA = 100;

%% bus data
%  bus_i  type  Pd    Qd  Gs  Bs  area  Vm        Va          baseKV  zone  Vmax  Vmin
mpc.bus = [
    4      3     0     0   0   0   1     1.040000  -2.216788   345     1     1.1   0.9;
    5      1     90    30  0   0   1     1.019544  -3.599309   345     1     1.1   0.9;
    6      2     0     0   0   0   1     1.025000   2.208471   345     1     1.1   0.9;
    7      1     100   35  0   0   1     1.012276   0.912347   345     1     1.1   0.9;
    8      2     0     0   0   0   1     1.025000   3.885641   345     1     1.1   0.9;
    9      1     125   50  0   0   1     1.005122  -3.900271   345     1     1.1   0.9;
];

%% generator data
%  bus  Pg          Qg          Qmax  Qmin   Vg     mBase  status  Pmax  Pmin
mpc.gen = [
    4    71.730424   38.076988   300   -300   1.040  100    1       250   10;
    8    163.000000  -11.552844  300   -300   1.025  100    1       300   10;
    6    85.000000   -26.910102  300   -300   1.025  100    1       270   10;
];

%% branch data
%  fbus  tbus  r       x       b       rateA  rateB  rateC  tap  shift  status  angmin  angmax
mpc.branch = [
    4     5     0.0170  0.0920  0.158   250    250    250    0    0      1       -360    360;
    5     6     0.0390  0.1700  0.358   150    150    150    0    0      1       -360    360;
    6     7     0.0119  0.1008  0.209   150    150    150    0    0      1       -360    360;
    7     8     0.0085  0.0720  0.149   250    250    250    0    0      1       -360    360;
    8     9     0.0320  0.1610  0.306   250    250    250    0    0      1       -360    360;
    9     4     0.0100  0.0850  0.176   250    250    250    0    0      1       -360    360;
];
