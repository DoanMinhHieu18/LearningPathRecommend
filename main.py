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
    
    ### Get data from Learner Input
    learner = Learner()
    
    ### Get Learner Log
    learner_log = [log for log in learn_log if log.student_id == learner.learner_mssv]
    
    ### Get Learner Major Course
    course_list = ReadFile.read_courses_from_csv(learner.learner_major)
    
    ### get course group c in course list
    course_group_c = [course for course in course_list if course.is_group_c]
    
    ### get last 3 semester
    last_3_semester = get_last_3_semester(241)
    
    ### Filter group c subjects studied in the last 3 semesters
    course_group_c = resort_course_group_c(course_group_c, last_3_semester, learn_log)
    
    ### Replace the group c subjects in the course list with the group c subjects that have been studied in the last 3 semesters
    course_list = replace_sublistcourse(course_list, course_group_c)
    
    if course_list == "Chua co thong tin":
        print(course_list)
        return
    
    ### Create Course Graph
    course_graph = CourseGraph.create_course_tree(course_list)
    # CourseGraph.print_tree(course_graph)
    
    ### Recommend Learing Path 
    learning_path_recommend = Recommend.recommend(learner, learner_log, course_list, course_graph, 241)
    print_learning_path(learning_path_recommend)

def get_last_3_semester(current_semester):
    if current_semester % 10 == 1:
        return [current_semester - 20 + 1, current_semester - 10, current_semester - 10 + 1]
    if current_semester % 10 == 2:
        return [current_semester - 10 - 1, current_semester - 10, current_semester - 1]
    if current_semester % 10 == 3:
        return [current_semester - 10 - 1, current_semester - 2, current_semester - 1]

def resort_course_group_c(course_group_c, last_3_semester, learn_log):
    course_group_c_resort = []
    course_group_c_not_in_last_3_semester = []
    for course in course_group_c:
        check = False
        for log in learn_log:
            if course.course_id == log.course_id and log.semester in last_3_semester:
                course_group_c_resort.append(course)
                check = True
                break
        if not check:
            course.note = "Mon hoc chua duoc mo trong 3 hoc ky chinh gan nhat"
            course_group_c_not_in_last_3_semester.append(course)
    return course_group_c_resort + course_group_c_not_in_last_3_semester

def replace_sublistcourse(course_list, course_group_c):
    indices = [course_list.index(course) for course in course_group_c if course in course_list]
    if len(indices) == 0:
        print("Không có phần tử nào trong course_list giống với course_group_c.")
        return course_list
    elif len(indices) == 1:
        return course_list
    elif len(indices) == 2:
        if indices[0] + 1 == indices[1]:
            start = indices[0]
            end = indices[1] + 1
            course_list[start:end] = course_group_c
            return course_list
        else:
            print("Các phần tử của course_group_c không liên tiếp trong course_list.")
            return course_list
    elif all(indices[i] + 1 == indices[i + 1] for i in range(len(indices) - 1)):
        start = indices[0]
        end = indices[-1] + 1
        course_list[start:end] = course_group_c
        return course_list
    else:
        print("Các phần tử của course_group_c không liên tiếp trong course_list.")
        return course_list

def print_learning_path(learning_path_recommend):
    try:
        for semester in learning_path_recommend:
            print("----------" + str(semester.semester) + "-----------------")
            for course in semester.courses:
                if course.note:
                    print(course.course_name + " - " + course.note)
                else:
                    print(course.course_name)
            print("Tong so tin chi trong hoc ky: " + str(semester.credit))
        print("")
    except:
        print(learning_path_recommend)
        

main()