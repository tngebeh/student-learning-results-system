"""
Student Learning and Results Management System
Domain: Education
Course: Object-Oriented Programming

This program demonstrates:
1. Classes and objects
2. Attributes and instance methods
3. A class method
4. A list data structure
5. Interaction between objects
6. Record addition and display
7. Input validation and privacy-conscious design
"""


class Course:
    """Represent a course offered by an educational institution."""

    total_courses = 0

    def __init__(self, course_code, course_name):
        if not course_code.strip() or not course_name.strip():
            raise ValueError("Course code and name cannot be empty.")

        self.course_code = course_code.strip().upper()
        self.course_name = course_name.strip()
        Course.total_courses += 1

    def display_course(self):
        """Display the course details."""
        return f"{self.course_code} - {self.course_name}"

    @classmethod
    def get_total_courses(cls):
        """Return the number of Course objects created."""
        return cls.total_courses


class Student:
    """Represent a student and their course results."""

    total_students = 0

    def __init__(self, student_id, name, level):
        if not student_id.strip() or not name.strip():
            raise ValueError("Student ID and name cannot be empty.")

        if not level.strip():
            raise ValueError("Student level cannot be empty.")

        self.student_id = student_id.strip().upper()
        self.name = name.strip()
        self.level = level.strip()
        self.results = {}

        Student.total_students += 1

    def enroll(self, course):
        """Enroll the student in a Course object."""
        if not isinstance(course, Course):
            raise TypeError("Enrollment requires a Course object.")

        if course.course_code in self.results:
            return False

        self.results[course.course_code] = {
            "course": course,
            "mark": None
        }
        return True

    def record_mark(self, course_code, mark):
        """Record a mark for a course in which the student is enrolled."""
        course_code = course_code.strip().upper()

        if course_code not in self.results:
            raise ValueError("Student is not enrolled in this course.")

        if not isinstance(mark, (int, float)) or isinstance(mark, bool):
            raise ValueError("Mark must be a number.")

        if not 0 <= mark <= 100:
            raise ValueError("Mark must be between 0 and 100.")

        self.results[course_code]["mark"] = mark

    def calculate_grade(self, mark):
        """Calculate the grade from a numerical mark."""
        if not isinstance(mark, (int, float)) or isinstance(mark, bool):
            raise ValueError("Mark must be a number.")

        if not 0 <= mark <= 100:
            raise ValueError("Mark must be between 0 and 100.")

        if mark >= 80:
            return "A"
        elif mark >= 70:
            return "B"
        elif mark >= 60:
            return "C"
        elif mark >= 50:
            return "D"
        else:
            return "F"

    def display_record(self):
        """Display the student's details and course results."""
        print("-" * 55)
        print(f"Student ID: {self.student_id}")
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print("Course Results:")

        if not self.results:
            print("  No courses registered.")

        for course_code, details in self.results.items():
            course = details["course"]
            mark = details["mark"]

            if mark is None:
                print(f"  {course.display_course()}: Not yet graded")
            else:
                grade = self.calculate_grade(mark)
                print(
                    f"  {course.display_course()}: "
                    f"{mark}/100 | Grade: {grade}"
                )

        print("-" * 55)

    @classmethod
    def get_total_students(cls):
        """Return the number of Student objects created."""
        return cls.total_students


# Task 2: Use a list to store multiple Student objects.
student_records = []


def add_student(student):
    """Add a Student object to the student list."""
    if not isinstance(student, Student):
        raise TypeError("Only Student objects can be added.")

    for existing_student in student_records:
        if existing_student.student_id == student.student_id:
            print("Error: This student ID already exists.")
            return False

    student_records.append(student)
    print("Student record added successfully.")
    return True


def display_all_students():
    """Display every student stored in the list."""
    if not student_records:
        print("No student records are available.")
        return

    for student in student_records:
        student.display_record()


