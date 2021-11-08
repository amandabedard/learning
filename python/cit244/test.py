def courseInfo():
    courseRooms = {}
    courseInstructors = {}
    
    inputCourses = input(f"Do you have a course to enter (yes/no): ")
    while(inputCourses == "yes"):
        course = input(f"Course: ")
        roomNum = input(f"Room number: ")
        instructor = input(f"Instructor: ")

        courseRooms[course] = roomNum
        courseInstructors[course] = instructor

        inputCourses = input(f"Do you have another course to enter (yes/no): ")
    
    getInfo = input(f"Enter a course number to get information (q to quit): ")
    while(getInfo != 'q'):
        if getInfo in courseRooms and getInfo in courseInstructors:
            print(f"Info for course {getInfo}: \n Room: {courseRooms[getInfo]}  Instructor:{courseInstructors[getInfo]}")
        else:
            print(f"No info found for course {getInfo}")
        getInfo = input(f"Enter a course number to get information (q to quit): ")


courseInfo()