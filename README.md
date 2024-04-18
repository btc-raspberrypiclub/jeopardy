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

Buttons:</br>
https://www.amazon.com/EG-STARTS-Buttons-100mm-Dome/dp/B086ZNTZ8H/ref=sr_1_3?crid=1D6Y5717I03AJ&dib=eyJ2IjoiMSJ9.h18wDCspquoELQx_4QZp4wWn28Dm9-6Vg3cEnVxOiHRZ9VxB-8SBWS6CXqsCeLDwPRz22ZliOY8eUWrv74gjOLgiGbPh9TEih17cR9TuuQw.T1Kkb5Q51lZCVslgmVYn64Vg4yu4cLPQSqYPrE5CvPE&dib_tag=se&keywords=100mm+eg+arcade+buttons&qid=1712113818&sprefix=100mm+eg+arcade+button%2Caps%2C168&sr=8-3

-suggested to have additional buttons setup

Button batteries:</br>
https://www.amazon.com/Amazon-Basics-23A-Alkaline-Battery/dp/B07GNMFLKH/ref=sr_1_6?crid=S6KZNZC5A81P&dib=eyJ2IjoiMSJ9.qHPvGJaQMBx6gVdPr_d8gmjHwodQ2Ut3YgTGczLIyqSPK1ZykgxuFB45s_QqFQ99viigGp2liN4i6byDbOCcSu-_NOUjgxrIDm_5-j2VmXEYJ_m5c2NC8QeD3lseU2v3H8_tzwNc1t2nruKsgswhZG-dbJUPioLn8hexczIzULjkY-eo5znp65cXImiBP4kHx451509IRMWB113mbQX75mCaL4_mW-m2QedChFF3RbuwQC7TemskBrQxuiWAfPawO6S8NnN0ACEEdivePtYwhfw_o-3rTs716UvqB52S4j4.v0oBlUGlWh7nmFbw_yML7eLB0FqOylt49szowXb4f70&dib_tag=se&keywords=12+v+battery&qid=1712113296&sprefix=12+v+battery+%2Caps%2C178&sr=8-6

-will require about 12 batteries for back ups and testing


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
