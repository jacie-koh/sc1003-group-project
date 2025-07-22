import matplotlib.pyplot as plt

# Initialise list for .csv data
mega_data = []
# Read and append .csv data to the list
with open("records.csv") as file:
    for line in file:
        mega_data.append(line.strip().split(","))

# Extract header and data rows from the .csv
header = mega_data[0]
rows = mega_data[1:]

# Group data by tutorial group
grouped_data = {}
for row in rows:
    tutorial_group = row[0]
    if tutorial_group not in grouped_data:
        grouped_data[tutorial_group] = []
    grouped_data[tutorial_group].append(row)

"""
Pre-Grouping Visualisation
"""

"""
Grouping Algorithm
"""
# Finding out the representative diversity of each tutorial group, by obtaining:
# 1. Average CGPA
# 2. Gender distribution
# 3. School diversity

# This function takes in the list of all students in the tutorial group as a 2D array,
# Returns and prints 1. mean GPA, 2. gender ratio, and 3. number of schools as a dictionary
def analyze_tutorial_groups(data):
    analysis = {}

    # Process each row
    for row in data:
        tutorial_group = row[0]
        gender = row[4]
        cgpa = float(row[5])
        school = row[2]

        # Initialise group statistics if new tutorial group
        if tutorial_group not in analysis:
            analysis[tutorial_group] = {
                'total_cgpa': 0.0,
                'num_students': 0,
                'male_count': 0,
                'female_count': 0,
                'schools': [],
                'students': []
            }

        # Update analysis dictionary for each data row
        analysis[tutorial_group]['total_cgpa'] += cgpa
        analysis[tutorial_group]['num_students'] += 1

        # Append eveery new school to keep track of all unique schools
        if school not in analysis[tutorial_group]['schools']:
            analysis[tutorial_group]['schools'].append(school)

        # Track the gender diversity of tutorial group
        if gender.lower() == 'male':
            analysis[tutorial_group]['male_count'] += 1
        elif gender.lower() == 'female':
            analysis[tutorial_group]['female_count'] += 1

        # Append student information to the students list
        analysis[tutorial_group]['students'].append(row)
    return analysis

# Create as diverse as possible project groups within each tutorial group, based on project group's:
# 1. Average CGPA
# 2. Gender distribution
# 3. School diversity

def calculate_cost(group_stats, overall_stats):
    # Calculate the cost as the sum of squared differences between group and overall stats
    cost = 0
    cost += (group_stats['mean_cgpa'] - overall_stats['mean_cgpa']) ** 2
    cost += (group_stats['male_count'] - overall_stats['male_count']) ** 2
    cost += (group_stats['female_count'] - overall_stats['female_count']) ** 2
    cost += (len(group_stats['schools']) - len(overall_stats['schools'])) ** 2
    return cost

# def create_project_groups_optimized(data, group_size=5):
#     # This is basically a greedy cost optimisation;
#     # Within each tutorial group, aim to minimize deviation from desired characteristics:
#     # 1. Average CGPA, 2. gender balance and 3. school diversity

#     # Analyze the data to get each tutorial group's statistics
#     tutorial_data = analyze_tutorial_groups(data)
#     # Disctionary to store summary of project groups for each tutorial group
#     project_groups_summary = {}

#     # Process tutorial groups independently
#     for tutorial_group, stats in tutorial_data.items():
#         # Extract students and calculate overall stats for comparison
#         students = stats['students']
#         overall_mean_cgpa = stats['total_cgpa'] / stats['num_students']
#         overall_stats = {
#             'mean_cgpa': overall_mean_cgpa,
#             'male_count': stats['male_count'] / stats['num_students'],
#             'female_count': stats['female_count'] / stats['num_students'],
#             'schools': stats['schools']
#         }

#         # Initialize list to store all project groups for the current tutorial group
#         project_groups_summary[tutorial_group] = []

