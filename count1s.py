import random
import matplotlib.pyplot as plt
import matplotlib.axes
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

def generator(counter, balls, strikes, outs):
	while True:
		sequence = []
		pitchDict={}
		pitch = random.randint(1,5)
		for i in range(pitch):
			index = random.randint(1,5)
			if index not in pitchDict:
				pitchDict[index]=1
		for i in range(5):
			if i+1 in pitchDict:
				sequence.append(1)
			else:
				sequence.append(random.randint(1,5))
		if sequence[0]!=5:
			break
	sequence.append(balls)
	sequence.append(strikes)
	sequence.append(outs)
	actualPitch = sequence.count(counter)
	return sequence, actualPitch

def pitch(count):
	result=random.randint(0,1)
	count[result]+=1
	return count

def generateData(atBats):
	counter = 1
	data = []
	actualPitches=[]
	outs=-1
	for i in range(atBats):
		count = [0, 0]
		outs += 1
		if outs==3:
			outs = 0
		while count[0]!=4 and count[1]!=3:
			chase=generator(counter, count[0], count[1], outs)
			data.append(chase[0])
			actualPitches.append(chase[1])
			count = pitch(count)
	return data, actualPitches



numAtBats=1800
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
ax.set_title("Neural Network Learning/Decoding of Pumps Scheme")
#  at-bats needed
plt.show()
