When you launch the server, you will see the message "WARNING: This is a development server. Do not use it in a
production deployment. Use a production WSGI server instead." It is a warning that Flask displays by default when you
run your Flask app in debug mode.
It reminds you that the built-in development server provided by Flask is not intended for production use due to its
limitations and security risks.

In a production environment, it is recommended to use a production-ready WSGI server, in this project, we use GUNICORN
which is designed to handle higher traffic loads and provide better performance, stability, and security.

Using Gunicorn for deployment

- Add gunicorn in requirements.txt

Open app.py in unifyiq/api/

- app.run(host="0.0.0.0", port=8080)

Test flask app with Gunicorn locally: run following command:
gunicorn app:app
It starts Gunicorn with your Flask app. It will handle incoming HTTP requests and route them to the appropriate Flask
routes for processing.
