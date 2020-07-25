import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
              

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    #Allows users to run multiple queries
    city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
    while city not in {'chicago', 'new york city', 'washington'}:
        city = input('We don\'t have data on that city. Please choose from Chicago, New York City, or Washington.\n').lower()
    print('Let\'s explore data from {}!'.format(city))

    # TO DO: get user input for month (all, january, february, ... , june)

    month = input('Which month would you like data for? January, February, March, April, May, June, or all?\n').lower()
    while month not in {'january', 'february', 'march', 'april', 'may', 'june', 'all'}:
        month = input('We don\'t have data from that month. Please select one of the following months: January, February, March, April, May, June, or all.\n').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('Which day of the week would you like? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?\n').lower()
    while day not in {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'}:
        day = input('That is an invalid day. Please select from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all.\n').lower()
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
    filename = CITY_DATA[city]
    # load data file into a dataframe
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = DAYS.index(day)
        df = df[df['day_of_week'] == day]

    return df

def convert_24hr_to_12hr(hour_24hr):
    """Converts 24 hour time to a 12 hour time"""
    hour_12hr = ''
    if hour_24hr == 0:
        hour_12hr = '12 am'
    elif hour_24hr < 12:
        hour_12hr = '{} am'.format(hour_24hr)
    elif hour_24hr == 12:
        hour_12hr = '12 pm'
    else:
        hour_12hr = '{} pm'.format(hour_24hr - 12)
    
    return hour_12hr

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month_index = df['month'].mode()[0]
    common_month_name = MONTHS[common_month_index - 1].title()
    print('\nThe Most Common Month in Query is: {}'.format(common_month_name))

    # TO DO: display the most common day of week
    common_day_index = df['day_of_week'].mode()[0]
    common_day_name = DAYS[common_day_index].title()
    print('\nThe Most Common Day of the Week in Query is: {}'.format(common_day_name))

    # TO DO: display the most common start hour
    common_start_hour_24hr = df['Start Time'].dt.hour.mode()[0]
    common_start_hour_12hr = convert_24hr_to_12hr(common_start_hour_24hr)

    print('\nThe Most Common Start Hour in Query is: {}'.format(common_start_hour_12hr))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('\nThe Most Common Start Station is: {}'.format(common_start_station))

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('\nThe Most Common End Station is: {}'.format(common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    station_combinations = df['Start Station'] + ' to ' + df['End Station']
    common_station_combination = station_combinations.mode()[0]
    print('\nThe Most Common Trip Combination is: {}'.format(common_station_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    print('* All travel times will be printed out in hh:mm:ss formating.')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    converted_total_travel_time = datetime.timedelta(seconds=int(total_travel_time))
    print('\nThe Total Travel Time is {}.'.format(converted_total_travel_time))

    # TO DO: display mean travel time
    average_travel_time = df['Trip Duration'].mean() 
    converted_average_travel_time = datetime.timedelta(seconds=int(average_travel_time))
    print('\nThe Average Travel Time is {}.'.format(converted_average_travel_time))

    median_travel_time = df['Trip Duration'].median()
    converted_median_travel_time = datetime.timedelta(seconds=int(median_travel_time))
    print('\nThe Median Travel Time is {}.'.format(converted_median_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df.groupby(['User Type'])['User Type'].count()
    print('\n{}'.format(user_type_count.to_string()))

    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender_count = df.groupby(['Gender'])['Gender'].count()
        print('\n{}'.format(gender_count.to_string()))
    else:
        print('\nNo gender data is available for your query.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        print('\nThe Earliest Birth Year is: {:.0f}'.format(earliest_birth_year))

        most_recent_birth_year = df['Birth Year'].max()
        print('\nThe Most Recent Birth Year is: {:.0f}'.format(most_recent_birth_year))

        most_common_birth_year = df['Birth Year'].mode()[0]
        print('\nThe Most Common Birth Year is: {:.0f}'.format(most_common_birth_year))
    else:
        print('\nNo birth year data is available for your query.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
