# CUDL Data Samples

This repo defines a Docker image containing a sample of item data from the main cudl-data repo.

The image is used to provide sample data for the CUDL Viewer dev environment.

## Building

```commandline
$ docker image build -t camdl/cudl-data-samples .
```

> Note: This will take quite a while to build, as the entire contents of cudl-data needs to be transferred to Docker to build the image...
> The resulting image is very small though, only the intermediate build step holds all the data.
