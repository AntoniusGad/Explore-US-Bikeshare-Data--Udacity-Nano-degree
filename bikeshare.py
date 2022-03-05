import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
WEEKDAYS = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']

LINE_LEN = 100

# To print line with any need Char 
print_line = lambda char: print(char[0] * LINE_LEN)


def print_processing_time(start_time):
#a function to print the processing time 
    time_str = "[... %s seconds]" % round((time.time() - start_time), 3)
    #to make a line after the result 
    print(time_str.rjust(LINE_LEN))
    print_line('=')

def get_filter_city():
    """
    a function to Asks user to specify a city.

    Returns:
        (str) city - name of the city to analyze
    """
    # make a start screen for the program 
    cities_list = []
    num_cities = 0

    for a_city in CITY_DATA:
        cities_list.append(a_city)
        num_cities += 1
        print('        {0:18}. {1}'.format(num_cities, a_city.title()))

    # ask user to input a number for a city from the list;
    while True:
        try:
            city_num = int(input("\n    Enter a number for the city (1 - {}):  ".format(len(cities_list))))
        except:
            continue

        if city_num in range(1, len(cities_list) + 1):
            break

    city = cities_list[city_num - 1]
    return city

def get_filter_month():
    """
    Asks user to specify a month to filter on, or choose all.

    Returns:
        (str) month - name of the month to filter by, or "all" for no filter
    """
    while True:
        try:
            month = input("                         1. January\n                         2. february\n                         3. March\n                         4. April\n                         5. May\n                         6. June\n                         a. all\n  \n    Enter a character for the month (1 - 6) or a:")
        except:
            print("        ---->>  Valid input:  1 - 6, a")
            continue

        if month == 'a':
            month = 'all'
            break
        elif month in {'1', '2', '3', '4', '5', '6'}:
            # reassign the string name for the month
            month = MONTHS[int(month) - 1]
            break
        else:
            continue

    return month

def get_filter_day():
    """
    Asks user to specify a day to filter on, or choose all.

    Returns:
        (str) day - day of the week to filter by, or "all" for no filter
    """
    while True:
        try:
            day = input(
                "                         1. Saturday=1\n                         2. Sunday\n                         3. Monday\n                         4. Tuesday\n                         5. Wednesday\n                         6. Thursday\n                         7. Friday\n                         a. all\n"
                "   \n    Enter a character for the day (1 - 7) or a:")
        except:
            print("        ---->>  Valid input:  1 - 7, a")
            continue

        if day == 'a':
            day = 'all'
            break
        elif day in {'1', '2', '3', '4', '5', '6', '7'}:
            # reassign the string name for the day
            day = WEEKDAYS[int(day) - 1]  # here we MUST -1 to get correct index
            break
        else:
            continue

    return day


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Make astart screen and get user name to write a welcome message 
    print_line('=')
    name = input("\n    *What is your name Sir ?").title()
    print('\n    Hello! Mr {} Let\'s explore some US bikeshare data!*_*'.format(name))

        # TO DO: get user input for city (chicago, new york city, washington). 
        # HINT: Use a while loop to handle invalid inputs
    city = get_filter_city()
     

    # TO DO: get user input for month (all, january, february, ... , june)
    month = get_filter_month()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_filter_day()

    print_line('=')
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
    start_time = time.time()

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month  # range (1-12)
    df['day_of_week'] = df['Start Time'].dt.dayofweek  # range (0-6)
    df['hour'] = df['Start Time'].dt.hour  # range (0-23)

    init_total_rides = len(df)
    filtered_rides = init_total_rides  # initially

    # filter by month if applicable
    if month != 'all':
        # use the index of the MONTHS list to get the corresponding int
        month_i = MONTHS.index(month) + 1 
        # filter by month to create the new dataframe
        df = df[df.month == month_i]
        month = month.title()

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the WEEKDAYS list to get the corresponding int
        day_i = WEEKDAYS.index(day)  

        # filter by day of week to create the new dataframe
        df = df[df.day_of_week == day_i]
        day = day.title()

    print_processing_time(start_time)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)


    # TO DO: display the most common day of week

    popular_day = df['day_of_week'].mode()[0]
    print('Most Common day:', popular_day)



    # TO DO: display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_processing_time(start_time)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', Start_Station)


    # TO DO: display most commonly used end station

    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:', End_Station)


    # TO DO: display most frequent combination of start station and end station trip

    Combination_Station = df.groupby(['Start Station', 'End Station']).count()
    print('\nMost Commonly used combination of start station and end station trip:', Start_Station, " & ", End_Station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_processing_time(start_time)


def station_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', Total_Travel_Time/60, " Minutes")


    # TO DO: display mean travel time

    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', Mean_Travel_Time/60, " Minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_processing_time(start_time)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', Total_Travel_Time/60, " Minutes")


    # TO DO: display mean travel time

    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', Mean_Travel_Time/60, " Minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_processing_time(start_time)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    user_types = df['User Type'].value_counts()
    #print(user_types)
    print('User Types:\n', user_types)

    # TO DO: Display counts of gender

    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("\nGender Types:\nNo data available for this month.")

    # TO DO: Display earliest, most recent, and most common year of birth

    try:
      Earliest_Year = df['Birth Year'].min()
      print('\nEarliest Year:', Earliest_Year)
    except KeyError:
      print("\nEarliest Year:\nNo data available for this month.")

    try:
      Most_Recent_Year = df['Birth Year'].max()
      print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
      print("\nMost Recent Year:\nNo data available for this month.")

    try:
      Most_Common_Year = df['Birth Year'].value_counts().idxmax()
      print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
      print("\nMost Common Year:\nNo data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_processing_time(start_time)
def display_raw_data(df):
    """
    Asks if the user would like to see some lines of data from the filtered dataset.
    """
    show_rows = 5
    rows_start = 0
    rows_end = show_rows - 1  # use index values for rows

    print('\n     Would you like to see some raw data from the current dataset?')
    while True:
        raw_data = input('      (y or n):  ')
        if raw_data.lower() == 'y':
            # display show_rows number of lines, but display to user as starting from row as 1
            # e.g. if rows_start = 0 and rows_end = 4, display to user as "rows 1 to 5"
            print('\n    Displaying rows {} to {}:'.format(rows_start + 1, rows_end + 1))

            print('\n', df.iloc[rows_start: rows_end + 1])
            rows_start += show_rows
            rows_end += show_rows

            print_line('.')
            print('\n    Would you like to see the next {} rows?'.format(show_rows))
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\n    Would you like to restart? (y or n):  ')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
