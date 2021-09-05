#
# This is a docker build file to run the latest version of scorch in a purpose built docker container
# The container contains very little else so dont expect bells and whistles, but can be used to run tests 
# on the creation of jobs rather than running the jobs themselves.
#
# Make sure you have docker installed
# sudo apt install docker.io
# docker build --network=host -f Dockerfile-0.2 -t webmarcit/scorch:latest .
# docker image ls
# docker run --rm -i --net=host webmarcit/scorch:latest
# docker exec -it <container-id> /bin/bash

FROM debian
LABEL maintainer "marc@webmarcit.com"

ENV dir_Scorch     /opt/scorch
ENV str_Protocol   http
ENV dir_Location   autoscorch.com/downloads
ENV str_User       scorch
ENV str_Group      scorch
ENV file_Local     scorch.tar

# add user and group    
RUN groupadd -r -g 999 ${str_Group} ; \
    useradd -r -g ${str_Group} -u 999 ${str_User}

# update debian
RUN apt-get update

# Add a couple of package prereqs
RUN	apt-get install -y --no-install-recommends \
    wget \
    curl \
    procps \
    python3 \
	;


# Set a working directory where scorch runs from
WORKDIR ${dir_Scorch}

# grab the latest version of scorch from the internet
RUN wget -O ${file_Local} ${str_Protocol}://${dir_Location}/latest.tar ; \
    tar -xf ${file_Local} ; \
    rm ${file_Local}  

# Run the creation of the primary directories
RUN mkdir -p -m 770 "${dir_Scorch}/jobs/pending" ; \
    mkdir -p -m 770 "${dir_Scorch}/jobs/new" ; \
    mkdir -p -m 770 "${dir_Scorch}/jobs/starting" ; \
    mkdir -p -m 770 "${dir_Scorch}/jobs/failed" ; \
    mkdir -p -m 770 "${dir_Scorch}/jobs/fixing" ; \
    mkdir -p -m 770 "${dir_Scorch}/jobs/deleted" ; \
    mkdir -p -m 770 "${dir_Scorch}/jobs/running" ; \
    mkdir -p -m 770 "${dir_Scorch}/jobs/superseded" ; \
    mkdir -p -m 770 "${dir_Scorch}/jobs/manual" ; \
    mkdir -p -m 770 "${dir_Scorch}/jobs/completed" ; \
    mkdir -p -m 770 "${dir_Scorch}/etc" ; \
    mkdir -p -m 770 "${dir_Scorch}/tmp/" ; \
    mkdir -p -m 770 "${dir_Scorch}/jobs/queued" ; \
    mkdir -p -m 770 "${dir_Scorch}/jobs/active" ; \
    mkdir -p -m 770 "${dir_Scorch}/jobs/archived" ; \
    mkdir -p -m 770 "${dir_Scorch}/var/" ; \
    mkdir -p -m 770 "${dir_Scorch}/var//log/" ; \
    mkdir -p -m 770 "${dir_Scorch}/var//locks/" ; \
    echo "root:POWER:ALL" >> ${dir_Scorch}/etc/users ; \
    touch ${dir_Scorch}/etc/motd
    
# Change ownership to scorch
RUN chown -R ${str_User}:${str_Group} ${dir_Scorch}

# Show how to use it
#RUN echo "# docker build --network=host -f Dockerfile-0.1 -t webmarcit/scorch:latest ."
#RUN echo "# docker image ls"
#RUN echo "# docker run --rm -i --net=host webmarcit/scorch:latest"
#RUN echo "# docker exec -it <container-id> /bin/bash"
#CMD /opt/scorch/scorch
