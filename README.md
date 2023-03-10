# codesign_assignment

------
## To run this project you have to follow some steps.

#### **Step No 1.**

#### Clone the hole project from [codesign_assignment](https://github.com/MdArifulislam21/codesign_assignment)

#### Step No 2.

> Go to the coller_palettes_api folder inside **codesign_assignment** directory and open the terminal in this directory 

> install virtualenv  
> for linux 
 ````python3 -m pip install --user virtualenv```
 ````python3 -m venv env```

> for windows 
 ````py -m pip install --user virtualenv```
 ````py -m venv env```
------
> activate virtualend  
> for linux ````source env/bin/activate````
>for windows ````.\env\Scripts\activate````


> after that run ````pip install -r requirements.txt````

> And run the command: ````python manage.py runserver````



## Api Documentation 

## Api Url: http://127.0.0.1:8000/graphql

### register api
```mutation {
  userRegister(
    input:{
      email: "ariful@test.com",
      username: "ariful",
      password1: "Test1234",
      password2: "Test1234",
    }
   
  ) {
    user{
      id
      username
      username
    }
  }
}
````
> response 
````{
  "data": {
    "userRegister": {
      "user": {
        "id": "VXNlclR5cGU6Ng==",
        "username": "arif10"
      }
    }
  }
}````

### login api
> It will return users token
```
mutation {
  loginToken(
    email: "ariful@test.com",
    password: "Test1234",

  ) {
    success,
    errors,
    token
  }
}
````
> response 
```
{
  "data": {
    "loginToken": {
      "success": true,
      "errors": null,
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFyaWYyIiwiZXhwIjoxNjc4NDUxOTU0LCJvcmlnSWF0IjoxNjc4NDUxNjU0fQ.K4RlfRq4lBg6iV8gndpu5l31meg8Pd_KNJV3meIGmCg"
    }
  }
}
````