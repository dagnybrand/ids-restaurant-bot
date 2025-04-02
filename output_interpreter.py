from review_client import ReviewClient
from gpt_client import GPTClient

class OutputInterpreter:
    def __init__(self, data_dir, api_key):
        self.rc = ReviewClient(data_dir)
        self.gpt = GPTClient(api_key)

    def interpret(self, output_file):
        df = None
        with open(output_file, 'r') as f:
            for line in f.readlines():
                inputs = line.split(' ')
                if inputs[0] == 'GET':
                    if inputs[1] == 'RESTAURANT':
                        if len(inputs) == 5:
                            df = self.rc.get_restaurants(inputs[2].lower().strip("\""), inputs[3].lower().strip("\""), int(inputs[4]))
                    elif inputs[1] == 'REVIEWS':
                        if len(inputs) == 4:
                            df = self.rc.get_reviews(inputs[2].lower().strip("\""), int(inputs[3]))
                    elif inputs[1] == 'TIPS':
                        if len(inputs) == 4:
                            df = self.rc.get_tips(inputs[2].lower().strip("\""), int(inputs[3]))
                elif inputs[0] == 'SUMMARIZE' and df is not None:
                    response = ''
                    if inputs[1] == 'BUSINESSES':
                        response = self.gpt.summarize_businesses(df)
                    if inputs[1] == 'REVIEWS':
                        response = self.gpt.summarize_reviews(df)
                    if inputs[1] == 'TIPS':
                        response = self.gpt.summarize_tips(df)
                    print(response)
                else:
                    df = None
                    continue


if __name__ == "__main__":
    key = 1 # need api key
    interpreter = OutputInterpreter('./data', key) 
    interpreter.interpret('new_training_data.txt')