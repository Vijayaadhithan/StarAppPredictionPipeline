# Predict star app using Ansible 

## Overview

The GitHub Star Predictor App is a machine learning-based application designed to forecast the star count for GitHub repositories. The project encompasses data collection from the top 1000 repositories, model training and evaluation, and an automated deployment pipeline for continuous integration and delivery.

## Key Features

## Data Ingestion:
* Utilizes GitHub API to collect historical data from the top 1000 repositories.
* Addresses API rate limits and implements error handling for robust data collection.
## Data Governance:
Ensures data integrity using RabbitMQ for messaging between distributed systems.
## Workflow Orchestration:
Ansible framework for configuration and contextualization of both development and production servers.
## Data Transformation:
Python program for data preprocessing, including one-hot encoding for the language column.
## Data Processing:
* Machine learning models (Linear Regression, Random Forest, Decision Tree, K-NN) were evaluated based on r2.
* Celery framework on the production server for distributed prediction using Docker workers.
## Integration and Deployment:
* Git Hooks enables continuous integration and deployment.
* Flask framework for a front-end component, providing web pages for scores, top GitHub repositories, and performance measurement.
## Scalability:
Docker on the production server allows for horizontal scalability with the addition of more workers.

## To run this model follow the below steps:
Project repo for Data Engineering.
Evaluating the accuracy of prediction of stargazers in Git hub repo using its token 

To start the development and production server: 
1. Go to model/single_node
2. Change key if needed in start_instances.py and then run it (*python3 start_instances.py*)

To apply Ansible to the servers:
1. Open the Ansible inventory file and add the IP addresses of the servers in that file (*sudo nano /etc/ansible/hosts*)
2. Add your github user and token to configuration.yml under name "Download git repository"
3. Run *export ANSIBLE_HOST_KEY_CHECKING=False* and *ansible-playbook configuration.yml --private-key=/home/ubuntu/cluster-keys/cluster-key*

To build an execution pipeline using GitHooks:
1. Go to development server generate a key (*ssh-keygen*) and add that key to production server (*nano /home/appuser/.ssh/authorized_keys*)
2. Create a jump directory in production server and do *git init --bare*
3. Create a git hook post-receive in production server git directory with the right directory: 
```
#!/bin/bash
while read oldrev newrev ref
do
 if [[ $ref =~ .*/master$ ]];
 then
  echo "Master ref received. Deploying master branch to production..."
  sudo git --work-tree=/Data_Eng_Proj_2/model/ci_cd/production_server --git-dir=/home/appuser/my_project checkout -f
 else
  echo "Ref $ref successfully received. Doing nothing: only the master branch may be deployed on this server."
 fi
done
```
4. Create empty git repository in development server (*git init*)
5. Add the files in model/ci_cd/development_server
6. Train and compare the models (run script *get_data.sh*)
7. Commit file to production server.
You should now be able to se the trained models and comparison on the webpage. As well as the top 10 git repositorys

Scalability test:
scalability tests was done by first loading the best model from the development server to the production server by using GitHooks execution pipeline. On the production server run
```
# docker compose up --scale worker_1=<insert_number> -d
# docker compose restart
```
with 1 to 3 workers. The result the  got automaticly posted to our server at 5100/time

