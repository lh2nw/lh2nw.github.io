import random

class Vehicle:
    def __init__(self, vehicle_id, speed):
        self.vehicle_id = vehicle_id
        self.speed = speed
        self.battery = 100.0
        self.status = "Idle"

    def charge(self):
        self.battery = 100.0
        self.status = "Charging"

class GroundVehicle(Vehicle):
    def move(self):
        # Consumes 80% battery per km (as per your documentation)
        distance = random.uniform(0.1, 1.0)
        self.battery -= (distance * 80)
        self.battery = max(0, self.battery)
        self.status = f"Driving ({distance:.2f} km)"

class Drone(Vehicle):
    def move(self):
        # Requires 15% to fly; consumes 150% per km
        if self.battery < 15:
            self.status = "Low Battery - Cannot Fly"
            return
        distance = random.uniform(0.1, 0.5)
        self.battery -= (distance * 150)
        self.battery = max(0, self.battery)
        self.status = f"Flying ({distance:.2f} km)"

class UGV(Vehicle):
    def deliver(self, weight):
        # Battery consumption proportional to cargo weight
        consumption = 10 + (weight * 2)
        self.battery -= consumption
        self.battery = max(0, self.battery)
        self.status = f"Delivering {weight}kg cargo"
