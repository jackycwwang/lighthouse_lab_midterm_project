## Project Description
No one enjoys flight delays. They're costly for airlines, and negative for passengers who need to get to their destination on time, without missing any connecting flights.  If we had the ability to predict delays, airlines could put plans in place to potentially save money - by no longer needing to reimburse passengers for meals and lodging, and prevent having to pay hefty airport penalties for not leaving the gate on time.  As delays beget more delays, planning to mitigate potential ones could save from having a cascading delay effect.  Airline staff could have greater job satisfaction without having to take the brunt of irate passenger complaints, having a two-fold effect on customer retention.

The goal of this project is to predict US domestic flight delays, for the first week of January 2020, from one week in advance.

### Data Analysis
Through our research, we found that there are 4 main factors that contribute to flight delays. In order of impact:
1. Late aircraft delay from previous flights
2. Airline delays (flight crew late, mechanical planes, bagage removal)
3. Airspace delays
4. Weather

Using this information, as well as using analysis of the given test data sets, we selected features to include.

##### Delays from previous flights
* More delays happen in the afternoon than morning as more flight legs have been accumulated as the day goes on, so we have included the hour of the day for scheduled flight departure and scheduled flight arrival.
* Included historic averages of delays of late aircraft per airport
* Distance and log of scheduled elapsed time as the distribution was skewed - longer flights could potentially indicate less prior flights, and also, longer flights have more chance to make up time in the air.

##### Airline delays
* These can be baggage delays, having aircrew time out, and other factors so we've included the 9 major airlines.
* Included the median delays for flight numbers (routes) for any route that had more than 30 records in the dataset/

##### Airspace delays 
* We looked at the busyness (number of flights) of the airports, city and state and included the top ones
* Included historic NAS delay per airport

##### Weather 
* Instead of bringing the actual historic weather data into our model, we chose to select a sample dataset that would closely represent the seasonal impact on flights from when we would test - being the first week of January and five days on either side.
* We also included the average weather delay metric per airport.

Other Features included
* Top 20 airports in terms of number of flights they see
* Top 10 cities and states in terms of number of flights they see 
* Median delays for flight numbers (routes) that occurred greater than 30 times in our sample data set.

### Feature Engineering and Feature Reduction

We used the linear regression model performance as an assessment metric for our feature selection process. We started by striping our training data to line up with the formatting of the data we received to test. From there we formatted the columns by initially binning some continuous features, to simplify the noise, like flight times and label encoding some features like airport, city and state by busyness, but then after talking with some mentors, we one-hot encoded all categorical variables, and binned, and encoded some continuous ones.  The remaining numerical features were scaled with a standard scaler that seemed to perform slightly better than the max/min scaler.  If the feature was skewed, and positive, we took the log to more centrally model the feature. 
 
We added feature by feature to the train set, and tested the linear regression with r-squared (r2), mean absolute error (MAE) and mean squared error(MSE) metrics.  The linear regression peaked out at about 0.08 for r2, but the MAE was lowest - around 3, when we sent all early flights (negative delays) to zero - as we only are concerned with delays.  Unfortunately the r2 also decreased, so we did not use this feature.  

The maximum number of features we had was 171. To reduce features, we did:

* **Forward filtering** when adding new features
* **RFE** was done to select 50 features, and this only told us that we need more features than 50, but was too time consuming to repeat for our project time frame.
* **Linear Discriminant Analysis** was done by creating a categorical target variable from a continuous one by binning the arrival delay time. Two components that explained the most variance were compared and features like the bins for the non-high-traffic airports, city and state were removed.  

This whole process was iterative. If we found our models weren’t performing well, after tuning hyperperameters, we would try new features to add like days of the week, average delay metrics for locations and flight routes. Then see if it improved the linear regression model, and then re-tuned the hyperperameters with grid search and cross validation for the more complex models.


### Modelling

### Machine Learning algorithms
Since we are predicting arrival delays in minutes, a continuous variable, this is a regression problem, we chose three additional more complex regression models to train after using Linear regression to baseline the model in order to better represent the complexities and improve the performance.

#### Linear Regression 
* Best performance was found with the last modifications to the training data: r2: 0.078, MSE: 271.24, MAE: 12.83

#### SVM
* This was a beast of a model and took several tries running it on google colab to have it not time out while a grid search to tune hyperparameters.
* Still waiting for results.

#### XGBoost
* The best performing model of the four chosen

#### Random Forests
* Initially performed worse than the linear regression model, but after tunning through grid search and cross validation was able to get MAE: 12.65 and r2 0.10

### Limitations
* This project has been optimized for prediction of flight delays taking place in the first week of January, and has trained models on data for that time frame (first week January plus 5 days around that time, as to not include Christmas).  Using this model to predict flights during the other times of the year will likely not perform as well.  
* Only two years of data were used, had we included additional years, we may have been able to increase the performance.
* As we were only concerned with delayed flights, any flights that did not arrive (cancelled/ diverted) were removed from the training set.  These models will not be able to predict cancelled flights.

### If we had more time, we would:
* Use greater granularity in the grid searches for the various models as this would allow for more accurate predicting.
* Add a feature to indicate if the airport origin for the flight is a hub for the particular airline for that flight.  This could indicate more resources to fix delays by more easily swapping aircraft if a previous one is late, or have the resources to repair minor mechanical issues in a more timely fashion.  
* Add in weather historic weather data as it relates to flight delay.  We had pulled weather data for each day, but did not have a chance to pull for more frequent time segments. 
* Investigate aircraft types commonly used for popular flight routes (are some are more affected by weather than others?.)
* Investigate using more ensemble combinations.
* It was interesting to see that the number of passengers per airport were not directly correlated with the number of flights that airport sees in all cases.  Chicago and Newark for instance had higher passenger to flight ratio than other relatively busier airports and personal experience revealed a less pleasant experience in those airports.  If we had more time, we would include this information.

