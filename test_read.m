file = fopen("data.out","r");

t = fscanf(file,"%d %d",2);
M = t(1);
N = t(2);

w = fscanf(file,"%d",N);
size(w)
E = fscanf(file,"%d",1);
ytest = fscanf(file,"%d",M);
size(ytest)
fclose(file);

save('answer_one.mat','w','E','ytest');
