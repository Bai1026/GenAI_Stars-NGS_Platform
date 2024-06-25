# How to use these script

- Stop and delete all the current docker
```bash
docker stop jovial_wright
docker rm jovial_wright
```

- Restart the Elasticsearch container using host network mode
```bash
docker run -d --network host --name elasticsearch elasticsearch:7.10.1
```

- Get the Docker container IP address
```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' jovial_wright
```

- Check the host to elasticsearch connection condition
```bash
curl -X GET "localhost:9200/"
```