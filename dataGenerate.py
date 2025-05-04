import pandas as pd
import numpy as np
import random

np.random.seed(42)

n=500

time_of_day_choices = ['Morning', 'Afternoon', 'Evening', 'Night']
room_size_choices = ['Small', 'Medium', 'Large']

data = {
    'time_of_day': np.random.choice(time_of_day_choices, n),
    'outside_temp': np.random.normal(loc=30, scale=5, size=n).round(1),
    'num_of_people_in_room': np.random.randint(0, 6, size=n),
    'fan_on': np.random.choice([0,1],n, p=[0.3, 0.7]),
    'ac_on': np.random.choice([0,1], n, p=[0.6, 0.4]),
    'window_open': np.random.choice([0,1], n),
    'room_size': np.random.choice(room_size_choices, n, p=[0.4, 0.4, 0.2]),
}

room_temp = []
for i in range(n):
    base = data['outside_temp'][i]
    adj = 0

    if data['fan_on'][i]:
        adj -=2
    if data['ac_on'][i]:
        adj -=5
    if data['window_open'][i]:
        adj -=1
    if data['room_size'][i] == 'Small':
        adj -= 2
    if data['room_size'][i] == 'Large':
        adj += 2
    
    adj += data['num_of_people_in_room'][i] * 1
    noise = np.random.normal(0, 1)
    room_temp.append(round(base+adj+noise, 1))

data['room_temp'] = room_temp

df = pd.DataFrame(data)
df.to_csv('room_temp_data.csv', index=False)
