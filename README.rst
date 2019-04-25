ros2-dev
==========================

This project builds a ROS 2.0 development environment in Docker. The user can
then step into the ROS 2.0 environment to perform additional ROS 2.0 actions
(build, rostopic list, etc.).

Basic Setup
-----------

Install this python package from source: ::

  $ sudo pip3 install -e .

Generate the Dockerfiles to build the base ROS 2.0 environment: ::

  $ ros2-dev generate

Build the Docker image for the base ROS 2.0 environment: ::

  $ ros2-dev build

Step into the base ROS 2.0 environment: ::

  $ ros2-dev env

Run a single command in the ROS 2.0 environment: ::

  $ ros2-dev run -c "ros2 topic list"

Install Additional Dependencies
-------------------------------

Since jinja2 is used to generate the Dockerfiles, a developer can extend the
base Dockerfile by overriding the "third_party" block. An example is provided
in this package at: ./src/ros2dev/templates/third_party.example. To generate a
Dockerfile with an override, use the following command: ::

  $ ros2-dev generate -o ./src/ros2dev/templates/third_party.example

Then build the docker image: ::

  $ ros2-dev build
