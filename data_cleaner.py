data = open('training_data.txt', 'r')

with open('new_training_data.txt', 'w') as f:
    for line in data.readlines():
        if line[0:2] == 'df':
            string = ''
            func = line.split('(')
            params = func[1].split(',')
            if func[0][12:15] == 'res':
                string = string + 'GET RESTAURANT '
            elif func[0][12:15] == 'rev':
                string = string + 'GET REVIEW '
            else:
                string = string + 'GET TIPS '
            for param in params:
                if param[0:6] == ' limit':
                    string = string + ' ' + param[7] + '\n'
                else:
                    string = string + param.upper().replace(")", '')
            f.write(string)
        elif line[0:8] == 'response':
            string = ''
            func = line.split('_')
            if func[1][0] == 'b':
                string = string + 'SUMMARIZE BUSINESSES '
            elif func[1][0] == 'r':
                string = string + 'SUMMARIZE REVIEWS '
            else:
                string = string + 'SUMMARIZE TIPS '
            f.write(string)
        elif line[0:5] == 'print':
            f.write('\n')
        else:
            f.write(line)
            

data.close()