#         # Track students already in project groups to prevent duplication
#         used_students = set()

#         # Form project groups until all students assigned
#         while len(used_students) < len(students):
#             current_group = []
#             current_group_stats = {
#                 'total_cgpa': 0.0,
#                 'male_count': 0,
#                 'female_count': 0,
#                 'schools': set(),
#                 'num_students': 0
#             }

#             # Try to fill the current project group up to specified group size
#             for _ in range(group_size):
#                 best_student = None
#                 best_student_index = -1
#                 # Set the minimum cost to infinity initially to ensure that any candidate
#                 # with a lower cost is selected
#                 min_cost = float('inf')

#                 # Iterate through each student in the tutorial group to find best candidate
#                 # to add to current project group based on optimization criteria
#                 for i, student in enumerate(students):
#                     # Skip students already in project groups
#                     if i in used_students:
#                         continue

#                     # Temporarily add current student to group and calculate new stats
#                     # to see if adding would minimizes deviation from desired group characteristics
#                     temp_group = current_group + [student]
#                     temp_group_stats = {
#                         'mean_cgpa': (current_group_stats['total_cgpa'] + float(student[5])) / len(temp_group),
#                         'male_count': current_group_stats['male_count'] + (1 if student[4].lower() == 'male' else 0),
#                         'female_count': current_group_stats['female_count'] + (1 if student[4].lower() == 'female' else 0),
#                         'schools': current_group_stats['schools'] | {student[2]}
#                     }

#                     # Normalize counts to proportions for gender ratio comparison
#                     temp_group_stats['male_count'] /= group_size
#                     temp_group_stats['female_count'] /= group_size

#                     # Calculate cost
#                     cost = calculate_cost(temp_group_stats, overall_stats)

#                     # If calculated cost is lowest so far, change best_student to current candidate
#                     if cost < min_cost:
#                         min_cost = cost
#                         best_student = student
#                         best_student_index = i

#                 # If best_student found, finalize their addition to the current group
#                 if best_student:
#                     current_group.append(best_student)
#                     used_students.add(best_student_index)
#                     current_group_stats['total_cgpa'] += float(best_student[5])
#                     current_group_stats['male_count'] += (1 if best_student[4].lower() == 'male' else 0)
#                     current_group_stats['female_count'] += (1 if best_student[4].lower() == 'female' else 0)
#                     current_group_stats['schools'].add(best_student[2])
#                     current_group_stats['num_students'] += 1

#             # Finalize the statistics (analysis results) of the current group
#             mean_cgpa = current_group_stats['total_cgpa'] / current_group_stats['num_students']
#             gender_ratio = f"{current_group_stats['male_count']}:{current_group_stats['female_count']}"
#             num_schools = len(current_group_stats['schools'])

#             # Append the analysis results to the summary
#             project_groups_summary[tutorial_group].append({
#                 'mean_cgpa': mean_cgpa,
#                 'gender_ratio': gender_ratio,
#                 'num_schools': num_schools,
#                 'students': current_group
#             })

#             # Print summary for each project group
#             print(f"\nProject Group {len(project_groups_summary[tutorial_group])} in Tutorial Group {tutorial_group}:")
#             print(f"Mean CGPA: {mean_cgpa:.2f}")
#             print(f"Gender Ratio (Male:Female): {gender_ratio}")
#             print(f"Number of Schools: {num_schools}")

#     return project_groups_summary

# # This is for any potential ungrouped students to be integrated in least disruptive manner
# # Least deviation from desired group characteristics (more specifically group size)

