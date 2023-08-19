import numpy as np
import matplotlib.pyplot as plt
import pandas as pd  # Import the pandas library

# New Parameters for Vertical Position Control
legend_vertical_position = 0.7  # Control the vertical position of the legend
data_label_vertical_position = 33  # Control the vertical position of the data labels
arrow_vertical_position = 29  # Control the vertical position of the double-headed arrow

# Read the CSV file
# The first row of the CSV file will be treated as the header (specimen names)
data = pd.read_csv('data2.csv')

# Iterate through the columns of the DataFrame
for column in data.columns:
    # Your dataset
    cell_sizes = data[column].dropna().values  # Drop NaN values, if any
    cell_sizes = np.array(cell_sizes)
    
    # Calculate the histogram
    bins = [40, 80, 120, 160, 200, 240, 280, 320]
    hist, edges = np.histogram(cell_sizes, bins=bins)
    relative_frequency = hist / hist.sum() * 100

    # Calculate the average and standard deviation
    average = np.mean(cell_sizes)
    std_dev = np.std(cell_sizes, ddof = 1)

    # Shift the position of the vertical lines to the left by 5 units
    shifted_average = average - 20
    shifted_std_dev_left = (average - std_dev) - 20
    shifted_std_dev_right = (average + std_dev) - 20

    # Plotting
    plt.figure(figsize=(16/2.54, 4.9/2.54), dpi=1000)
    plt.plot(edges[:-1], relative_frequency, marker='o', linestyle='-', color='b', label='Cell Size Distribution')

    # Highlight the histogram bins using a bar plot
    bin_width = np.diff(edges)  # Calculate the width of each bin
    plt.bar(edges[:-1] - 20, relative_frequency, width=bin_width, align='edge', 
        edgecolor='black', linewidth=1, color='lightblue', alpha=0.1, label='Histogram')

    # Conversion factor from inches to data coordinates
    inch_to_data = (plt.ylim()[1] - plt.ylim()[0]) / (4.9/2.54)
    offset = 0.64 * inch_to_data  # 1 inch upward

    # Data labels for each marker
    for x, y in zip(edges[:-1], relative_frequency):
        plt.text(x, y, f'{y:.1f}%', color='black', fontname='Calibri', fontsize=9, zorder=5,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='black', boxstyle='round,pad=0.2'))

    # Average line
    plt.axvline(x=shifted_average, color='r', linestyle='--', linewidth=1.0, label='Mean')

    # Data label for the mean (3 pt below the double-headed arrow)
    plt.text(shifted_average, data_label_vertical_position + offset, f'{average:.2f} µm', color='black', fontname='Calibri', fontsize=8, ha='center',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='black', boxstyle='round,pad=0.2'))

    # Standard deviation lines
    plt.axvline(x=shifted_std_dev_left, color='g', linestyle='--', linewidth=1.0, label=f'Std Dev: ±{std_dev:.2f} µm')
    plt.axvline(x=shifted_std_dev_right, color='g', linestyle='--', linewidth=1.0)

    # Standard deviation data labels (3 pt below the double-headed arrow)
    plt.text(shifted_std_dev_left, data_label_vertical_position + offset, f'{average - std_dev:.2f} µm', color='black', fontname='Calibri', fontsize=8, ha='center',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='black', boxstyle='round,pad=0.2'))
    plt.text(shifted_std_dev_right, data_label_vertical_position + offset, f'{average + std_dev:.2f} µm', color='black', fontname='Calibri', fontsize=8, ha='center',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='black', boxstyle='round,pad=0.2'))

    # Double-headed arrows for standard deviation (3 pt below the data labels)
    plt.annotate('', xy=(shifted_std_dev_left, arrow_vertical_position + offset), xytext=(shifted_std_dev_right, arrow_vertical_position + offset),
                arrowprops=dict(arrowstyle='<->', color='g'))

    # Chart details
    plt.title(column, fontname='Calibri', fontsize=11)  # Use column name as the title
    
    plt.xlabel('Cell Size [µm]', fontname='Calibri', fontsize=10)
    plt.ylabel('Frequency [%]', fontname='Calibri', fontsize=10)
    plt.grid(axis='y', linestyle='--')
    plt.ylim(0, 50)  # Set bounds for vertical axis from 0% to 40%

    # Y-axis in percentage
    plt.gca().set_yticklabels(['{:.0f}%'.format(x) for x in plt.gca().get_yticks()])

    # Custom x-axis labels
    new_labels = [f'[{bins[i]}, {bins[i+1]})' for i in range(len(bins)-1)]
    bin_middles = [(bins[i] + bins[i+1]) / 2 for i in range(len(bins)-1)]
    new_positions = [pos - 20 for pos in bin_middles]  # Shift the label positions to the left by 20 units
    plt.xticks(new_positions, new_labels, fontsize=9, fontname='Calibri')


    # Remove borders
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    # Set the size of the axis labels
    plt.yticks(fontsize=9, fontname='Calibri')

    # Add legend (font size decreased to 8)
    legend = plt.legend(loc='upper right', fontsize=6, bbox_to_anchor=(1, legend_vertical_position))
    legend.get_frame().set_edgecolor('black')
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.8)
    
    # Save the plot as a file with a unique name based on the column name
    plt.savefig(f'{column}_cell_size_distribution.png', format='png', bbox_inches='tight')
    
    # Show the plot
    plt.show()
