class Major:
    def __init__(self, major_id, major_name, faculty_id):
        self.major_id = major_id
        self.major_name = major_name
        self.faculty_id = faculty_id

    def __repr__(self):
        return f"Major({self.major_id}, {self.major_name}, {self.faculty_id})"