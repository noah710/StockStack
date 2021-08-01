# StockStack

*UPDATE: This project no longer works, as it relies on the [Yahoo! Finance](https://finance.yahoo.com) Historical Data API, which was decomissioned in July 2021*

This was created as a final project for my Web Applications Programming class (CS1520.) I led my team in creating a stock portfolio website that allows users to lookup stocks and create and track their own portfolio. This was implemented with a Flask backend, GCP datastore database, and HTML/CSS/JS. 

## Demos
I deployed this app on GCP AppEngine, check it out [here!](https://cs1520-stockstack.uc.r.appspot.com/)
### Things I thought were cool to implement
#### Async loading of tickers on homepage
![async_loading](https://user-images.githubusercontent.com/42897161/117897349-9e8ce280-b290-11eb-82b2-1e08ba48beaf.gif)

#### User portfolio and removing from portfolio
![profile_load_remove](https://user-images.githubusercontent.com/42897161/117897354-a0ef3c80-b290-11eb-8aa9-d601ce030cd7.gif)

#### Adding to user portfolio
![portfolio_add](https://user-images.githubusercontent.com/42897161/117897358-a482c380-b290-11eb-8d99-1f0f33a5baee.gif)

## Installation

Please install Docker 
## Usage - Docker
<b>You must copy the GCP key to as deploy/GCP_ds_key.json before running serve.sh</b><br>
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
Pages are lazy loaded so any file can be modified while the server is running, besides main.py. If you edit main.py just cntl+c serve.sh and run it again.<br>

## License 
[MIT](https://choosealicense.com/licenses/mit/)

