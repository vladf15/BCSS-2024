import random
import matplotlib.pyplot as plt
import numpy as np

#USER DATA TAKEN FROM FOLLOWING STUDIES:

#https://www.researchgate.net/figure/The-frequency-of-physical-activity-per-week_tbl2_259148040
#Milanović, Z., Sporiš, G., Trajkovič, N., Vračan, D., Andrijašević, M., Pantelić, S. and Baić, M., 2013. 
# Attitudes towards exercise and the physical exercise habits of University of Zagreb students. Annales Kinesiologiae, 4(1).

#https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4642397/


# Function to generate users
def generate_users(names, traits, starting_level):
    users = []
    for i in range(len(names)):
        user = {
            # user info and stats
            'name': names[i],
            'motivation': starting_level[i],
            'workout_chance': starting_level[i],  # Start with set activity level
            'traits': traits[i],
            
            # data the algorithm has access to
            #'activity_level' : activity_level[i],
            'workouts_this_week': 0,
            'nudges_received': 0,
            'encouragements_received': 0,
            'nudge_chance' : 1,
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
            'motivation': weekly_workouts*100.0 / 7.0,
            'workout_chance': weekly_workouts*100.0 / 7.0,
            'traits': [],
            'workouts_this_week': 0,
            'nudges_received': 0,
            'nudge_chance' : 1,
        }
        users.append(user)
    return users


# Function to calculate moving average for really large timeframes
def moving_average(lst, window_size=3):
    return [sum(lst[i:i+window_size])/window_size for i in range(len(lst)-window_size+1)]



def nudge(user, workout_frequency_history, day):
    #Every day, check if user is behind or ahead of average
    user_mean = np.mean([workout for user_workouts in workout_frequency_history.values() for workout in user_workouts])
    if user['workouts_this_week'] <= ((2.5+(user_mean))/2)/(7 - (day%7)):  # User is behind, send nudge
        user['nudge_chance'] *= 1.5
    
    if  user['nudge_chance'] > random.randint(0,100):  # User has a chance of being nudged
        user['nudges_received'] += 1
        user['nudge_chance'] *= 0.5
        user['workout_chance'] += np.random.normal(20, 25)  # Increase workout chance in response to nudge
        user['motivation'] += np.random.normal(1.5, 3)
        user['workout_chance'] = max(0, min(100, user['workout_chance']))  # Limit workout frequency
        user['motivation'] = max(0, min(100, user['motivation']))  # Limit user motivation

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
    if 'enthusiastic' in user['traits']:
        user['workout_chance'] += np.random.normal(80, 10)/np.sqrt(day+1)
    if 'unmotivated' in user['traits']:
        user['motivation'] += np.random.normal(-0.5, 0.5)
    if 'busy' in user['traits']:
        if(day%7 < 5):
            user['workout_chance'] += np.random.normal(-10, 30)
            user['motivation'] += np.random.normal(-0.05, 1)
        else:
            user['workout_chance'] += np.random.normal(10, 30)
            user['motivation'] += np.random.normal(0.1, 0.5)
        
    user['workout_chance'] = max(0, min(100, user['workout_chance']))  # Limit workout frequency
    user['motivation'] = max(0, min(100, user['motivation']))  # Limit user motivation

# Function to simulate app influence on workout frequency / week
def simulate_normal_behaviour(users, num_days=84):  # for now we will plot it over ~3 months
    workout_frequency_history = {user['name']: [] for user in users}  # workout frequency history for each user      
    for day in range(num_days):
        for user in users:
            user['workout_chance'] = user['motivation']  # Reset workout chance to motivation level
            # add user traits for individual personas
            check_traits(user, day)
            # Probability of a workout occurring, account for at least 1 rest day per week
            workout_occurred = user['workouts_this_week'] < 6 and random.random() < user['workout_chance'] / 100 
            if workout_occurred:
                user['workouts_this_week'] += 1
            if day % 7 == 6:  # End of the week
                workout_frequency_history[user['name']].append(user['workouts_this_week'])
                user['workouts_this_week'] = 0  # Reset for the next week
                user['motivation'] += np.random.normal(-0.05, 2)
    return workout_frequency_history


# Function to simulate app influence on workout frequency / week
def simulate_app_influence(users, num_days=84):  # for now we will plot it over ~3 months
    workout_frequency_history = {user['name']: [] for user in users}  # workout frequency history for each user    
    nudge_frequency_history = {user['name']: [] for user in users}  # Nudge frequency history for each user 
    for day in range(num_days):
        for user in users:
            user['workout_chance'] = user['motivation']  # Reset workout chance to motivation level
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
                user['motivation'] += np.random.normal(-0.05, 2)
    return workout_frequency_history, nudge_frequency_history


