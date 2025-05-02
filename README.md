# ids-restaurant-bot
**CSE 40982 Final Project**
**Dagny Brand and Zach Brown**

## Running Locally
### Clone the Repository
1. Clone the directory with `git clone git@github.com:dagnybrand/ids-restaurant-bot.git`

### Find Yelp Data
1. Ensure access to `/data/cse40982/students/dbrand/project/ids-restaurant-bot/data/` or download the data 

### Install Dependencies
1. Create and activate a new virtual environment
2. Install necessary dependencies listed in `requirements.txt`
3. Create a `.env` file in the root directory of the project with `OPENAI_KEY` to an OpenAI key

### To Run Model
1. Run `python restaurant_bot.py -m {model_dir} -d {yelp_data_dir}` from the root directory to open the chat. `model_dir` is the path to the `ckpt.pt` file for the GPT2 model and defaults to `jam/out-restaurant-bot`. `yelp_data_dir` is the path to the Yelp JSON files, likely `/data/cse40982/students/dbrand/project/ids-restaurant-bot/data/`. If `yelp_data_dir` is not specified, the bot will attempt to connect to a local ClickHouse instance. 
2. Type in a question regarding a restaurant suggetions, tips, or reviews
- to receive a restaurant suggestion, specify a food type and a city
3. Type `exit` or `quit` to stop

## Training the Model
### Generate Training Data
1. From the root directory, run `generate_training_data.py` to generate the training data file from the provided templates and values in the data directory
### Prepare the Data Binaries
1. From the root directory, run `prepare_data.py` to convert the files in the tmp directory created above into the training and validation binaries
### Train the Model
1. `cd jam`
2. From jam, run `CUDA_DEVICE_ORDER='PCI_BUS_ID' OMP_NUM_THREADS=2 torchrun --rdzv-backend=c10d --rdzv-endpoint=localhost:0 --nnodes=1 --nproc-per-node=1 train.py config/train_restaurant_bot.py --out_dir=out-restaurant-bot`. To target a specific GPU, `CUDA_VISIBLE_DEVICES='{i}'` can be set.


## Yelp Data Options
Yelp provides this data as 5 JSON files with some as large as 5+ GB. These files can be large and difficult to parse. Attempting to load them into memory using the json library or pandas either took far too long or was not supported on this machine. We found two possible options to better search these files, each with their own pros and cons. 
### JSON Files (Default)
The first option is keeping the data in its native format as JSON files and searching the files using `chdb` a limited, yet powerful Python ClickHouse library. This option is the simplest as nothing has to be changed about the data. The queries in our system can take up to around 10 seconds using this option. However, the resource consumption is reasonable.
### ClickHouse Database
The other option is making this data available through a ClickHouse server. All of the pieces to run the server are available at `/data/cse40982/students/zbrown2/ids-restaurant-bot/db`, where the data is already loaded in. To start the server, in that directory run `./clickhouse server -C config.xml`. Then, the restaurant bot can be run the same as above, but without providing a data directory CLI argument. Based on initial tests, this option can be up to 100x faster than keeping the data in the JSON files. However, it consumes a vast amount of resources and resulted in me getting kicked off of gpu00 for running too many processes and maybe using too much memory. For the highest level of performance, this option is definitely preferable; however, it may not be practical with the constraints of gpu00. 