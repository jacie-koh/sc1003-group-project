import ipywidgets as widgets
students = []
output = []
with open("records.csv", "r") as file:
    for row in file:
        students.append(row.strip().split(","))
header = students[0] + ["Team Assigned"]
students = students[1:]
students_split = dict()

for i in students:
    if i[0] in students_split.keys():
        students_split[i[0]].append(i)
    else:
        students_split[i[0]] = [i]

avg = sum([float(i[5]) for i in students])/6000

# for i in set([i[2] for i in students]):
#     print( f'{i} (HIGH): {[i[2] for i in students if float(i[5]) >= avg].count(i)}',
#            f'(LOW): {[i[2] for i in students if float(i[5]) <= avg].count(i)}',
#            f'(Male): {[i[2] for i in students if i[4] == "Male"].count(i)}',
#            f'(Female): {[i[2] for i in students if i[4] == "Female"].count(i)}',
#            f'{i} (Total): {[i[2] for i in students].count(i)}')
# print()
# for i in set([i[4] for i in students]):
#     print( f'{i} (HIGH): {[i[4] for i in students if float(i[5]) >= avg].count(i)}',
#            f'(LOW): {[i[4] for i in students if float(i[5]) <= avg].count(i)}')

# for i, j in students_split.items():
#     print(f'{i}: {len(set(k[2] for k in j))} Male: {sum(1 for a in j if a[-2] == "Male")} Female: {sum(1 for a in j if a[-2] == "Female")}')

# group_size = 5

output = []
w = widgets.BoundedIntText(
    value=5,
    min=4,
    max=10,
    step=1,
    description="Group Size:",
    disabled=False
)
group_size = w.value

for tut_grp, data in students_split.items():
    grouped = []
    avg_gpa = sum([float(i[5]) for i in data])/50
    male_high = sorted([i for i in data if i[4] == "Male" and float(i[5]) >= avg], key=lambda x: x[5], reverse=True)
    male_low = sorted([i for i in data if i[4] == "Male" and float(i[5]) < avg], key=lambda x: x[5])
    female_high = sorted([i for i in data if i[4] == "Female" and float(i[5]) >= avg], key=lambda x: x[5], reverse=True)
    female_low = sorted([i for i in data if i[4] == "Female" and float(i[5]) < avg], key=lambda x: x[5])
    schools = dict([(j, [i[2] for i in data].count(j)) for j in set([i[2] for i in data])])
 
    project_group = 1
    categories = [male_high, female_high, male_low, female_low]
    for entry in range(len(data)):
        if entry%group_size == 0:
            chosen = []
        project_group = entry//group_size + 1
        
        pos = entry%group_size
        if pos >= len(categories):
            pos = [len(i) for i in categories].index(max([len(i) for i in categories]))
        category = categories[pos]

        filtered = [i for i in category if i[2] not in chosen]
        if len(filtered) == 0:
            filtered = category
        counts = [schools[i[2]] for i in filtered]
        person = filtered[counts.index(max(counts))]
        schools[person[2]] -= 1 
        output.append(person + [str(project_group)])
        category.remove(person)
        if len(category) == 0:
            categories.pop(pos)
        else:
            categories[pos] = category
        chosen.append(person[2])

n = 0
avg_gpas = []
for i in range(0, len(output)-5, 5):
    male = sum([1 for j in output[i:i+5] if j[4] == "Male"])
    female = sum([1 for j in output[i:i+5] if j[4] == "Female"])
    avg_gpas.append(sum([float(j[5]) for j in output[i:i+5]])/5)

    # sch_dist = dict()
    # for j in set([i[2] for i in output[i:i+5]]):
    #     count = [i[2] for i in output[i:i+5]].count(j)
    #     sch_dist[j] = count
    # print(sch_dist)

    # if output[i][0] in ["G-114", "G-4"]:
    #     print(male, female)
    # if male > 4:
    #     n += 1
    #     print(output[i][0], male, female, avg)
    #     print()
    # elif female > 4:
    #     n+= 1
    #     print(output[i][0], male, female, avg)
    #     print()
avg_grp = sum(avg_gpas)/1200
sd = (sum((i - avg_grp) for i in avg_gpas)/(1200))**(0.5)
print(sd)
print(n) 

with open("out.txt", "w") as f:
    f.write(",".join(header) + "\n")
    for i in output:
        f.write(",".join(i) + "\n")