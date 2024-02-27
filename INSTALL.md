# Initial Configurations

To set up and operate Smart HPA, you will require an AWS EKS cluster and 10 AWS EC2 instances for running the microservice benchmark application. Additionally, you will need a separate machine to run Smart HPA and the load testing tool, Locust (https://locust.io).  

### EKS Cluster Configurations

The Amazon EKS cluster employs Kubernetes version 1.24, with default AWS VPC network and subnet settings, IPv4 IP cluster family, API server endpoints having both private and public network access, and incorporates add-ons networking features of EKS cluster, such as kube-proxy, CoreDNS, and VPC CNI.

### EC2 Nodes configurations

Each EC2 instance (VM machine) is configured as a t3.medium instance, equipped with an Intel Xeon Platinum 8000 series processor,  2-core 3.1 GHz CPU, 4GB of RAM, 5Gbps network bandwidth, 5GiB disk size, supporting up to 3 elastic network interfaces and 18 IP addresses. All 10 EC2 instances run on the Linux operating system (AL2_x86_64) with the EKS-optimized Amazon Linux AMI.

### Local Machine Configurations

Smart HPA and Load Generating Tool (i.e., Locust) are hosted on a local machine, featuring an Intel Corei7 2.60GHz CPU and 16GB RAM. Smart HPA is connected to the application running on AWS EKS through the AWS command-line interface.


# Steps for Setup

#### Step 1: Connect EKS Cluster with Local Machine
Create an EKS Cluster on AWS account with 10 EC2 nodes (VM machines) with the specified configurations. Connect the EKS cluster with the local machine through the following command.

aws eks update-kubeconfig --region YourRegionName --name YourClusterName


#### Step 2: Deploy the Benchmark Application
Deploy the benchmark application (Online Boutique) to the EKS cluster:

kubectl apply -f ./release/kubernetes-manifests.yaml

#### Step 3: Install metrics server on AWS EKS cluster

https://docs.aws.amazon.com/eks/latest/userguide/metrics-server.html 

Verify the installation: kubectl top pod

#### Step 4: Get the Frontend's External IP (Benchmark Application Access Link)
kubectl get all

Note the frontend’s external IP, for example: a4aa7c15864d64938addf2e4f76e84ef-313638180.ap-southeast-2.elb.amazonaws.com

Access the web frontend in a browser using the frontend's external IP.

#### You have now successfully set up the benchmark application, EKS cluster, and worker nodes.

### Step 5 and 6 Run in Parallel

These steps should be run in parallel, starting at the same time.

#### Step 5: Run Smart HPA

Run the “Microservice Capacity Analyzer” script placed in the “Smart HPA Codebase folder.” It will call the Microservice Managers scripts and Adaptive Resource Manager script. Ensure these scripts are placed in the same directory as Microservice Capacity Analyzer. Check the path of the Knowledge Base in the scripts of Microservice Managers.

#### Step 6: Run Load Test Script

Run the Load Test Script placed in the benchmark application. Go to the directory of the Load Test script in the command window and enter the following command:

locust -f Load_Test_Script.py --host=YourFrontendIP --csv=my_results --csv-full-history

Open the browser and go to the Locust interface through http://localhost:8089 to run the load test.

Configure the load test settings:

Number of Users: 600, 
Spawn Rate: 2, 
Host: Your frontend’s external IP address, 
Time: 900s (i.e., 15 minutes)



