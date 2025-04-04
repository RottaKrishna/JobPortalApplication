package com.telusko.springbootrest.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.telusko.springbootrest.model.JobPost;
import com.telusko.springbootrest.repo.JobRepo;


@Service
public class JobService {

    @Autowired
    public JobRepo repo;





    //method to return all JobPosts
    public List<JobPost> getAllJobs() {
        return repo.findAll();


    }









    // method to add a jobPost
    public void addJob(JobPost jobPost) {
        repo.save(jobPost);

    }




    //method to get job by id
    public JobPost getJob(int postId) {

        return repo.findById(postId).orElse(new JobPost());
    }




    //method to update job with job post object
    public String updateJob(int postId,JobPost jobPost) {
        Optional<JobPost> job = repo.findById(postId);
        if (job.isPresent()) {
            JobPost obtainedJob = job.get();
            if (obtainedJob.getEmployerId() == jobPost.getEmployerId()) {
                repo.save(jobPost);
                return "Success";
            } else {
                return "UNORTHERIZED";
            }
        } else {
            return "Job Not Found";
        }
        
    }







    //method to delete job post by id
    public String deleteJob(int postId,int employerId) {
        Optional<JobPost> job = repo.findById(postId);
        if(job.isPresent())
        {
            JobPost jobpost = job.get();
            if(jobpost.getEmployerId()==employerId)
            {
                repo.delete(jobpost);
                return "JobPost Deleted Successfully";
            }
            else {
                return "UNAUTHORIZED";
            }}
        else
        {
            return "Job Not Found";
        }
    }











public void load() {
    // arrayList to store store JobPost objects
    List<JobPost> jobs =
            new ArrayList<>(List.of(
                    new JobPost(1, "Product Manager", "Seeking an experienced product manager for a tech firm.", 5, List.of("Agile", "Scrum", "Stakeholder Management", "Product Strategy"), 106),

                    new JobPost(2, "Data Analyst", "Seeking a data analyst with expertise in SQL and Python.", 2, List.of("SQL", "Python", "Tableau", "Data Visualization"), 107),
                    new JobPost(3, "Frontend Developer", "Looking for a creative frontend developer skilled in React.", 3, List.of("React", "JavaScript", "CSS", "HTML"), 108),
                    new JobPost(4, "DevOps Engineer", "Hiring a DevOps engineer to manage CI/CD pipelines.", 4, List.of("AWS", "Docker", "Kubernetes", "Jenkins"), 109),
                    new JobPost(5, "Machine Learning Engineer", "Exciting opportunity in AI and ML development.", 5, List.of("Python", "TensorFlow", "PyTorch", "NLP"), 110),
                    new JobPost(6, "Cybersecurity Analyst", "Looking for an expert in cybersecurity and threat analysis.", 3, List.of("Network Security", "Penetration Testing", "SIEM", "Firewall Management"), 106),
                    new JobPost(7, "Full Stack Developer", "Seeking a full stack developer for web applications.", 4, List.of("Node.js", "React", "MongoDB", "Express.js"), 107),
                    new JobPost(8, "Cloud Engineer", "Hiring a cloud engineer with expertise in AWS and Azure.", 4, List.of("AWS", "Azure", "Terraform", "Cloud Security"), 108),
                    new JobPost(9, "QA Engineer", "Looking for a QA engineer to enhance testing processes.", 2, List.of("Selenium", "TestNG", "Manual Testing", "Automation Testing"), 109),
                    new JobPost(10, "Backend Developer", "Exciting opportunity to build robust backend applications.", 4, List.of("Java", "Spring Boot", "PostgreSQL", "Microservices"), 110)



            ));

    repo.saveAll(jobs);

}









public List<JobPost> search(String keyword) {

    return repo.findByPostProfileContainingOrPostDescContaining(keyword,keyword);
}


public List<JobPost> viewJobsByEmployerId(int employerId) {

        return repo.findJobsPostedByEmployer(employerId);
}

    public List<JobPost> findJobsByEmployer(int employerId) {
        return repo.findJobsPostedByEmployer(employerId);
    }
}
