# Quantitative Equity Portfolio Management: An Active Approach to Portfolio Construction and Management, Second Edition

- **book_name**: 5073 Quantitative Equity Portfolio Management, Second Ed.
- **main_source**: epub
- **cross_check_source**: none
- **pdf_role**: not_needed
- **split_scope**: chapter file = chapter08

---

CHAPTER 8
Forecasting Factor Premiums and Exposures
All things appear and disappear because of the concurrence of causes and conditions. Nothing ever exists entirely alone; everything is in relation to everything else
.
—Buddha
8.1 INTRODUCTION
In the two preceding chapters we established the framework for factor models, our main quantitative equity portfolio management (QEPM) tools for assessing stock returns and risk. As we have seen, one idea underlies all factor models: The average stock return equals the product of factor premiums and factor exposures. We have shown how to build both the fundamental factor model and the economic factor model on this idea using past data and estimates based on the data. While the model is built from past data, though, it runs on future values because managers want to predict future stock returns. The predicted future average stock return equals the product of future factor premiums and future factor exposures. Put more formally, the return on stock
i
at time
T
+ 1,
r
i,T
+1
, is determined by
where
α
i
is the constant term,
β
i,T
+1
is the
K
-dimensional vector of the exposure for stock
i
at time
T
+1,
f
T
+1
is the
K
-dimensional
vector of the factor premium at time
T
+ 1, and
ϵ
i,T
+1
is the deviation of stock
i
’s return from its average.
To generalize the stock return equation here to all types of factor models, we have added a time subscript to both the factor exposure and factor premium terms. Depending on the type of factor model, however, the time subscript can be dropped from one of the variables but kept for the other. In the fundamental factor model that we presented in
Chapter 6
, for example, only the factor exposure changes over time, and, given stock returns and factor exposures up to time
T
, we estimated a fixed factor premium through time
T
.
1
In
Chapter 7
, on the other hand, we saw that in the economic factor model, only the factor premium changes over time, and, given stock returns and factor premiums up to time
T
, we estimated a fixed factor exposure through
T
.
Now we must look beyond the given data to time
T
+ 1 and determine the future factor premium (
f
T
+1
) and the future factor exposure (
β
i,T
+1
), together with the constant term (
α
i
) from the information available at time
T
. In order to do this, we sometimes need to forecast. The term
forecast
takes on a very specific meaning in this chapter. Assuming that a variable follows a normal distribution, forecasting the variable means specifying the variable’s distribution (a.k.a.
predictive distribution
) by finding the distribution mean and variance. Once we have found—whether by forecasting or otherwise—the future values of the factor premium and factor exposure, we can forecast future stock returns. Predicting future stock returns, after all, is our goal; if we can predict returns, we can build a high-return portfolio.
8.2 WHEN IS FORECASTING NECESSARY?
To predict future stock returns, we need future values of the factor premium and factor exposure. In some cases we need to forecast these values; in other cases we can skip the forecasting step. Whether we need to forecast depends largely on the type of factor model we are using.
In fact, if we are using the simple version of the fundamental factor model from
Chapter 6
, we do not need to forecast anything. We do not need to forecast the explanatory variable, the factor exposure. The fundamental factor model is dynamic in the sense that the explanatory variable is realized before the dependent variable. The explanatory variable (factor exposure
β
it
) is measured at the beginning of time
t
, whereas the dependent variable (stock return
r
it
) is measured during time
t
. Thus, at the end of time
T
, we actually have the value of the factor exposure for time
T
+ 1, so we do not need to forecast
β
i,T
+1
to predict the dependent variable for time
T
+ 1, namely,
r
i,T
+1
.
We do not need to forecast the factor premium either. For any type of factor model, it is conventional to assume that the model estimates will remain constant for a while. Thus, in the fundamental factor model, we can assume that the factor premium
f
estimated from time periods 1, …,
T
will be valid for time
T
+ 1. This assumption follows logically from the way we estimated the factor premium from time 1 to time
T
; since we assumed that the parameters stay constant from time 1 to time
T
, we can assume that these parameters stay constant for one more period, time
T
+ 1.
Forecasting becomes a necessary step when we are using the economic factor model from
Chapter 7
. The economic factor model is not dynamic, so we need to forecast the value of the explanatory variable, the factor premium. In the economic factor model, the explanatory variable (factor premium
f
t
) is known only at the end of time
t
, as is the dependent variable (stock return
r
i
t
). Thus, at the end of time
T
, we do not have the value of the factor premium for time
T
+ 1, and we cannot predict the return for time
T
+ 1, namely,
r
i,T
+1
, without forecasting
f
T
+1
.
However, since we can always assume that the estimates in a model remain fairly constant, we can avoid forecasting the factor exposure. The factor exposure
estimated from time periods 1, …,
T
still should be valid for time
T
+ 1.
The principal point is that, regardless of the factor model selected, there is no need to forecast the factor exposure. However,
depending on the factor model selected, one may need to forecast the factor premium.
8.3 COMBINING EXTERNAL FORECASTS
When reliable external forecasts are available, the portfolio manager should use them rather than attempt to do forecasts in-house. Factor premium forecasts can be obtained from economists who publish their forecasts, from various economic forecasting agencies, and from research analysts at various firms. This section discusses the way to combine multiple external forecasts.
Suppose that we obtained the predicted value of the factor premium
f
T
+1
from
J
different forecasters. We denote these predicted values by
Assuming that each forecaster is equally reliable, the best prediction of
f
T
+1
is the simple average of the
J
predictions.
2
This average prediction is our expected value of
f
T
+1
; thus we may write
Not only should a portfolio manager care about the expected value of the factor premium from the various forecasts, but he or she also should care about how reliable it is and how much confidence he or she can place in it. If the
J
forecasters more or less agree, we can be more confident about a prediction than we would be if their predictions were widely divergent. One way to measure the confidence of the combined forecast, therefore, is to measure the inverse of the variance of the
J
predictions. The variance of
f
T
+1
is given by
and the inverse of this variance can be used as a measure of our confidence. Thus, if the variance of the predictions is large, we have little confidence, and if it is small, we have more confidence. If we assume that
f
T
+1
has a normal distribution, the mean and the variance of
f
T
+1
given above completely specify the distribution of
f
T
+1
, and our task of forecasting the factor premium is done.
8.4 MODEL-BASED FORECAST
Forecasting is not usually a portfolio manager’s forte. It is a challenging task even for highly quantitatively oriented portfolio managers, and, in any case, it is not the best use of their time. However, there may be an in-house model that seems to forecast a particular factor very well. In this case, the portfolio could benefit from time spent on forecasting. Let us consider a simple example of a model that could be used to forecast the factor premium for an economic factor model that includes a market factor:
where
is the next month’s return on the Standard and Poor’s (S&P) 500, and
LI
t
is the value of a leading economic indicator. The leading economic indicator can be the actual leading indicator published by the Bureau of Economic Analysis or one component of it, such as average workweek, initial unemployment claims, new orders for consumer goods, plant and equipment orders, sensitive material prices, changes in consumer confidence, changes in gross domestic product (GDP), and so on. Testing whether or not the model can serve as the basis for a forecast is simple. One first estimates the historical relationship that the model describes. If it turns out the estimate for
b
is significant, then the model can be used to forecast the market factor in the economic factor model. If the economic factor model contains factors besides the market factor, similar regressions can be run to forecast the values of the other factors. Given a leading economic indicator for month
T
, the return and estimated variance determined from the preceding model can be used to forecast the factor premium for time
T
+ 1.
8.5 ECONOMETRIC FORECAST
A portfolio manager might not find external factor premium forecasts satisfactory either because he or she does not believe the forecasters are reliable or because he or she simply cannot find outside forecasts for the particular factors in his or her model. At the same time, there may be no satisfactory in-house forecasting model. In this situation, the manager might consider using some basic econometric
or statistical forecasting techniques.
3
We have chosen to focus on the most basic technique, called
vector autoregression
(VAR).
4
Although the VAR procedure is rather mechanical, it has been shown to work well at predicting out of sample in many contexts.
In VAR, we model the factor premiums as a vector autoregressive process. That is, the current factor premiums are a linear function of past factor premiums, that is,
Each of
γ
1
, …,
γ
L
is a
K
×
K
matrix of coefficients, where
K
is the number of factors (the size of vector
f
t
).
L
is the number of past factor premiums relevant for the current factor premium. This model is sometimes denoted as VAR(
L
) because there are
L
lags included on the right-hand side.
Given this modeling strategy, the only thing to decide is the number of lags
L
—in other words, how many past values should enter the equation.
5
Including many past values reduces the potential for misspecification.
6
At the same time, including many past values substantially increases the number of parameters to be estimated. The number of lags therefore should be decided based on the amount of available data. Note that given
K
factors and
L
lags, the number of parameters to be estimated is (
KL
+ 1) ×
K
because
γ
0
has
K
elements and all other
γ
’s have
K
2
elements. For three factors, the number of parameters to be estimated would be 12, 21, and 30 for
L
= 1, 2, 3. For four factors, the number of parameters to be estimated would be 20, 36, and 52. Note also that the number of observations available for estimation declines as the lag size grows. In practical situations, it is not very common to include more than one lagged value. For example, if there are 60 observations,
estimating even 12 or 20 parameters is already challenging because the precision of the estimates will be quite low.
By running regressions, we obtain the estimates
We also obtain the variance-covariance matrix estimates of
ω
. We will call this estimate
Then the predicted factor premium (i.e., the expected factor premium) for
T
+ 1 is
The estimated variance of the factor premiums for
T
+ 1 is
This completes our task of forecasting factor premiums.
Table 8.1
presents the estimates of VAR(1) for five factor premiums: the premiums of the unemployment rate, consumer sentiment growth, excess market return, the log of market capitalization, and book-to-price ratio. To estimate this model, we used five years of monthly data from January 2016 to December 2020. A VAR(1) means that we chose a lag length of 1; thus
L
is 1, and
T
is 59 (= 60 − 1). Each column in the table represents an equation
for one factor. Since there are five factors, there are five equations. The first row corresponds to
γ
0
, and each row from the second to the sixth row corresponds to each column in
γ
1
.
TABLE 8.1
Estimates of the VAR Factor Forecasting Equation
The premium for the unemployment factor is the U.S. unemployment rate of the previous month in percentage terms. The premium for the consumer sentiment growth factor is the percentage change in the University of Michigan Consumer Sentiment Index from the previous month. The premium for the excess market factor is the S&P 500 total return in excess of the one-month Treasury bill return. The premiums for the log of market capitalization factor and the book-to-price factor are calculated by constructing zero-investment portfolios of those factors (see
Chapter 7
for more details).
Given the estimates in
Table 8.1
, we can easily calculate the expected value of the factor premium for January 2020, which is time
T
+ 1. Using
Eq. (8.6)
, we obtained the expected value reported in
Table 8.2
.
Table 8.3
reports the estimate of the variance-covariance matrix
Σ
ω
. Since
Σ
ω
is a symmetric matrix, we report
only the lower triangular part of the matrix. For example, the unemployment rate variance is 1.072, which is roughly equal to (1.035)
2
. Thus the standard deviation of the unemployment factor is 1.035% per month.
TABLE 8.2
Predicted Value of Factor Premium from VAR
TABLE 8.3
Variance–Covariance of Factor Premium Forecasts from VAR
8.6 PARAMETER UNCERTAINTY
The variance of the factor premiums calculated in the preceding section reflects the uncertainty of the future factor premiums. This uncertainty, like the uncertainty of stock returns themselves, is a component of investment risk and must be recognized as such. Even by recognizing the variance-related risk, though, we still have not fully acknowledged the risk inherent in forecasting until we consider parameter uncertainty. The variance computed above shows the part of the variation in the future factor premiums that cannot be explained by the model. This would be all that mattered if the model were exact and the parameters we estimated
were exact, but the parameters we estimated are not exact. All we can say is that the true value of
γ
0
, …,
γ
L
is likely to be near what we have estimated with the VAR, and our confidence in the estimates is included in the standard error of the estimation. If the standard error of the estimation is large, there is more uncertainty regarding the future factor premiums, and, as a result, the investment risk is higher. To fully account for the parameter uncertainty in the computation of investment risk, we need to include the standard error of
γ
0
, …,
γ
L
in the calculation of the variance of the future factor premiums. We will examine two approaches to do this. One is an exact method, and the other is an approximate method.
In the exact method, we recognize that the future factor premium has two sources of variation, one coming from the estimation of
γ
0
, …,
γ
L
and the other coming from the variation allowed in the model. The first component goes in a
K
(
L
+1) ×
K
(
L
+1)-dimensional variance-covariance matrix
, and the second component goes in a
K
×
K
-dimensional variance-covariance matrix
. Once we arrive at the VAR estimator, we can compute both these components in a straightforward way. The correct variance of the future factor premium is
where
d
is a constant computed from
f
T
, …,
f
T–L
(see Appendix 8A).
7
Table 8.4
is a recalculation of the variance-covariance matrix of
f
T
+1
reported in
Table 8.3
. Note that each diagonal element of
Table 8.4
is greater than the corresponding figure in
Table 8.3
. This shows that as we account for parameter uncertainty, our ignorance (measured by the variance) increases.
TABLE 8.4
Variance–Covariance of Factor Premium Forecasts, Parameter Uncertainty Considered
If the complexity of the setup increases and the number of parameters increases, this approach may no longer be feasible. The alternative method is known as
bootstrapping
. Given the sample of
T
observations, we can create
T
pseudosamples of
T
– 1 observations by dropping one observation at a time. From each pseudosample, we estimate
γ
0
, …,
γ
L
and
Σ
ω
and obtain
T
sets of estimates. From each set of estimates, we calculate the predicted value of the future factor premiums and obtain
T
sets of future factor premiums. These
T
sets of future factor premiums can be treated as if each were obtained from an independent forecaster (as we discussed at the beginning of this section). That is, the variance of the
T
sets of future factor premiums includes parameter uncertainty, as well as the variance of the model error.
8
8.7 FORECASTING THE STOCK RETURN
Up to this point we have discussed ways to forecast the distribution of the factor premium for time
T
+ 1, namely,
f
T
+1
. As we mentioned earlier, the factor exposure for time
T
+ 1,
β
i,T
+1
, is either observable (in the case of the fundamental factor model) or is assumed to be the same as the factor exposure that was estimated from the data through time
T
(in the case of the economic factor model). Given our forecasts for
f
T
+1
and
β
i,T
+1
, we can now proceed to the forecasting of the stock return. Assuming a normal distribution as usual, the distribution of the stock return is specified by estimating the mean and variance. From the relationship
the mean and variance of the stock return are
We have the estimates for
E
(
f
T
+1
) and
V
(
f
T
+1
) from the previous sections, and we know the value (or the estimate) of
α
i
β
i,T
+1
.
V
(
ϵ
i,T
+1
) was estimated in previous chapters. Thus we simply may substitute the estimates for each component and obtain the estimates for the mean and variance of the stock return, that is,
If we estimate
α
i
+
β
i,T
+1
, this expression does not account for the uncertainty regarding the true value of
α
i
and
β
i,T
+1
. We have to add the estimation error generated in the estimation of
α
i
and
β
i,T
+1
to the preceding formula. Note that the estimation error associated with
β
i,T
+1
is captured by the variance–covariance matrix
as presented in the preceding chapter. Similarly, the estimation error associated with
α
i
is represented by the variance
. The only remaining question is how these terms enter into the preceding equation.
9
Table 8.5
reports the mean and standard deviation estimates of selected stock returns for January 2021, based on the economic factor model of
Chapter 7
. The last column in the table shows the standard deviation estimate considering parameter uncertainty.
Consideration of parameter uncertainty increases the standard deviation estimate, hence the increase between the third and the last columns.
TABLE 8.5
Predictive Return Distribution for Selected Stocks
Once we have estimates of the mean and variance of the stock returns, we can plot the whole distribution of the stock return.
Figure 8.1
shows the predictive distribution of the return to ExxonMobil’s stock. The figure is based on the variance estimate,
not accounting for parameter uncertainty. The height of each bar corresponds to the probability of a particular stock return. For example, there is about an 4.5% chance that the stock return in January 2021 will be around 0% and approximately a 1% chance that the stock return will be around 10%.
FIGURE 8.1
Predictive return for Walmart stock (January 2021). (Based on the data from January 2016 to December 2020.)
8.8 CONCLUSION
We have arrived at the point at which we can set up and run a factor model to generate predictions of stock returns and risk. In
Chapters 6
and
7
we had formulated fundamental and economic factor models from past data on stock returns, factor premiums, and factor exposures. In this chapter we showed how the models relate future stock returns to future values of the factor exposure and factor premium. In the case of the simple fundamental factor model, we did not have to worry about forecasting the factor exposure or factor premium because the model uses the existing values of both variables. In the case of the economic factor model, we also could use the existing factor exposure estimate, but we needed a forecast of the future factor premiums. Although we recommend that portfolio managers use outside forecasts whenever possible, we realize that in some cases they want to do forecasts in-house. For this reason, we went through the steps of different forecasting methods and also discussed the need to consider the parameter uncertainty of forecasts. Finally, and most importantly, we showed how to forecast the future returns and risks of stocks regardless of the type of factor model used. Forecasting a stock’s return and risk is always the last step of modeling. The goal of this process, after all, is to predict risk-adjusted returns in order to decide which stocks to include in the portfolio. There may be no crystal ball to gaze into for a picture of future stock movements, but a good model may be the closest thing to it. Once we know what a stock might yield and know that we want to include it in the portfolio, we can then decide exactly how much of the portfolio to dedicate to it. Portfolio weighting means building the portfolio, and we start building in the next chapter.
QUESTIONS
8.1.
Whether to forecast a factor exposure depends on whether the exposure is likely to change in the near future. Discuss, for each of the following factors, whether the exposure is likely to change in 1 month: size, price-to-earnings (P/E) ratio, dividend yield, and return on equity (ROE).
8.2
Explain why forecasting factor exposures is not necessary in a fundamental factor model if the model is in dynamic form, that is,
r
i,t
+1
=
α
+
β
i,
t
f
t
+
ϵ
i,
t
+1
8.3.
Consider an economic factor model:
r
it
=
α
i
+
β
i
1
f
1
t
+ … +
β
i
K
f
Kt
+
ϵ
it
Suppose that we estimated this model using time-series data (
r
i
1
,
f
11
, …,
f
K
1
), …, (
r
iT
, f
1
T
, …,
f
KT
) and obtained the estimates
. Using this model, we would like to predict the future stock return
r
i,T
+1
, especially its expected value.
(a)   Instead of forecasting
f
1,
T
+1
, …,
f
K,T
+1
as discussed in the chapter, if we use the last value of the factor premium
f
1,
T
, …,
f
K,T
, what would be the expected value of
r
i,T
+1
?
(b)   Instead of forecasting
f
1,
T
+1
, …,
f
K,T
+1
as discussed in the chapter, if we use the sample average of the factor premium
, what would be the predicted value of
r
i,T
+1
?
(c)   Explain why forecasting factor premiums is necessary in the economic factor model.
8.4.
Suppose that a portfolio manager obtained GDP forecasts
x
1
, …,
x
10
from 10 independent forecasters.
(a)   What would be the expected GDP of the portfolio manager?
(b)   If it turns out that the tenth forecaster simply averaged the forecasts of the other nine forecasters, what would be the expected GDP of the portfolio manager?
(c)   Suppose that the tenth forecaster made her own forecast
, but instead of reporting her own forecast, she used the formula:
and reported
x
10
. What would be the expected GDP of the portfolio manager?
(d)   Discuss why it is important to obtain independent forecasts.
8.5.
What are the strengths and the weaknesses of model-based forecasts compared with econometric forecasts?
8.6.
Suppose that the unemployment rate is forecast with the econometric forecasting technique.
(a)   Is it reasonable to assume a normal distribution for the error?
(b)   Explain how one may obtain a more normal looking distribution by transforming the variable.
8.7.
After estimating an AR(1) model for a factor premium, we obtained the following estimates:
where
η
t
is an error, and
N
(
·
) indicates a normal distribution.
(a)   If
f
T
= 1.1, what would be the predicted distribution of
f
T
+1
?
(b)   If
f
T
= 1.1, what would be the predicted distribution of
f
T
+2
?
(c)   Find the general formula for the distribution of
f
T
+
s
.
8.8.
Consider an AR(1) model of a factor premium:
Suppose that we estimate this model using
T
observations
f
1
, …,
f
T
.
(a)   Write down the estimates
and
as a function of data
f
1
, …,
f
T
.
(b)   Show that
and
are independent of
η
T
+1
, the future error.
(c)   Show that the predicted variance of
f
T
+1
is the sum of the error variance and the parameter uncertainty. Explain why it is important here to have the answer to part (b).
8.9.
Describe the strengths and weaknesses of the vector autoregression (VAR) technique.
8.10.
In a VAR model, the number of parameters grows very fast as the number of variables
K
or the number of lags
L
increases.
(a)    If there are five factors and we want to estimate a VAR(2) for these factors, how many parameters do we need to estimate?
(b)    If we have 50 observations, what would be the degrees of freedom?
(c)    What is the practical implication of having negative degrees of freedom?
8.11.
What is parameter uncertainty? Why is it important in QEPM? Explain how the parameter uncertainty can be accounted for in QEPM.
8.12.
Consider an economic factor model of the stock return:
We estimate this model using
T
observations (
r
i
1
,
f
1
), …, (
r
iT
, f
T
). Using the same data, we also estimate an AR(1) model of the factor premium:
(a)    Express
in terms of data and errors.
(b)    Express
in terms of data and error.
(c)    Are
and
independent of each other conditional on the data? What would happen if they were not independent?
8.13.
Consider two random variables
A
and
B
whose joint distribution is multivariate standard normal. That is, each variable has a standard normal distribution and is independent of the other variable.
(a)    Is the distribution of the product
AB
still normal?
(b)    Explain why the predictive distribution of the stock return may not be normal when considering parameter uncertainty if the factor premium has to be forecasted.
8.14.
Consider an economic factor model:
where the factor premium is an AR(1) process:
(a)    Show that the stock return is serially correlated as long as
δ
≠ 0.
(b)    Specify the condition under which we may observe momentum profit (i.e., positive serial correlation in the stock return) and contrarian profit (i.e., negative serial correlation in the stock return).
8.15.
The bootstrap standard error is often calculated when calculating the exact standard error is too complicated. Let
x
t
be the data observed in time
t
. The sample is a collection of observations made at different times. Suppose that our sample is made of observations from
t
= 1 to
t
=
T
, that is, (
x
1
, …,
x
T
). Given the sample of size
T
, we may create
T
subsets of the sample, where each subset has
T
– 1 elements. If we index the subsets by
j
, then subset
j
is a set of all observations except
x
j
. We may carry out the estimation using each subset and call the resulting estimate
θ
(
j
)
. The bootstrap standard error is defined as the sample standard deviation of
θ
(1)
, …,
θ
(T)
.
(a)    Explain the relationship between the bootstrap standard error and the regular standard error.
(b)    Under what situation would one prefer the bootstrap standard error to the regular standard error?
(c)    What modifications are necessary in order to calculate the bootstrap standard error in a VAR model?
1
In
Chapter 6
, we presented two types of fundamental factors models. One, which we call the simple one, takes the factor exposures of stocks over time along with the stock returns over time and estimates a factor premium over the historical sample period. In this case, there is only one factor premium estimated from the data and one estimate of the factor premium at time
T
+ 1, which is simply the historical estimate up to time
T
. However, in the last part of
Chapter 6
, and also in
Chapter 16
, we estimate the fundamental factor model as a series of cross-sectional regressions. That is, for each period or month in our historical data, we use stock returns and factor exposures of stocks to estimate a different factor premium in each period or month. We thus have a series of factor premiums for each time period. In this case, if we choose, we can use a VAR to forecast the period
T
+ 1 factor premiums based on the time series of factor premiums through time
T
. Thus, in the more “complicated” fundamental factor model, both factor premiums and factor exposures change through time. Finally, as a reminder, when we say a fixed factor premium is estimated, we are referring to {
f
1
, … ,
f
T
}, and when we say a fixed factor exposure is estimated, we are referring to {
β
i
,1
, … ,
β
i,T
}.
2
For combining forecasts from forecasters of differing abilities, we refer the reader to
Chapter 9
of Granger and Newbold (1986).
3
There are many sophisticated econometric techniques to forecast factor premiums. The reader should be warned, though, that more sophisticated models do not necessarily produce better forecasts. Sophisticated models come with an extra set of assumptions, which may or may not apply well to a particular factor model. Unless there is a strong reason for an econometric model, we suggest sticking with a simpler forecasting technique.
4
Most standard statistical packages can perform VAR estimations and forecasts.
5
Several selection criteria can be used to determine the number of lags. The two most common are the Akaike information criterion (AIC) and the Schwarz Bayesian information criterion (SIC/BIC/SBIC). Please consult an econometrics textbook on how to use these tools.
6
Omitting relevant variables creates a problem, whereas including irrelevant variables does not. See Appendix C at
www.ludwigbc.com
under QEPM Exclusive Content for more details on this matter.
7
Appendix 8A can be found at
www.ludwigbc.com
under QEPM Exclusive Content.
8
When an observation is dropped in the creation of the pseudosample, the order of the remaining
T
– 1 observations should not change. The time distance among observations should not change either. This reduces the effective sample size by more than one. For example, if
f
2
is dropped, we have to ignore not only
f
2
=
γ
0
+
γ
1
f
1
+
ω
2
but also
f
3
=
γ
0
+
γ
1
f
2
+
ω
3
. Thus the effective sample size is reduced by 2. See Appendix 8A at
www.ludwigbc.com
under QEPM Exclusive Content for a general discussion of bootstrapping.
9
We provide the exact formula in Appendix 8A, which can be found at
www.ludwigbc.com
under QEPM Exclusive Content.
