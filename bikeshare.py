from os import system, name
import time
import pandas as pd

# Pandas display options settings
pd.set_option('display.max_rows', 10)
pd.set_option('colheader_justify', 'center')

# all possible month and day selections
months = ['January', 'February', 'March', 'April', 'May', 'June']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday']


def clrscr():
    """Method for clearing the screen"""
    # for windows os
    if name == 'nt':
        _ = system('cls')

    # for mac and linux os(The name is posix)
    else:
        _ = system('clear')


CITY_DATA = {'chicago': 'chicago.csv',
                'new york city': 'new_york_city.csv',
                'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
    """

    # if there's no input, no filters will be applied
    month = "all"
    day = "all"

    # a list containing the differents input possibilities for city
    cities = ['chicago', 'new', 'new york', 'new york city', 'washington', 'c', 'n', 'w']

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        clrscr()
        print('Hello! Let\'s explore some US bikeshare data!')
        print('='*70)
        city = input("You want to see data from wich city? (Chicago, New York City, Washington): ").lower().strip()
        # if the input is in the list of valid options, standarize the name of the city
        if city in cities:
            if city == 'c':
                city = 'chicago'
            elif city == 'new' or city == 'new york' or city == 'n':
                city = 'new york city'
            elif city == 'w':
                city = 'washington'
            break
        print("Sorry, you must input a valid city, try again ")
        time.sleep(2)

    # Get the filter for month, day or both
    print('City selected:', city.title())
    while True:
        data_filter = input("Would you like to filter by month, day, both or none: ").lower().strip()
        filter_options = ['month', 'day', 'both', 'none']
        if data_filter in filter_options:
            break
        else:
            print("Sorry, you must input month, day, both or none, try again\n")
            time.sleep(1)

    # get user input for month (all, january, february, ... , june)
    if data_filter == 'month' or data_filter == 'both':
        while True:
            clrscr()
            print('Hello! Let\'s explore some US bikeshare data!')
            print('City selected:', city.title())
            print('='*70)
            print("For witch month you do want to see the data? You can choose: ")
            print('\t', *months, sep=' | ')

            month = input("Your choice: ").lower().strip()
            if month.title() not in months:
                print("Sorry, you must input a valid month, try again")
                time.sleep(2)
            else:
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if data_filter == 'day' or data_filter == 'both':
        while True:
            clrscr()
            print('Hello! Let\'s explore some US bikeshare data!')
            print('City selected: ', city.title())
            print("Month selected: ", month.title())
            print('='*70)
            print("For witch day you do want to see the data? You can choose: ")
            print("\t", *days, sep=' | ')

            day = input("Your choice: ").lower()
            if day.title() not in days:
                print("Sorry, you must input a valid day, try again")
                time.sleep(2)
            else:
                break

    # show the city and filters
    clrscr()
    print('Exploring US bikeshare data for ', city.title())
    print("Month: ", month.title())
    print('Day: ', day.title())
    time.sleep(1)
    print('='*70)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Times columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month.title()) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    print('-'*70)
    start_time = time.time()

    # display the most common month
    most_common_month = months[(df['month'].mode()[0]) - 1].title()
    print("The most commont month is: ", most_common_month)

    # display the most common day of week
    print("The most common day of the week is: ", df['day_of_week'].mode()[0])

    # display the most common start hour
    start_hour = df['Start Time'].dt.hour
    print("The most common Start hour is: ", start_hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    print('-'*70)
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is: ", df.mode()['Start Station'][0])

    # display most commonly used end station
    print("The most commonly used end station is: ", df.mode()['End Station'][0])

    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most frequent combination of start station and end station are:")
    print(f"{'Starting Station: ':>20}{combination[0]}")
    print(f"{'Ending Station: ':>20}{combination[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    print('-'*70)
    start_time = time.time()

    # display total travel time
    df['diff_min'] = (df['End Time'] - df['Start Time'])
    total_travel_time = df['diff_min'].sum()
    print("Total travel time: ", total_travel_time)
    # display mean travel time
    mean_travel_time = df['diff_min'].mean()
    print("Mean travel time: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    print('-'*70)
    start_time = time.time()

    # Display counts of user types
    print("\nDifferents user types and its count:\n")
    print(df['User Type'].value_counts().to_frame().T)
    print()

    # Display counts of gender
    print("\nDifferents genders and its count:\n")
    print(df['Gender'].value_counts().to_frame().T)
    print()

    # Display earliest, most recent, and most common year of birth
    print("Earliest year of birth :", df['Birth Year'].min().astype(int))
    print("Most recent year of birth :", df['Birth Year'].max().astype(int))
    print("Most common year of birth :", df['Birth Year'].mode()[0].astype(int))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def show_raw_data(df):
    """Displays the raw data to the user"""
    x = 0
    rd = df.drop(['month', 'day_of_week', 'diff_min'], axis=1)
    rd.rename(columns={'Unnamed: 0': 'Id'}, inplace=True)
    while True:
        try:
            for x in range(x, x + 5):
                print(rd.iloc[x].to_string())
                print('-'*60)
                # Check for end of file
                if x > rd.shape[0]:
                    raise IndexError()
            print(f"Looking at row {x - 3} to {x + 1}")
            selection = input("Do you want to see the next 5 rows? Press y to continue: ").lower().strip()
            if selection == 'y':
                x += 1
            else:
                break
        except (IndexError, KeyError):
            print("\n*** END OF FILE ***")
            break


def main():
    """Main Program"""

    while True:
        city, month, day = get_filters() # Get the user filters
        df = load_data(city, month, day) # Apply the user filters
        #Show all stats
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        # Washington doesn't have user_stats
        if city != 'washington':
            user_stats(df)
        else:
            print("\n* THERE IS NO USER DATA FOR WASHINGTON *\n")
            
        # Request for raw data
        raw_data = input("Would you like to see raw data? Enter yes or no: ").lower().strip()
        if raw_data == 'yes':
            print("Raw Data:\n")
            show_raw_data(df)
        # Request for restart
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower().strip()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
