# ArubaCentralAPI
Python code to interface with the Aruba Central APIs (including OATH token management)

## Getting Started
These instructions will assist get the project up and running on your local machine for development and testing purposes.

### Prerequisites
* An active Aruba Central account and an application defined in "Maintenance -> API Gateway -> System Apps & Tokens".  Take note of the CLIENT ID and CLIENT SECRET associated with your API application.
* A unique user defined in "Global Settings -> Users & Roles" that will be used to authenticate to Aruba Central and generate an access and refresh token using the full OATH workflow.  It is recommended that this user is allocated a "readonly" role if you do not wish for your environment to be modified. Note that **HPE SSO does NOT work**, so please refer to these [instructions](https://arubapedia.arubanetworks.com/arubapedia/index.php/SEEL_-_ArubaCentral_setup_and_Demo#Restrictions_on_email_addresses_that_can_be_added_on_Internal) to create a non-HPE username/password for INTERNAL accounts.

### Installing
Deploy all files into a new project using your preferred Python IDE, and modify "token.json" and "creds.json" as below before running "ArubaCentralLab.py" for the first time:

#### *token.json*
Manually edit OR select your API application in Aruba Central and save JSON from "View Tokens -> Download Token"
```
{
  "access_token": "can_be_blank_if_no_valid_token_exists",
  "refresh_token": "can_be_blank_if_no_valid_token_exists"
}
```
Note that *token.json* will be automatically updated with the most recent access and refresh token/s if either are generated or refreshed through the OATH workflow.

#### *creds.json*
```
{
  "base_url": "https://internal-apigw.central.arubanetworks.com (INTERNAL) OR https://app1-apigw.central.arubanetworks.com (PRODUCTION)",
  "customer_id": "Customer_ID_of_API_application_as_defined_in_prerequisities",
  "username": "unique_user_as_defined_in_prerequisities",
  "password": "unique_user_as_defined_in_prerequisities",
  "client_id": "CLIENT_ID_as_defined_in_prerequisities",
  "client_secret": "CLIENT_SECRET_as_defined_in_prerequisities"
}
```

## Running
There are sample use cases in *ArubaCentralLab.py* to demonstrate how to use *ArubaCentralAPI.py*.

The high-level process is to first instantiate a user which will ensure that a valid access token exists:
```
user = ArubaCentralAPI.getUser()
```

If both *token.json* and *creds.json* are accessible and have all required key/value pairs:
```
Importing Tokens...
SUCCESS

Importing Credentials...
SUCCESS
```

If any key/value pairs are missing from either *token.json* and/or *creds.json*:
```
Importing Tokens...
ERROR -> Missing key/value pair in token.json -> 'access_token'

Importing Credentials...
ERROR -> Missing key/value pair in creds.json -> 'base_url'
```

If *token.json* contains a valid "access_token":
```
Verifying Access Token...
SUCCESS
```

If *token.json* contains an invalid "access_token" but a valid "refresh_token":
```
Verifying Access Token...
ERROR -> Invalid Access Token: invalid_token -> The access token is invalid or has expired

Refreshing access token using refresh token...
Access Token: ******************************** 
Refresh Token: ********************************
```

If *token.json* contains both an invalid "access_token" and "refresh_token":
```
Verifying Access Token...
ERROR -> Invalid Access Token: invalid_token -> The access token is invalid or has expired

Refreshing access token using refresh token...
ERROR -> Invalid Refresh Token: invalid_request -> Invalid refresh_token

Authenticating to Aruba Central...
CSRF Cookie: ****************************************** 
Session Cookie: *************************************************************

Requesting authorization code...
Authorization Code: ********************************

Exchanging for access and refresh token...
Access Token: ******************************** 
Refresh Token: ********************************
```

Once a valid user has been instantiated, a generic GET query can be made by providing the specific URL suffix for the API call that is required.  For example, to return the "Total Clients Count":
```
request_path = "/monitoring/v1/clients/count"
api_response = ArubaCentralAPI.genericQuery(user, request_path)
```

## Contributing
I am open to requests to update, modify and improve this code!  Please let me know if you have feedback or would like to contribute and we can discuss options to do so.

## Versioning
* *v1.0 (January 2019)* - **Nick Harders** @ [NicholasHarders](https://github.hpe.com/nicholas-harders)
