package com.telusko.springbootrest.service;

// JobApplicationService.java (Service)
import com.telusko.springbootrest.model.JobApplication;
import com.telusko.springbootrest.model.JobPost;
import com.telusko.springbootrest.model.User;
import com.telusko.springbootrest.repo.JobApplicationRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
public class JobApplicationService {

    @Autowired
    private JobApplicationRepo jobApplicationRepository;



    public void store() {
        List<JobApplication> applications = List.of(
                new JobApplication(200,101,1,"Google",2),
                new JobApplication(201,102,2,"Apple",3),

                new JobApplication(203,103,3,"Microsoft",4),
                new JobApplication(204,104,4,"Yahoo",2),
                new JobApplication(205,105,5,"Ola",3),
                new JobApplication(206,106,6,"Uber",2)
        );

       jobApplicationRepository.saveAll(applications);
    }

    public List<JobApplication> getAllApplications() {
        return jobApplicationRepository.findAll();
    }

    public void addApplication(JobApplication jobApplication) {
        jobApplicationRepository.save(jobApplication);
    }

    public List<JobPost> getJobsAppliedByEmployee(int userId)
    {
        return jobApplicationRepository.findJobsAppliedByEmployee(userId);
    }

    public int getApplicantsCount(int jobId) {
        return jobApplicationRepository.countApplicantsForJob(jobId);
    }

    public List<JobApplication> getJobsApplicants(int jobId) {
        return jobApplicationRepository.findJobsAppliedByJobId(jobId);
    }


    // Method to fetch job applications by user

}

