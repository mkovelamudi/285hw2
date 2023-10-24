# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /

# Copy the current directory contents into the container at /app
COPY . .
# Install the required packages

RUN pip install -r requirements.txt


# Make port 8000 available to the world outside this container
# EXPOSE 8000

# Define an environment variable for Flask to run in production mode
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
ENV PORT=5000

# ENTRYPOINT [ "python" ]
# Run the Flask application when the container launches
CMD ["flask", "run"]
