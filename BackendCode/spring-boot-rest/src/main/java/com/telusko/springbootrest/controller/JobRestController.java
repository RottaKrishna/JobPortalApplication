package com.telusko.springbootrest.controller;

import java.util.List;


import com.telusko.springbootrest.model.JobApplication;
import com.telusko.springbootrest.service.JobApplicationService;
import com.telusko.springbootrest.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.telusko.springbootrest.model.JobPost;
import com.telusko.springbootrest.model.User;
import com.telusko.springbootrest.service.JobService;

@RestController
@CrossOrigin
public class JobRestController {
	
	@Autowired
	private JobService service;

	@Autowired
	private UserService uservice;

	@Autowired
	private JobApplicationService jobApplicationService;
	
	
	
	
	@GetMapping("jobPosts")
	public List<JobPost> getAllJobs() {
		return service.getAllJobs();
		
	}

	@GetMapping("viewJobPost/{employerId}")
	public List<JobPost> viewJobs(@PathVariable int employerId)
	{
		return service.viewJobsByEmployerId(employerId);
	}

	
	
	
	
	
	@GetMapping("/jobPost/{postId}")
	public JobPost getJob(@PathVariable int postId) {
		return service.getJob(postId);
	}
	
	
	@GetMapping("jobPosts/keyword/{keyword}")
	public List<JobPost> searchByKeyword(@PathVariable("keyword") String keyword){
		return service.search(keyword);
		
	}
	
	
	

	@PostMapping("jobPost")
	public JobPost addJob(@RequestBody JobPost jobPost) {
		service.addJob(jobPost);
		return service.getJob(jobPost.getPostId());
	}
	
	
	
	@PutMapping("jobPost/{postId}")
	public String updateJob(@PathVariable int postId,@RequestBody JobPost jobPost) {
		return service.updateJob(postId,jobPost);
		//return service.getJob(jobPost.getPostId());
	}
	
	
	
	
	@DeleteMapping("jobPost/{postId}")
	public String deleteJob(@PathVariable int postId, @RequestParam int employerId)
	{
		return service.deleteJob(postId,employerId);

	}
	
	
	@GetMapping("load")
	public String loadData() {
		service.load();
		return "success";
	}
	//To store predefined users
	@GetMapping("store")

		public String storeData(){
			uservice.store();
			return "Success";


	}

	@GetMapping("/jobPosts/employer/{employerId}")
	public List<JobPost> getJobsByEmployer(@PathVariable int employerId) {
		//return jobRepo.findJobsPostedByEmployer(employerId);
		return service.findJobsByEmployer(employerId);
	}


	@GetMapping("users")
	public List<User> getAllUsers() {
		return uservice.getAllUsers();

	}



	@PostMapping("register")
	public String addUser(@RequestBody User user)
	{
		uservice.registerUser(user);
		return "Successfully registered";
	}


	@PostMapping("login")
	public ResponseEntity<String> login(@RequestBody User loginRequest) {
		// Use the service class to validate the login credentials
		boolean isValid = uservice.validateUser(
				loginRequest.getUserName(),
				loginRequest.getId(),
				loginRequest.getRole()
		);

		if (isValid) {
			// Successful login
			return ResponseEntity.ok("Login successful");
		} else {
			// Invalid credentials
			return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid login credentials");
		}
	}

	@GetMapping("apply")

	public String applyData(){
		jobApplicationService.store();
		return "Success";


	}

	@GetMapping("applications")
	public List<JobApplication> getAllApplications() {
		return jobApplicationService.getAllApplications();

	}

	@GetMapping("/applications/{userId}")
	public List<JobPost> getAppliedJobs(@PathVariable int userId){
	 List<JobPost> jobs = jobApplicationService.getJobsAppliedByEmployee(userId);{
	return jobs;}
	}

	@GetMapping("/applicants/{jobId}")
	public List<JobApplication> getApplicantDetails(@PathVariable int jobId){
		List<JobApplication> jobs = jobApplicationService.getJobsApplicants(jobId);{
			return jobs;}
	}




	@PostMapping("apply")
	public String addApplication(@RequestBody JobApplication jobApplication) {
		jobApplicationService.addApplication(jobApplication);
		String message = "Applied successfully";
		return message;
	}

	@GetMapping("/count/{postId}")
	public ResponseEntity<?> getApplicantsCount(@PathVariable int postId) {
		int count = jobApplicationService.getApplicantsCount(postId);
		return ResponseEntity.ok(count);
	}




}
