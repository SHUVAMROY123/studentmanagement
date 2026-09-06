import streamlit as st
import pandas as pd
import os



st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

FILE_NAME = "students.csv"




AVAILABLE_SUBJECTS = [
    "Python",
    "Java",
    "C Programming",
    "C++",
    "Data Structures",
    "Database Management",
    "Web Technology",
    "Computer Networks",
    "Operating Systems",
    "Mathematics",
    "Machine Learning",
    "Artificial Intelligence",
    "Data Science",
    "Software Engineering",
    "Discrete Mathematics",
    "Digital Logic Design",
    "Computer Architecture",
    "Compiler Design",
    "Information Security",
    "Cloud Computing",
    "Big Data",
    "Mobile Application Development",
    "BASIC ELETRICAL ENGINEERING",
    "Computer Graphics",
    "Human-Computer Interaction",
    "SOFT COMPUTING",
    "Computer Vision",
    "Natural Language Processing",
    "Robotics",
]



if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame()




def calculate_grade(percentage):

    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def calculate_result(marks):

    
    if all(mark >= 40 for mark in marks):
        return "PASS"

    return "FAIL"



st.sidebar.title("🎓 Student Management")

page = st.sidebar.radio(
    "Choose Page",
    [
        "🏠 Home",
        "➕ Add Student",
        "📋 Student Records",
        "📊 Performance Dashboard",
        "🔎 Search Student"
    ]
)




