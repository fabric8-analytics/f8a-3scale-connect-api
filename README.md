# 3scale-connect-api

A simple flask application.  

run this command: export FLASK_APP=app.py
flask run

to run this application.
 
### How does it help?
 
1. Navigate to http://localhost:5000 once the server is up,
2. You can enter the authentication token in the text area available and click on the button
3. It configures a full fledged 3 Scale setup for that particular information provided you setup your THREE_SCALE_API_ACCESS_KEY and THREE_SCALE_API_ACCOUNT_ID in your OS environment variables.

If everything is perfect, upon completion of the request, it returns you with the app_id, app_key, production and staging urls.
