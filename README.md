# Sales_Forecasting
Time series analysis and forecasting project on a kaggle data set.

In this project I use state-of-the-art forecasting techniques from exponential smoothing and ARIMA models to Facebook's Prophet library in order to forecast the future sales profits of a russian company. The data set was obtained from Kaggle.com. 

The performance of the models was analysed using the RMSE between the model one step forecasts and the actual values. The best performing model was Prophet, followed by a triple exponential smoothing model. 

After finding the model the best performing model I have applied it to forecasting the future profits of the individual shops in the company. The results can be found in the sales_plots branch; they are in the form of interactive plotly HTML files. The files cannot be displayed by GitHub, therefore I have left the links for the previews of some of the files in here: 

https://htmlpreview.github.io/?https://github.com/rd2g16/Sales_Forecasting/blob/master/sales_plots/shop5_sales.html
https://htmlpreview.github.io/?https://github.com/rd2g16/Sales_Forecasting/blob/master/sales_plots/shop10_sales.html
https://htmlpreview.github.io/?https://github.com/rd2g16/Sales_Forecasting/blob/master/sales_plots/shop26_sales.html
https://htmlpreview.github.io/?https://github.com/rd2g16/Sales_Forecasting/blob/master/sales_plots/shop49_sales.html
