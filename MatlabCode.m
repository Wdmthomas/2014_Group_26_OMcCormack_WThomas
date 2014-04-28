data = CocaColaFinalTweetDataCSV2;
resultsRHO = zeros(0,40);
resultsPVAL = zeros(0,40);



testPercentage = 0.3;
testCount = round(testPercentage*length(data(:,1)));

resultsYvec = zeros(0,testCount);
resultsYactual = zeros(0,testCount);
RMSerrorVec = zeros(0,1);


kfold = 10;


for i=1:kfold,

 data=data(randsample(1:length(data(:,1)),length(data(:,1))),:);

y = data(:,1);
y = y/norm(y);
y=y-mean(y);

% use the below to select the columns to be used in x.  [16 30] is just the
% lagged share prices

%x = data(:,3:end);

x = data(:,[6:14]);

trainCount = length(data(:,1))- testCount;

yTrain = (y(1:trainCount,:));
%yTrain = (yTrain/2);
%yTrain = (yTrain+1);


yTest =  (y(trainCount+1:end,:));
%yTest =  (yTest/2);
%yTest =  (yTest+1);


xTrain = x(1:trainCount,:);
xTest = x(trainCount+1:end,:);


xTrain = xTrain.';
yTrain = yTrain.';
xTest = xTest.';
yTest = yTest.';


net = fitnet(15);
%view(net);
[net,tr] = train(net,xTrain,yTrain);
%nntraintool;
%plotperform(tr);

Yresults = net(xTest);

RMSEnn = (sum((Yresults-yTest).^2)/testCount)^(1/2);
%}



[RHO,PVAL] = corr(xTest.',yTest.');

resultsYvec = [resultsYvec; Yresults];
resultsYactual = [resultsYactual;yTest];
RMSerrorVec = [RMSerrorVec;RMSEnn];


resultsRHO = [resultsRHO; RHO.'];
resultsPVAL = [resultsPVAL; PVAL.'];

end