## Data Description
 
##### This is the engineered feature space for training the model
- **origin**: Origin Airport (top 20 one-hot encoded, remainder bucketed in to _0 encoded category)
- **dest**: Destination Airport (top 20 one-hot encoded, remainder bucketed in to _0 encoded category)
- **dep_hour**: Scheduled flight departure hour (minutes floored to hour) in local time - one-hot encoded
- **arr_hour**: Scheduled flight arrival hour (minutes floored to hour) in local time - one-hot encoded
- **weekday**: Numeric day of week (M=0) - on-hot encoded
- **origin_city**: Origin City (top 10 one-hot encoded, remainder bucketed in to _0 encoded category)
- **dest_city**: Origin City (top 10 one-hot encoded, remainder bucketed in to _0 encoded category)
- **fl_num_delay**: Average arrival delay to each route (consider only the flight frequency higher than 30, remainder replaced with median arr_delay)
- **log_crs_elapsed_time**: Average log scheduled elapsed time binned to 20 categories and one-hot-encoded
- **mkt_unique_carrier**: One-hot-encoded the carrier codes
- **avg_carrier_delay**: Average Carrier Delay, in Minutes
- **avg_weather_delay**: Average Weather Delay, in Minutes
- **avg_nas_delay**: Aveerage National Air System Delay, in Minutes
- **avg_security_delay**: Average Security Delay, in Minutes
- **avg_late_aircraft_delay**: Average Late Aircraft Delay, in Minutes
- **avg_dep_delay**: Average departure delay to airports, in Minutes
- **origin_airport_fl_amt**: Frequency of origin flights per airport bucketed into 7 bins
- **dest_airport_fl_amt**: Frequency of dest flights per airport bucketed into 7 bins

#### Variables:
We can find the **all** information about specific attributes in this file.
### Table **flights**
##### This is the available feature space for this project

- of the ones we used?  ie _0 in all one hot encoding is the 
##### Variables from Flights.csv
- **fl_date**: Flight Date (yyyy-mm-dd)
- **mkt_unique_carrier**: Unique Marketing Carrier Code. When the same code has been used by multiple carriers, a numeric suffix is used for earlier users, for example, PA, PA(1), PA(2). Use this field for analysis across a range of years.
- **branded_code_share**: Reporting Carrier Operated or Branded Code Share Partners
- **mkt_carrier**: Code assigned by IATA and commonly used to identify a carrier. As the same code may have been assigned to different carriers over time, the code is not always unique. For analysis, use the Unique Carrier Code.
- **mkt_carrier_fl_num**: Flight Number
- **op_unique_carrier**: Unique Scheduled Operating Carrier Code. When the same code has been used by multiple carriers, a numeric suffix is used for earlier users,for example, PA, PA(1), PA(2). Use this field for analysis across a range of years.
- **tail_num**: Tail Number
- **op_carrier_fl_num**: Flight Number
- **origin_airport_id**: Origin Airport, Airport ID. An identification number assigned by US DOT to identify a unique airport. Use this field for airport analysis across a range of years because an airport can change its airport code and airport codes can be reused.
- **origin**: Origin Airport
- **origin_city_name**: Origin Airport, City Name
- **dest_airport_id**: Destination Airport, Airport ID. An identification number assigned by US DOT to identify a unique airport. Use this field for airport analysis across a range of years because an airport can change its airport code and airport codes can be reused.
- **dest**: Destination Airport
- **dest_city_name**: Destination Airport, City Name
- **crs_dep_time**: CRS Departure Time (local time: hhmm)
- **dep_time**: Actual Departure Time (local time: hhmm)
- **dep_delay**: Difference in minutes between scheduled and actual departure time. Early departures show negative numbers.	
- **taxi_out**: Taxi Out Time, in Minutes
- **wheels_off**: Wheels Off Time (local time: hhmm)
- **wheels_on**: Wheels On Time (local time: hhmm)
- **taxi_in**: 	Taxi In Time, in Minutes
- **crs_arr_time**: CRS Arrival Time (local time: hhmm)
- **arr_time**: Actual Arrival Time (local time: hhmm)
- **arr_delay**: Difference in minutes between scheduled and actual arrival time. Early arrivals show negative numbers.
- **cancelled**: Cancelled Flight Indicator (1=Yes)
- **cancellation_code**: Specifies The Reason For Cancellation
- **diverted**: Diverted Flight Indicator (1=Yes)
- **dup**: Duplicate flag marked Y if the flight is swapped based on Form-3A data
- **crs_elapsed_time**: CRS Elapsed Time of Flight, in Minutes
- **actual_elapsed_time**: Elapsed Time of Flight, in Minutes
- **air_time**: Flight Time, in Minutes
- **flights**: Number of Flights
- **distance**: Distance between airports (miles)
- **carrier_delay**: Carrier Delay, in Minutes
- **weather_delay**: Weather Delay, in Minutes
- **nas_delay**: National Air System Delay, in Minutes
- **security_delay**: Security Delay, in Minutes
- **late_aircraft_delay**: Late Aircraft Delay, in Minutes
- **first_dep_time**: First Gate Departure Time at Origin Airport
- **total_add_gtime**: Total Ground Time Away from Gate for Gate Return or Cancelled Flight
- **longest_add_gtime**: Longest Time Away from Gate for Gate Return or Cancelled Flight


