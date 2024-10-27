from model.course import Course
learning_path = []
current_semester = 0
course_group_c = []
num_course_group_c = 0
num_course_group_d = 0
learn_summer_semester = False
credit_summer_semester = 0
total_course_group_c = 0
### cac van de chua giai quyet
### goi y nhom c
class LearningPathElement:
    def __init__(self, semester):
        self.semester = semester
        self.courses = []
        self.credit = 0
        
### Unlearned_log contains unlearned_subject
def recommend(learner, learner_log, unlearned_log, course_graph, semester):
    global learning_path
    global current_semester
    global learn_summer_semester
    global credit_summer_semester
    global num_course_group_c
    global total_course_group_c
    ### Caculate number of course group c
    for course in unlearned_log:
        if course.is_group_c == True:
            total_course_group_c = total_course_group_c + 1
            
    if learner.learn_summer_semester == True:
        learn_summer_semester = True
        credit_summer_semester = learner.summer_semester_credit
    num_course_group_c = 5 + 3 - learner.number_of_free_elective_credit
    if num_course_group_c > total_course_group_c/2:
        return "Môn nhóm C không đủ"
    current_semester = semester
    course_id_leaner_log = [log.course_id for log in learner_log]
    add_english_course_to_learning_path(learner.learner_english_level, course_id_leaner_log, unlearned_log)
    travel_course_graph(learner, course_id_leaner_log, unlearned_log, course_graph)
    learner_log = sorted(learner_log, key=lambda log: log.score)
    # global learning_path
    # for semester in learning_path:
    #     if int(semester.semester)%10 == 3:
    #         continue
    #     if semester.credit<14:
    #         for log in learner_log:
    #             if int(semester.credit) + int(log.credit) <= 18:
    #                 semester.courses.append(log)
    #                 learner_log.remove(log)
    #                 semester.credit = semester.credit + log.credit
    #                 if semester.credit >= 14:
    #                     break
    return learning_path
    
### Add english 
### Travel course and add new course to learning_path
### Step 1: if it is not course not ---> recursive
### Step 2: if it is course node ---> check is_subject_learned
### Step 3: Check prerequisite
def travel_course_graph(learner, learner_log, unlearned_log, course_graph):
    global course_group_c
    global num_course_group_c
    global num_course_group_d
            
    for child_node in course_graph.children:
        if child_node.course_node.is_course == False:
            travel_course_graph(learner, learner_log, unlearned_log, child_node)
        else: 
            if is_subject_learned(child_node.course_node.course_id, learner_log, unlearned_log):
                if child_node.course_node.is_group_c == True and child_node.course_node.course_id not in course_group_c:
                    course_group_c.append(child_node.course_node.course_id)
                continue
            else:
                ### Check group c
                if child_node.course_node.is_group_c == True and len(course_group_c) == num_course_group_c:
                    continue
                
                
                ### Check group d
                if child_node.course_node.is_group_d == True and num_course_group_d < 4:
                    num_course_group_d = num_course_group_d + 1
                    continue
                elif child_node.course_node.is_group_d == True and num_course_group_d == 4:
                    child_node.course_node.course_name = "Tín chỉ tự chọn nhóm D"
                    check_prerequisite_and_add_learning_path(learner.learner_english_level, child_node.course_node,learner_log, unlearned_log)
                    continue
                
                ### Check free elective course
                if child_node.course_node.course_id in ["TCTD1", "TCTD2", "TCTD3"]:
                    if learner.number_of_free_elective_credit > 0:
                        learner.number_of_free_elective_credit = learner.number_of_free_elective_credit - 1
                        check_prerequisite_and_add_learning_path(learner.learner_english_level, child_node.course_node,learner_log, unlearned_log)
                    continue
                
                check_prerequisite_and_add_learning_path(learner.learner_english_level, child_node.course_node,learner_log, unlearned_log)
                if child_node.course_node.is_group_c == True and child_node.course_node.course_id not in course_group_c:
                    course_group_c.append(child_node.course_node.course_id)
    
