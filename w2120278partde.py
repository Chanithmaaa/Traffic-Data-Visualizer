import tkinter as tk
from w2120278partabc import valid_date, process_csv_data, display_outcomes, save_results_to_file

class HistogramApp:
    """
    A class to create a traffic volume histogram application using Tkinter.
    """
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with traffic data and date.

        Args:
            traffic_data (dict): Dictionary containing traffic volume data for two junctions.
            date (str): The date for which traffic data is displayed.
        """
        self.root = tk.Tk()
        self.root.title(f"Traffic Volume Histogram - {date}")

        # Create a canvas for drawing the histogram
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Store data and configuration
        self.traffic_data = traffic_data
        self.date = date

        self.window_width = 800
        self.window_height = 600
        self.margin_left = 50
        self.margin_bottom = 50
        self.bar_width = 10
        self.bar_spacing = 10
        self.max_bar_height = 400

        # Draw the histogram
        self.draw_histogram()

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def draw_histogram(self):
        """
        Draws the complete histogram, including axes, bars, and legend.
        """
        # Find the maximum value in the data for scaling
        max_value = max(
            max(self.traffic_data["Hanley Highway/Westway"]), max(self.traffic_data["Elm Avenue/Rabbit Road"])
        )

        # Draw axes
        self._draw_axes(max_value)

        # Draw bars for each hour and junction
        self._draw_bars(max_value)

        # Draw legend
        self._draw_legend()

    def _draw_axes(self, max_value):
        """
        Draws X and Y axes, including labels for hours and frequencies.

        Args:
            max_value (int): The maximum traffic volume, used for scaling.
        """
        # Draw X-axis
        self.canvas.create_line(
            self.margin_left,
            self.window_height - self.margin_bottom,
            self.window_width - 50,
            self.window_height - self.margin_bottom,
            width=2
        )

        # Draw Y-axis
        self.canvas.create_line(
            self.margin_left,
            self.window_height - self.margin_bottom,
            self.margin_left,
            100,
            width=2
        )

        # Add labels for hours on X-axis
        for i in range(24):
            x = self.margin_left + i * (self.bar_width * 2 + self.bar_spacing)
            self.canvas.create_text(
                x + self.bar_width / 2,
                self.window_height - self.margin_bottom + 20,
                text=f"{i:02d}",
                font=("Arial", 8)
            )

        # Add labels for frequencies on Y-axis
        y_label_count = 5
        for i in range(y_label_count + 1):
            value = int((max_value / y_label_count) * i)
            y = self.window_height - self.margin_bottom - (i * (self.max_bar_height / y_label_count))
            self.canvas.create_text(
                self.margin_left - 20,
                y,
                text=str(value),
                font=("Arial", 8)
            )

        # Add title
        self.canvas.create_text(
            self.window_width / 2,
            50,
            text=f"Traffic Volume Histogram - {self.date}",
            font=("Arial", 14, "bold")
        )

    def _draw_bars(self, max_value):
        """
        Draws bars for each hour and displays numerical values on top.

        Args:
            max_value (int): The maximum traffic volume, used for scaling.
        """
        for hour, (junction1, junction2) in enumerate(zip(
            self.traffic_data["Hanley Highway/Westway"],
            self.traffic_data["Elm Avenue/Rabbit Road"]
        )):
            # Calculate x-coordinate for the bars of the current hour
            x = self.margin_left + hour * (self.bar_width * 2 + self.bar_spacing)

            # Draw bar for Junction 1 (Hanley Highway/Westway)
            junction1_height = (junction1 / max_value) * self.max_bar_height
            self.canvas.create_rectangle(
                x,
                self.window_height - self.margin_bottom,
                x + self.bar_width,
                self.window_height - self.margin_bottom - junction1_height,
                fill="red"
            )
            # Add value label above the Junction 1 bar
            self.canvas.create_text(
                x + self.bar_width / 2,
                self.window_height - self.margin_bottom - junction1_height - 10,
                text=str(junction1),
                font=("Arial", 8),
                fill="black"
            )

            # Draw bar for Junction 2 (Elm Avenue/Rabbit Road)
            junction2_height = (junction2 / max_value) * self.max_bar_height
            self.canvas.create_rectangle(
                x + self.bar_width,
                self.window_height - self.margin_bottom,
                x + self.bar_width * 2,
                self.window_height - self.margin_bottom - junction2_height,
                fill="green"
            )
            # Add value label above the Junction 2 bar
            self.canvas.create_text(
                x + self.bar_width * 1.5,
                self.window_height - self.margin_bottom - junction2_height - 10,
                text=str(junction2),
                font=("Arial", 8),
                fill="black"
            )

    def _draw_legend(self):
        """
        Draws a legend to explain the colors of the bars.
        """
        # Legend for Junction 1
        self.canvas.create_rectangle(60, 100, 80, 120, fill="red")
        self.canvas.create_text(90, 110, text="Hanley Highway/Westway", anchor="w")

        # Legend for Junction 2
        self.canvas.create_rectangle(60, 130, 80, 150, fill="green")
        self.canvas.create_text(90, 140, text="Elm Avenue/Rabbit Road", anchor="w")

    def on_close(self):
        """
        Handles the window close event.
        """
        print("Closing the histogram window.")
        self.root.destroy()


def main_program():
    """
    Main program loop for processing user input and generating histograms.
    """
    while True:
        # Prompt user for a valid date
        user_date = valid_date()
        
        # Build the file name based on the user-provided date
        file_name = f"traffic_data{user_date}.csv"
        
        # Process CSV file and retrieve traffic data
        result = process_csv_data(file_name)

        if result:
            # Display outcomes in the console
            display_outcomes(result[0])
            
            # Save outcomes to a results file
            save_results_to_file(result[0])

            # Organize data for the histogram
            data = {
                "Hanley Highway/Westway": list(result[1].values()),
                "Elm Avenue/Rabbit Road": list(result[2].values())
            }
            
            # Launch histogram application
            app = HistogramApp(data, user_date)
        
        # Ask the user if they want another date
        while True:
            continue_choice = input("Do you want to select another date? (Y/N): ").upper()
            if continue_choice == 'N':
                return  # Exit the program
            elif continue_choice == 'Y':
                break  # Continue to process another date
            else:
                print('Please enter "Y"/"N"...')


if __name__ == '__main__':
    main_program()
