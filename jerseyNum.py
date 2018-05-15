import random
import matplotlib.pyplot as plt
import matplotlib.axes
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

def generator(chaser, balls, strikes, outs):
	sequence = []
	for i in range(5):
			sequence.append(random.randint(1,5))
	
	jerseyNum = random.randint(1,5)
	sequence.append(balls)
	sequence.append(strikes)
	sequence.append(outs)
	sequence.append(jerseyNum)

	actualPitch = sequence[jerseyNum%5]
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

numAtBats=2600
X, y = generateData(numAtBats)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
clf=MLPClassifier()
clf.fit(X_train,y_train)
print numAtBats, clf.score(X_test, y_test)

datapoints=[]
for i in range(2,numAtBats):
	X, y = generateData(i)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
	#print X_train, X_test, y_train, y_test
	clf=MLPClassifier()
	clf.fit(X_train,y_train)
	datapoints.append((i/2, clf.score(X_test, y_test)))
	print i, clf.score(X_test, y_test)
fig, ax = plt.subplots()
plt.plot(*zip(*datapoints))
ax.axhline(y=0.8, c='r')
ax.set_xlabel("Number of At-Bats Seen")
ax.set_ylabel("Pitch Prediction Accuracy")
ax.set_title("Neural Network Learning/Decoding of Jersey Number Scheme")
# 1000 at-bats needed
plt.show()
