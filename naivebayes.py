import math
import sys
#This is an extremely pretty basic naive bayes classifier in python
#it should probably not be used in any production setting, and should be kept to its intended use as a prototype.
class Classifier(object):
  #this is what one category with three vectors should look like.
  # ([[1,2,3],[1,1,2],[2,3,5]], "some category")
  #training_data and testing_data have the same format
  #this is what training data or testing data with two categoryes should look like
  # [[[[1,1,1],[1,2,3], [1,0,1]], "category1"], [[20,20,20],[21,21,21],[19,19,19], "category2"]]]

  #The preproccessor argument expects a function that accepts a vector (list), and returns a list with the
  #dimension
  def __init__(self, training_data, preprocessor=None):
    self.Classes = {}
    self.preprocessor = preprocessor
    self.train(training_data)
    for each in self.Classes:
      self.Length = len(self.Classes[each][0])
      break

  #training method
  def train(self, training_data):
    if self.preprocessor is None: 
      for each in training_data:
        #Self.Classes[class or state][0][dimension] are the means for their respective class and dimensions
        #Self.Classes[class or state][1][dimension] are the standard deviation for their respective class and dimensions
        self.Classes[each[1]] = [[sum(zip(*each[0])[i])/float(len(each[0]))for i in range(len(each[0][0]))]]
        self.Classes[each[1]].append([sum([(j-self.Classes[each[1]][0][i])**2 for j in zip(*each[0])[i]])/len(each[0])for i in range(len(each[0][0]))])
    else:
      for each in training_data:
        self.Classes[each[1]] = [[sum(zip(*[self.preprocessor(j) for j in each[0]])[i])/float(len(each[0]))for i in range(len(each[0][0]))]]
        self.Classes[each[1]].append([sum([(j-self.Classes[each[1]][0][i])**2 for j in zip(*each[0])[i]])/len(each[0])for i in range(len(each[0][0]))])

  def test(self, test_data):
    x = 0
    matrix_key = {}
    for each in test_data:
      matrix_key[each[1]] = x
      x += 1
    test_list = [[0 for i in range(len(matrix_key))] for j in range(len(matrix_key))]
    for i in test_data:
      for j in i[0]:
       test_list[matrix_key[i[1]]][matrix_key[self.predict(j)[1]]] += 1
      test_list[matrix_key[i[1]]] = [ x / float(len(i[0])) for x in test_list[matrix_key[i[1]]]]
    return test_list
  
  #prediction method
  #adding a training_mode argument allows for this to return a true or false if the prediction is accurate
  def predict(self, test_vector, training_mode=None):
    i = [0, None]
    if self.preprocessor is not None:
      test = self.preprocessor(test_vector)
    else:
      test = test_vector
    for each in self.Classes:
      a = 1
      for x, y, z in zip(test, self.Classes[each][0], self.Classes[each][1]):
        if z is not 0:
          a *= self.gaussian(x, y, z)
      if i[1] is None or a > i[0]:
        i = [a, each]
    if i[1] is training_mode:
      return 1
    if training_mode is not None:
      return 0
    return i

  #Calculates probability of x given the parameters of some assumed normal distribution
  def gaussian(self, x, mean, stdev):
    try:
      return (1/math.sqrt(2*math.pi*stdev)) * math.exp(-(x-mean)**2/(2 * stdev))
    except ZeroDivisionError:
      if mean is x:
        return 1
      return 0

  def getModel(self):
    return self.Classes
  def getLength(self):
    return self.Length
#standard boiler plate
#this will attempt to categorize vectors in a file
#it will cut each class in half to divide it into training and testing data
#it works on the format of files given by HMM app.
def prepro(emg):
  #only works for 8 feature vectors
  new_emg = []
  for e in range(8):
    new_emg.append((emg[e] + emg[(e+1)%8]/2 + emg[(e-1)%8]/2 + emg[(e+2)%8]/4 +  emg[(e-2)%8]/4 + emg[(e+3)%8]/8 + emg[(e-3)%8]/8 + emg[(e+4)%8]/16)/8)
  return new_emg
               
if __name__ == "__main__":
  paths = sys.argv[1:]
  for fp in paths:
    data = {}
    for each in open(fp, "r").readlines():
      key="gesture" + each.split()[0]
      if key not in data:
        data[key] = []
      data[key].append([float(x) for x in each.split()[1:-1]])
    training = []
    testing = []
    for each in data:
      training.append((data[each][:len(data[each])/2], each))
      testing.append((data[each][len(data[each])/2:], each))
    print "Attempting to classify " + fp
    c = Classifier(training)
    for i in c.test(testing):
      print i
    j = c.getModel()
    for each in j:
      if 0 in j[each][1]:
        print fp + " has a zero standard deviation for " + each


  
  




