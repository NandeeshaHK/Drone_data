import csv
import time
from pymavlink import mavutil

# Initialize the connection to the drone
master = mavutil.mavlink_connection('udp:0.0.0.0:14550')

# Prompt the user for a tag name
tag_name = input("Enter a tag name (limited to 20 characters): ")

# Create and open a CSV file for writing
csv_file = open('drone_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Tag', 'Latitude', 'Longitude', 'Relative Altitude', 'Yaw Angle'])

try:
    # Continuously collect and save data
    while True:
        # Read data from the drone
        msg = master.recv_match(type=['GLOBAL_POSITION_INT', 'ATTITUDE'], blocking=True)

        # Extract relevant data
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        alt_rel = msg.relative_alt / 1e3  # Convert to meters
        yaw = msg.yaw / 100  # Convert to degrees

        # Write data to CSV file
        csv_writer.writerow([tag_name, lat, lon, alt_rel, yaw])

        # Display collected data
        print(f"Tag: {tag_name}, Latitude: {lat}, Longitude: {lon}, Altitude: {alt_rel}, Yaw: {yaw}")

except KeyboardInterrupt:
    pass
finally:
    # Close the CSV file
    csv_file.close()
    print("Data collection stopped. Collected data has been saved to 'drone_data.csv'.")
