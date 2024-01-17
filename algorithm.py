import random
import matplotlib.pyplot as plt
import numpy as np

#USER DATA TAKEN FROM FOLLOWING STUDIES:

#https://www.researchgate.net/figure/The-frequency-of-physical-activity-per-week_tbl2_259148040
#Milanović, Z., Sporiš, G., Trajkovič, N., Vračan, D., Andrijašević, M., Pantelić, S. and Baić, M., 2013. 
# Attitudes towards exercise and the physical exercise habits of University of Zagreb students. Annales Kinesiologiae, 4(1).

#https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4642397/


# Function to generate users
def generate_users(names, traits):
    users = []
    for i in range(len(names)):
        user = {
            # user info and stats
            'name': names[i],
            'workout_chance': np.random.normal(0, 10),  # Start with low activity level
            'traits': traits[i],
            
            # data the algorithm has access to
            #'activity_level' : activity_level[i],
            'workouts_this_week': 0,
            'nudges_received': 0,
            'encouragements_received': 0,
            'nudge_chance' : 0,
        }
        users.append(user)
    return users


# Function to generate users
def generate_generic_users(nr_users):
    users = []
    for i in range(nr_users):
        #stats based on cited study
        x = random.randint(0,100)
        weekly_workouts = 0
        if(x >= 57 and x < 59): weekly_workouts = 1
        elif(x < 78): weekly_workouts = 2
        elif(x < 91): weekly_workouts = 3
        elif(x < 95): weekly_workouts = 4
        elif(x < 97): weekly_workouts = 5
        else: weekly_workouts = 6
        user = {
            # user info and stats
            'name': i,
            'workout_chance': weekly_workouts/7.0*100,
            'traits': [],
            'workouts_this_week': 0,
            'nudges_received': 0,
            'nudge_chance' : 0.5,
        }
        users.append(user)
    return users


# Function to calculate moving average for really large timeframes
def moving_average(lst, window_size=3):
    return [sum(lst[i:i+window_size])/window_size for i in range(len(lst)-window_size+1)]



def nudge(user, workout_frequency_history, day):
    #Every day, check if user is behind or ahead of average
    if user['workouts_this_week'] < np.mean([workout for user_workouts in workout_frequency_history.values() for workout in user_workouts])/(7 - (day%7)):  # User is behind, send nudge
        user['nudge_chance'] *= 1.5

    if user['nudge_chance'] > random.randint(0,100) and user['nudges_received'] < 5:  # User has a chance of being nudged
        user['nudges_received'] += 1
        user['nudge_chance'] *= 0.5
        user['workout_chance'] += np.random.normal(3, 8)  # Increase workout frequency in response to nudge
        user['workout_chance'] = max(0, min(100, user['workout_chance']))  # Limit workout frequency 

'''
Weekly feedback function, not used in this version

def weekly_feedback(user, workout_frequency_history):
    if user['workouts_this_week'] >= np.mean([workout for user_workouts in workout_frequency_history.values() for workout in user_workouts]):  # User is ahead, send encouragement
        user['nudges_received'] += 1
        user['workout_chance'] += np.random.normal(7, 7)
    else:  # User is behind, send nudge
        user['nudges_received'] += 1
        user['nudge_chance'] *= 0.5
        user['workout_chance'] += np.random.normal(4, 10)
'''

def check_traits(user, day):
    if 'local' in user['traits'] and day == 0:
        user['workout_chance'] += np.random.normal(20, 40)
    if 'busy' in user['traits']: 
        user['workout_chance'] += np.random.normal(-1, 0)
    if 'local' in user['traits']:
        user['workout_chance'] += np.random.normal(0, 5)
    if 'local' in user['traits']:
        user['workout_chance'] += np.random.normal(0, 5)
    if 'local' in user['traits']:
        user['workout_chance'] += np.random.normal(0, 5)
    user['workout_chance'] = max(0, user['workout_chance'] + np.random.normal(0, 1)) # make sure it does not go negative

