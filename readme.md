
Пример веб-сервиса на Flask, который демонстрирует работу модели k-NN (алгоритма классификации) на классическом датасете "Ирисы Фишера". 

1. Отправка файла csv:
Перейдите на страницу http://ec2-3-128-182-25.us-east-2.compute.amazonaws.com:5000/submit, введите наименование файла предикта (итогового файла с предсказаниями класса цветка), загрузите файл формата csv с параметрами лепестков ириса (см. пример ниже) 

-----------
| 1,2,4,5 |
| 2,1,4,0 |
-----------

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

После нажатия на кнопку "Go", скачается файл формата csv с предсказаниями классов цветков (исходя из параметров):

---
|0|
|2|
|1|
---







Docker commands:

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

  
