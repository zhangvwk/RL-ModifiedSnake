import pandas as pd

agent = 'QL'
epsilon = 0.0


data_path = '/home/zhangvwk/Documents/Stanford/cs221/project/modified-snake-reinforcement-learning/training/ql/'
file_name = 'training_' + agent + '_' + str(epsilon) + '.csv'
file_path = data_path + file_name

df = pd.read_csv(file_path)

# print(df)
print(df.tail(200)['2'])