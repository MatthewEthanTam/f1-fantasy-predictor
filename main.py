"""
Main module for the project.    
"""
from src.openf1 import OpenF1

if __name__ == "__main__":
    openf1 = OpenF1()

    openf1.get_laps_per_session()