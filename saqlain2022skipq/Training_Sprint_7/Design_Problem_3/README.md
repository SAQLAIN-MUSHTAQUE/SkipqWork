 # Welcome to Design and Develop Problem 3!

## **Question of Design Problem :**
 **1.** ***How would you automate deployment (e-g on AWS) for a system that has source code in a repo.***  
 ***a) How do we generate an artifact from the repo that gets published and later is used in some services?***  
 We can build an artifact and store in S3 Bucket and retrive that artifact using Amazon ECR (Elastic Container Registry) for later use.  
 ![Alt text](Design_part%201.drawio.png)   

 ***b) Are there more than one solutions?***  
 Yes, there are number of ways to automate deployment on AWS for a system with source code stored in a repository and produce an artifact that can be shared and subsequently utilized in some services. Here are a few potential answers:

 **i.** *AWS CodePipeline:* Every time there is a code change, AWS CodePipeline, a fully managed continuous delivery service, can build, test, and deploy your code and also create a docker image. To fully automate the deployment process, CodePipeline interfaces with other AWS services like CodeBuild, CodeDeploy, and S3.  

 **ii.** *AWS Elastic Beanstalk:* This platform-as-a-service (PaaS) allows for the automatic deployment and scalability of web applications. Elastic Beanstalk has the ability to build your code, build a Docker container, and deploy it to an active environment. It is integrated with other AWS services including CodeBuild, CodeCommit, and CodePipeline.  
  
 **iii.** *Third-party tools:* There are also many third-party tools available that can help you automate your deployment pipeline, such as Jenkins, Travis CI, and CircleCI. These tools can integrate with AWS services like CodeCommit, CodeBuild, and CodeDeploy to build, test, and deploy your code.  

   
 **2.** ***Deploy, maintain and rollback pipeline for an artifact deployment e-g lambda package, docker image etc.***  
 The design architecture is given below:
 ![Alt text](design_problem_3_part2.drawio%20(1).png)  

 **a.** ***If the latest deployment is failing, why do you think that is?***  
  **i.** Any kind of syntax error, semantic error or logical error in the build process that result in a broken artifact.  
  **ii.** Artefact and target environment incompatibility problems.  
  **iii.** Configuration errors in the deployment process.  
  **iv.** Lack of resources in the target environment.  

  **b.** ***How will you rollback?***  
  Use the Rollback stage in AWS CodePipeline to undo a failed deployment. This stage is designed to automate the rollback procedure by redeploying the previous working version of the artifact using the AWS CodeDeploy service. [[1]](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html)  

  **c.** ***How do you reduce such failures so there is less need to rollback?***  
  There are many ways to reduce failures in the deployment process and minimize the need for rollbacks,some of them are given below:    

 **i.** *Automated Testing:* Implement a good automated testing strategy to catch issues early in the development process. Use unit tests, integration tests, and functional tests to validate the application and ensure it meets the required quality standards.    

  **ii.** *Continuous Integration:* Implement a continuous integration (CI) method that automatically builds and tests the application while integrating code changes frequently. This procedure makes sure that every change is verified and tested in the same setting.  
    
  **iii.** *Canary Deployments:* Use canary deployments to gradually introduce changes to a limited group of users while keeping an eye on the outcomes. With this method, problems can be found early and, if required, rapidly corrected.  
   
  **iv.** *Blue-Green Deployments:* To reduce downtime and the impact of failures, use blue-green deployments. In this method, a new application version is deployed alongside the current version, tested, and then the traffic is switched to the new version.


 



 