def add_english_course_to_learning_path(learner_english_level, learner_log, unlearned_log):
    global learning_path
    english_1 = Course("LA1003", "Anh văn 1", 5, None, 1, 0, 0, 2, True, False, False)
    english_2 = Course("LA1005", "Anh văn 2", 5, "LA1003", 2, 0, 0, 2, True, False, False)
    english_3 = Course("LA1007", "Anh văn 3", 5, "LA1005", 3, 0, 0, 2, True, False, False)
    english_4 = Course("LA1009", "Anh văn 4", 5, "LA1009", 4, 0, 0, 2, True, False, False)
    english_course = [english_1, english_2, english_3, english_4]
    unlearned_course = []
    for course in english_course:
        learned = False
        for unlearned_couse in unlearned_log:
            if unlearned_couse.course_name == course.course_name:
                unlearned_log.remove(unlearned_couse)
                break
        for log in learner_log:
            if log == course.course_id:
                learned = True
                break
        if not learned:
            unlearned_course.append(course)
        
    for course in unlearned_course:
        global current_semester
        learning_path_element = LearningPathElement(current_semester)
        learning_path_element.courses.append(course)
        learning_path_element.credit = 2
        learning_path.append(learning_path_element)
        current_semester = next_semester(current_semester)
        
### If course was learned, remove it unlearned_log
def is_subject_learned(course__id, learner_log, unlearned_log):
    if course__id in ["LA1003", "LA1005", "LA1007", "LA1009"]:
        return True
    if course__id in learner_log:
        for course in unlearned_log:
            if course.course_id == course__id:
                unlearned_log.remove(course)
                return True
    return False
    
def check_prerequisite_and_add_learning_path(english_level, course, leaner_log, unlearned_log):
    ### Chech subject prerequisite
    ### If this course has subject prerequisite: 2 cases
    ### Case 1: Subject prerequisite was learned (In leaner_log) -> add learning_path this semester
    ### Case 2: Subject prerequisite was recommend (Not in unlearned_log) -> add learning_path next semester
    english_course = get_english_course_level(course.course_id)
    if course.prerequisite != None and english_level >= english_course:
        if course.prerequisite in leaner_log:
            add_course_to_learning_path_in_case_prerequisite_in_lean_log(course, unlearned_log)
        else:
            add_course_to_learning_path_in_case_prerequisite_recommended(course, unlearned_log)
    
    ### Check English
    if course.prerequisite == None and english_level < english_course:
        add_course_to_learning_path_with_english(course, english_course, unlearned_log)
    
    ### Check subject prerequisite and English
    if course.prerequisite != None and english_level < english_course:
        if course.prerequisite in leaner_log:
            add_course_to_learning_path_with_english(course, english_course, unlearned_log)
        else:
            add_course_to_learning_path_with_prerequisite_and_english(course, english_course, unlearned_log)
    
    if course.prerequisite == None and english_level >= english_course:
        add_course_to_learning_path(course, unlearned_log)
            
def next_semester(semester):
    if semester%10 == 1:
        return semester + 1
    if semester%10 == 2:
        global learn_summer_semester
        if learn_summer_semester:
            return semester + 1
        return semester + 10 - 1
    if semester%10 == 3:
        return semester + 10 - 2
     
def get_english_course_level(course_id):
    if  course_id == "DATH":
        return 3
    if course_id == "DADN":
        return 3
    if course_id in ["TCTD1", "TCTD2", "TCTD3"]:
        return 1
    return int(course_id[2])
            
def add_course_to_learning_path_in_case_prerequisite_in_lean_log(course, unlearned_log):
    ### Add any semester has total credit <= 18
    ### After add successfull, remove this course from unlearned_log
    ### If not any semester can add, create new node and add course to this new node
    global learning_path
    added_course = False
    for element in learning_path:
        if element.credit + course.credit <= (18 if int(element.semester)%10 != 3 else int(credit_summer_semester)):
            element.courses.append(course)
            added_course = True
            element.credit = element.credit + course.credit
            for unlearned_couse in unlearned_log:
                if unlearned_couse.course_id == course.course_id:
                    unlearned_log.remove(course)
                    break
            break
    if not added_course:
        global current_semester
        current_semester = next_semester(learning_path[-1].semester)
        learning_path_element = LearningPathElement(current_semester)
        learning_path_element.courses.append(course)
        learning_path_element.credit = course.credit
        learning_path.append(learning_path_element)
        
def add_course_to_learning_path_in_case_prerequisite_recommended(course, unlearned_log):
    ### Find semester has prerequisite
    ### Add any semester has total credit <= 18
    ### After add successfull, remove this course from unlearned_log
    ### If not any semester can add, create new node and add course to this new node
    global learning_path
    find_prerequisite = False
    added_course = False
    for element in learning_path:
        if not find_prerequisite:
            for element_course in element.courses:
                if element_course.course_id == course.prerequisite:
                    find_prerequisite = True
                    break
        else:
            if element.credit + course.credit <= (18 if int(element.semester)%10 != 3 else int(credit_summer_semester)):
                element.courses.append(course)
                added_course = True
                element.credit = element.credit + course.credit
                for unlearned_couse in unlearned_log:
                    if unlearned_couse.course_id == course.course_id:
                        unlearned_log.remove(course)
                        break
                break
    if not added_course:
        global current_semester
        current_semester = next_semester(learning_path[-1].semester)
        learning_path_element = LearningPathElement(current_semester)
        learning_path_element.courses.append(course)
        learning_path_element.credit = course.credit
        learning_path.append(learning_path_element)
        
