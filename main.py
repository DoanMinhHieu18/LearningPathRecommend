from model.learner import Learner
from service.datapath import DataPath
import service.readfile as ReadFile
import service.course_graph as CourseGraph
import service.recommend as Recommend

def main():
    ### Get data path
    data_path = DataPath()
    
    ### Get Major and Log data
    majors_list = ReadFile.read_majors_from_csv(data_path.major_data_path)
    learn_log = ReadFile.read_learn_logs_from_csv(data_path.learn_log_path)
    
    ### Calculate grade point average for a subject
    ### hihi chua lam
    
    
    ### Get data from Learner Input
    learner = Learner(majors_list)
    
    ### Get Learner Log
    learner_log = [log for log in learn_log if log.student_id == learner.learner_mssv]
    
    ### Get Learner Major Course
    course_list = ReadFile.read_courses_from_csv(learner.learner_major)
    if course_list == "Chua co thong tin":
        print(course_list)
        return
    
    ### Create Course Graph
    course_graph = CourseGraph.create_course_tree(course_list)
    # CourseGraph.print_tree(course_graph)
    
    ### Recommend Learing Path 
    learning_path_recommend = Recommend.recommend(learner, learner_log, course_list, course_graph, 241)
    print_learning_path(learning_path_recommend)

def print_learning_path(learning_path_recommend):
    for semester in learning_path_recommend:
        print("----------" + str(semester.semester) + "-----------------")
        for course in semester.courses:
            print(course.course_name)
        print("Tong so tin chi trong hoc ky: " + str(semester.credit))

main()