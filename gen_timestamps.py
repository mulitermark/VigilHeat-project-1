import csv
import random

def generate_synthetic_data():
    data = []
    
    for hour in range(6, 22):
        # Adjust the mean and standard deviation values to match your desired distribution
        mean = 50  # Average number of people
        std_dev = 10  # Standard deviation of the number of people
        
        # Generate a random number of people based on a normal distribution
        num_people = int(random.normalvariate(mean, std_dev))
        
        # Ensure the number of people is non-negative
        num_people = max(num_people, 0)
        
        # Append the hour and number of people to the data list
        data.append((hour, num_people))
    
    return data


def write_data_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Hour', 'Number of People'])  # Write the header
        
        for row in data:
            writer.writerow(row)


# Generate synthetic data
synthetic_data = generate_synthetic_data()

# Write data to CSV file
filename = 'crowd_data.csv'
write_data_to_csv(filename, synthetic_data)
