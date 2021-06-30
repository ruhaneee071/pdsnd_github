import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv' }
MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
WEEK_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = ''
    CITY_DATA_key = CITY_DATA.keys()
    city_list = list(CITY_DATA_key)
    while city not in CITY_DATA.keys():
        print("\nWelcome to Bike Share Data Analysis. Please choose city from the list below:")
        print(city_list)
        city = input().lower()
        #converting user input to lower case
        if city not in CITY_DATA.keys():
            print("\nSorry! Currently no data available for this city. Please select city from the above city list")
        print("\nLets begin to analyze data for {}".format(city))

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in MONTH_DATA:
        print("\nSelect any month from the list or select all to select all the months")
        print(MONTH_DATA)
		#converting user input to lower case
        month = input().lower()
        
        
        if month not in MONTH_DATA:
            print("\nSorry! Currently no data available for this month. Please select month from the above month list")
    print("\nLets begin to analyze data for {}".format(month))


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in WEEK_DATA:
        print(WEEK_DATA)
        print("\nSelect any day from the list or select all to select all the days")
		#converting user input to lower case
        day = input().lower()
        if day not in WEEK_DATA:
            print('\nSorry! Please check the spelling and select day or all from the above day list')
    print('\nLets begin to analyze data for {}'.format(day))
    print('\nYou have selected Bike Share Data analysis for the CITY: {}, MONTH(s): {}, DAY(s): {}'.format(city.upper(),month.upper(),day.upper()))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load city data into panda dataframe
    df = pd.read_csv(CITY_DATA[city]) 


    # convert 'Start Time' & 'End Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extract months and days of week information from 'Start Time' column and create month column and day column
    df['month'] = df['Start Time'].dt.month
    df['day_of_the_week'] = df['Start Time'].dt.dayofweek

    # Apply month filter(if applicable)
    if month != 'all':
        # Define a list for months 'month_list' to use the corresponding index
        month_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month = month_list.index(month) + 1
        # create new dataframe for the month input by the user
        df = df[df['month'] == month]

    # Apply day filter (if applicable)
    if day != 'all':
        # Define a list for days 'days_list' to use the corresponding index
        days_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday', 'sunday']
        day = days_list.index(day)
        df = df[df['day_of_the_week'] == day]

    # extract time from the column 'Start Time'
    df['hour'] = df['Start Time'].dt.hour

    return df

def time_stats(df, month, day, city):
    """Displays statistics on the most frequent times of travel.
       Plot probability distribution of weekly days of bike rental and
       Save the plots to files.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print('*'*40)
    start_time = time.time()
    month_list = ['january', 'february', 'march', 'april', 'may', 'june']
    days_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                  'saturday', 'sunday']

    # display the most common month
    if month != 'all':
        print('\nOnly {} is selected as input'.format(month.upper()))
    else:
        common_month = df['month'].mode()[0]
        print('\nThe most common month: {}'.format(month_list[common_month - 1].upper()))
        # display the most common day of week
    if day != 'all':
        print('\nOnly {} is selected as input'.format(day.upper()))
        
    else:
        common_day_of_the_week = df['day_of_the_week'].mode()[0]
        print('\nThe most common day of week: {}'.format(days_list[common_day_of_the_week].upper()))
    
    
    # display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print('\nThe most common start hour: {}'.format(common_start_hour))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    return



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print('*'*40)
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station: {}'.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station: {}'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    df['concatenate_start_to_end'] = df['Start Station'] + ' ' + 'to' + ' ' + df['End Station']
    frequent_start_to_end = df['concatenate_start_to_end'].mode()[0]
    count_frequent_start_to_end = df['concatenate_start_to_end'].value_counts().max()
    print('\nThe most frequent combination of start station and end station trip: {} and number of time this combination used: {}'.format(frequent_start_to_end,count_frequent_start_to_end))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    print('*'*40)
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    minutes, seconds = divmod(total_travel_time, 60)
    hours, minutes = divmod(minutes,60)
    print('\nTotal travel time {} hr(s) {} min(s) {} sec(s)'.format(hours,minutes,seconds))

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())

    # display the mean travel time in minutes and seconds
    avg_minutes, avg_seconds = divmod(mean_travel_time, 60)
    if minutes > 60:
        avg_hours, avg_minutes = divmod(avg_minutes, 60)
        print("\nThe mean travel time: {} hr(s) {} min(s) {} sec(s)".format(avg_hours,avg_minutes,avg_seconds))
    else:
        print("\nThe mean travel time: {} min(s) {} sec(s)".format(avg_minutes,avg_seconds))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    print('*'*40)
    start_time = time.time()

    # Display counts of user types
    user_types_counts= df['User Type'].value_counts()
    print('\nThe counts of user types are: {}\n'.format(user_types_counts))

    # Display counts of gender. This code will check if 'Gender' column is present in the csv file.
    try:
        gender_counts = df['Gender'].value_counts()
        print('\nThe counts of each gender are: {}\n'.format(gender_counts))
    except:
        print("\nThere is no 'Gender' specific data for this city.\n")

    # Display earliest, most recent, and most common year of birth. This code will check if 'Birth Year' column is present in the csv file.
    try:
        earliest_birth_year= int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest birth year of the bike user is : {}\n\nThe most recent year of birth of the bike user is: {}\n\nThe most common year of birth of the bike user is: {}".format(earliest_birth_year,recent_birth_year,common_birth_year))
    except:
        print("\nThere is no 'Birth Year' specific data for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def display_csv_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you want to work with.
    Returns:
        None.
    """
    USER_RESPONSE_LIST = ['yes', 'no']
    row_data = ''
    index = 0
    while row_data not in USER_RESPONSE_LIST:
        print("\nDo you want to view the raw data?")
        print("\nAccepted responses:\nYes or No")
        row_data = input().lower()
        #the raw data from the df is displayed if user opts for it
        if row_data == "yes":
            print(df.head())
        elif row_data not in USER_RESPONSE_LIST:
            print("\nPlease select your input as \nYes or No.")
            print("\nRestarting...\n")

    #Additional while loop if the user want to continue viewing data
    while row_data == 'yes':
        print("Do you want to view more raw data?")
        print("\nAccepted responses:\nYes or No")
        index += 5
        row_data = input().lower()
        # This displays next 5 rows of data
        if row_data == "yes":
             print(df[index:index+5])
        elif row_data != "yes":
             break

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day, city)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_csv_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

