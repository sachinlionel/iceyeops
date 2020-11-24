# Dockerized hello service
- Docker Image instructions are on `Dockerfile`
- `docker-compose.yml` is a manifest for running Hello server as containerized service.
- `.env` is used to override default environment variable for docker-compose.yml, following are env variables.
    1. PORT
    2. IP_ADDR 
- `testops.ym`l is manifest containing hello server deployment & cluster ID service
- `app/hello.py` python test client for hello
- `test.py` basic tests (uses Unittest module, `python3 test.py` to execute tests)

## Docker Image Instructions
```
# Base os for continer, LINUX OS
FROM alpine:3.12

# Install curl with no cache arg, curl to used for bash testing, python3 for python tests
RUN  apk --no-cache add curl python3

# Specify WORKDIR, After the layer, PWD will be mentioned WORKDIR
WORKDIR /usr/local/app

# Copy binary and other modules to WORKDIR
COPY hello hello
COPY app app
COPY .env .env
COPY test.py test.py

# Set default ENV variables
ENV PORT "8080"
ENV IP_ADDR "0.0.0.0"

# Default contianer executable default
# `&> server.log` directs std output & std log to server.log
CMD ["sh", "-c", "./hello -addr ${IP_ADDR}:${PORT} &> server.log"]
```

## How to build Docker IMAGE ?
```
syntax: docker build . -t {IMAGE_NAME}:{IMAGE_TAG} # Make sure Dockerfile is in PWD
commnad: docker build . -t testops:0.1
```

## How to check Docker IMAGE ?
```
docker images
REPOSITORY                                TAG                 IMAGE ID            CREATED             SIZE
testops                                  0.1                 c072eac7a9b9        About an hour ago   53.6MB
docker inspect {IMAGE ID} # for details
```

## Docker image takes two env arguments
```
PORT -- server port, default 8080
IP_ADDR -- server ip, default 0.0.0.0, (null, will work too)
```

## Run local dockerized service
```
syntax: docker run -p={HOST_PORT}:{CONTAINER_PORT} {IMAGE_NAME}:{IMAGE_TAG} &
commnad: docker run -p=8080:8080 testops:0.1 &
```
## Tests:
```
curl 0.0.0.0:8080/--sachin--
Hi there, --sachin--!
curl 127.0.0.1:8080/--sachin--
Hi there, --sachin--!
```
## Clean up
```
docker stop {CONTAINER_ID}
docker rm {CONTAINER_ID}
``` 

## Run local dockerized service using docker-compose
```
syntax: docker-compose up -d # make sure docker-compose.yml is in PWD
commnad:  docker-compose up -d
```
## Tests:
```
curl 0.0.0.0:8080/--sachin--
Hi there, --sachin--!
curl 127.0.0.1:8080/--sachin--
Hi there, --sachin--!
```
## Clean up
```
docker-compose down
```

## Run local dockerized service on custom port?
```
syntax: docker run --env {ARG_KEY}={ARG_VALUE} -p={HOST_PORT}:{CONTAINER_PORT} {IMAGE_NAME}:{IMAGE_TAG} &
commnad: docker run --env PORT=9090 -p=9090:9090 testops:0.1 &
```
## Tests:
```
curl 0.0.0.0:9090/--sachin--
Hi there, --sachin--!
```

## Clean up
```
docker stop {CONTAINER_ID}
docker rm {CONTAINER_ID}
``` 

## Prepare local Kubernetes cluster
Download and install minikube 
```
# Make sure you have docker installed on you OS
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64 # Download binary
sudo install minikube-darwin-amd64 /usr/local/bin/minikube # Install binary
minikube start # Start minikube
minikube kubectl # Install kubernetes command line tool kubectl
eval $(minikube docker-env) # Execute on every terminal to access minikube docker environment using docker commands
```

## Run the service in your cluster:
Build docker image on minikube docker env
```
eval $(minikube docker-env) # activate minikube docker env
docker build . -t testops:0.1 # build docker image for kubernetes
```
Minikube provides single node cluster for kubernetes deployment, make sure nodes are in ready state. 
```
kubectl get nodes
NAME       STATUS   ROLES    AGE   VERSION
minikube   Ready    master   37h   v1.18.3
```
Deployments and service are defined in testops.yml, use one of the below commands to create deployments && sevice
```
kubectl create -f testops.yml
kubectl apply -f testops.yml

output:
deployment.apps/testops-deployment created
service/testops-service created
```
Make sure kubernetes pods & service are created.
```
$ kubectl get pods 
NAME                                   READY   STATUS    RESTARTS   AGE
testops-deployment-57f47585b5-47964   1/1     Running   0          56s
testops-deployment-57f47585b5-67mk5   1/1     Running   0          56s
testops-deployment-57f47585b5-zxbh9   1/1     Running   0          56s
You have new mail in /var/mail/sachin
$ kubectl get service
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
testops-service   ClusterIP   10.103.118.14   <none>        8080/TCP   69s
kubernetes         ClusterIP   10.96.0.1       <none>        443/TCP    38h
```
- The testops-service[CLUSTER-IP] is cluster internal IP, can be accessed internally from nodes or kubernetes pods (testops-deployment container)
## Tests from minikube node
```
$ minikube ssh
                         _             _            
            _         _ ( )           ( )           
  ___ ___  (_)  ___  (_)| |/')  _   _ | |_      __  
/' _ ` _ `\| |/' _ `\| || , <  ( ) ( )| '_`\  /'__`\
| ( ) ( ) || || ( ) || || |\`\ | (_) || |_) )(  ___/
(_) (_) (_)(_)(_) (_)(_)(_) (_)`\___/'(_,__/'`\____)

$ curl 10.103.118.14:8080
Hi there, !
$ curl 10.103.118.14:8080/--sachin--
Hi there, --sachin--!
```
## Tests from kubernetes pods
```
$ kubectl exec --stdin --tty testops-deployment-57f47585b5-47964 sh
/usr/local/app # curl 10.103.118.14:8080/--sachin--
Hi there, --sachin--!
```
## To access service from local execute below commands, forwards localhost:port traffic to clusterIP:port
```
kubectl port-forward service/testops-service 8080:8080

output:
Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
Handling connection for 8080
```
## Tests from local:
```
$ curl 0.0.0.0:8080/--sachin--
Hi there, --sachin--!S
```
## To production:
Using NodePort/LoadBalancer
- Use NodePort/LoadBalancer service type in service manifest
- Create service and activate, `command to activate, minikube service testops-service --url`
- Add firewall rule to allow traffic to nodePort from internet.
```
# Service NodePort/LoadBalancer manifest
---
apiVersion: v1
kind: Service
metadata:
  name: testops-service

spec:
  type: NodePort/LoadBalancer
  selector:
    app: test
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
      nodePort: 30001
```
## Test from local:
```
# Update the service and execute below commands
$ kubectl delete -f testops.yml 
$ kubectl apply -f testops.yml 
$ minikube service testops-service --url
http://192.168.64.4:30001
$ curl http://192.168.64.4:30001
Hi there, !
$ curl http://192.168.64.4:30001/--sachin--
Hi there, --sachin--! 
```

## Clean up
```
kubectl delete -f testops.yml
minikube stop
```

## QA client and tests
- QA client is available at `app/hello.py`
- QA tests are available at `test.py` (Unittest)
- On any container of testops:0.1 docker image, execute `python3 tests.py` for tests.