def redistribute_leftover_students(project_groups_summary, leftover_students, overall_stats, group_size):
    for student in leftover_students:
        min_cost_increase = float('inf')
        chosen_group = None
        chosen_tutorial_group = None

        # Iterate over all tutorial groups and their project groups to find the best slot
        for tutorial_group, project_groups in project_groups_summary.items():
            for group in project_groups:
                # Allow group size to exceed by only 1
                if len(group['students']) > group_size:
                    continue

                # Create a temporary group with the new student added
                temp_group = group['students'] + [student]
                total_cgpa = sum(float(s[5]) for s in temp_group)
                male_count = sum(1 for s in temp_group if s[4].lower() == 'male')
                female_count = sum(1 for s in temp_group if s[4].lower() == 'female')
                schools = set(s[2] for s in temp_group)

                # Update temporary group statistics
                temp_group_stats = {
                    'mean_cgpa': total_cgpa / len(temp_group),
                    'male_count': male_count / len(temp_group),
                    'female_count': female_count / len(temp_group),
                    'schools': schools
                }

                # Calculate the cost increase
                cost_increase = calculate_cost(temp_group_stats, overall_stats)

                # Choose the group with the minimal cost increase
                if cost_increase < min_cost_increase:
                    min_cost_increase = cost_increase
                    chosen_group = group
                    chosen_tutorial_group = tutorial_group

        # Add the student to the chosen group if a suitable group was found
        if chosen_group:
            chosen_group['students'].append(student)

            # Recalculate group statistics (analysis results) after adding the student
            chosen_group['mean_cgpa'] = sum(float(s[5]) for s in chosen_group['students']) / len(chosen_group['students'])
            male_count = sum(1 for s in chosen_group['students'] if s[4].lower() == 'male')
            female_count = sum(1 for s in chosen_group['students'] if s[4].lower() == 'female')
            chosen_group['gender_ratio'] = f"{male_count}:{female_count}"
            chosen_group['num_schools'] = len(set(s[2] for s in chosen_group['students']))

    return project_groups_summary

# Bonus section: allow project groups to be created for any specified group size

