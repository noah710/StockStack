# StockStack

StockStack is a Flask app for CS1520

## Installation

Please install Docker 
## Usage
To run the flask server, run this from the root directory
```bash
./serve.sh
```
Then navigate to http://localhost:8080 <br><br>
To install new requirements or fresh build, run it like this
```bash
./serve.sh fresh
```
## Use without docker
```bash
cd src
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/cs1520-stockstack-747fd526bb24.json
python3 main.py
```
<br>
Pages are lazy loaded so any file can be modified while the server is running, besides main.py. If you edit main.py just cntl+c serve.sh and run it again.
## License
[MIT](https://choosealicense.com/licenses/mit/)
