import csv
from model.course import Course
from model.learn_log import LearnerLog
from model.major import Major
from service.datapath import DataPath

def read_majors_from_csv(file_path):
    majors = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) == 3: # Make sure each row has 3 elements
                major_id, major_name, faculty_id = row
                major = Major(int(major_id), major_name, int(faculty_id))
                majors.append(major)
            else:
                print(f"Skipped invalid row: {row}")
    return majors

def read_courses_from_csv(learner_major):
    learner_major = int(learner_major)
    data_path = DataPath()
    if learner_major == 5:
        file_path = data_path.course_software_engineering_path
    else:
        return "Chua co thong tin"
    courses = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) == 10:  # Make sure each row has 8 elements
                course_id, course_name, major_id, prerequisite, semester, count_learner, average_score, credit, is_group_c, is_group_d = row
                course = Course(
                    course_id,
                    course_name,
                    int(major_id),
                    prerequisite if prerequisite else None,  # If there is no prerequisite then set None
                    int(semester),
                    int(count_learner),
                    float(average_score),
                    int(credit),
                    True, 
                    True if is_group_c == 1 else False,
                    True if is_group_d == 1 else False
                )
                courses.append(course)
            else:
                print(f"Skipped invalid row: {row}")
    return courses

def read_learn_logs_from_csv(file_path):
    learner_logs = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) == 6:  # Make sure each row has 4 elements
                student_id, course_id, score, count_learns, course_name, credit = row
                log = LearnerLog(
                    int(student_id),
                    course_id,
                    float(score) if score != "MT" else 10,
                    int(count_learns),
                    course_name,
                    int(credit)
                )
                learner_logs.append(log)
            else:
                print(f"Skipped invalid row: {row}")
    return learner_logs