def create_project_groups_optimized_any_size(data, group_size):
    # Analyze the data to get tutorial group statistics
    tutorial_data = analyze_tutorial_groups(data)
    # Dictionary to store summary of project groups created for each tutorial group
    project_groups_summary = {}

    # Iterate over each tutorial group to form project groups independently
    for tutorial_group, stats in tutorial_data.items():
        # Extract students and calculate overall statistics (analysis results) for comparison
        students = stats['students']
        overall_mean_cgpa = stats['total_cgpa'] / stats['num_students']
        overall_stats = {
            'mean_cgpa': overall_mean_cgpa,
            'male_count': stats['male_count'] / stats['num_students'],
            'female_count': stats['female_count'] / stats['num_students'],
            'schools': stats['schools']
        }

        # Initialize empty list to store finalized project groups for current tutorial group
        project_groups_summary[tutorial_group] = []
        # Track students already in project groups to prevent duplication
        used_students = set()
        # List to temporarily hold students if they cannot form complete group
        leftover_students = []
        
        # Continue forming groups until all students have been assigned
        while len(used_students) < len(students):
            # Initialize new project group + track stats
            current_group = []
            current_group_stats = {
                'total_cgpa': 0.0,
                'male_count': 0,
                'female_count': 0,
                'schools': set(),
                'num_students': 0
            }

            # Try to fill the current project group up to specified group size
            for _ in range(min(group_size, len(students) - len(used_students))):
                best_student = None
                best_student_index = -1
                # Set the minimum cost to infinity initially to ensure that any candidate
                # with a lower cost is selected
                min_cost = float('inf')

                # Find best match to group
                for i, student in enumerate(students):
                    # Skipping students already in groups
                    if i in used_students:
                        continue

                    # Create a temporary group with the new student added
                    temp_group = current_group + [student]
                    # Update temporary group statistics
                    temp_group_stats = {
                        'mean_cgpa': (current_group_stats['total_cgpa'] + float(student[5])) / len(temp_group),
                        'male_count': current_group_stats['male_count'] + (1 if student[4].lower() == 'male' else 0),
                        'female_count': current_group_stats['female_count'] + (1 if student[4].lower() == 'female' else 0),
                        'schools': current_group_stats['schools'] | {student[2]}
                    }

                    # Normalize counts to proportions for gender ratio comparison
                    temp_group_stats['male_count'] /= group_size
                    temp_group_stats['female_count'] /= group_size

                    # Calculate cost
                    cost = calculate_cost(temp_group_stats, overall_stats)

                    # Select student as potential addition if cost is lowest so far
                    if cost < min_cost:
                        min_cost = cost
                        best_student = student
                        best_student_index = i

                # If a suitable student is found, add them to the current group
                if best_student:
                    current_group.append(best_student)
                    used_students.add(best_student_index)
                    # Update new group stats
                    current_group_stats['total_cgpa'] += float(best_student[5])
                    current_group_stats['male_count'] += (1 if best_student[4].lower() == 'male' else 0)
                    current_group_stats['female_count'] += (1 if best_student[4].lower() == 'female' else 0)
                    current_group_stats['schools'].add(best_student[2])
                    current_group_stats['num_students'] += 1

            # Handle incomplete groups by adding students to leftover_students for later redistribution
            if len(current_group) < group_size:
                leftover_students.extend(current_group)
            # Calculate the project group's final statistics (analysis results)
            else:
                mean_cgpa = current_group_stats['total_cgpa'] / current_group_stats['num_students']
                gender_ratio = f"{current_group_stats['male_count']}:{current_group_stats['female_count']}"
                num_schools = len(current_group_stats['schools'])

                # Append the analysis results to the summary
                project_groups_summary[tutorial_group].append({
                    'mean_cgpa': mean_cgpa,
                    'gender_ratio': gender_ratio,
                    'num_schools': num_schools,
                    'students': current_group
                })

                # Print summary for each project group
                # print(f"\nProject Group {len(project_groups_summary[tutorial_group])} in Tutorial Group {tutorial_group}:")
                # print(f"Mean CGPA: {mean_cgpa:.2f}")
                # print(f"Gender Ratio (Male:Female): {gender_ratio}")
                # print(f"Number of Schools: {num_schools}")

        # Redistribute leftover students (using function defined in code cell 9)
        if leftover_students:
            # print(leftover_students)
            project_groups_summary = redistribute_leftover_students(project_groups_summary, leftover_students, overall_stats, group_size)

    return project_groups_summary

# Input custom project group size
group_size = input("Input group size:\t")
output = dict()
for key in grouped_data:
    sorted = create_project_groups_optimized_any_size(grouped_data[key],int(group_size))
    output.update(sorted)

def analyze_generated_groups(grouped_data):
    # Dictionary to store analysis results for each tutorial group and its groups
    analysis_results = {}
    # Iterate through each tutorial group in the project groups
    for tutorial, groups in grouped_data.items():
        tutorial_analysis = []

        # Process each project group in the tutorial group
        for idx, group in enumerate(groups):
            total_gpa = 0.0
            gender_counts = {'Male': 0, 'Female': 0}
            school_counts = {}

            # Process each student in the project group
            for student in group:
                # Sum up GPA
                total_gpa += float(student[5])

                # Update gender count
                gender = student[4]
                if gender in gender_counts:
                    gender_counts[gender] += 1
                # Handles unexpected gender values (if any)
                else:
                    gender_counts[gender] = 1

                # Count school distribution
                school = student[2]
                if school in school_counts:
                    school_counts[school] += 1
                else:
                    school_counts[school] = 1

            # Calculate mean GPA
            mean_gpa = total_gpa / len(group) if group else 0
            sd = (sum((float(student[5])-mean_gpa)**2 for student in group) / len(group))**0.5

            # Gender ratio
            total_students = len(group)
            gender_ratio = {gender: count / total_students for gender, count in gender_counts.items()}

            # Store the analysis for the current project group
            group_analysis = {
                "group_number": idx + 1,
                "mean_gpa": mean_gpa,
                "sd": sd,
                "gender_ratio": gender_ratio,
                "school_distribution": len(school_counts)
            }

            # Append project group analysis to the tutorial analysis list
            tutorial_analysis.append(group_analysis)

        # Store the analysis for the entire tutorial group
        analysis_results[tutorial] = tutorial_analysis
    
    return analysis_results
