# SSYS_Test
API with defined routes and functionalities as challenge.


## Contents

* [Definition of Done](#definition-of-done)
* [Setup](#setup)

## Definition of Done

Create SSYS Employee Manager CRUD containing the given routes:

* GET /employees/ (employee list)
* POST /employees/ (create)
* UPDATE /employees/ID
* DELETE /employees/ID
* GET /employees/ID/ (employee detail)

Reports:

 * GET /reports/employees/salary/ (must have lowest, highest and average fields)
 * GET /reports/employees/age/ (must have youger, older and average fields)

Last but not least important, persist data and use authentication to access.

* Registering new users

```
curl -X POST -H 
$ curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser", "password1":"testpassword", "password2":"testpassword"}' localhost:8000/registration/
```
* Expected response:

```
{"key":"1565c60a136420bc733b10c4a165e07698014acb"}
```

* To use the API make the request as example:
```
$ curl -X GET -H 'Authorization: Token 1565c60a136420bc733b10c4a165e07698014acb' localhost:8000/employees
```

## Setup
To install all dependencies, run the command below:
```
$ pip3 install -r requirements.txt
```