
#### The model interface API is runned on docker.\n
## To run the model all you need to do is:
## 1. Clone the source code
## 2. Navigate the interface forder 
## 3. Run the docker by the following:
### 3-a. Build the docker image by this command:
`docker build -t image-name .`
### 3-b. Create a container for the image and run it:
`docker run -d -p 80:80 --name container-name image-name`


## How to use the API:

### 1. Locate the API on the URL:
`http://localhost/docs`
### 2.Click recommend
### 3. Click on the "Try it out" button, then on the json file enter the book name on the string text and number of books you want to get recommended on the count field. Finally click "execute" button. The numbers shown are the ISBN of the recommended books.



# Note: I had an issue wit running the project with docker, so I had to run it on my local machine. I will try to fix it as soon as possible.

## Here is the way to run the project on your local machine using uvicorn:
### 1. Clone the source code
### 2. Navigate the interface forder.
``` cd app ```
### 3. Run the following command:
``` uvicorn main:app```
### 4. Open your browser and navigate to:
``` http://127.0.0.1:8000/docs ```

#### And you are good to go.

#### Engooooy it!!!