if page == "🏠 Home":

    st.title("🎓 Student Management & Performance Dashboard")

    st.write(
        "A student management system built using "
        "Python, Streamlit and Pandas."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    total_students = len(df)

    if total_students > 0:

        average = df["Percentage"].mean()

        passed = len(
            df[df["Result"] == "PASS"]
        )

        failed = len(
            df[df["Result"] == "FAIL"]
        )

    else:

        average = 0
        passed = 0
        failed = 0

    col1.metric(
        "👨‍🎓 Students",
        total_students
    )

    col2.metric(
        "📊 Average %",
        f"{average:.2f}%"
    )

    col3.metric(
        "✅ Passed",
        passed
    )

    col4.metric(
        "❌ Failed",
        failed
    )

    st.subheader("✨ Project Features")

    st.markdown("""
    - 👤 Student registration
    - 📚 User-selected subjects
    - 📝 Marks input
    - 📊 Automatic percentage calculation
    - 🏆 Grade calculation
    - ✅ Pass/Fail calculation
    - 📅 Attendance tracking
    - 🔎 Student search
    - 📈 Performance charts
    - 🏆 Top student ranking
    - ✏️ Edit student records
    - 🗑️ Delete student records
    - 📥 Download student data
    """)



elif page == "➕ Add Student":

    st.title("➕ Add New Student")

    st.write(
        "Enter student information and choose the subjects."
    )

    

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "👤 Student Name"
        )

        roll_no = st.text_input(
            "🔢 Roll Number"
        )

        department = st.selectbox(
            "🏫 Department",
            [
                "Computer Science",
                "Information Technology",
                "Electronics",
                "Mechanical",
                "Civil",
                "Electrical",
                "Other"
            ]
        )

    with col2:

        semester = st.selectbox(
            "📚 Semester",
            [1, 2, 3, 4, 5, 6, 7, 8]
        )

        attendance = st.number_input(
            "📅 Attendance (%)",
            min_value=0.0,
            max_value=100.0,
            value=75.0
        )

    st.divider()

    
    st.subheader("📚 Choose Subjects")

    selected_subjects = st.multiselect(
        "Select the subjects for this student",
        AVAILABLE_SUBJECTS,
        default=[
            "Python",
            "Database Management",
            "Mathematics"
        ]
    )

    if len(selected_subjects) == 0:

        st.warning(
            "Please select at least one subject."
        )

    else:

        st.success(
            f"{len(selected_subjects)} subject(s) selected."
        )

        st.subheader("📝 Enter Marks")

        marks = {}

        # Create columns dynamically
        columns = st.columns(3)

        for index, subject in enumerate(selected_subjects):

            with columns[index % 3]:

                marks[subject] = st.number_input(
                    f"{subject} Marks",
                    min_value=0,
                    max_value=100,
                    value=0,
                    key=f"marks_{subject}"
                )

        st.divider()

        # -------------------------------------------------
        # PREVIEW
        # -------------------------------------------------

        total_marks = sum(marks.values())

        max_marks = len(selected_subjects) * 100

        percentage = (
            total_marks / max_marks * 100
        )

        grade = calculate_grade(
            percentage
        )

        result = calculate_result(
            list(marks.values())
        )

        st.subheader("📊 Result Preview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Marks",
            f"{total_marks}/{max_marks}"
        )

        col2.metric(
            "Percentage",
            f"{percentage:.2f}%"
        )

        col3.metric(
            "Grade",
            grade
        )

        col4.metric(
            "Attendance",
            f"{attendance:.1f}%"
        )

        if result == "PASS":
            st.success("Result: PASS")
        else:
            st.error(
                "Result: FAIL - One or more subjects are below 40 marks."
            )

        # -------------------------------------------------
        # SAVE STUDENT
        # -------------------------------------------------

        if st.button(
            "💾 Save Student",
            type="primary"
        ):

            if name.strip() == "":
                st.error(
                    "Please enter the student name."
                )

            elif roll_no.strip() == "":
                st.error(
                    "Please enter the roll number."
                )

            elif len(selected_subjects) == 0:
                st.error(
                    "Please select at least one subject."
                )

            elif not df.empty and roll_no in df["Roll No"].astype(str).values:
                st.error(
                    "A student with this roll number already exists."
                )

            else:

                student_data = {
                    "Roll No": roll_no,
                    "Name": name,
                    "Department": department,
                    "Semester": semester,
                    "Attendance": attendance,
                    "Total": total_marks,
                    "Max Marks": max_marks,
                    "Percentage": percentage,
                    "Grade": grade,
                    "Result": result,
                    "Subjects": ", ".join(selected_subjects)
                }

                # Store subject marks
                for subject, mark in marks.items():
                    student_data[subject] = mark

                new_student = pd.DataFrame(
                    [student_data]
                )

                if df.empty:
                    df = new_student
                else:
                    df = pd.concat(
                        [df, new_student],
                        ignore_index=True
                    )

                df.to_csv(
                    FILE_NAME,
                    index=False
                )

                st.success(
                    f"🎉 {name} added successfully!"
                )



elif page == "📋 Student Records":

    st.title("📋 Student Records")

    if df.empty:

        st.info(
            "No student records available."
        )

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # -------------------------------------------------
        # DELETE STUDENT
        # -------------------------------------------------

        st.subheader("🗑️ Delete Student")

        roll_to_delete = st.text_input(
            "Enter Roll Number to Delete"
        )

        if st.button(
            "Delete Student",
            type="secondary"
        ):

            if roll_to_delete in df["Roll No"].astype(str).values:

                df = df[
                    df["Roll No"].astype(str)
                    != roll_to_delete
                ]

                df.to_csv(
                    FILE_NAME,
                    index=False
                )

                st.success(
                    "Student deleted successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Roll number not found."
                )

        
        st.subheader("📥 Download Data")

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="student_records.csv",
            mime="text/csv"
        )



