students = {
    "Alice": [88, 92, 79],
    "Bob": [90, 85, 87],
    "Charlie": [70, 80, 75]
}

def get_letter_grade(score):
    if score >= 90: return 'A'
    elif score >= 80: return 'B'
    elif score >= 70: return 'C'
    elif score >= 60: return 'D'
    else: return 'F'

# 1. Compute average and 2. Create new dictionary
gradebook = {}
for name, grades in students.items():
    avg = sum(grades) / len(grades)
    letter = get_letter_grade(avg)
    gradebook[name] = (round(avg, 2), letter)

# 3. Sort students by average score
# item[1][0] accesses the average score inside the value tuple
sorted_students = sorted(gradebook.items(), key=lambda item: item[1][0], reverse=True)

# 4. Output the top student
top_student_name, top_data = sorted_students[0]

print("Gradebook:", gradebook)
print("\nStudents Sorted by Average:", sorted_students)
print(f"\nTop Student: {top_student_name} with an average of {top_data[0]}")