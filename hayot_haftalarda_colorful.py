import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import matplotlib.patches as mpatches
import math
from datetime import datetime
import textwrap

# Define the number of years and weeks per year
years = 90
weeks_per_year = 52

# Create the data and reshape it
data = np.arange(1, years * weeks_per_year + 1).reshape(years, weeks_per_year)

# Create discrete colormap
cmap = colors.ListedColormap([
    "#A5D6A7",  # Early Childhood
    "#FF8A80",  # School Years
    "#FFF59D",  # College
    "#90CAF9",  # Career
    "#CE93D8"   # Retirement
])

# Define the bounds
bounds = [0, 347, 937, 1145, 3121, 5200]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots(figsize=(20, 12))
extent = [0, weeks_per_year, years, 0]
im = ax.imshow(data, cmap=cmap, norm=norm, aspect='auto', extent=extent)

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

# Create custom legend
legend_patches = [
    mpatches.Patch(color="#A5D6A7", label='Bolalik (0-7 yosh)'),
    mpatches.Patch(color="#FF8A80", label='Maktab yillari (7-18 yosh)'),
    mpatches.Patch(color="#FFF59D", label='Oliy ta\'lim (18-22 yosh)'),
    mpatches.Patch(color="#90CAF9", label='Ish faoliyati (22-60 yosh)'),
    mpatches.Patch(color="#CE93D8", label='Nafaqa davri (60-100 yosh)')
]

# Add the legend to the plot, positioned to the top right and outside the plot
ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1, 1), fontsize='xx-large')

# Annotate the weeks
def annotate_week(ax, week, text, previous_annotations, right_annotations_y):
    year = week // weeks_per_year
    week_in_year = week % weeks_per_year

    # Calculate the center of the box for the given week
    center_x = week_in_year + 0.5
    center_y = year + 0.5

    # Wrap text if it's too long
    wrapped_text = "\n".join(textwrap.wrap(text, width=30))

    # Determine the x and y offset based on position to avoid overlap
    if week_in_year <= 26:
        x_offset = -150  # Adjust for outside the grid
        ha = 'right'
    else:
        x_offset = 150  # Adjust for outside the grid
        ha = 'left'
        center_y = right_annotations_y.pop(0)  # Adjust y position for right-side annotations

    # Calculate the offset for the annotation text to avoid overlap
    offset = 0
    for prev_center_y, prev_text in previous_annotations:
        if abs(prev_center_y - center_y) < 5:  # If the y position is very close to previous
            offset += 20  # Adjust the offset as needed to avoid overlap

    xytext = (x_offset, center_y + offset)

    # Create the main annotation box with the updated placement
    ax.annotate(
        wrapped_text,
        xy=(center_x, center_y),
        xytext=xytext,
        textcoords='data',
        va='center', ha=ha,
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='black'),
        fontsize=14,
        arrowprops=dict(arrowstyle='-|>', edgecolor='black', facecolor='black', shrinkA=0, shrinkB=5, connectionstyle="arc3,rad=0.1"),
        annotation_clip=False
    )

    # Append the current center_y and text length to the list of previous annotations
    previous_annotations.append((center_y + offset, wrapped_text))

def week_calculator(birthday, date_str):
    birth_date = datetime.strptime(birthday, "%d.%m.%Y")
    target_date = datetime.strptime(date_str, "%d.%m.%Y")
    delta = target_date - birth_date
    return delta.days // 7  # Convert days to weeks

def weeks_from_birthday_to_today(birthday):
    birth_date = datetime.strptime(birthday, "%d.%m.%Y")
    today = datetime.today()
    delta = today - birth_date
    return delta.days // 7  # Convert days to weeks

def draw_life_line(ax, birthday):
    weeks_to_today = weeks_from_birthday_to_today(birthday)
    current_year = weeks_to_today // weeks_per_year
    current_week_in_year = weeks_to_today % weeks_per_year

    for row in range(current_year + 1):
        if row == current_year:
            ax.hlines(y=row + 0.5, xmin=0, xmax=current_week_in_year, color='black', linewidth=2, linestyle='-')
        else:
            ax.hlines(y=row + 0.5, xmin=0, xmax=weeks_per_year, color='black', linewidth=2, linestyle='-')

# Main function
def main():
    # Get user's birthday
    birthday_input = input("Enter your birthday (dd.mm.yyyy): ")
    
    # Validate birthday input
    try:
        datetime.strptime(birthday_input, "%d.%m.%Y")
    except ValueError:
        print("Please enter a valid date in dd.mm.yyyy format.")
        return

    # Draw life line from birthday to today
    draw_life_line(ax, birthday_input)

    previous_annotations = []
    right_annotations_y = list(range(10, 90, 10))  # Adjust the range and step as needed

    stop_loop = False
    while not stop_loop:
        date_input = input("Enter an important date (dd.mm.yyyy) (or type 'stop' to stop): ")
        
        if date_input.lower() == 'stop':
            stop_loop = True
            continue
        
        try:
            week_number = week_calculator(birthday_input, date_input)
            annotation_text = input("Enter the annotation text: ")

            # Annotate the user input
            annotate_week(ax, week_number, annotation_text, previous_annotations, right_annotations_y)
            
            # Display the updated plot
            plt.draw()
        except ValueError:
            print("Please enter a valid date in dd.mm.yyyy format.")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
