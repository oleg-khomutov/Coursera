function [C, sigma] = dataset3Params(X, y, Xval, yval)
%EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1;
sigma = 0.3;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
% =========================================================================

totalNumberOfSteps = 8;
initialValue = 0.01;
er = 1000;

step = ones(1, totalNumberOfSteps) * initialValue;

for i = 2:totalNumberOfSteps
	step(i:totalNumberOfSteps) *= 3;
end

for c_i = 1:8
	C1 = step(c_i);

	for sigma_i = 1:8
		sigma1 = step(sigma_i);
		
		model = svmTrain(X, y, C1, @(x1, x2) gaussianKernel(x1, x2, sigma1)); 
		predictions = svmPredict(model, Xval);

		if (er > mean(double(predictions != yval)))
			er = mean(double(predictions != yval))
			C = C1;
			sigma = sigma1;
		endif
	end
end

end