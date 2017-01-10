## Build and Run
```
docker build -t pythonjora -f Dockerfile.dev .

docker run --name pythonjora -it -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -v ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro -v `pwd`:/code -p 9999:9999 pythonjora /bin/bash -c "/opt/conda/bin/jupyter notebook --notebook-dir=/code/notebooks --ip='*' --port=9999 --no-browser"
```
to build the model connect to the running dev container and run
```
docker exec -it pythonjora python train_model.py
```


## Run redshift query
you have to share your bastian private key using: `` -v ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro ``` in the run command

open a new console and run
```
docker exec -it pythonjora ssh -L 9001:redshift-production-cluster.cfecu3xsn81y.us-west-1.redshift.amazonaws.com:5439 ubuntu@52.8.171.106
docker exec -it pythonjora python get_data.py
```


