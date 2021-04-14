#docker get into container
docker exec -it ds_flask_flask_1 bash

docker exec -it ds_flask_flask_1 python train_model.py

# upload json
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"flower":"1,2,3,7"}' \
  http://localhost:5000/iris_post

# upload file 
curl \
  -F "file=@/home/dshunevich/Documents/test1.txt" \
  http://localhost:5000/upload

  