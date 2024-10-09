from datetime import datetime, timedelta
import re
import random
import os


class Reservations:
    def __init__(self):
        self.reservations = { # Initialize a dictionary to store reservations for each session.
            '12:00 pm - 02:00 pm': [],
            '02:00 pm - 04:00 pm': [],
            '06:00 pm - 08:00 pm': [],
            '08:00 pm - 10:00 pm': []
        }
        self.reservation_dates = {}  # Store reservation dates by session

    def main_menu(self):
        # Display the main options and handle user's choice
        while True:
            print ("Welcome to Charming Thyme Tratorria!")     
            print("\nMain Menu:")
            print("[1] Add Reservation")
            print("[2] Cancel Reservation")
            print("[3] Edit/Update Reservation")
            print("[4] Generate Menu Recommendations")
            print("[5] Display All Reservations")
            print("[6] Exit")
                
            choice = input("Choose an option: ")
                
            if choice == "1":
                self.make_reservation()
            elif choice == "2":
                self.cancel_reservation()
            elif choice == "3":
                self.edit_reservation()
            elif choice == "4":
                menu = Menu()
                menu.generate_recommendations()
            elif choice == "5":
                self.print_reservations()
            elif choice == "6":
                os.system('cls' if os.name == 'nt' else 'clear') # Clear the terminal screen for a cleaner look
                print("Exiting the program.")
                choice = input("To start reservation, Enter 'charming': ") # Enter safe word to start again
                if choice.lower() == "charming":
                    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen for a cleaner look
                else:
                    raise StopIteration # Stop reservation process
            else:
                print("Invalid choice.")
  
    def make_reservation(self):
        """To make a reservation.
        Prompts the user for necessary information to make the reservation valid and adds it to
        the reservations vocabulary."""
        while True:
            print("Make a reservation:")
            name = str(input("Enter the guest name:"))
            phone_number = self.get_valid_phone_number()  # prompts user to enter a valid phone number
            email_address = self.get_valid_email_address()  # prompts user to enter a valid email address

            while True:
                try:
                    group_size = int(input("Enter the number of guests coming/the group size:"))
                    if self.is_valid_group_size(group_size):  # ensures only 4pax per table/reservation
                        break
                    else:
                        print("Invalid group size. Maximum group size is 4.")
                except ValueError:
                    print("Invalid input. Please enter a valid group size.")

            session = self.select_session()
            reservation_date = self.get_reservation_date()

            if not self.is_valid_reservation(session, reservation_date): # error counter
                print("Invalid reservation. Please make sure to book at least 5 days in advance.")
                continue
            if not self.is_available(session, group_size): # error counter
                print("Sorry, the selected session is fully booked or cannot accommodate your group size.")
                continue
