# Predict star app using Ansible 
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