# Function to simulate app influence on workout frequency / week
def simulate_normal_behaviour(users, num_days=84):  # for now we will plot it over ~3 months
    workout_frequency_history = {user['name']: [] for user in users}  # workout frequency history for each user      
    for day in range(num_days):
        for user in users:
            # add user quirks for individual personas
            check_traits(user, day)
            # Probability of a workout occurring, account for at least 1 rest day per week
            workout_occurred = user['workouts_this_week'] < 6 and random.random() < user['workout_chance'] / 100 
            if workout_occurred:
                user['workouts_this_week'] += 1
            if day % 7 == 6:  # End of the week
                workout_frequency_history[user['name']].append(user['workouts_this_week'])
                user['workouts_this_week'] = 0  # Reset for the next week
    return workout_frequency_history


# Function to simulate app influence on workout frequency / week
def simulate_app_influence(users, num_days=84):  # for now we will plot it over ~3 months
    workout_frequency_history = {user['name']: [] for user in users}  # workout frequency history for each user    
    nudge_frequency_history = {user['name']: [] for user in users}  # Nudge frequency history for each user 
    for day in range(num_days):
        for user in users:
            # add user quirks for individual personas
            check_traits(user, day)
            # Probability of a workout occurring, account for at least 1 rest day per week
            workout_occurred = user['workouts_this_week'] < 6 and random.random() < user['workout_chance'] / 100 
            if workout_occurred:
                user['workouts_this_week'] += 1
            
            nudge(user, workout_frequency_history, day)
            # End of the week
            if day % 7 == 6:  
                #weekly_feedback(user, workout_frequency_history, nudge_frequency_history)
                workout_frequency_history[user['name']].append(user['workouts_this_week'])
                nudge_frequency_history[user['name']].append(user['nudges_received'])
                user['workouts_this_week'] = 0  # Reset for the next week
                user['nudges_received'] = 0  # Reset for the next week
                
    # Calculate moving average of workout frequency (for long term graphs)
    #for i in range(len(workout_frequency_history)):
    #    workout_frequency_history[i] = moving_average(workout_frequency_history[i])

    return workout_frequency_history, nudge_frequency_history

'''Simulation with personas'''
# List of user names and habits
#names = ['Liam', 'Matteo', 'Alex']
#traits = [['local', 'active'], ['active', 'busy'], ['unmotivated', 'busy']]
#activity_levels = ['intermediate', 'beginner', 'untrained']
#users = generate_users(names, traits)
# Simulate normal behaviour for 12 weeks
#unassisted_workout_history = simulate_normal_behaviour(users, 12 * 7)

# Reset users
# users = generate_users(names, traits)
# Simulate app influence for 12 weeks
#assisted_workout_history, nudge_frequency_history = simulate_app_influence(users, 12 * 7)


'''Simulation with generic users'''
users = generate_generic_users(100)

unassisted_workout_history = simulate_normal_behaviour(users, 24 * 7)
assisted_workout_history, nudge_frequency_history = simulate_app_influence(users, 24 * 7)


# Create three subplots
fig, (ax0, ax1, ax2) = plt.subplots(3, 1, sharex=True)
# Plot workout frequency history for each user on the first subplot
#for name, user_history in assisted_workout_history.items():
#    ax1.plot(range(1, len(user_history) + 1), user_history, label=name)



# Convert the dictionary values to lists
unassisted_workout_list = list(unassisted_workout_history.values())
assisted_workout_list = list(assisted_workout_history.values())
nudge_frequency_list = list(nudge_frequency_history.values())

# Calculate the mean of the lists
unassisted_workout_mean = np.mean(unassisted_workout_list, axis=0)
assisted_workout_mean = np.mean(assisted_workout_list, axis=0)
nudge_frequency_mean = np.mean(nudge_frequency_list, axis=0)

# Plot the mean workout frequency history on the subplots
ax0.plot(unassisted_workout_mean, label='Unassisted')
ax0.set_ylabel('Workouts per week')
ax0.set_ylim([0, 7])
ax0.legend()

ax1.plot(assisted_workout_mean, label='Assisted')
ax1.set_ylabel('Workouts per week')
ax1.set_ylim([0, 7])
ax1.legend()

# Plot nudge frequency history for each user on the second subplot
#for name, user_history in nudge_frequency_history.items():
#    ax2.plot(range(1, len(user_history) + 1), user_history, label=name)

# Plot the mean nudge frequency history on the subplot
ax2.plot(nudge_frequency_mean, label='Nudge frequency')
ax2.set_xlabel('Week')
ax2.set_ylabel('Nudges per week')
ax2.set_ylim([0, 7])
ax2.legend()

# Show the plot
plt.show()