def find_student(student_id):
    """Find a student by their unique ID."""
    student_id = student_id.strip().upper()

    for student in student_records:
        if student.student_id == student_id:
            return student

    return None


def get_non_empty_input(prompt):
    """Keep asking until the user enters a non-empty value."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def create_course(courses):
    """Create and store a new Course object."""
    code = get_non_empty_input("Enter course code: ").upper()

    if code in courses:
        print("This course code already exists.")
        return

    name = get_non_empty_input("Enter course name: ")
    courses[code] = Course(code, name)
    print("Course created successfully.")


def register_student(courses):
    """Collect details and register a new student."""
    student_id = get_non_empty_input("Enter student ID: ").upper()

    if find_student(student_id) is not None:
        print("A student with this ID already exists.")
        return

    name = get_non_empty_input("Enter student name: ")
    level = get_non_empty_input("Enter student level: ")

    student = Student(student_id, name, level)

    if not add_student(student):
        return

    print("\nAvailable courses:")

    if not courses:
        print("No courses available yet.")
        return

    for course in courses.values():
        print(course.display_course())

    course_code = input(
        "Enter a course code to enroll the student "
        "(or press Enter to skip): "
    ).strip().upper()

    if course_code:
        if course_code not in courses:
            print("Course not found. Student remains registered.")
        else:
            student.enroll(courses[course_code])
            print("Student enrolled successfully.")


def enter_result():
    """Record a mark for an existing student."""
    student_id = input("Enter student ID: ").strip()
    student = find_student(student_id)

    if student is None:
        print("Student not found.")
        return

    if not student.results:
        print("This student is not enrolled in any course.")
        return

    print("Enrolled courses:")
    for code, details in student.results.items():
        print(f"{code} - {details['course'].course_name}")

    course_code = input("Enter course code: ").strip().upper()

    if course_code not in student.results:
        print("The student is not enrolled in that course.")
        return

    try:
        mark = float(input("Enter mark (0-100): "))
        student.record_mark(course_code, mark)
        print("Result recorded successfully.")
    except ValueError as error:
        print(f"Error: {error}")


def show_menu():
    """Display the main program menu."""
    print("\nSTUDENT LEARNING AND RESULTS MANAGEMENT SYSTEM")
    print("1. Add a course")
    print("2. Register a student")
    print("3. Record a result")
    print("4. Display all students")
    print("5. Search for a student")
    print("6. Display system statistics")
    print("0. Exit")


def main():
    """Run the main application."""
    courses = {}

    # Demonstration data using fictional students.
    programming = Course("OOP101", "Object-Oriented Programming")
    database = Course("DBS101", "Database Systems")

    courses[programming.course_code] = programming
    courses[database.course_code] = database

    student_one = Student("ST001", "Musa Kamara", "Year 2")
    student_two = Student("ST002", "Fatmata Sesay", "Year 2")

    student_one.enroll(programming)
    student_one.enroll(database)
    student_two.enroll(programming)

    student_one.record_mark("OOP101", 85)
    student_one.record_mark("DBS101", 74)
    student_two.record_mark("OOP101", 68)

    add_student(student_one)
    add_student(student_two)

    while True:
        show_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            create_course(courses)

        elif choice == "2":
            register_student(courses)

        elif choice == "3":
            enter_result()

        elif choice == "4":
            display_all_students()

        elif choice == "5":
            student_id = input("Enter student ID: ")
            student = find_student(student_id)

            if student:
                student.display_record()
            else:
                print("Student not found.")

        elif choice == "6":
            print(f"Student objects created: "
                  f"{Student.get_total_students()}")
            print(f"Course objects created: "
                  f"{Course.get_total_courses()}")
            print(f"Registered student records: "
                  f"{len(student_records)}")

        elif choice == "0":
            print("Thank you for using the system.")
            break

        else:
            print("Invalid choice. Please select a listed option.")


if __name__ == "__main__":
    main()