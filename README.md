# Attendance Fetcher Webservice

##### Test it out in your local machine

1. Clone the project
`git clone https://github.com/devwaseem/Attendance-Fetcher.git`

2. change directory to Attendance-Fetcher: 
`cd Attendance-Fetcher`

3. install virtualenv:
`pip install virtualenv`

4. create a virual environment:
 `virtualenv Attendance-Fetcher-env`
 
5. activate virtualenv:
`source Attendance-Fetcher-env/bin/activate`

6. install the required dependencies:
`pip install -r requirements.txt`

	(this will install the required dependencies for the project automatically)

7. Now run the flask app using:
`python app.py`

Now you will get something like this:
```
* Running on http://0.0.0.0:9000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
```

Now open any browser you like and type this in url:
`http://localhost:9000`

you will be welcomed with: 
```
{
"status": true, 
"Message": "Welcome to TCS-ion Fetcher Webservice"
}
```

At this stage the project is working fine.
you are ready to test the Web service


## API Calls

_I recommend you to use Postman App for making API calls_


### Login 
**URL:** `http://localhost:9000/login`

**METHOD:** `POST`

**PARAMS:** 

field | type
------------ | -------------
username | String
password | String

**RESPONSE:** 

```json
{
	"status": true,
    "code":null,
    "Message": "Login Successful",
    
}
```

field | type | Description
------------ | ------------- | -------------
status | Boolean | This field indicates if the login is successful or not
code | Integer | This helps to find what caused the error
Message | String | Message that can be passed to frontend/user





### Fetch Attendance 
**URL:** `http://localhost:9000/fetch`

**METHOD:** `POST`

**PARAMS:** 

field | type
------------ | -------------
username | String
password | String

**RESPONSE:** 

```json
{
	"status": true,
    "code":null,
    "Message": "Attendance Extraction successful",
    "data":{}
}
```

field | type | Description
------------ | ------------- | -------------
status | Boolean | This field indicates if the login is successful or not
code | Integer | This helps to find what caused the error
Message | String | Message that can be passed to frontend/user
data | String | The actual attendance data


## Error Codes
code | description
-----|-----
100| Login Credentials incorrect
101| Some fields are missing in post body
102| Timeout fetching the attendance


## Changelog

##### [v1.0] 11-Mar-2k19
- Initial Release
- fixed minor bugs
- added requirements.txt for easy dependency installation

