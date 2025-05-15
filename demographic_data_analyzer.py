import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    #df = None
    df = pd.read_csv('adult.data.csv')
    N = df.shape[0]

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    #race_count = None
    race_count = df['race'].value_counts()

    # What is the average age of men?
    #average_age_men = None
    average_age_men = df[df.sex == 'Male']['age'].mean()
    average_age_men = average_age_men.round(1) #note: values must be rounded as per the tests; this is not mentioned in the instructions though


    # What is the percentage of people who have a Bachelor's degree?
    #percentage_bachelors = None
    percentage_bachelors = 100 * (df['education'] == 'Bachelors').sum()/N
    #apparently this is NOT out of valid i.e those who a) are not missing b) have some eduation, but out of ALL rows which is strange since why would one count missing observations?
    percentage_bachelors = percentage_bachelors.round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    #higher_education = None
    #lower_education = None

    sel_degrees = ['Bachelors','Masters','Doctorate']
    higher_education = df['education'].isin(sel_degrees)
    lower_education = ~higher_education


    # percentage with salary >50K
    #higher_education_rich = None
    #lower_education_rich = None
    higher_education_rich = 100 * (df[higher_education]['salary'] == '>50K').sum() / higher_education.sum() #as per tests needs to be rounded to 1 decimals
    #this has to be compared to all of the selected degrees NOT all rows
    higher_education_rich = higher_education_rich.round(1)
    
    lower_education_rich = 100 * (df[lower_education]['salary'] == '>50K').sum() / lower_education.sum()
    lower_education_rich = lower_education_rich.round(1)
    

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    #min_work_hours = None
    min_work_hours = df['hours-per-week'].min()


    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    #num_min_workers = None

    min_workers = df[df['hours-per-week'] == min_work_hours]
    num_min_workers = min_workers.shape[0]

    #rich_percentage = None
    rich_percentage = 100 * (min_workers['salary'] == '>50K').sum() / num_min_workers
    rich_percentage = rich_percentage.round(1)


    # What country has the highest percentage of people that earn >50K?
    #highest_earning_country = None
    counts_by_country = df.groupby('native-country').size() #note: counts() will leave redundant groups and needs additional work, unlike size()
    countries_by_salary = df.groupby('native-country')['salary'].value_counts()

    rich_countries_by_salary_pct = 100 * countries_by_salary.loc[:, '>50K'] / counts_by_country
    highest_earning_country = rich_countries_by_salary_pct.idxmax() #idxmax returns the corresponding index


    #highest_earning_country_percentage = None
    highest_earning_country_percentage = rich_countries_by_salary_pct.max()
    highest_earning_country_percentage = highest_earning_country_percentage.round(1)


    # Identify the most popular occupation for those who earn >50K in India.
    #top_IN_occupation = None
    rich_and_india = (df['salary'] == '>50K') & (df['native-country'] == 'India') #note: must use brackets to work; python's 'and' won't work here
    top_IN_occupation = df.loc[rich_and_india, 'occupation'].value_counts().idxmax() 

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
