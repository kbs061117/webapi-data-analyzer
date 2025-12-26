# webapi_data_analyzer

## Install
pip install -r requirements.txt

## Run (examples)
python main.py --example users --save-csv
python main.py --example todos --save-csv

## Run (custom url)
python main.py --url "https://jsonplaceholder.typicode.com/users" --save-csv

## Choose columns
python main.py --example todos --hist id --bar completed --save-csv
