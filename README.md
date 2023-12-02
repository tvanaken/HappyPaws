# Our Fast API app!

## Environment Setup

To run this in its current form, you'll need to make sure you have
python 3.11 and pip installed on your system. There is plenty of
documentation online on how to do that for your specific
environment. Once your setup is complete, you should be able to do
something like this and see roughly the same output:

```
$ python --version
Python 3.11.4
$ pip --version
pip 22.3.1 from /usr/lib/python3.11/site-packages/pip (python 3.11)
```

Once you have those installed, you'll need to install `poetry`
globally. If everything is working you should be able to do this as
follows:

```
$ pip install poetry
```

And once it's correctly installed you should be able to do something
like this:

```
$ poetry --version
Poetry (version 1.6.1)
```

## Dev Setup

Now you're ready to install dependencies. Inside the `src` directory,
you'll use `poetry` to do that.

```
$ poetry install
```

Now you can run the development server:

```
$ poetry run uvicorn server:app --reload
```

Open your browser and go to localhost:8000 and you should see the app
running. Uvicorn will reload on changes to the server.py file, so you
should be able to make changes and then just reload the page.

## Formatting

To sort Python files with isort, run the following...

```
$ poetry run isort .
```

To run the flake8 linter on our project, run the following...

```
$ poetry run flake8 .
```

## Docker

### Setup

Pull the latest changes to your local repo.

```
git checkout main
git pull
```

Make sure docker is installed and the daemon is running.

```
docker --version
```

Build the container image.

```
docker build -t csci338-app:latest .
```

### Run the app

Run the container using `docker run` followed by any options and the image
name.

The `-d` option runs the container in "Detached" mode, which frees up your terminal.

The `-p 8000:8000` option maps port 8000 on your host machine to the
container's port 8000. Without this option you will not be able to see the app
from the browser on your host machine.

The `-v ./src:/app` option tells docker to map the `./src` directory on your
host machine to the `/app` directory inside the container. This allows you to
edit the code on your machine and see the updates in the container without
restarting the container.

```
docker run -d -p 8000:8000 -v ./src:/app csci338-app
```

Visit `http://localhost:8000` and behold! The app running in a container!

### Stop the container

Stop the container using `docker stop` followed by the container name or id.

```
docker stop <container-id>
```

### Restart the container

You do not need to run a new container each time you want to work on the code.
You can restart a stopped container using `docker start` followed by the
container name or container id.

```
docker start <container-id>
```

### Remove old images

When a new version of the Dockerfile is available you will need to build the
image again using `docker build` and run a new container using `docker run`.

After a while you may end up with old versions of the image on your system.
These can take up quite a bit of disk space, so it is good to check every so
often and remove old images from your system.

To show the images on your local machine use `docker image ls`.

```
docker image ls
```

Remove any unneeded images using `docker image rm` followed by a list of one or
more image ids or image names.

```
docker image rm <image-id>
```

### Remove old containers

You may want to remove old containers after building and running a new image.
List the containers on your system using `docker container ls`. This will only
show running containers, add the `-a' flag to see stopped containers as well.

```
docker container ls -a
```

You can remove any containers you need by using `docker container rm` followed
by container name or id.

```
docker container rm <container-id>
```

##Python Testing

Once you start your docker container, you'll need to get some new dependencies via poetry.lock:

```
docker start <containerID>
docker exec -it <containerID> poetry install
```

See if it worked:

```
docker exec -it <containerID> poetry run pytest --version
```

Poetry will get what ever dependencies got added to the .lock file and install them in your container. In this case it's Pytest and aiohttp. Pytest is our testing framework. Pytest will grab tests from any module that fit the naming format "test\_\*.py". If you want to run every python test in the project you can enter:

```
docker exec -it <containerID> poetry run pytest
```

or, you can test specific modules and specific functions, by including the moduleName::functionName at the end. The "-v" flag will give you more specific feedback in your test results. Here's an example that tests one function in one file:

```
docker exec -it <containerID> poetry run pytest -v test_example_endpoints.py::test_root
```

## JavaScript Linting

Go into src/ui and enter:

```
npm run lint
```

## Application Developers

| Name | GitHub Username |
|--|--|
| Mason Bradley | @mbradle07 |
| Alex Clark | @aclark1997 |
| Jackson Coley | @jcoley1 |
| Taylor Fields | @36-Chambers |
| Haley Grant | @hgrant2 |
| Taylor Hodges | @Christian-Hodges |
| Hayden Holbrook | @hholb |
| Nicholas Howe | @nghowe |
| Chris Hooke | @BACONWRAP |
| Anthony Mason| @Amason-0224 |
| Tom Philipps | @tomphlpp |
| Semmy Purewal | @semmypurewal |
| Will Shamblin | @wcshamblin |
|Seth Satterwhite | ssatterw@unca.edu |
| Kamren Sims | @ksims20 |
| Taylor Van Aken | @tvanaken |
| Sarah Van Wart | @vanwars |
| Drew Yost | @dsyost |

```
