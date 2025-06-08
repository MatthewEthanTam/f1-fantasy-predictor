"""
Main module for the project.    
"""
from openf1 import OpenF1

if __name__ == "__main__":
    openf1 = OpenF1()

    # print(openf1.get_latest_meeting())
    print(openf1.get_latest_meetings_session_keys_with_sessions_type())