# Add reservation details to the respective session's reservation list.
            self.reservations[session].append( 
                (name, phone_number, email_address, group_size, session, reservation_date))
            self.reservation_dates.setdefault(session, []).append(reservation_date) 

            print("Reservation successful!")
            self.write_to_file(name, phone_number, email_address, group_size, session, reservation_date)
            # append guest details to reservation text file 
            choice = input("Do you want to add another reservation? (yes/no)")
            if choice.lower() != "yes":
                break

    def write_to_file(self, name, phone_number, email_address, group_size, session, reservation_date, file_path = 'Restaurant/reservations_21071097.txt'):
        #Write the guest reservation details to the text file from add reservations
        with open(file_path, "a") as file:
            file.write(f"\n{reservation_date}|Session {session}|{name}|{email_address}|{phone_number}|Number of pax = {group_size}\n")
            file.flush() # for fast response


    def get_valid_phone_number(self):
        """Ensures the phone number entered is valid and in the format of +60-XXXXXXXXX
        (the Malaysian phone number format). Returns the valid phone number"""
        while True:
            phone_number = input("Enter the guest phone number (+60-XXXXXXXX): ")
            if re.match(r'^\+60-\d{9}$', phone_number):
                return phone_number
            else:
                print("Invalid phone number format. Please enter in the format +60-XXXXXXXX.")

    def get_valid_email_address(self):
        """Ensures the email address entered is valid then returns the email address."""
        while True:
            email = input("Enter the guest email address: ")
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                return email
            else:
                print("Invalid email address format. Please enter a valid email address.")

    def select_session(self):
        """Method to prompt the user to select a session from the available session options provided.
        Returns the selected session"""
        print("\nAvailable Sessions:")
        session_options = list(self.reservations.keys())
        for i, session in enumerate(session_options, start=1):
            print(f"{i}. {session}")
        while True:
            session_choice = input("Select a session between 1 to 4: ")
            if session_choice.isdigit() and 1 <= int(session_choice) <= len(session_options):
                return session_options[int(session_choice) - 1]
            else:
                print("Invalid session choice.")

    def get_reservation_date(self):
        """Prompts the user to enter a date in the format of YYYY-MM-DD.
        Returns the parsed reservation date."""
        while True:
            try:
                date_input = input("Enter the reservation date (YYYY-MM-DD): ")
                reservation_date = datetime.strptime(date_input, "%Y-%m-%d").date()
                return reservation_date
            except ValueError:
                print("Invalid date format. Please enter in the format YYYY-MM-DD.")

    def is_valid_reservation(self, session, reservation_date):
        """Checks if the reservation is valid.
        Returns True if the reservation is valid (at least 5 days in advance), False otherwise."""
        current_date = datetime.now().date()
        min_reservation_date = current_date + timedelta(days=5)
        return reservation_date >= min_reservation_date

    def is_valid_group_size(self, group_size):
        """Checks if the group size is valid (maximum 4 guests per table).
        Returns True if the group size is within the allowed limit, False otherwise."""
        return group_size <= 4

    def is_available(self, session, group_size):
        """Checks if the selected session is available for the given group size and
        does not exceed the maximum number of reservations.
        Returns True if the session is available, False otherwise."""
        session_reservations = self.reservations[session]
        if len(session_reservations) >= 8:  # Maximum of 8 reservations per session
            return False
        total_group_size = sum(group_size for _, _, _, group_size, _, _ in session_reservations)
        return total_group_size + group_size <= 4 * 8 - 1

    
    def print_reservations(self, file_path='Restaurant/reservations_21071097.txt'):
        # Prints the existing reservations from the text file in an easily readable format.
        try:
            with open(file_path, "r") as file:
                content = file.readlines()

            if not content:
                print("No reservations found.")
            else:
                for line in content:
                    reservation_details = line.strip().split("|")
                    if len(reservation_details) == 6:
                        reservation_date, session, name, email_address, phone_number, group_size = reservation_details
                        print(f"Reservation Date: {reservation_date}")
                        print(f"Session: {session}")
                        print(f"Name: {name}")
                        print(f"Email Address: {email_address}")
                        print(f"Phone Number: {phone_number}")
                        print(f"{group_size}")
                        print("-" * 20)
        except FileNotFoundError:
            print(f"Error:{file_path} file not found.")

    def cancel_reservation(self, file_path='Restaurant/reservations_21071097.txt'):
        # For the user to cancel a reservation chosen from the text file according to number of reservation
        try:
            with open(file_path, "r") as file:
                content = file.readlines()

            if not content:
                print("No reservations found.")
                return

            print("Below are the existing reservations:")
            for i, line in enumerate(content, start=1):
                reservation_details = line.strip().split("|")
                if len(reservation_details) == 6:
                    reservation_date, session, name, email_address, phone_number, group_size = reservation_details
                    print(f"{i}. Reservation Date: {reservation_date}, Session: {session}, Name: {name}, Group Size: {group_size}")

            while True:
                try:
                    choice = int(input("Enter the number of the reservation you want to cancel (0 to exit): "))
                    if choice == 0:
                        print("Reservation cancellation--process aborted.")
                        return
                    elif 1 <= choice <= len(content):
                        break
                    else:
                        print("Invalid choice. Please enter a valid reservation number.")
                except ValueError:
                    print("Invalid input. Please enter a valid reservation number.")

            # Remove the cancelled reservation from text file
            with open(file_path, "w") as file:
                for i, line in enumerate(content, start=1):
                    if i != choice:
                        file.write(line)

            print("Reservation canceled successfully.")
            self.update_reservation_data()
        except FileNotFoundError:
            print(f"Error: {file_path} file not found.")

    def update_reservation_data(self, file_path='Restaurant/reservations_21071097.txt'):
        # Update the in-memory reservations dictionary based on the latest the text file.
        self.reservations = {
            '12:00 pm - 02:00 pm': [],
            '02:00 pm - 04:00 pm': [],
            '06:00 pm - 08:00 pm': [],
            '08:00 pm - 10:00 pm': []
        }
        try:
            with open(file_path, "r") as file:
                content = file.readlines()

            for line in content:
                reservation_details = line.strip().split("|")
                if len(reservation_details) == 6:
                    reservation_date, session, name, email_address, phone_number, group_size = reservation_details
                    if session in self.reservations:
                        self.reservations[session].append((name, phone_number, email_address, int(group_size), session, reservation_date))
        except FileNotFoundError:
            print(f"Error: {file_path} file not found.")


    def edit_reservation(self, file_path='Restaurant/reservations_21071097.txt'):
        """Allows the user to edit a specific part of a reservation."""
        try:
            with open(file_path, "r") as file:
                content = file.readlines()
                
            if not content:
                print("No reservations found.")
                return
            print("Before you can edit a reservation, we need to verify your reservation details.")
            check_value = input("Please enter your name, session, or reservation date:")
            matching_reservations = [(i, line) for i, line in enumerate(content) if check_value in line] # allow user to find reservations according to details.
            if not matching_reservations:
                print("No matching reservations found.")
                return
            print("Below are the existing reservations:")
            for i,  (_, line) in enumerate(matching_reservations, start=1):
                reservation_details = line.strip().split("|")
                if len(reservation_details) == 6:
                    reservation_date, session, name, email_address, phone_number, group_size = reservation_details
                    print(f"{i}. Reservation Date: {reservation_date}, Session: {session}, Name: {name}, Group Size: {group_size}")
                
            while True:
                try:
                    choice = int(input("Enter the number of the reservation you want to edit (0 to exit): "))
                    if choice == 0:
                        print("Reservation editing--process aborted.")
                        return
                    elif 1 <= choice <= len(matching_reservations):
                        break
                    else:
                        print("Invalid choice. Please enter a valid reservation number.")
                except ValueError:
                    print("Invalid input. Please enter a valid reservation number.")
                
            # Get the chosen reservation's details.
            chosen_index, chosen_reservation = matching_reservations[choice - 1]
            reservation_details = chosen_reservation.strip().split("|")
            if len(reservation_details) == 6:
                reservation_date, session, name, email_address, phone_number, group_size = reservation_details
                session = session.replace('Session ', '')  
                print(f"\nEditing Reservation #{choice}:")
                print(f"Reservation Date: {reservation_date}")
                print(f"Session: {session}")
                print(f"Name: {name}")
                print(f"Email Address: {email_address}")
                print(f"Phone Number: {phone_number}")
                print(f"Group Size: {group_size}") 
                    # Display reservation in a readable format to easily choose a part to edit.
                while True:
                    update_choice = input("\nEnter the part you want to update (name, email, session, date, phone number, group size or 0 to exit): ")
                    update_choice = update_choice.lower()
                    if update_choice == '0':
                        print("Reservation editing process cancelled.")
                        return
                    elif update_choice in ['name', 'email', 'session', 'date', 'phone number', 'group size']:
                        break
                    else:
                        print("Invalid choice. Please enter a valid option.")
                    
                # Update the chosen detail with the new detail updated.
                if update_choice == 'name':
                    name = input("Enter the new guest name (letters only): ")
                elif update_choice == 'email':
                    email_address = input("Enter the new email address: ")
                elif update_choice == 'session':
                    session = self.select_session()
                elif update_choice == 'date':
                    reservation_date = self.get_reservation_date()
                elif update_choice == 'phone number':
                    phone_number = self.get_valid_phone_number()
                elif update_choice == 'group size':
                    group_size = input("Enter the new group size: ")
                    group_size = 'Number of pax = ' + group_size  
                
                # Update the reservation details in the content list.
                content[chosen_index] = f"{reservation_date}|Session {session}|{name}|{email_address}|{phone_number}|{group_size}\n"
                
                # Write the updated reservation details back to the file.
                with open(file_path, "w") as file:
                    file.writelines(content)
                
                print("Reservation updated successfully.")
                self.update_reservation_data()
        except FileNotFoundError:
            print(f"Error: {file_path} file not found.")


class Menu:
    def generate_recommendations(self):
        # Generate random menu recommendations from text file content list.
        try:
            with open("Restaurant/menuItems_21071097.txt", "r") as file:
                menu_items = file.readlines()
                
            print("\nMenu Recommendations:")
            num_recommendations = int(input("How many meal recommendations would you like? "))
            if num_recommendations <= 0:
                print (f"Please enter a positive number.")
            elif num_recommendations > len(menu_items):
                print (f"Sorry, there are only {len(menu_items)} meal recommendation choices available.") # error counter when meal recommendation > meal available.
            else:
                recommendations = random.sample(menu_items, num_recommendations)
                for i, item in enumerate(recommendations, start=1):
                    print(f"{i}. {item.strip()}")
        except FileNotFoundError:
            print("Error: 'menuItems_21071097.txt' file not found.")
if __name__ == "__main__":
    reservations = Reservations()
    reservations.main_menu()

reservations = Reservations()
reservations.make_reservation()
reservations.print_reservations()    