"""
"""
"""
"""
"""
"""
"""
Edited Stuff Starts Here
"""
"""
"""
"""
"""

visualisation_data = analyze_generated_groups(dict((tut, [i["students"] for i in data]) for (tut, data) in output.items()))

"""
Visualisation Section
"""

while True:
    tutorial_group_to_plot = input("Which tutorial group would you like to visualise? (e.g. G-1, G-98) ")
    if tutorial_group_to_plot in visualisation_data:
        break

def plot_data(tutorial_group):

    # Extract specific tutorial group's data (e.g., G-1, G-98) to plot
    tutorial_data = visualisation_data[tutorial_group]

    """
    Prepare Data for Plotting
    """
    # Initialise data to be plotted
    group_numbers = []
    mean_gpas = []
    males = []
    females = []
    school_distributions = []

    # Iterate through students in user-specified tutorial group
    for record in tutorial_data:
        # Prepare Group Numbers for plotting ([1, 2, 3, 4,..., 9, 10])
        group_numbers.append(record['group_number'])

        # Prepare Mean GPAs for plotting ([4.082, 4.112,..., 4.117])
        mean_gpas.append(record['mean_gpa'])

        # Prepare Male & Female Count for plotting ([0.4, 0.6,..., 0.4])
        males.append(record['gender_ratio']['Male'])
        females.append(record['gender_ratio']['Female'])

        # Prepare School Distributions for plotting ([5, 4,..., 5])
        school_distributions.append(record['school_distribution'])

    """
    Plotting Mean GPA
    """
    # Create a figure (fig) with 3 graphs (axs) on top of one another
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Setting graph type
    axs[0].plot(group_numbers, mean_gpas, color='blue', marker='o', label='Mean GPA')

    # Setting y-axis range
    axs[0].set_ylim(3.0, 5.0)

    # Setting graph title
    axs[0].set_title(f'{tutorial_group}: Mean GPA by Group Number')
    
    # Setting axis labels
    axs[0].set_ylabel('Mean GPA')
    axs[0].set_xlabel('Group Number')

    # Setting position of legend
    axs[0].legend(loc='upper left')

    """
    Plotting Gender Distribution
    """

    # Standardising width of bars
    width = 0.6

    # Setting graph type
    axs[1].bar(group_numbers, females, width=width, bottom=males, color='lightblue', label='Female')
    axs[1].bar(group_numbers, males, width=width, color='lightgreen', label='Male')

    # Setting y-axis range
    axs[1].set_ylim(0.0, 1.0)

    # Setting graph title
    axs[1].set_title(f'{tutorial_group}: Gender Ratio by Group Number')

    # Setting axis labels
    axs[1].set_ylabel('Gender Ratio')
    axs[1].set_xlabel('Group Number')

    # Setting position of legend
    axs[1].legend(loc='upper left')

    """
    Plotting School Distribution
    """
    # Setting graph type
    axs[2].plot(group_numbers, school_distributions, color='red', marker='s', linestyle=':', label='School Distribution')
    
    # Setting y-axis range
    axs[2].set_ylim(0, 9)

    # Setting graph title
    axs[2].set_title(f'{tutorial_group}: School Distribution by Group Number')

    # Setting axis labels
    axs[2].set_ylabel('School Distribution')
    axs[2].set_xlabel('Group Number')

    # Setting position of legend
    axs[2].legend(loc='upper left')

    # Adjusting layout and spacing between plots
    fig.subplots_adjust(hspace=0.5)
    plt.show()

# Plot data of user specified tutorial group
plot_data(tutorial_group_to_plot)
