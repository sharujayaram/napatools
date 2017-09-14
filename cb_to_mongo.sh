set -x
python cb_to_mongo.py -threads 10 -customers 1000000 -offset 0 -cbpassword password &
python cb_to_mongo.py -threads 10 -customers 1000000 -offset 1000000 -cbpassword password &
python cb_to_mongo.py -threads 10 -customers 1000000 -offset 2000000 -cbpassword password &
python cb_to_mongo.py -threads 10 -customers 1000000 -offset 3000000 -cbpassword password &
python cb_to_mongo.py -threads 10 -customers 1000000 -offset 4000000 -cbpassword password &
python cb_to_mongo.py -threads 10 -customers 1000000 -offset 5000000 -cbpassword password &
python cb_to_mongo.py -threads 10 -customers 1000000 -offset 6000000 -cbpassword password &
python cb_to_mongo.py -threads 10 -customers 1000000 -offset 7000000 -cbpassword password &
python cb_to_mongo.py -threads 10 -customers 1000000 -offset 8000000 -cbpassword password &
python cb_to_mongo.py -threads 10 -customers 1000000 -offset 9000000 -cbpassword password
