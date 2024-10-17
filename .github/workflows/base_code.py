# Standardise important indexes and file directory to be used
# Also makes the code more flexible to changes in e.g. swapped columns, filepath
FILE_DIRECTORY = "records.csv"
TUTORIAL_GROUP_INDEX = 0
SCHOOL_INDEX = 2
GENDER_INDEX = 4
GPA_INDEX = 5


# This function extracts the student info and saves it as a list
def extract_student_info(file_location):
    
    # Initialise a list to hold file info
    file_information = []

    # Read the file
    with open(file_location, 'r') as csvfile:

        # Iterate through the lines in the file
        for lines in csvfile:

            # Save the cleaned column info of each row to a list
            file_rows = lines.strip("\n").split(",")

            # Add each row of info to the consolidated file info
            file_information.append(file_rows)

        header = file_information[0]
        student_records = file_information[1:]

    return header, student_records

header, student_records = extract_student_info(FILE_DIRECTORY)
# print(f"Student Record: {student_records}")


# This function takes in a list of student records and groups the records based on the index of criteria specified
def group_records(records, index):
    groups = {}
    for record in records:
        # If tutorial group exists, add student to list, else create a new tutorial group
        if record[index] in groups:
            groups[record[index]].append(record)
        else:
            groups[record[index]] = [record]
    return groups


def calculate_males(student_list):
    males = 0
    for student in student_list:
        if student[GENDER_INDEX] == "Male":
            males += 1
    return males


tutorial_groups = group_records(student_records, TUTORIAL_GROUP_INDEX)
# print(tutorial_groups)

for tutorial_number, students in tutorial_groups.items():
    print(f"Tutorial Number: {tutorial_number}")
    print(f"Students: {students}")

    number_of_males = calculate_males(students)
    print(f"Number of Males: {number_of_males}")

    # dictionary of keys as schools and values as students
    students_grouped_by_schools = group_records(students, SCHOOL_INDEX)
    print(students_grouped_by_schools)

# To continue using statistics and dictionary of tutorial groups
# Add Algorithm Here
