# ids-restaurant-bot
**CSE 40982 Final Project**
**Dagny Brand and Zach Brown**

### Steps to generate data
1. Add data to `new_training_data.txt` in QUERY RESPONSE format
2. Run `format_training_data.py` to split data into seperate files for tokenizing
3. Temp data files will be located in `tmp\`

### Steps to train model
1. Run `prepare_data.py` to split data into train, test, and validation sets and to tokenize
2. From the `jam` directory, run CUDA on `train.py` with `config/train_restaurant_bot.py` as a specification
3. Trained model will be saved to `jam/restaurant-bot`

### Steps to run model
1. Run `sample_restaurant_bot.py` from the root directory