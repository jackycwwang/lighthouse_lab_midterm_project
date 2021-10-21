## Project Description
No one enjoys flight delays. They're costly for airlines -  having to reimburse passengers for meals, hotels, and in some cases, having to pay airport penalties.  Delays beget more delays.  Passengers' disatisfaction rub off on airline staff who take the brunt of their complaints, and can also impact customer retention.

The goal of this project is to predict flight delays US domestic flights, one week in advance during the first week of January 2020. 

### Data Analysis
There are 4 main factors that impact flight delays. In order of impact:
1. Cascading delays from previous flight(s) 
2. Airline delays (flight crew late, mechanical planes, bagage removal)
3. Airspace delays
4. Weather

Using this information, as well as using analysis of the given test data set, we selected features to include.

##### Delays from previous flights
* More delays happen in the afternoon than morning as more flight legs have been accumulated as the day goes on, so we have included the hour of the day for scheduled flight departure and scheduled flight arrival.
* Included historic averages of delays of late aircraft per airport
* Distance and scheduled time, if longer, could potentially indicate less prior flights, and also, longer flights have more chance to make up time in the air.

##### Airline delays
* These can be baggage delays, having aircrew time out, and other factors so we've included the 9 major airlines, and flight numbers in the model

##### Airspace delays 
* We looked at the busyness (number of flights) of the airports, city and state and included the top ones
* Included historic NAS delay per airport

##### Weather 
* Instead of bringing the actual historic weather data into our model, we chose to select sample dataset that would closely represent the seasonal impact on flights from when we would test - being end of December, early January.
* We also included the average weather delay metric per airport

### Feature Engineering and Feature Reduction
We used a linear regression model for our feature selection process. We started by striping our test data to line up with the formatting of the data we will recieve to test. From there we formatted the columns by initally binning some continous features like flight times and label encoding some features like airport by busyness, but then after talking mentors we one-hot encoded all categorical variables.  Numerical features were scaled with a standard scaler that seemed to perform slightly better than the max/min scaler.  
We added feature by feature and tested the linear regression with r2 and MAE metrics.  The linear regression peaked out at about 0.08 but the MAE was lowest when the r2 was lower when we shrunk all early flights (negative delays) to zero - as we only are concerned with delays. 

RFE was done for 50 features, and only told us that we need more features than 50
PCA and LDA were also performed
* For LDA the target was transformed catigorical by bining the arrival delay
* The best number of features were 134 for the set we had

Features not included
* Flight numbers - as there were too many to one-hot encode 
* Airport id 

Departure Delay - as Included avg departure delay
* Distance - we found didn't impact the arrival delays
* Days of week - we thought that weekends would have a different delay pattern, or fridays, but does not
* Flight numbers - we chose not to include this for sake of time 
* included the log of scheduled elasped time as the distribution was skewed and aircraft can sometimes make up for lost time in the air.  We binned this value and one-hot encoded it

** mention skewed ness of data logging
We binned a number of features to simplify the model 
we originally label encoded a number of features in order of magnitude ie busyness of airport, but then found out linear regression handles one-hot encoding better, so we converted most bi**

### Baseline Modelling

### Machine Learning algorithms
Since this is a regression problem, as we are predicting delays in minutes, we chose three additional more complex models to use after using Linear regression to baseline the model. 

#### SVM

#### XGBoost

#### Random Forests

### Limitations
* This project has been optimized for predicting flight delays taking place on the first week of January, and have trained models on data for that time frame (first week January plus 5 days around that time, as to not include Christmas).  Using this model to predict flights during the other times of the year will likely not perform as well.  
* Only two years of data were used, had we included additional years, we may have been able to increase the performance.
* As we were only concerned with delayed flights, any flights that did not arrive were removed from the training set.  These models will not be able to predict cancelled flights.

### If we had more time, we would:
* Use greater granularity in the grid searches for the various models as this would allow for more accurate predicting.
* Add a feature to indicate if the airport origin for the flight is a hub for the particular airline for that flight.  This could indicate more resources to fix delays by more easily swapping aircraft is a precious one is late, or have the resources to repair minor mechanical issues in a more timely fashion.  
* Add in weather historic weather data as it relates to flight delay.  We had pulled weather data for each day, but didn't pull for more frequent time segments. 
* Investigate including popular flight routes.
* Investigate aircraft type commonly used for those popular flight routes.
* Investigate using more ensemble combinations.
* It was interesting to see that number of passengers per airport were not directly correlated with the number of flights that airport sees in all cases.  Chicago and Newark for instance had higher passenger to flight ratio than other busyer airports and personal experience reveals a less pleasant experience in those airports.  If we had more time, we would include this information.

## Data Description

We can find the **all** information about specific attributes in this file.


### Table **flights**
- **origin**: Origin Airport (top 20 one-hot encoded, remainder bucketed in to _0 encoded category)
- **dest**: Destination Airport (top 20 one-hot encoded, remainder bucketed in to _0 encoded category)
- **dep_hour**: Scheduled flight departure hour (minutes floored to hour) in local time - one-hot encoded
- **arr_hour**: Scheduled flight arrival hour (minutes floored to hour) in local time - one-hot encoded
- **weekday**: Numeric day of week (M=0) - on-hot encoded
- **origin_city**: Origin City (top 10 one-hot encoded, remainder bucketed in to _0 encoded category)
- **dest_city**: Origin City (top 10 one-hot encoded, remainder bucketed in to _0 encoded category)


#### Variables:
##### Variables Used in Training Data

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



