import time
import pandas as pd
import numpy as np
from scipy import stats


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

MY_CITY = None

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
		input_city = input("Enter the city: ")
		if input_city.lower() in ['chicago', 'new york city', 'washington']:
			global MY_CITY
			MY_CITY = input_city
			break
		else:
			print("Enter the correct city")

	# get user input for month (all, january, february, ... , june)
	while True:
		input_month = input("Enter the month: ")
		if input_month.lower() in MONTHS: 
			month = input_month
			break
		else:
			print("Enter the correct month")

	# get user input for day of week (all, monday, tuesday, ... sunday)
	while True:
		input_day = input("Enter the day: ")
		if input_day.lower() in DAYS: 
			day = input_day
			break
		else:
			print("Enter the correct day")

	print('-'*40)
	return MY_CITY, month, day


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

	# creating a data frame
	df = pd.read_csv(CITY_DATA[city])

	df['Start Time'] = pd.to_datetime(df['Start Time'])
	if month != 'all' or day != 'all':
		df = df[
				(
					df['Start Time'].dt.month == MONTHS.index(month) if month != 'all' else True
				) 
				& (
					df['Start Time'].dt.weekday == DAYS.index(day) if day != 'all' else True
				)
			]

	return df


def time_stats(df):
	"""Displays statistics on the most frequent times of travel."""

	print('\nCalculating The Most Frequent Times of Travel...\n')
	start_time = time.time()


	# display the most common month
	common_month = stats.mode(df['Start Time'].dt.month.to_numpy())[0][0]
	print("The most common month is: {}".format(MONTHS[common_month]))

	# display the most common day of week
	common_day = stats.mode(df['Start Time'].dt.weekday.to_numpy())[0][0]
	print("The most common day is: {}".format(DAYS[common_day]))

	# display the most common start hour
	common_hour = stats.mode(df['Start Time'].dt.hour.to_numpy())[0][0]
	print("The most common hour is: {}".format(common_hour))

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def station_stats(df):
	"""Displays statistics on the most popular stations and trip."""

	print('\nCalculating The Most Popular Stations and Trip...\n')
	start_time = time.time()

	# display most commonly used start station
	common_start_station =df['Start Station'].mode().iloc[0]
	print("The most common Start Station is: {}".format(common_start_station))

	# display most commonly used end station
	common_end_station =df['End Station'].mode().iloc[0]
	print("The most common End Station is: {}".format(common_end_station))

	# display most frequent combination of start station and end station trip
	df['Start Station'] = df['Start Station'] + ', ' + df['End Station']
	common_trip =df['Start Station'].mode().iloc[0]
	print("The most common Trip is: {}".format(common_trip))

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def trip_duration_stats(df):
	"""Displays statistics on the total and average trip duration."""

	print('\nCalculating Trip Duration...\n')
	start_time = time.time()

	# display total travel time
	total_travel = df['Trip Duration'].sum()
	print("the total travel time is: {}".format(total_travel))

	# display mean travel time
	mean_travel = df['Trip Duration'].mean()
	print("the mean travel time is: {}".format(mean_travel))

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def user_stats(df):
	"""Displays statistics on bikeshare users."""

	print('\nCalculating User Stats...\n')
	start_time = time.time()

	# Display counts of user types
	print("Display counts of user types\n{")
	for index,types in enumerate(df['User Type'].value_counts().index.tolist()):
		print('   User Type: {}, Counts: {}'.format(types,df['User Type'].value_counts()[index]))

	print("}\n")

	# Display counts of gender
	print("Display counts of gender\n{")
	if MY_CITY == 'washington':
		print("   Sorry, we don't have data about gender to {}".format(MY_CITY))
	else:
		for index,gender in enumerate(df['Gender'].value_counts().index.tolist()):
			print('   Gender: {}, Counts: {}'.format(gender,df['Gender'].value_counts()[index]))

	print("}\n")

	# Display earliest, most recent, and most common year of birth
	print("Display year of birth\n{")
	if MY_CITY == 'washington':
		print("   Sorry, we don't have data about birth day to {}".format(MY_CITY))
	else:	
		print('   earliest year of birth day: {}'.format(int(df['Birth Year'].min())))
		print('   most recent year of birth day: {}'.format(int(df['Birth Year'].max())))
		print('   most common year of birth day: {}'.format(int(df['Birth Year'].mode().iloc[0])))
	print("}\n")



	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def main():
	while True:
		city, month, day = get_filters()
		print("City: {}, Month: {}, Day: {}\n\n".format(city, month, day))
		df = load_data(city, month, day)
		print(df)
		print('-'*40)
		time_stats(df)
		station_stats(df)
		trip_duration_stats(df)
		user_stats(df)

		restart = input('\nWould you like to restart? Enter yes or no.\n')
		if restart.lower() != 'yes':
			break


if __name__ == "__main__":
	main()
