import matplotlib.pyplot as plt

amts = [line.split('\t')[1] for line in open('logs/repo.counts', 'r').readlines()]
plt.plot(amts)
plt.show()
