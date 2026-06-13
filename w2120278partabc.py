def valid_date():
    # Input valid day
    while True:
        try:
            day = int(input("Enter the date as dd:"))
            if day < 1 or day > 31:
                print("Out of range - values must be in the range 1 and 31")
            else:
                break
        except ValueError:
            print("Integer required")

    # Input valid month
    while True:
        try:
            month = int(input("Enter the month as mm:"))
            if month < 1 or month > 12:
                print("Out of range - values must be in the range 1 and 12")
            else:
                break
        except ValueError:
            print("Integer required")

    # Input valid year
    while True:
        try:
            year = int(input("Enter the year as yyyy:"))
            if year < 2000 or year > 2024:
                print("Out of range - values must be in the range 2000 and 2024")
            else:
                break
        except ValueError:
            print("Integer required")

    user_input = f"{day:02d}{month:02d}{year}"
    return user_input


def valid_date_continue():
    # Ask user if they want another date
    while True:
        another = input("Do you want to select another date? (Y/N): ").upper()
        if another == "Y":
            user_date = valid_date()
            file_name = f"traffic_data{user_date}.csv"
            result = process_csv_data(file_name)

            if result:
                # Display the outcomes
                display_outcomes(result[0])
                # Save the outcomes in the results file
                save_results_to_file(result[0])

                # Create histogram data
                data = {
                    "Junction1": list(result[1].values()),
                    "Junction2": list(result[2].values())
                }
                # Display histogram
                return data, user_date

        elif another == "N":
            break
        else:
            print('Please enter "Y"/"N"...')


# Process CSV data for the selected date
def process_csv_data(file_name):
    try:
        # Open and read CSV file
        with open(file_name, "r") as file:
            lines = file.readlines()

        # Initialize counters
        total_vehicles = 0
        total_trucks = 0
        total_electric_vehicles = 0
        total_two_wheeled = 0
        total_buses_north = 0
        total_no_turn = 0
        total_over_speed = 0
        total_elm_vehicles = 0
        total_hanley_vehicles = 0
        total_scooters_elm = 0
        total_bicycles = 0
        rain_hours = set()  # Use a set to store unique rainy hours
        hanley_hours = []
        vehicle_count_by_hour_Hanley_Highway_Westway = {str(i).zfill(2): 0 for i in range(24)}
        vehicle_count_by_hour_Elm_Avenue_Rabbit_Road = {str(i).zfill(2): 0 for i in range(24)} # Initialize vehicle count by hour

        for r in lines[1:]:  # Skip header
            row = r.strip().split(',')
            junction_name = row[0]
            date = row[1]
            time = row[2]
            travel_in = row[3]
            travel_out = row[4]
            weather = row[5]
            junction_speed_limit = int(row[6])
            vehicle_speed = int(row[7])
            vehicle_type = row[8]
            is_electric = row[9].lower() == "true"

            # General vehicle counts
            total_vehicles += 1
            if vehicle_type == "Truck":
                total_trucks += 1
            if is_electric:
                total_electric_vehicles += 1
            if vehicle_type in ["Bicycle", "Motorcycle", "Scooter"]:
                total_two_wheeled += 1
            if vehicle_type == "Bicycle":
                total_bicycles += 1

            # Elm Avenue/Rabbit Road junction
            if junction_name == "Elm Avenue/Rabbit Road":
                total_elm_vehicles += 1
                if vehicle_type == "Scooter":
                    total_scooters_elm += 1
                if travel_out == "N" and vehicle_type == "Buss":
                    total_buses_north += 1

            # Hanley Highway/Westway junction
            if junction_name == "Hanley Highway/Westway":
                total_hanley_vehicles += 1
                hanley_hours.append(time[:2])  # Extract hour
                vehicle_count_by_hour_Hanley_Highway_Westway[time[0:2]] += 1  # Count vehicles by hour

            if junction_name == "Elm Avenue/Rabbit Road":
                hanley_hours.append(time[:2])  # Extract hour
                vehicle_count_by_hour_Elm_Avenue_Rabbit_Road[time[0:2]] += 1

            # No turn vehicles
            if travel_in == travel_out:
                total_no_turn += 1

            # Over speed vehicles
            if vehicle_speed > junction_speed_limit:
                total_over_speed += 1

            # Rain hours - store unique hours when weather is rain/heavy rain
            if weather.lower() in ["rain", "heavy rain"]:
                rain_hours.add(time[:2])  # Add hour to the set (unique hours only)

        # Additional calculations
        truck_percentage = round((total_trucks / total_vehicles) * 100)
        avg_bicycles_per_hour = round(total_bicycles / 24)
        scooters_elm_percentage = (
            int((total_scooters_elm / total_elm_vehicles) * 100)
            if total_elm_vehicles > 0
            else 0)
        
        # Calculate busiest hour
        busiest_hour = max(vehicle_count_by_hour_Hanley_Highway_Westway, key=vehicle_count_by_hour_Hanley_Highway_Westway.get)
        busiest_hour_count = vehicle_count_by_hour_Hanley_Highway_Westway[busiest_hour]
        next_hour = (int(busiest_hour) + 1) % 24  # Handle hour overflow

        # Add results into dictionary
        result = {
            "file_name": file_name,
            "total_vehicles": total_vehicles,
            "total_trucks": total_trucks,
            "total_electric_vehicles": total_electric_vehicles,
            "total_two_wheeled": total_two_wheeled,
            "total_buses_north": total_buses_north,
            "total_no_turn": total_no_turn,
            "truck_percentage": truck_percentage,
            "avg_bicycles_per_hour": avg_bicycles_per_hour,
            "total_over_speed": total_over_speed,
            "total_elm_vehicles": total_elm_vehicles,
            "total_hanley_vehicles": total_hanley_vehicles,
            "scooters_elm_percentage": scooters_elm_percentage,
            "busiest_hour": busiest_hour,
            "max_count": busiest_hour_count,
            "next_hour": next_hour,
            "rain_hours": len(rain_hours),  # The number of unique rainy hours
        }

        return [result, vehicle_count_by_hour_Hanley_Highway_Westway, vehicle_count_by_hour_Elm_Avenue_Rabbit_Road]

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None


