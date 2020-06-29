import random

corpus = {'1.html': {'2.html'}, '2.html': {'3.html', '1.html'}, '3.html': {'4.html', '2.html'}, '4.html': {'2.html'}}
page = "3.html"
damping_factor = 0.85
distribution = {}
l = len(corpus[page])
# print(corpus[page], l)
if l != 0:
    for i in corpus:
        distribution[i] = (1 - damping_factor) / len(corpus)
    for i in corpus[page]:
        distribution[i] += damping_factor / l
else:
    for i in corpus:
        distribution[i] = 1 / len(corpus)
print(distribution)

for i, j in distribution.items():
    print(i, j)