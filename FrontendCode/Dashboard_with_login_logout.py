import streamlit as st
import requests

# Backend URL
BASE_URL = "http://localhost:8080"

def logout():
    st.session_state.logged_in = False
    st.session_state.first_run = True
    st.rerun()

def dashboard_header():
    col1, col2 = st.columns([8, 2])  # Left-aligned title, right-aligned logout button
    with col1:
        st.header("Job Portal")
    with col2:
        if st.button("Logout"):
            logout()

def registration_page():
    st.header("Register as a New User")
    
    #user_id = st.number_input("User ID", min_value=1, step=1)
    user_id_input = st.text_input("User ID")

    if user_id_input.isdigit():
        user_id = int(user_id_input)
    else:
        user_id = None  # or show warning if needed

    user_name = st.text_input("Username")
    role = st.radio("Role", ["Employee", "Employer"])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Register"):
            if user_id is not None and user_name and role:
                user_data = {"id": user_id, "userName": user_name, "role": role}
                response = requests.post(f"{BASE_URL}/register", json=user_data)
                
                if response.status_code == 200:
                    st.success("User registered successfully! You can now log in.")
                else:
                    st.error("Failed to register user. Try again.")
            else:
                st.warning("Please fill in all fields.")
    
    with col2:
        if st.button("Back to Login"):
            st.session_state.show_register = False
            st.rerun()



# Login Page
def login_page():
    st.markdown("<h2 style='text-align: center;'>Welcome to the Job Portal</h2>", unsafe_allow_html=True)
    
    # Create some spacing
    st.write("")
    st.write("")

    # Center the login form using columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            st.subheader("Login")
            user_name = st.text_input("Username")
            user_id = st.number_input("ID", min_value=1, step=1)
            role = st.radio("Role", ["Employee", "Employer"], horizontal=True)

            login_btn = st.form_submit_button("Login")

            if login_btn:
                if user_name and user_id and role:
                    login_data = {
                        "userName": user_name,
                        "id": str(user_id),
                        "role": role
                    }
                    response = requests.post(f"{BASE_URL}/login", json=login_data)
                    if response.status_code == 200:
                        st.session_state.logged_in = True
                        st.session_state.user_name = user_name
                        st.session_state.user_role = role
                        st.session_state.user_id = user_id
                        st.success("Login Successful")
                        st.session_state.first_run = False
                        st.rerun()
                    else:
                        st.error("Invalid Credentials. Please try again.")
                else:
                    st.warning("Please fill in all fields.")

    # New User? Register Here Section
    st.markdown("---")
    st.markdown("<div style='text-align: center;'>New user?</div>", unsafe_allow_html=True)
    register_col = st.columns([6, 3, 6])[1]
    with register_col:
        if st.button("Register Here"):
            st.session_state.show_register = True
            st.rerun()





