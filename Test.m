

data = NikeTrainingSet;
%data = McDonaldsTrainingSet;
%data = CokeTrainingSet;
results = zeros(0,6);


kfold = 10;

for i=1:kfold,
    
data=data(randsample(1:length(data),length(data)),:);

y = data(:,1);

x = data(:,2:end);

testPercentage = 0.15;
testCount = round(0.15*length(data));
trainCount = length(data)- testCount;

yTrain = (y(1:trainCount,:)+1);
yTest = (y(trainCount+1:end,:)+1);

xTrain = x(1:trainCount,:);
xTest = x(trainCount+1:end,:);

[B,dev,stats] = mnrfit(xTrain,yTrain);

[TestPredict,testLow,testHi] = mnrval(B,xTest,stats);

[TrainPredict,trainLow,trainHi] = mnrval(B,xTrain,stats);

RMSETrain = (sum(((yTrain-1)-(TrainPredict(:,2))).^2)/trainCount)^(1/2)

RMSETest = (sum(((yTest-1)-(TestPredict(:,2))).^2)/testCount)^(1/2)

[X,Y,T,AUC,OPTROCPT,SUBY,SUBYNAMES] = perfcurve((yTest-1),TestPredict(:,2),1);

thresh = OPTROCPT(1);

[c ind1] = min(abs(X-thresh));

threshFinal = T(ind1)+0.2;

TestPredictCat =TestPredict(:,2);

for i=1:length(TestPredict),
    
    if TestPredict(i,2)>threshFinal;
        % 0.7011
        TestPredictCat(i) = 1;
    else
        TestPredictCat(i) = 0;
    end
end

RMSETestCat = (sum(((yTest-1)-(TestPredictCat)).^2)/testCount)^(1/2);

results = [results; AUC threshFinal RMSETestCat B(1) B(2) B(3)]

end
