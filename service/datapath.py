import os


class DataPath:
    def __init__(self):
        # Path 
        service_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(service_dir)
        data_dir = os.path.join(base_dir, "data")
        self.major_data_path = os.path.join(data_dir, "major.csv")
        self.course_software_engineering_path = os.path.join(data_dir, "course_software_engineering.csv")
        self.learn_log_path = os.path.join(data_dir, "learnerlog.csv")