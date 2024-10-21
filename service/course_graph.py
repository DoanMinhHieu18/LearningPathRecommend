from model.course import Course
from model.course_node import CourseNode
import networkx as nx

def create_course_tree(course_list):
    # Sort by semester
    sorted_courses = sorted(course_list, key=lambda c: c.semester)

    # Initialize root node
    init_course_node = Course(None, 'Semester 1', None, None, 1, None, None, None, False, None, None)
    root = CourseNode(init_course_node)

    current_semester = 1
    current_node = root
    
    # Travel Sorted_Courses to create Course Tree
    # Node semester n contains the subjects belonging to semester n and node semester n+1
    for course in sorted_courses:
        # If subject belonging other semester, create new node semester and add this node to new node semester
        if course.semester > current_semester:
            current_semester = course.semester
            
            # Create new node semester
            new_course_semester = Course(None, f'Semester {current_semester}', None, None, 1, None, None, None, False, None, None)
            new_node = CourseNode(new_course_semester)
            current_node.add_child(new_node)
            current_node = current_node.get_last_child()
            
            # Add this course to new node semeter
            new_course_node = CourseNode(course)
            current_node.add_child(new_course_node)
        else:
            # Add this course to current node semeter
            new_course_node = CourseNode(course)
            current_node.add_child(new_course_node)

    return root

def print_tree(node, level=0):
    indent = "  " * level
    print(f"{indent}{node.course_node.course_name}")
    for child in node.children:
        print_tree(child, level + 1)