def add_course_to_learning_path_with_english(course, english_course, unlearned_log):
    ### Find semester has english_course
    ### Add any semester has total credit <= 18
    ### After add successfull, remove this course from unlearned_log
    ### If not any semester can add, create new node and add course to this new node
    global learning_path
    find_english_course = False
    added_course = False
    if english_course == 1:
        english_course = None
    if english_course == 2:
        english_course = "Anh văn 2"
    if english_course == 3:
        english_course = "Anh văn 3"
    if english_course == 4:
        english_course = "Anh văn 4"
    for element in learning_path:
        if not find_english_course:
            for element_course in element.courses:
                if element_course.course_name == english_course:
                    find_english_course = True
                    break
        else:
            if element.credit + course.credit <= (18 if int(element.semester)%10 != 3 else int(credit_summer_semester)):
                element.courses.append(course)
                added_course = True
                element.credit = element.credit + course.credit
                for unlearned_couse in unlearned_log:
                    if unlearned_couse.course_id == course.course_id:
                        unlearned_log.remove(course)
                        break
                break
    if not added_course:
        global current_semester
        current_semester = next_semester(learning_path[-1].semester)
        learning_path_element = LearningPathElement(current_semester)
        learning_path_element.courses.append(course)
        learning_path_element.credit = course.credit
        learning_path.append(learning_path_element)
        
def add_course_to_learning_path_with_prerequisite_and_english(course, english_course, unlearned_log):
    ### Find semester has prerequisite and english
    ### Add any semester has total credit <= 18
    ### After add successfull, remove this course from unlearned_log
    ### If not any semester can add, create new node and add course to this new node
    global learning_path
    find_prerequisite = False
    find_english_course = False
    added_course = False
    for element in learning_path:
        if not find_prerequisite or not find_english_course:
            for element_course in element.courses:
                if element_course.course_id == course.prerequisite:
                    find_prerequisite = True
                if element_course.course_name == english_course:
                    find_english_course = True
                if find_english_course and find_prerequisite:
                    break    
        else:
            if element.credit + course.credit <= (18 if int(element.semester)%10 != 3 else int(credit_summer_semester)):
                element.courses.append(course)
                added_course = True
                element.credit = element.credit + course.credit
                for unlearned_couse in unlearned_log:
                    if unlearned_couse.course_id == course.course_id:
                        unlearned_log.remove(course)
                        break
                break
    if not added_course:
        global current_semester
        current_semester = next_semester(learning_path[-1].semester)
        learning_path_element = LearningPathElement(current_semester)
        learning_path_element.courses.append(course)
        learning_path_element.credit = course.credit
        learning_path.append(learning_path_element)
        
def add_course_to_learning_path(course, unlearned_log):
    ### Add any semester has total credit <= 18
    ### After add successfull, remove this course from unlearned_log
    ### If not any semester can add, create new node and add course to this new node
    global learning_path
    added_course = False
    for element in learning_path:
        if element.credit + course.credit <= (18 if int(element.semester)%10 != 3 else int(credit_summer_semester)):
            element.courses.append(course)
            added_course = True
            element.credit = element.credit + course.credit
            for unlearned_couse in unlearned_log:
                if unlearned_couse.course_id == course.course_id:
                    unlearned_log.remove(course)
                    break
            break
    if not added_course:
        global current_semester
        if len(learning_path) == 0:
            learning_path_element = LearningPathElement(current_semester)
            learning_path_element.courses.append(course)
            learning_path_element.credit = course.credit
            learning_path.append(learning_path_element)
        else:
            current_semester = next_semester(current_semester)
            learning_path_element = LearningPathElement(current_semester)
            learning_path_element.courses.append(course)
            learning_path_element.credit = course.credit
            learning_path.append(learning_path_element)
            
# def print_learning_path(learning_path_recommend):
#     for semester in learning_path_recommend:
#         print("----------" + str(semester.semester) + "-----------------")
#         for course in semester.courses:
#             print(course.course_name)

# def print_unlearned_log(log):
#     for ele in log:
#         print(ele)