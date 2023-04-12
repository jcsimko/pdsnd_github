import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

DAY_OF_WEEK = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'all']
MONTH_DATA = ["jan", "feb", "mar", "apr", "may", "jun", "all"]


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
    while True:
        city = str(input('\nWhat city would you like to analyze (Chicago, New York, or Washington)?\n')).lower()
            
        if city not in CITY_DATA.keys():
            print('\nYou must select Chicago, New York, or Washington')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input('\nWhat month would you like to analyze (Jan, Feb, Mar, Apr, May, or Jun)? Type All for no month filter\n')).lower()
            
        if month not in MONTH_DATA:
            print('\nYou must enter Jan, Feb, Mar, Apr, May, Jun or All')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input('\nWhat day of week would you like to analyze (Sun, Mon, Tue, Wed, Thu, Fri, Sat)? Type All for no day of week filter\n')).lower()
            
        if day not in DAY_OF_WEEK:
            print('\nYou must enter Sun, Mon, Tue, Wed, Thu, Fri, Sat or All')
            continue
        else:
            break

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
    try:
        df = pd.read_csv(CITY_DATA[city])
    except IOError:
        print("Error: Could not find file or read data")

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
   
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTH_DATA.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == DAY_OF_WEEK.index(day)]
    
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # create combined start and end station column
    df["Combined Station"] = df["Start Station"] + " - " + df["End Station"]

    return df


def generic_stats(df):
    """Displays generic statistics on the df."""

    print('\nCalculating Generic Statistics ...\n')
    start_time = time.time()

    # display count, mean, standard deviation, minimum, and maximum
    print('\nShow count, mean, standard deviation, minimum, and maximum.')
    print(df.describe())

    # display dimensions of the DataFrame
    print('\nShow the dimensions of the DataFrame.')
    print(df.shape)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = MONTH_DATA[df['month'].mode()[0]-1]
    print('\nMost common month:', common_month)

    # display the most common day of week
    common_dow = DAY_OF_WEEK[df['day_of_week'].mode()[0]]
    print('\nMost common day of week:', common_dow)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('\nMost common hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_st = df['Start Station'].mode()[0]
    print('\nMost commonly used start station:', common_start_st)

    # display most commonly used end station     
    common_end_st = df['End Station'].mode()[0]
    print('\nMost commonly used end station:', common_end_st)

    # display most frequent combination of start station and end station trip      
    common_combined = df['Combined Station'].mode()[0]
    print('\nMost commonly used combination of start and end station trip:', common_combined)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    
    hours = total_travel_time // 3600
    minutes = (total_travel_time % 3600) // 60
    remaining_seconds = total_travel_time % 60

    print(f"Total travel time: {hours:,} hours, {minutes} minutes and {remaining_seconds} seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    
    hours = mean_travel_time // 3600
    minutes = (mean_travel_time % 3600) // 60
    remaining_seconds = mean_travel_time % 60

    print(f"Mean travel time: {hours:,} hours, {minutes} minutes and {remaining_seconds} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().apply(lambda x: '{:,}'.format(x))
    
    print(user_types)

    if 'Gender' in df.columns:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts().apply(lambda x: '{:,}'.format(x))
    
        print(gender_counts)

        # Create a bar chart of Gender counts
        gender_counts_no_formatting = df['Gender'].value_counts()
        ax = gender_counts_no_formatting.plot.bar()
       
        # Set the xticklabels orientation to horizontal
        plt.xticks(rotation=0)

        # Format y-axis tick labels with commas
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        ax.set(xlabel='Gender', ylabel='Count', title='Bar chart of Gender Counts')

        # Show the plot
        plt.show(block=False)

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_yr = df['Birth Year'].min()
        print('\nEarliest birth year:', int(earliest_birth_yr))

        most_recent_birth_yr = df['Birth Year'].max()
        print('\nMost recent birth year:', int(most_recent_birth_yr))

        common_birth_yr = df['Birth Year'].mode()[0]
        print('\nMost common birth year:', int(common_birth_yr))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    # prompt user if they want to see 5 lines of raw data
    
    start = 0
    end = 5
    
    while True:
        see_raw = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n')
        if see_raw.lower() == 'yes' and start < df.size:
            print(df.iloc[start:end])
            start += 5
            end += 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print('\nBased on your selections there are no records available to generate stats.')
        else:
            generic_stats(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
