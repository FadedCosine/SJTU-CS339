# SJTU-CS339
For group project of Computer Network on an analysis of mobility in a campus Wireless Network.

We have established a mathematical model which is more suitable for simulating SJTU's campus network on the basis of the model discussed in the paper, and processed SJTU's data set and analyzed the statistics of SJTU's campus network.
## Details Of preprocess_SJTU_data.py

### Variables

* path1

> path of our dataset

* minDuration

> The mininum time of keeping connected for a valid connect, it is determined by the inflextion of line chart

* weekday

> a list of dates in weekdays in our dataset

* weekend

> a list of dates in weekends in our dataset

* arrival_rate

> a list of average arrival rate in each minutes in weekdays or weekends

### Functions

* count_association_time(path1, filelst)

> record all the connection in the dataset once a minute

* count_AP("AP_time_users.pk",minDuration)

> calculate the total number of APs

* draw_vaild_connect(path1, filelst)

> draw the line chart of relations between the number of valid connections and minDuration, and we use the value of minDuration in the inflextion, that is, minDuration = 10

* buildDic_users_time_AP(path1, filelst, minDuration)

> build a nested dictionary of users_time_AP, which is used to record a list of AP, to which a certain user connected in every minute

* buildDic_time_AP_users(path1, filelst, minDuration)

> buid a nested dictionary of time_AP_users, which is used to record a list of users, to which a certain AP connected in every minute

* buildDic_AP_time_users(path1, filelst, minDuration)

> build a nested dictionary of AP_time_users, which is used to record, in each minute,  a list of users, to which a certain AP connected

* arrival_rate_varyingtime("time_AP_users.pk")

> calculate the arrival_rate

* draw_arrival_rate(arrival_rate)

> draw the line chart of arrival rate, which determines the value of active hour in weekdays and weekends

* find_open_close_class("users_time_AP.pk", 2, active_hour_weekday, active_hour_weekend,  list(range(10,250,10)))

> calculate the number of users in open class or closed class, and draw the line chart of relations between the number of closed class and minDuration

* calculate_AP_arrival_rate("AP_time_users.pk", minDuration)

> calculate the average arrival rate in the active hour of weekdays or weekends, and the arrival rate is used in the modelization

* calculate_AP_residence_time(path1, filelst, minDuration)

> calculate the average resident time in active hour in weekdays or weekends

* draw_occupancy_distribution("MH-XXY-1F-102",minDuration)

> draw the occupancy distribution for a certain AP

* visualization_of_top10_AP_time("time_AP_users.pk", "SJTU_AP_Weekday.csv", "SJTU_AP_Weekend.csv", minDuration)

> record the number of users that connected to each AP, and output the top-ten APs to the csv file, which is used to make the demostration
