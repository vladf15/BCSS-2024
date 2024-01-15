import random
import matplotlib.pyplot as plt

# Function to generate users
def generate_users(num_users):
    users = []
    for i in range(num_users):
        user = {
            'id': i + 1,
            'workout_chance': random.randint(0, 20),  # Start with few workouts per week
            'workouts_this_week': 0,
            'nudges_received': 0,
            'encouragements_received': 0,
        }
        users.append(user)
    return users


# Function to calculate moving average
def moving_average(lst, window_size=3):
    return [sum(lst[i:i+window_size])/window_size for i in range(len(lst)-window_size+1)]

# Function to simulate app influence on workout frequency / week
def simulate_app_influence(users, num_days=84):  # for now we will plot it over ~3 months
    workout_frequency_history = [[] for _ in range(len(users))]  # workout frequency history for each user
    for day in range(num_days):
        for user in users:
            workout_occurred = random.random() < user['workout_chance'] / 100  # probability of a workout 
            if workout_occurred:
                user['workouts_this_week'] += 1
            #End of week
            if day % 7 == 6:  
                workout_frequency_history[user['id'] - 1].append(user['workouts_this_week'])
                user['workouts_this_week'] = 0  # Reset for the next week
                if user['workouts_this_week'] > 3 :  # User is ahead, send encouragement
                    user['encouragements_received'] += 1
                    user['workout_chance'] += random.randint(0, 35)
                else:  # User is behind, send nudge
                    user['nudges_received'] += 1
                    user['workout_chance'] += random.randint(-5, 20)  # Increase workout frequency in response to nudge
            #Every other day
            elif day != 1 and not workout_occurred and not user['workouts_this_week'] > 3:  # User is behind, send nudge
                    user['nudges_received'] += 1
                    user['workout_chance'] += random.randint(-5, 20)  # Increase workout frequency in response to nudge
            else:
                user['workout_chance'] += random.randint(-10, 5)
            user['workout_chance'] = max(0, min(100, user['workout_chance']))  # Limit workout frequency to 1-7 days per week

    # Calculate moving average of workout frequency (for long term graphs)
    for i in range(len(workout_frequency_history)):
        workout_frequency_history[i] = moving_average(workout_frequency_history[i])

    return workout_frequency_history

# Generate 10 generic users
users = generate_users(10)

# Simulate app influence for 12 weeks
workout_frequency_history = simulate_app_influence(users, 12 * 7)

# Plot workout frequency history for each user
for i, user_history in enumerate(workout_frequency_history):
    plt.plot(range(1, len(user_history) + 1), user_history, label=f'User {i + 1}')

plt.xlabel('Week')
plt.ylabel('Workouts per week')
plt.legend()
plt.show()
