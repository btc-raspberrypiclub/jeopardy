# The original project is very old and still uses Python 2.7.18
# This needs to be updated to Python 3.8.5 or later after the project is updated
FROM python:2.7.18-buster

# Set the working directory for installations
WORKDIR /app

# Add our python requirements file to the working directory
ADD requirements.txt .

# Install Python basic libraries from the requirements file
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy in any/all additional files from our project
ADD ./ .
# The above is a lazy shortcut to adding all files from the project
# - replace with the following if you want to be more specific
# ADD ./games .
# ADD ./jeoparpy .
# ADD ./res .
# ADD ./button.py .
# ADD ./setup.py .
# ADD ./start.py .
# ADD ?????

# Set default command to run the start.py file
CMD ["/usr/local/bin/python", "start.py"]