elif page == "📊 Performance Dashboard":

    st.title("📊 Performance Dashboard")

    if df.empty:

        st.info(
            "Add students first to view performance."
        )

    else:

        
        col1, col2 = st.columns(2)

        with col1:

            departments = [
                "All"
            ] + sorted(
                df["Department"].unique().tolist()
            )

            selected_department = st.selectbox(
                "Filter by Department",
                departments
            )

        with col2:

            semesters = [
                "All"
            ] + sorted(
                df["Semester"].unique().tolist()
            )

            selected_semester = st.selectbox(
                "Filter by Semester",
                semesters
            )

        filtered_df = df.copy()

        if selected_department != "All":

            filtered_df = filtered_df[
                filtered_df["Department"]
                == selected_department
            ]

        if selected_semester != "All":

            filtered_df = filtered_df[
                filtered_df["Semester"]
                == selected_semester
            ]

        st.divider()

        
        total_students = len(
            filtered_df
        )

        if total_students > 0:

            average = filtered_df[
                "Percentage"
            ].mean()

            highest = filtered_df[
                "Percentage"
            ].max()

            pass_count = len(
                filtered_df[
                    filtered_df["Result"] == "PASS"
                ]
            )

        else:

            average = 0
            highest = 0
            pass_count = 0

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "👨‍🎓 Students",
            total_students
        )

        col2.metric(
            "📊 Average",
            f"{average:.2f}%"
        )

        col3.metric(
            "🏆 Highest",
            f"{highest:.2f}%"
        )

        col4.metric(
            "✅ Pass Count",
            pass_count
        )

        
        st.subheader("🏆 Top Performing Students")

        top_students = filtered_df.sort_values(
            "Percentage",
            ascending=False
        ).head(5)

        st.dataframe(
            top_students[
                [
                    "Roll No",
                    "Name",
                    "Department",
                    "Percentage",
                    "Grade"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        
        st.subheader("📈 Student Performance")

        performance_chart = filtered_df[
            ["Name", "Percentage"]
        ].set_index("Name")

        st.bar_chart(
            performance_chart
        )

        

        st.subheader("📚 Subject-wise Performance")

        subject_data = {}

        for subject in AVAILABLE_SUBJECTS:

            if subject in filtered_df.columns:

                average_mark = filtered_df[
                    subject
                ].mean()

                if not pd.isna(average_mark):

                    subject_data[
                        subject
                    ] = average_mark

        if subject_data:

            subject_df = pd.DataFrame(
                {
                    "Average Marks":
                        subject_data
                }
            )

            st.bar_chart(
                subject_df
            )

        
        st.subheader("🎯 Grade Distribution")

        grade_count = filtered_df[
            "Grade"
        ].value_counts()

        st.bar_chart(
            grade_count
        )

        
        st.subheader("📅 Attendance Analysis")

        attendance_data = filtered_df[
            ["Name", "Attendance"]
        ].set_index("Name")

        st.bar_chart(
            attendance_data
        )




elif page == "🔎 Search Student":

    st.title("🔎 Search Student")

    if df.empty:

        st.info(
            "No student records available."
        )

    else:

        search = st.text_input(
            "Enter student name or roll number"
        )

        if search:

            results = df[
                df["Name"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                df["Roll No"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

            if results.empty:

                st.warning(
                    "No student found."
                )

            else:

                st.success(
                    f"{len(results)} student(s) found."
                )

                st.dataframe(
                    results,
                    use_container_width=True,
                    hide_index=True
                )

                # Show detailed student information
                for _, student in results.iterrows():

                    with st.expander(
                        f"👤 {student['Name']} - Roll No: {student['Roll No']}"
                    ):

                        col1, col2, col3 = st.columns(3)

                        col1.metric(
                            "Percentage",
                            f"{student['Percentage']:.2f}%"
                        )

                        col2.metric(
                            "Grade",
                            student["Grade"]
                        )

                        col3.metric(
                            "Attendance",
                            f"{student['Attendance']:.1f}%"
                        )

                        st.write(
                            f"**Department:** {student['Department']}"
                        )

                        st.write(
                            f"**Semester:** {student['Semester']}"
                        )

                        st.write(
                            f"**Subjects:** {student['Subjects']}"
                        )

                        st.write(
                            f"**Result:** {student['Result']}"
                        )
