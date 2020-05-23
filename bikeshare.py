import time
import pandas as pd
import numpy as np
import statistics as st

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city= input('\nWould you like to see the data for Chicago, New York City, or Washington?\n').lower()
    
    while(True):
        if (city == 'chicago' or city == 'new york city' or city == 'washington' or city == 'all'):
            break
        else:
            city=input('Please Enter Correct city name:').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('\nWhich month? January, February, March, April, May, or June?\n').lower()
    
    while(True):
        if(month=='january' or month=='february' or month=='march' or month=='april' or month=='may' or month=='june' or month=='all'):
            break
        else:
            month = input('Please Enter valid month name\n').lower()
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=input('Which day of the week or enter all  to display data of all days?\n').lower()
    
    while(True):
        if(day=='monday' or day=='tuesday' or day=='wednesday' or day=='thursday' or day=='friday' or day=='saturday' or day=='sunday' or               day=='all'):
            break
        else:
            day= input('Please enter the correct day name:').lower()
            
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    if month !='all':
        months=['january', 'february', 'march', 'april', 'may', 'june']
        monthIndex=months.index(month) + 1
        print("helloDF" + str(monthIndex) + str(month))
        df=df[df['Start Time'].dt.month == monthIndex]
    
    if day != 'all':
        df=df[df['Start Time'].dt.weekday_name == day.title()]
        
    print(df.head())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_popular_month = df['Start Time'].dt.month.mode()[0]
    print('Most Common Month:', most_popular_month)

    # display the most common day of week
    most_popular_day = df['Start Time'].dt.weekday_name.mode()[0]
    print('Most Common day of week:', most_popular_day)

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', most_popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #  display most commonly used start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', Start_Station)

    # TO DO: display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:', End_Station)

    #  display most frequent combination of start station and end station trip
    Combination_Station = df.groupby(['Start Station', 'End Station']).count()
    print('\nMost frequently used combination of start station and end station trip:', Start_Station, " & ", End_Station)
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    time_travel = total_travel_time
    day_travel = time_travel // (24 * 3600)
    time_travel = time_travel % (24 * 3600)
    hour_travel = time_travel // 3600
    time_travel %= 3600
    minutes_travel = time_travel // 60
    time_travel %= 60
    seconds_travel = time_travel
    print('\nTotal travel time is {} days {} hours {} minutes {} seconds'.format(day_travel, hour_travel, minutes_travel, seconds_travel))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    time_mean = mean_travel_time
    day_mean = time_mean // (24 * 3600)
    time_mean = time_mean % (24 * 3600)
    hour_mean = time_mean // 3600
    time_mean %= 3600
    minutes_mean = time_mean // 60
    time_mean %= 60
    seconds_mean = time_mean
    print('\nMean travel time is {} hours {} minutes {} seconds'.format(hour_mean, minutes_mean, seconds_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_of_subscribers = df['User Type'].str.count('Subscriber').sum()
    count_of_customers = df['User Type'].str.count('Customer').sum()
    print('\nNumber of users as subscribers are {}\n'.format(int(count_of_subscribers)))
    print('\nNumber of users as customers are {}\n'.format(int(count_of_customers)))

    
    # Display counts of gender
    if('Gender' in df):
        male_users = df['Gender'].str.count('Male').sum()
        female_users = df['Gender'].str.count('Female').sum()
        print('\nNumber of male users are {}\n'.format(int(male_users)))
        print('\nNumber of female users are {}\n'.format(int(female_users)))

    # Display earliest, most recent, and most common year of birth
    if('Birth Year' in df):
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_birth_year = st.mode(df['Birth Year'])
        print('\n Oldest Birth Year is {}\n Youngest Birth Year is {}\n Most popular Birth Year is {}\n'.format(int(earliest_year),                 int(most_recent_year), int(most_common_birth_year)))


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
