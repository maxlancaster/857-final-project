import random
import matplotlib.pyplot as plt
import matplotlib.axes
import numpy as np
from numpy.random import choice
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

def generator(chaser, balls, strikes, outs):
	sequence = []
	for i in range(5):
			sequence.append(random.randint(1,5))

	sequence.append(balls)
	sequence.append(strikes)
	sequence.append(outs)
	rightHanded = choice([0,1], 1, p=[0.4, 0.6])
	sequence.append(rightHanded)

	if rightHanded==0:
		actualPitch = sequence[0]
	else:
		actualPitch = sequence[1]
	return sequence, actualPitch

def pitch(count):
	result=random.randint(0,1)
	count[result]+=1
	return count

def generateData(atBats):
	chaser = 2
	data = []
	actualPitches=[]
	outs=-1
	for i in range(atBats):
		count = [0, 0]
		outs += 1
		if outs==3:
			outs = 0
		while count[0]!=4 and count[1]!=3:
			chase=generator(chaser, count[0], count[1], outs)
			data.append(chase[0])
			actualPitches.append(chase[1])
			count = pitch(count)
	return data, actualPitches

numAtBats=497
X, y = generateData(numAtBats)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
clf=MLPClassifier()
clf.fit(X_train,y_train)
print numAtBats, clf.score(X_test, y_test)

datapoints=[]
for i in range(2,numAtBats, 3):
	X, y = generateData(i)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
	#print X_train, X_test, y_train, y_test
	clf=MLPClassifier()
	clf.fit(X_train,y_train)
	datapoints.append((i/2, clf.score(X_test, y_test)))
	print i, clf.score(X_test, y_test)
fig, ax = plt.subplots()
plt.plot(*zip(*datapoints))
x = np.array([i[0] for i in datapoints])
y = np.array([i[1] for i in datapoints])
x_avg = np.mean(x.reshape(-1, 5), axis=1)
y_avg = np.mean(y.reshape(-1, 5), axis=1)
plt.plot(x_avg, y_avg)
ax.axhline(y=0.8, c='r')
ax.set_xlabel("Number of At-Bats Seen")
ax.set_ylabel("Pitch Prediction Accuracy")
ax.set_title("Neural Network Learning/Decoding of Righty/Lefty Scheme")
# 138 at-bats needed
plt.show()
