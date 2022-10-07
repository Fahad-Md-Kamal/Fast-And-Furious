from sklearn.datasets import load_digits

digits = load_digits()

data = digits.data
targets = digits.target

print(data[0].reshape((8,8)))
print(targets[0])
