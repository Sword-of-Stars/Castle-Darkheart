import csv
import matplotlib.pyplot as plt

# Read data from the CSV file
with open("fps_tracker4.txt", "r") as csvfile:
    reader = csv.reader(csvfile)
    # Extract and process data for plotting
    # This will depend on the structure of your data
    x_data = []
    y_data = []
    for row in reader:
        # Adapt this based on your data format
        x_data.append(float(row[0]))
        y_data.append(float(row[1]))

# Create the plot
plt.plot(x_data, y_data)

# Customize the plot (labels, title, etc.)
plt.xlabel("Time")
plt.ylabel("Frames Per Second")
plt.title("FPS Visualizer")

# Display the plot
plt.show()
