FROM python:3.11.8-bullseye

# Set some basic image metadata
LABEL org.opencontainers.image.description = "A Jeopardy game for the Raspberry Pi"
LABEL org.opencontainers.image.source=https://github.com/btc-raspberrypiclub/jeopardy
LABEL org.opencontainers.image.licenses=GPL3

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