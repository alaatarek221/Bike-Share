import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def check_data_entry(prompt, valid_entries): 
    """
    Asks user to type some input and verify if the entry typed is valid.
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted 
    Returns:
        (str) user_input - the user's valid input
    """

    try:
        user_input = str(input(prompt)).lower()

        while user_input not in valid_entries : 
            print('Sorry... it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()

        print('Great! the chosen entry is: {}\n'.format(user_input))
        return user_input

    except:
        print('Seems like there is an issue with your input')


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
    valid_cities = CITY_DATA.keys()
    prompt_cities = "Please input the city you want 'chicago' , 'new york city' or 'washington': "
    city = check_data_entry(prompt_cities,valid_cities)

    # get user input for month (all, january, february, ... , june)
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    prompt_month = "Please choose month (All, January, February, March, April, May, June): "
    month = check_data_entry(prompt_month, valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all', 'monday', 'tuesday','wedensday','thursday', 'friday', 'saturday', 'sunday']
    prompt_day =  "Please choose day (All, Monday, Tuesday, Wedensday, Thursday, Friday, Saturday, Sunday): "
    day = check_data_entry(prompt_day, valid_days)
  
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
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day"] = df["Start Time"].dt.day_name()
    df["hour"] = df["Start Time"].dt.hour

    if month != "all":
       months = ['january', 'february', 'march', 'april', 'may', 'june']
       month = months.index(month) + 1
       df = df[df["month"] == month]

    if day != "all":
        df = df[df["day"] == day.title()]

    return df


def time_stats(df):
  
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    common_month = df["month"].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']

    print("The most common month is {}".format(months[common_month - 1]))

    # display the most common day of week
    common_day = df["day"].mode()[0]
    print("The most common day is {}".format(common_day))

    # display the most common start hour
    common_hour = df["hour"].mode()[0]
    print("The most common hour is {}".format(common_hour) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df["Start Station"].mode()[0]
    print("The most common start station is {}".format(start_station))

    # display most commonly used end station

    end_station =  df["End Station"].mode()[0]
    print("The most common end station is {}".format(end_station))
    
    # display most frequent combination of start station and end station trip
    df["line"] = df["Start Station"] + " , " + df["End Station"]
    path = df["line"].mode()[0]
    print("The most common path is {}".format(path))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = (df["Trip Duration"].sum()).round()
    print("Total travel time is {}".format(total_travel_time))
    

    # display mean travel time
    average_travel_time = (df["Trip Duration"].mean()).round()
    print("Average travel time is {}".format(average_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,selected_city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_of_user = df["User Type"].value_counts().to_frame()
    print("The count of user types is")
    print(count_of_user)

    # Display counts of gender
    if selected_city != 'washington':
      count_of_gender = df["Gender"].value_counts().to_frame()
      print("The count of gender is ")
      print(count_of_gender)

    # Display earliest, most recent, and most common year of birth
    
      earliest_birth = int(df["Birth Year"].min())
      print("The earlist year of birth is {}".format(earliest_birth))

      recent_birth = int(df["Birth Year"].max())
      print("The recent year of birth is {}".format(recent_birth))

      common_birth = int(df["Birth Year"].mode()[0])
      print("The common year of birth is {}".format(common_birth))

    else:
      print("Gender & Birth year aren't avaliable for Washington city")    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays 5 rows of data if user wants to see them"""

    print('More data is available to check')
    see_rows = input("Do you want to see the 5 rows of data ?  Enter yes or no. ").lower()
    if see_rows == "yes" :
      row_count = 0
      while row_count+5 < df.shape[0]:
        print(df.iloc[row_count:row_count+5])
        row_count += 5
        see_rows = input("Do you wish to continue ? Enter yes or no. ").lower()
        if see_rows != "yes":
          break
    
def main():
   while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.empty:
          print("No data available")  
        else:    
          time_stats(df)
          station_stats(df)
          trip_duration_stats(df)
          user_stats(df,city)
          display_data(df)  

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
