# lift_prototype.py
# This program functions as a way to represent how an elevator works in a first person perspective view

'''
Explanation:
This program is designed to represent a first person POV of an elevator.
It doesn't take into account inputs at other floors when it's in operation
because it will take too much separate input screens.
There is a way, however, to combat this with random number generators, but 
it still raises an infinite loop risk and makes it confusing.
The unlucky numbers are listed as below to account for superstitious users.
The functions in this program is also equipped with fail-safes.
The program can be terminated by giving 0 in check_people_num() or by keyboard
interrupt with Ctrl+C.
'''

import os, time, random, sys

def clear_screen():

    # Clears terminal screen for both windows and unix based OS.

    os.system('clear' if os.name == 'posix' else 'cls')

def num_people_check():

    # Checks the number of people boarding the elevator
    # If the user inputs a 0, the program will terminate signaling
    # there is no one who wants to board the elevator

    while True:
        try:
            num_people = int(input("Ada berapa orang yang ingin naik lift? "))
            if num_people < 0:
                print("Maaf, silakan masukkan jumlah orang lagi.")
            elif num_people == 0:
                clear_screen()
                sys.exit()
            else:
                return num_people
        except ValueError:
            print("Maaf, silakan masukkan angka.")

def num_floor():

    # This function demands how many floors are there in the building.
    # Thanks to this function, this program can be dynamically executed.

    while True:
        try:
            num_floor = int(input("Ada berapa lantai dalam gedung ini? "))
            if num_floor < 2:
                print("Maaf, silakan memasukkan angka lebih dari 1.")
            elif num_floor > 100:
                print("Maaf, jumlah lantai telah melebihi batas")
            else:
                for i in range(num_floor):
                    if i+1 in unlucky_num:
                        num_floor += 1
                return num_floor
        except ValueError:
            clear_screen()
            print("Silakan masukkan angka."); time.sleep(1.2)

def overweight_check(num_people):

    # Lift capacity declaration

    max_weight = 800 
    total_weight = 0

    # The following is a random number generator that generates
    # an array of people's weight based on the average of Indonesian's.
    
    for i in range(num_people):
        total_weight += round(random.uniform(58.0, 68.9), 1)

    # Determines if the elevator is overweight or not.

    if  total_weight <= max_weight:
        return num_people, False

def check_position(num_floor):

    # This function demands the initial position of the user.
    # It's also equipped with a failsafe for ValueError

    while True:
        try:
            while True:
                position = int(input("Masukkan posisi anda: "))
                if position > num_floor or position < 1:
                    print("Maaf, lantai anda tidak nyata.")
                else:
                    return position
        except ValueError:
            print("Silakan masukkan angka."); time.sleep(1.2)
        
def check_destination(num_people, num_floor, position):

    # This function demands the destination of every user and it's equipped with a failsafe.
    # After that, it compiles it to a sorted list and determines the most efficient route to take.

    list_destination = list()
    while True:
        for i in range(num_people):
            while True:
                try:
                    destination = int(input(f"Orang ke-{i+1} ingin ke lantai berapa? "))
                    if destination > num_floor or destination == position or destination < 1 or destination in unlucky_num:
                        print("Maaf, silakan masukkan tujuan anda lagi.")
                    else:
                        if destination not in list_destination:
                            list_destination.append(destination)
                        break
                except ValueError:
                    print("Silakan masukkan angka.")
        list_destination.sort()
        if (list_destination[-1] - position) + (list_destination[-1] - list_destination[0]) < (position - list_destination[0]) + (list_destination[-1] - list_destination[0]):
            return list_destination, True
        return list_destination, False

def elevator_doors(open):

    # This function controls the movement of the elevator doors.

    if open:
        print("Pintu lift terbuka.")
        time.sleep(1)

    # Before closing the doors, the function will ask if there's something
    # holding the door from closing.
        
    else:
        while True:
            sensor = str(input("Apakah ada yang menghalangi pintu? (Ya/Tidak) "))
            if sensor.lower() == 'tidak':
                clear_screen()
                print("Pintu lift akan tertutup.")
                time.sleep(1)
                break
            elif sensor.lower() == 'ya':
                pass
            else:
                print("Jawaban hanya Ya/Tidak.")

def elevator_movement(position, destination, is_up):

    # This function prints the movement of the elevator according to its direction.
    # After arriving at one of the destinations, it removes the destination to prevent
    # going to the same floor twice.
    # In the end, it will return the current position so it this program could form
    # an infinite loop.

    if is_up: # If the elevator is going up first...
        for i in range(position, destination[-1]):
            if i+1 not in unlucky_num: # Doesn't prints unlucky numbers
                for j in range(3):
                    for k in range(4):
                        clear_screen()
                        print(f"Lift bergerak ke lantai {i+1}{'.'*k}")
                        time.sleep(0.3)
                if i+1 in destination:
                    destination.remove(i+1) # removes the destination
                    position = i+1 # Updates the position
                    elevator_doors(True)
                    print(f"Lift telah sampai di lantai {i+1}.")
                    time.sleep(2)
                    if len(destination) > 0:
                        elevator_doors(False) # prevents door closing when there's no on left

        for i in range(position, destination[0]-2, -1):
            if i+1 not in unlucky_num:
                for j in range(3):
                    for k in range(4):
                        clear_screen()
                        print(f"Lift bergerak ke lantai {i+1}{'.'*k}")
                        time.sleep(0.3)
                if i+1 in destination:
                    destination.remove(i+1)
                    position = i+1
                    elevator_doors(True)
                    print(f"Lift telah sampai di lantai {i+1}.")
                    time.sleep(2)
                    if len(destination) > 0:
                        elevator_doors(False)

    else:
        for i in range(position-1, destination[0]-2, -1):
            if i+1 not in unlucky_num:
                for j in range(3):
                    for k in range(4):
                        clear_screen()
                        print(f"Lift bergerak ke lantai {i+1}{'.'*k}")
                        time.sleep(0.3)
                if i+1 in destination:
                    destination.remove(i+1)
                    position = i+1
                    elevator_doors(True)
                    print(f"Lift telah sampai di lantai {i+1}.")
                    time.sleep(2)
                    if len(destination) > 0:
                        elevator_doors(False)

        for i in range(position, destination[-1]):
            if i+1 not in unlucky_num:
                for j in range(3):
                    for k in range(4):
                        clear_screen()
                        print(f"Lift bergerak ke lantai {i+1}{'.'*k}")
                        time.sleep(0.3)
                if i+1 in destination:
                    destination.remove(i+1)
                    position = i+1
                    elevator_doors(True)
                    print(f"Lift telah sampai di lantai {i+1}.")
                    time.sleep(2)
                    if len(destination) > 0:
                        elevator_doors(False)
    return position

def inside_check(num_floor):

    # This function does most of the calling.

    position = check_position(num_floor)
    while True:
        overweight = True
        while overweight:
            try:
                num_people, overweight = overweight_check(num_people_check())
                clear_screen()
            except TypeError:
                print("Lift overload.")
        elevator_doors(True)
        print("Halo, selamat datang di lift ITB.")
        time.sleep(1)
        destination, is_up = check_destination(num_people, num_floor, position)
        elevator_doors(False)
        position = elevator_movement(position, destination, is_up)

if __name__ == '__main__':
    try:
        unlucky_num = [4, 9, 13, 14, 24, 34, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 54, 64, 74, 84, 94]
        clear_screen()
        inside_check(num_floor())
    except KeyboardInterrupt:
        clear_screen()
