# Jeopardy Pi Edition

Play Jeopardy on your Raspberry Pi

## Setup

How to get Jeopardy running on your Raspberry Pi

- install docker
- create a copy of the `docker-compose.yml` file
- run `docker compose up`

### Hardware

Follow these instructions:</br>
http://hackaday.io/project/3721/instructions

### Software

Follow these instructions:</br>
http://hackaday.io/project/3721-game-show-emulator/log/12365

## Building

To build the container image localy:

    docker compose --profile build build

## Notes

This software is designed to be used with the Raspberry Pi. If you would like to run Jeopardy on a Windows or Ubuntu please use Adam Beagle's <a href='https://github.com/adambeagle/jeoparpy'>jeoparpy software</a>. 

Also, to use the X11 system from within a container, see this [Medium article](https://medium.com/geekculture/run-a-gui-software-inside-a-docker-container-dce61771f9).

WARNING!!! This repo is under rapid development as we move it to modern Python and put it into a container image to more easily be run and maintained.
