 # Welcome to Design and Develop Problem 8!

## **Question of Design Problem :**
You are a DevOps engineer working at a big tech company and your manager has given you a task to migrate a three-tier PHP-based monolithic application to microservices. Consider the scenario that the application is running on a EC2 server with ALB in front of it. Now design an E2E architecture that would containerize the application.  
+ How the application would be migrated to microservices
+ Need a running application of container based services
+ The application should have an E2E CI/CD pipeline that would build the application and deploy the updated code/manifest on the container-based services


The structural design fro the given problem is given below:
![Alt text](Design%208.jpg)

## **Method:**   

**1.** The MONOLITH have 3-tier of PHP and it converted into container and send to AWS ECR.  

**2.**  Store the Docker image of the monolithic application.  

**3.** Create an ECS cluster and an ECS task definition for the monolithic application. The task definition should specify the Docker image and any necessary parameters for the container, such as the port mapping and environment variables.  

**4.** ALB: Configure the Application Load Balancer to route traffic to the ECS container instances running the monolithic application.  

**5.** CodePipeline: Automate the build, test, and deployment of the monolithic application using a pipeline that includes CodeBuild, ECR, ECS, and ALB.


