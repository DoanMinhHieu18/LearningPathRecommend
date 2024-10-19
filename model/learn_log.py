class LearnerLog:
    def __init__(self, student_id, course_id, score, count_learns):
        self.student_id = student_id
        self.course_id = course_id
        self.score = score
        self.count_learns = count_learns
        
    def __repr__(self):
        return (f"LearnerLog(student_id={self.student_id}, course_id={self.course_id}, "
                f"score={self.score}, count_learns={self.count_learns})")