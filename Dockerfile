# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5002

# Define environment variable
ENV NAME hm

# Run app.py when the container launches
CMD ["python", "server.py"]



# Set proxy server, replace host:port with values for your servers
#ENV http_proxy 172.16.50.167:5002
#ENV https_proxy 172.16.50.167:5002

