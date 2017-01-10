## Overview

Simple Blog is a simple blogging framework that can be modified and built upon to meet your needs.

It is built to be deployed on [Google App Engine](https://cloud.google.com/appengine/docs/python/), upon the [webapp2 framework] (https://cloud.google.com/appengine/docs/python/tools/webapp2) and [jinja2 template engine](http://jinja.pocoo.org/).

## Motivation

This is one of my projects for my Udacity Full Stack Developer Nanodegree.

See working example here: https://simple-blog-151718.appspot.com

## Installation

Download Simple Blog first.

Simple Blog requires Python 2.7.x. Please ensure it is installed.

You will need to install required third party libraries. To do so, create a directory at the root of Simple Blog and run:
`pip install -t lib -r requirements.txt`

Because Simple Blog is meant to run on Google App Engine, you will need to deploy it to Google App Engine or run it locally.

You can use Cloud SDK for both of these.

To install Cloud SDK, please see instructions here: https://cloud.google.com/sdk/downloads

To deploy to Google App Engine, see instructions here: https://cloud.google.com/appengine/docs/python/getting-started/deploying-the-application

To run Simple Blog locally, within the Simple Blog directory, run:
`dev_appserver.py .`

Open a browser and visit: localhost:8080

## Running Simple Blog

Simple Blog is, as you guessed, a simple blog. It allows basic functionality you would need in a blog.

The front page allows you to view all blog posts.

A visitor can:
1. create a new account (`/signup`)
2. login (`/login`)
3. (`/logout`)

When logged in, a user can:
1. create a new post
2. edit an existing post
3. comment on posts
4. like/unlike posts


## Acknowledgements

[Google App Engine Boilerplate] (https://github.com/droot/gae-boilerplate) from Sunil Arora

## License

MIT License

Copyright (c) 2016 Brandon Yanofsky

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
