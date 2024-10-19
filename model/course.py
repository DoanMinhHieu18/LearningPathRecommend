class Course:
    def __init__(self, course_id, course_name, major_id, prerequisite, semester, count_learner, average_score, credit, is_course):
        self.course_id = course_id
        self.course_name = course_name 
        self.major_id = major_id 
        self.prerequisite = prerequisite
        self.semester = semester
        self.count_learner = count_learner 
        self.average_score = average_score
        self.credit = credit
        self.is_course = is_course
        
    def __repr__(self):
        return (f"Course(course_id={self.course_id}, course_name='{self.course_name}', major_id={self.major_id}, "
                f"prerequisite={self.prerequisite}, semester={self.semester}, count_learner={self.count_learner}, "
                f"average_score={self.average_score}, credit={self.credit}, is_course={self.is_course})")