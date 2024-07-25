import matplotlib.pyplot as plt
import numpy as np

# Define the number of years and months per year
years = 90
months_per_year = 12

# Create the data and reshape it
data = np.arange(1, years * months_per_year + 1).reshape(years, months_per_year)

# Create plain white grid
fig, ax = plt.subplots(figsize=(10, 15))  # Adjust the figsize to ensure a better visual representation
extent = [0, months_per_year, years, 0]
im = ax.imshow(data, cmap="gray", aspect='auto', extent=extent, vmin=0, vmax=1)

im.format_cursor_data = lambda data: ""

# Draw gridlines
ax.grid(which='both', axis='both', linestyle='-', color='k', linewidth=0.27)

# Set ticks for months on x-axis
ax.set_xticks(np.arange(0, months_per_year, 1))
ax.set_xticks(np.arange(0, months_per_year + 1, 1), minor=True)

# Set ticks for years on y-axis
ax.set_yticks(np.arange(0, years, 5))
ax.set_yticks(np.arange(0, years + 1, 1), minor=True)

tick_label_size = 12  # Define your desired tick label size here
ax.tick_params(axis='both', which='major', labelsize=tick_label_size)
ax.tick_params(axis='both', which='minor', labelsize=tick_label_size * 0.8)

# Place x-axis labels on top
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')

# Hide the top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Set labels and title
ax.set_xlabel('Oylar', fontsize=24, color='#800000')
ax.set_ylabel('Yillar', fontsize=24, color='#800000')
ax.yaxis.set_label_position('left')
ax.yaxis.set_label_coords(-0.05, 0.97)
plt.title('Hayot oylarda: 90 yil', fontsize=28, color='#191970')

plt.tight_layout()
plt.show()

