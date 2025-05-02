# ids-restaurant-bot
**CSE 40982 Final Project**
**Dagny Brand and Zach Brown**

### To Find Data
1. The data is located in `/data/cse40982/students/dbrand/project/ids-restaurant-bot/data/`

### Install Dependencies
1. Create virtual environment
2. Install necessary dependencies listed in `requirements.txt`

### To Train Model
1. From the root directory, run `generate_training_data.py`
2. From the root directory, run `prepare_data.py`
3. `cd jam`
4. From jam, run `train.py config/train_restaurant_bot.py`

### To Run Model
1. Run `python restaurant_bot.py` from the root directory to open the chat
2. Type in a question regarding a restaurant suggetions, tips, or reviews
- to receive a restaurant suggestion, specify a food type and a city
3. Type `exit` or `quit` to stop