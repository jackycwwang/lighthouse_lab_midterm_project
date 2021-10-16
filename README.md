## Project Description




## Data Description

We can find the **all** information about specific attributes in this file.


### Table **flights**

#### Variables:

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



