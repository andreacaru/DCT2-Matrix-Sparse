%Andrea Carubelli: 803192
%Alessio Abondio: 808752
myFolder = 'C:\Users\Andrea\Documents\MATLAB\MatriciCalcoloNumerico'; %cartella in cui ci sono le matrici
filePattern = fullfile(myFolder, '*.mat'); %pattern
matFiles = dir(filePattern);

for k = 1:length(matFiles)
    load(matFiles(k).name); %carico la matrice
    A = Problem.A; %assegno la matrice
    n = length(A); %numero righe della matrice A
    xe = ones(n,1); %vettori di 1 di lunghezza n
    b=A*xe;
    fprintf('Tempo di calcolo per: ');
    fprintf(matFiles(k).name);
    fprintf(' ');
    tic; %inizio calcolo tempo
    x=A\b; %soluzione
    toc; %fine calcolo tempo
    
    %accuratezza
    error = norm((x-xe)/norm(x)); %calcolo errore relativo
    fprintf('Errore relativo -> ');
    disp(error); %mostro errore relativo
end