def display_outcomes(outcomes):
    #function to display results
    print("**********************************")
    print(f"Data file selected: {outcomes['file_name']}")#display the file name
    print("**********************************")
    print(f"The total number of vehicles recorded for this date is: {outcomes['total_vehicles']}")
    print(f"The total number of trucks recorded for this date is: {outcomes['total_trucks']}")
    print(f"The total number of electric vehicles for this date is: {outcomes['total_electric_vehicles']}")
    print(f"The number of “two wheeled” vehicles for this date is: {outcomes['total_two_wheeled']}")
    print(f"The total number of busses leaving Elm Avenue/Rabbit Road junction heading North is: {outcomes['total_buses_north']}")
    print(f"The total number of vehicles through both junctions not turning left or right is: {outcomes['total_no_turn']}")
    print(f"The percentage of total vehicles recorded that are Trucks for this date : {outcomes['truck_percentage']}%")
    print(f"The average number of Bicycles per hour for this date is : {outcomes['avg_bicycles_per_hour']}")
    print(f"The total number of vehicles recorded as over the speed limit for this date is: {outcomes['total_over_speed']}")
    print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is: {outcomes['total_elm_vehicles']}")
    print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is: {outcomes['total_hanley_vehicles']}")
    print(f"Vehicles recorded through Elm Avenue/Rabbit Road as scooters: {outcomes['scooters_elm_percentage']}%")
    print(f"The number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway: {outcomes['max_count']}")
    print(f"The most vehicles through Hanley Highway/Westway were recorded between: {outcomes['busiest_hour']}:00 and {outcomes['next_hour']}:00")
    print(f"The number of hours of rain for this date is: {outcomes['rain_hours']} hours")


def save_results_to_file(outcomes, file_name="results.txt"):
    """Saves the processed outcomes to a text file and appends if the program loops."""
    with open(file_name, "a") as result_file:
        #append to the results file
        result_file.write(f"Date file selected: {outcomes['file_name']}\n")
        result_file.write(f"The total number of vehicles recorded for this date is: {outcomes['total_vehicles']}\n")
        result_file.write(f"The total number of trucks recorded for this date is: {outcomes['total_trucks']}\n")
        result_file.write(f"The total number of electric vehicles for this date is: {outcomes['total_electric_vehicles']}\n")
        result_file.write(f"The number of “two wheeled” vehicles for this date is: {outcomes['total_two_wheeled']}\n")
        result_file.write(f"The total number of busses leaving Elm Avenue/Rabbit Road junction heading North is: {outcomes['total_buses_north']}\n")
        result_file.write(f"The total number of vehicles through both junctions not turning left or right is: {outcomes['total_no_turn']}\n")
        result_file.write(f"The percentage of total vehicles recorded that are Trucks for this date: {outcomes['truck_percentage']}%\n")
        result_file.write(f"The average number of Bicycles per hour for this date is: {outcomes['avg_bicycles_per_hour']}\n")
        result_file.write(f"The total number of vehicles recorded as over the speed limit for this date is: {outcomes['total_over_speed']}\n")
        result_file.write(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is: {outcomes['total_elm_vehicles']}\n")
        result_file.write(f"The total number of vehicles recorded through Hanley Highway/Westway junction is: {outcomes['total_hanley_vehicles']}\n")
        result_file.write(f"Vehicles recorded through Elm Avenue/Rabbit Road are scooters (%): {outcomes['scooters_elm_percentage']}%\n")
        result_file.write(f"The number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway: {outcomes['max_count']}\n")
        result_file.write(f"The most vehicles through Hanley Highway/Westway were recorded between: {outcomes['busiest_hour']}:00 and {outcomes['next_hour']}:00\n")
        result_file.write(f"The number of hours of rain for this date is: {outcomes['rain_hours']} hours\n")
        result_file.write("\n")  # Add a newline between entries
