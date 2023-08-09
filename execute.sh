#!/bin/sh -xe
export PATH=$PATH: https://github.com/siya2799/77721767513_telecomchurn.git
if [ $( docker ps -a -q --filter ancestor=telecomchurn --format="{{.ID}}" | wc -l ) -gt 0 ]; then
	docker rm $(docker stop $(docker ps -a -q --filter ancestor=telecomchurn --format="{{.ID}}"))
fi
docker build -t telecom .
docker run --name telecom -p 4000:8000 telecom &