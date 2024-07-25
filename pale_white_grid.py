import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import random
from datetime import datetime
import textwrap

# Define the number of years and weeks per year
years = 90
weeks_per_year = 52

# Create the data and reshape it
data = np.arange(1, years * weeks_per_year + 1).reshape(years, weeks_per_year)

# Create plain white grid
fig, ax = plt.subplots(figsize=(20, 12))
extent = [0, weeks_per_year, years, 0]
im = ax.imshow(data, cmap="gray", aspect='auto', extent=extent, vmin=0, vmax=1)

im.format_cursor_data = lambda data: ""

# Draw gridlines
ax.grid(which='both', axis='both', linestyle='-', color='k', linewidth=0.27)

# Set ticks for weeks on x-axis
ax.set_xticks(np.arange(0, weeks_per_year, 5))
ax.set_xticks(np.arange(0, weeks_per_year + 1, 1), minor=True)

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
ax.set_xlabel('Haftalar', fontsize=24, color='#800000')
ax.set_ylabel('Yillar', fontsize=24, color='#800000')
ax.yaxis.set_label_position('left')
ax.yaxis.set_label_coords(-0.05, 0.97)
plt.title('Hayot haftalarda: 90 yil', fontsize=28, color='#191970')

# Annotate the weeks
def annotate_week(ax, week, text, previous_annotations):
    year = week // weeks_per_year
    week_in_year = week % weeks_per_year

    # Calculate the center of the box for the given week
    center_x = week_in_year + 0.5
    center_y = year + 0.5

    # Wrap text if it's too long
    wrapped_text = "\n".join(textwrap.wrap(text, width=30))

    # Calculate the offset for the annotation text to avoid overlap
    offset = 0
    for prev_center_y, prev_text in previous_annotations:
        if abs(prev_center_y - center_y) < 5:  # If the y position is very close to previous
            offset += 20  # Adjust the offset as needed to avoid overlap

    xytext = (-17, center_y + offset)

    # Choose a random color for the annotation
    colors = ['darkred', 'darkblue', 'green']
    color = random.choice(colors)

    # Create the main annotation box with the updated placement
    ax.annotate(
        wrapped_text, 
        xy=(center_x, center_y), 
        xytext=xytext,  # Adjusted xytext coordinates
        textcoords='data',
        va='center', ha='left',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor=color),
        fontsize=14,
        color=color,  # Set the text color
        arrowprops=dict(arrowstyle='-|>', edgecolor=color, facecolor=color, shrinkA=0, shrinkB=5, connectionstyle="arc3, rad=0.1"),
        annotation_clip=False
    )

    # Append the current center_y and text length to the list of previous annotations
    previous_annotations.append((center_y + offset, wrapped_text))

def week_calculator(birthday, date_str):
    birth_date = datetime.strptime(birthday, "%d.%m.%Y")
    target_date = datetime.strptime(date_str, "%d.%m.%Y")
    delta = target_date - birth_date
    return delta.days // 7  # Convert days to weeks

def main():
    previous_annotations = []

    while True:
        # Get famous person's birthday
        birthday_input = input("Enter the birthday of a famous person (dd.mm.yyyy) or type 'stop' to finish: ")
        
        if birthday_input.lower() == 'stop':
            break

        # Validate birthday input
        try:
            datetime.strptime(birthday_input, "%d.%m.%Y")
        except ValueError:
            print("Please enter a valid date in dd.mm.yyyy format.")
            continue

        date_input = input("Enter an important date in their life (dd.mm.yyyy): ")
        try:
            week_number = week_calculator(birthday_input, date_input)
            annotation_text = input("Enter the annotation text: ")

            # Annotate the user input
            annotate_week(ax, week_number, annotation_text, previous_annotations)
            
            # Display the updated plot
            plt.draw()
        except ValueError:
            print("Please enter a valid date in dd.mm.yyyy format.")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()