# Employee Dashboard
def employee_dashboard():
    dashboard_header()
    
    st.header("Employee Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs(["View All Jobs", "Search Jobs", "Apply for Job", "Applied Jobs"])

    # View All Jobs
    with tab1:
        st.subheader("All Available Jobs")

        # Create two columns for the job listings
        cols = st.columns(2)

        response = requests.get(f"{BASE_URL}/jobPosts")
        
        if response.status_code == 200:
            jobs = response.json()
            if jobs:
                jobs_sorted = sorted(jobs, key=lambda x: x["postId"])
                for i, job in enumerate(jobs_sorted):
                    with cols[i % 2]:  # Alternate between the two columns
                        st.markdown(f"""
                            <div style="border: 1px solid #ddd; padding: 16px; margin: 8px; border-radius: 8px; background-color: #f1f1f1;">
                                <h4 style="color: #333;">{job["postProfile"]} (ID: {job["postId"]})</h4>
                                <p style="color: #555;">{job["postDesc"]}</p>
                                <p style="color: #555;"><b>Experience Required:</b> {job["reqExperience"]} years</p>
                                <p style="color: #555;"><b>Tech Stack:</b> {", ".join(job["postTechStack"])}</p>
                                <p style="color: #555;"><b>Employer ID:</b> {job["employerId"]}</p>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No jobs available.")
        else:
            st.error("Failed to fetch jobs.")

    # Search Jobs
    with tab2:
        st.subheader("Search Jobs")
        keyword = st.text_input("Enter keyword to search for jobs")
        if st.button("Search"):
            search_response = requests.get(f"{BASE_URL}/jobPosts/keyword/{keyword}")
            if search_response.status_code == 200:
                search_results = search_response.json()
                if search_results:
                    for job in search_results:
                        st.markdown(f"""
                            <div style="border: 1px solid #ddd; padding: 16px; margin: 8px; border-radius: 8px; background-color: #f1f1f1;">
                                <h4 style="color: #333;">{job["postProfile"]} (ID: {job["postId"]})</h4>
                                <p style="color: #555;">{job["postDesc"]}</p>
                                <p style="color: #555;"><b>Experience Required:</b> {job["reqExperience"]} years</p>
                                <p style="color: #555;"><b>Tech Stack:</b> {", ".join(job["postTechStack"])}</p>
                                <p style="color: #555;"><b>Employer ID:</b> {job["employerId"]}</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No jobs found for this keyword.")
            else:
                st.error("Failed to search jobs.")

    # Apply for Job
    with tab3:
        st.subheader("Apply for a Job")

        # Fetch jobs for selection
        jobs_response = requests.get(f"{BASE_URL}/jobPosts")
        if jobs_response.status_code == 200 and jobs_response.json():
            jobs = jobs_response.json()
            job_options = {job["postId"]: job["postProfile"] for job in jobs}
            selected_job_id = st.selectbox("Select Job ID to Apply", options=job_options.keys(), format_func=lambda x: f"{x} - {job_options[x]}")
            employee_id=st.session_state.user_id
            current_company = st.text_input("Current Company")
            experience = st.number_input("Years of Experience",min_value=0,step=1)
            
            # Inputs for job application
            

            if st.button("Apply"):
                if not current_company or experience is None:
                    st.warning("Please fill in all fields")
                # Create application data based on employee ID, selected job ID, and status
                application_data = {
                    
                    "userId": employee_id,  # Using the employee ID stored in session state
                    "jobId": selected_job_id,
                    "currentCompany":current_company,
                    "currentExp":experience  # Status is set to "Pending"
                    
                }

                # Send POST request to backend to submit application
                response = requests.post(f"{BASE_URL}/apply", json=application_data)

                if response.status_code == 200:
                    st.success("Applied successfully!")
                else:
                    st.error("Failed to apply for job.")


    #Applied Jobs
    with tab4:
        st.subheader("Applied Jobs")
        employee_id = st.session_state.user_id
        response = requests.get(f"{BASE_URL}/applications/{employee_id}")
        if response.status_code==200:
            applied_jobs = response.json()
            if applied_jobs:
                for job in applied_jobs:
                    st.markdown(f"""
                            <div style="border: 1px solid #ddd; padding: 16px; margin: 8px; border-radius: 8px; background-color: #f1f1f1;">
                                <h4 style="color: #333;">{job["postProfile"]} (ID: {job["postId"]})</h4>
                                <p style="color: #555;">{job["postDesc"]}</p>
                                <p style="color: #555;"><b>Experience Required:</b> {job["reqExperience"]} years</p>
                                <p style="color: #555;"><b>Tech Stack:</b> {", ".join(job["postTechStack"])}</p>
                                <p style="color: #555;"><b>Employer ID:</b> {job["employerId"]}</p>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No applied jobs found")
        else:
            st.error("Failed to fetch applied jobs")




# Employer Dashboard
def employer_dashboard():
    dashboard_header()
    
    st.header("Employer Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs(["Jobs Posted", "Add Job", "Update Job", "Delete Job"])
    with tab1:
        st.subheader("Posted Jobs")
        employer_id = st.session_state.user_id
        response = requests.get(f"{BASE_URL}/viewJobPost/{employer_id}")
        if response.status_code==200:
            posted_jobs = response.json()
            if posted_jobs:
                for job in posted_jobs:
                    job_id = job["postId"]
                    applicant_response = requests.get(f"{BASE_URL}/count/{job_id}")
                    if applicant_response.status_code == 200:
                        applicant_count = applicant_response.text.strip()
                    else:
                        applicant_count = "N/A"
                    col1, col2 = st.columns([6, 3])
                    with col1:

                        st.markdown(f"""
                                <div style="border: 1px solid #ddd; padding: 16px; margin: 8px; border-radius: 8px; background-color: #f1f1f1;">
                                    <h4 style="color: #333;">{job["postProfile"]} (ID: {job["postId"]})</h4>
                                    <p style="color: #555;">{job["postDesc"]}</p>
                                    <p style="color: #555;"><b>Experience Required:</b> {job["reqExperience"]} years</p>
                                    <p style="color: #555;"><b>Tech Stack:</b> {", ".join(job["postTechStack"])}</p>
                                    <p style="color: #555;"><b>Employer ID:</b> {job["employerId"]}</p>
                                    <p style="color: #555;"><b>Applicants:</b> {applicant_count}</p>
                                </div>
                            """, unsafe_allow_html=True)
                    with col2:
                        if st.button(f"View Applicants", key=f"view_{job_id}"):
                            # Fetch applicants for the selected job
                            applicants_response = requests.get(f"{BASE_URL}/applicants/{job_id}")
                            
                            if applicants_response.status_code == 200:
                                applicants = applicants_response.json()
                                if applicants:
                                    st.subheader(f"Applicants for {job['postProfile']} (ID: {job_id})")
                                    for applicant in applicants:
                                        st.markdown(f"""
                                            <div style="border: 1px solid #ddd; padding: 10px; margin: 5px; border-radius: 8px; background-color: #eaf2ff;">
                                                <p style="color: #555;"><b>Applicant ID:</b> {applicant["applicationId"]}</p>
                                                <p style="color: #555;"><b>UserId:</b> {applicant["userId"]}</p>
                                                <p style="color: #555;"><b>Current Company:</b> {applicant["currentCompany"]}</p>
                                                <p style="color: #555;"><b>Experience:</b> {applicant["currentExp"]} years</p>
                                            </div>
                                        """, unsafe_allow_html=True)
                    
            else:
                st.warning("No jobs posted")
        else:
            st.error("Failed to fetch posted jobs")



    

    # Add Job
    with tab2:
        st.subheader("Add a New Job")
        post_id = st.number_input("Job ID", min_value=1, step=1)
        employer_id = st.session_state.user_id
        post_profile = st.text_input("Job Role")
        post_desc = st.text_area("Job Description")
        req_experience = st.number_input("Required Experience (Years)", min_value=0, step=1)
        post_tech_stack = st.text_input("Required Tech Stack (comma-separated)")

        if st.button("Add Job"):
            job_data = {
                "postId": post_id, 
                "employerId": employer_id,
                "postProfile": post_profile,
                "postDesc": post_desc,
                "reqExperience": req_experience,
                "postTechStack": post_tech_stack.split(",")  # Convert to list
            }
            response = requests.post(f"{BASE_URL}/jobPost", json=job_data)

            if response.status_code == 200:
                st.success("Job added successfully!")
            else:
                st.error("Failed to add job.")

    # Update Job
    with tab3:
        st.subheader("Update an Existing Job")
        employerId = st.session_state.user_id

        # Fetch jobs for selection
        jobs_response = requests.get(f"{BASE_URL}/jobPosts/employer/{employerId}")
        if jobs_response.status_code == 200 and jobs_response.json():
            jobs = jobs_response.json()
            job_options = {job["postId"]: job["postProfile"] for job in jobs}
            selected_job_id = st.selectbox("Select Job ID to Update", options=job_options.keys(), format_func=lambda x: f"{x} - {job_options[x]}")

            # Fetch job details for the selected job
            job_data = next((job for job in jobs if job["postId"] == selected_job_id), None)

            if job_data:
                employer_id = st.session_state.user_id
                new_profile = st.text_input("Job Role", value=job_data["postProfile"])
                new_desc = st.text_area("Job Description", value=job_data["postDesc"])
                new_experience = st.number_input("Required Experience (Years)", min_value=0, step=1, value=job_data["reqExperience"])
                new_skills = st.text_input("Required Tech Stack (comma-separated)", value=",".join(job_data["postTechStack"]))

                if st.button("Save Changes"):
                    updated_job = {
                        "postId": selected_job_id,
                        "employerId": employer_id,
                        "postProfile": new_profile,
                        "postDesc": new_desc,
                        "reqExperience": new_experience,
                        "postTechStack": new_skills.split(",")
                    }
                    update_response = requests.put(f"{BASE_URL}/jobPost/{post_id}", json=updated_job)

                    if update_response.status_code == 200:
                        st.success("Job updated successfully!")
                    else:
                        st.error("Failed to update job.")

        else:
            st.warning("No jobs available for updating.")

    # Delete Job
    with tab4:
        st.subheader("Delete a Job")
        employerId = st.session_state.user_id
        # Fetch jobs for selection
        jobs_response = requests.get(f"{BASE_URL}/jobPosts/employer/{employerId}")

        if jobs_response.status_code == 200 and jobs_response.json():
            jobs = jobs_response.json()
            job_options = {job["postId"]: job["postProfile"] for job in jobs}
            selected_job_id = st.selectbox("Select Job ID to Delete", options=job_options.keys(), format_func=lambda x: f"{x} - {job_options[x]}")

            if st.button("Delete Job"):
                delete_response = requests.delete(f"{BASE_URL}/jobPost/{selected_job_id}?employerId={employerId}")


                if delete_response.status_code == 200:
                    st.success("Job deleted successfully!")
                else:
                    st.error("Failed to delete job.")
        else:
            st.warning("No jobs available for deletion.")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.first_run = True
    st.session_state.show_register = False  # Control register view


if not st.session_state.logged_in:
    if st.session_state.show_register:
        registration_page()
    else:
        login_page()
else:
    if st.session_state.user_role == "Employee":
        employee_dashboard()
    elif st.session_state.user_role == "Employer":
        employer_dashboard()




