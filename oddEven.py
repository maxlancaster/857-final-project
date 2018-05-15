import random
import matplotlib.pyplot as plt
import matplotlib.axes
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

def generator(chaser, balls, strikes, outs):
	sequence = []
	for i in range(5):
			sequence.append(random.randint(1,5))

	sequence.append(balls)
	sequence.append(strikes)
	#sequence.append((balls+strikes)%2)
	sequence.append(outs)
	if (balls-strikes)%2==0:
		actualPitch = sequence[0]
	if (balls-strikes)%2==1:
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

numAtBats=2000
X, y = generateData(numAtBats)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
clf=MLPClassifier()
clf.fit(X_train,y_train)
print numAtBats, clf.score(X_test, y_test)

# datapoints=[]
# for i in range(2,numAtBats):
# 	X, y = generateData(i)
# 	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
# 	#print X_train, X_test, y_train, y_test
# 	clf=MLPClassifier()
# 	clf.fit(X_train,y_train)
# 	datapoints.append((i/2, clf.score(X_test, y_test)))
# 	print i, clf.score(X_test, y_test)
# fig, ax = plt.subplots()
# plt.plot(*zip(*datapoints))
# ax.axhline(y=0.8, c='r')
# ax.set_xlabel("Number of At-Bats Seen")
# ax.set_ylabel("Test Data Performance")
# ax.set_title("Neural Network Learning/Decoding of Constant Location Scheme")
# # at-bats needed
# plt.show()
