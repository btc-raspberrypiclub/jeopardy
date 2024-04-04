FROM python:3.11.8-bullseye

# Set some basic image metadata
LABEL org.opencontainers.image.description = "A Jeopardy game for the Raspberry Pi"
LABEL org.opencontainers.image.source=https://github.com/btc-raspberrypiclub/jeopardy
LABEL org.opencontainers.image.licenses=GPL3

# Set the working directory for installations
WORKDIR /app

# Install OS packages
RUN apt update && apt install -y \
    libsdl2-dev libsdl2-2.0-0 \
    libjpeg-dev libpng-dev libwebp-dev libtiff-dev \
    libsdl2-image-dev libsdl2-image-2.0-0 \
    libmikmod-dev libfishsound1-dev libsmpeg-dev liboggz2-dev \
    libflac-dev libfluidsynth-dev libsdl2-mixer-dev libsdl2-mixer-2.0-0 \
    libfreetype6-dev libsdl2-ttf-dev libsdl2-ttf-2.0-0 pipewire

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
