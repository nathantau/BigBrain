# BigBrain (API)

In a nutshell, *BigBrain* is a REST API that accepts MRIs of animal brains, and classifies whether or not a tumor is present. You can check it out the live deployment at [bigbrain.nathanau.ca](http://bigbrain.nathanau.ca/). Although the concept of this API seems simple, there are many underlying components and pieces that had to come together to build it successfully (and many iterative attempts).

---

## System Design  

The following is an illustration of *BigBrain's* architecture:

![System Design Architecture](assets/BigBrainSystemDesign.jpg)

---

## Tech Stack

I developed this API with the following tech stack:

### Hosting

- Docker: Docker is a containerization tool that allows applications and dependencies to be packaged in a lightweight container, so that the applications can be run in any Docker compatible environment. I used it along with Docker Compose to containerize my server-side application and my database service.

- Kubernetes: Since Google Cloud Platform does not support Docker Compose, I decided to use Kubernetes to orchestrate and manage my Docker containers.

- Ingress: To add an extra layer of security and to prevent my application to crash from too many requests, I chose to deploy an Ingress service to act as a load balancer.

- Google Cloud Platform: Because I had $300.00 of Google Cloud Platform Credits, I chose to deploy my application with this Cloud Service Provider.

### Server

- Python: To leverage machine learning, I designed this application with Python as it is becoming an increasingly popular and powerful language.

- Flask: Flask/Django are popular server-side frameworks for Python, but I decided to go with Flask due to preference.

- PostgreSQL: As I had sufficient knowledge about PostgreSQL, but never used it in the past, I decided to incorporate it with this project as a learning experience.

### Machine Learning

- Numpy/OpenCV: These libraries are two staples in machine learning. I had to leverage each of them to create an image preprocessing pipeline to prepare the MRIs of animal brains. Unfortunately, I had an unbalanced dataset, so I had to use techniques such as Data Augmentation to compensate. 

- Pytorch: I definitely prefer Pytorch over Tensorflow, as it is more Pythonic in nature and the machine learning aspect definitely feels more hands-on. I used Pytorch to create a convolutional neural network capable of binary classification (Tumor / No tumor), and trained it using the images I preprocessed.

---

## REST Endpoints (for now!)

### Home

*GET:* `/`

*Description:* This endpoint is to test if you can connect to the API successfully. 

### Authorization

*POST:* `/authorization`

*Description:* This endpoint is used to authorize one's user and allow them to access other endpoints. Upon registering/logging in with an email and password, the user will receive an authorization token that will be used in the header of other requests.

*Sample Request:*

```json
{
  "email": "email@email.com",
  "password": "password"
}
```

*Sample Response:* 

```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzUxNTM2OTMsImlhdCI6MTU3NTE1MDA5Mywic3ViIjoibmF0aGFuQGdtYWlsLmNvbSJ9.1CaW-a4mdxbzxXUo4qD1H29b0VmbV6jt_wTXZ0eXGcU"
}
```

### Detect

*POST:* `/detect`

*Description:* This endpoint is used to detect if the Brain MRI passed into it contains a tumor or not. An authorization header is required, or there will be an authorization error.

*Sample Request:*

Header:

```
auth-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzUxNTM2OTMsImlhdCI6MTU3NTE1MDA5Mywic3ViIjoibmF0aGFuQGdtYWlsLmNvbSJ9.1CaW-a4mdxbzxXUo4qD1H29b0VmbV6jt_wTXZ0eXGcU
```

Body:

```
File: image_with_no_tumor.png
```

![Image with no tumor](assets/image_with_no_tumor.jpg)

*Sample Response:* 

```json
{
  "result": "No Tumor"
}
```