# Calculate moving average of workout frequency (for long term graphs)
#   for i in range(len(workout_frequency_history)):
#     workout_frequency_history[i] = moving_average(workout_frequency_history[i])

def average_simulations(simulation_type, users, num_days=84, runs=4):
    # Run the simulation multiple times to get an average
    old_users = users
    workout_frequency_history = {user['name']: [] for user in users}  # workout frequency history for each user
    nudge_frequency_history = {user['name']: [] for user in users}  # Nudge frequency history for each user 
    for _ in range(runs):
        if simulation_type == 'normal':
            run_workout_frequency_history = simulate_normal_behaviour(users, num_days)
        elif simulation_type == 'app':
            run_workout_frequency_history, run_nudge_frequency_history = simulate_app_influence(users, num_days)
            for user in users:
                nudge_frequency_history[user['name']].append(run_nudge_frequency_history[user['name']])
        for user in users:
            workout_frequency_history[user['name']].append(run_workout_frequency_history[user['name']])
        users = old_users
    for user in users:
        #mean of workout frequency history for each user
        workout_frequency_history[user['name']] = np.mean(workout_frequency_history[user['name']], axis=0)
        nudge_frequency_history[user['name']] = np.mean(nudge_frequency_history[user['name']], axis=0)
    return workout_frequency_history, nudge_frequency_history


'''Simulation with generic users'''
users = generate_generic_users(100)
unassisted_workout_history = simulate_normal_behaviour(users, 26 * 7)
users = generate_generic_users(100)
assisted_workout_history, nudge_frequency_history = simulate_app_influence(users, 26 * 7)

# Create three subplots
fig, ([generic_graph, generic_nudge_graph]) = plt.subplots(1,2)
fig2, ([assisted_persona_graph, persona_nudge_graph], [persona_graph, empty]) = plt.subplots(2,2)
empty.remove()
# Convert the dictionary values to lists
unassisted_workout_list = list(unassisted_workout_history.values())
assisted_workout_list = list(assisted_workout_history.values())
nudge_frequency_list = list(nudge_frequency_history.values())
# Calculate the mean of the lists
unassisted_workout_mean = np.mean(unassisted_workout_list, axis=0)
assisted_workout_mean = np.mean(assisted_workout_list, axis=0)
nudge_frequency_mean = np.mean(nudge_frequency_list, axis=0)

# Plot the mean workout frequency history on the subplots
generic_graph.set_title('Workout frequency for the average of 100 generic students')
generic_graph.plot(unassisted_workout_mean, label='Unassisted')
generic_graph.plot(assisted_workout_mean, label='Assisted')
generic_graph.set_xlabel('Week')
generic_graph.set_ylabel('Workouts per week')
generic_graph.set_ylim([0, 7])
generic_graph.legend()
generic_nudge_graph.set_title('Average nudge frequency for 100 generic students')
generic_nudge_graph.plot(nudge_frequency_mean, label='Nudge frequency')
generic_nudge_graph.set_xlabel('Week')
generic_nudge_graph.set_ylabel('Nudges per week')
generic_nudge_graph.legend()


'''Simulation with personas'''
#List of user names and habits
names = ['Liam', 'Matteo', 'Alex']
traits = [['busy'],['enthusiastic'],['unmotivated']]
starting_level = [40, 10, 0]
users = generate_users(names, traits, starting_level)

unassisted_persona_history, _ = average_simulations('normal', users, 26 * 7, 5)
for name in unassisted_persona_history:
    persona_graph.plot(unassisted_persona_history[name], label=name)
persona_graph.set_title('Workout frequency for each persona normally')
persona_graph.set_xlabel('Week')
persona_graph.set_ylabel('Workouts per week')
persona_graph.set_ylim([0, 7])
persona_graph.legend()

users = generate_users(names, traits, starting_level)
assisted_persona_history, nudge_persona_history = average_simulations('app', users, 26 * 7, 5)

# Plot workout frequency history for each user on the first subplot
for name in assisted_persona_history:
    assisted_persona_graph.plot(assisted_persona_history[name], label=name)
assisted_persona_graph.set_title('Workout frequency for each persona with app assistance')
assisted_persona_graph.set_ylabel('Workouts per week')
assisted_persona_graph.set_ylim([0, 7])
assisted_persona_graph.legend()


# Plot nudge frequency history for each user on the second subplot
for name in nudge_persona_history:
    persona_nudge_graph.plot(nudge_persona_history[name], label=name)
persona_nudge_graph.set_title('Nudge frequency for each persona')
persona_nudge_graph.set_xlabel('Week')
persona_nudge_graph.set_ylabel('Nudges per week')
persona_nudge_graph.legend()


# Show the plot
plt.show()





