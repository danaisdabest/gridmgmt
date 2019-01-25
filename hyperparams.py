
import string
import itertools
import collections
import dill

# #notused
# def dictionaryproduct(dictlists):
# 	#convert dictionary to lists of tuples
# 	pools=[]	
# 	for key in dictlists:
# 		pools.append([(key,value) for value in dictlists[key]])
# 	tupleproduct=itertools.product(*pools)	
# 	#convert tuple lists to dictionaries
# 	newdicts=[]	
# 	for tupleset in tupleproduct:
# 		newdict={}
# 		for tkey, tvalue in tupleset:
# 			newdict[tkey]=tvalue
# 		newdicts.append(newdict)
# 	return newdicts
# print(dictionaryproduct({'a':[1,2],'b':[3,4]}))

paramdescrip=collections.namedtuple('paramdescrip',['name','category'])
class hyperparam():
	def __init__(self,name,value,category=''):
		self.name=name
		self.value=value
		self.category=category #'train'/'test'

	def printhyperparam(self):
		print(self.category,end=', ')
		print(self.name,end=', ')
		print(str(self.value))


#defines one cell in the grid search, one set of hyperparameters
class paramset():
	def __init__(self,hyperparams=[],name=''):
		self.name=name
		self.namecat_to_hyperparam={}
		self.category_to_hyperparam={}
		self.trainsetid=''
		for hyperparam in hyperparams:
			self.namecat_to_hyperparam[(hyperparam.category,hyperparam.name)]=hyperparam
			if(hyperparam.category in self.category_to_hyperparam):
				self.category_to_hyperparam[hyperparam.category].append(hyperparam)
			else:
				self.category_to_hyperparam[hyperparam.category]=[hyperparam]

	def checkparamvalue(self, category,name):
		if((category,name) in self.namecat_to_hyperparam):
			return self.namecat_to_hyperparam[(category,name)].value

		else:
			return None
	def gettrainid(self):
		return self.trainsetid

	def updatetrainid(self,trainid):
		self.trainsetid=trainid

	def getcategoryhyperparams(self,category):
		return self.category_to_hyperparam[category]

	def checkparammatch(self,category,name,value):
		if(self.checkparamvalue(category=category,name=name)==value):
			return True
		else:
			return False

	def checkreqprohiblist(self,reqdict={},prohibdict={}):
		for tparamdesc in reqdict:
			meetsreq=False
			for tparamval in reqdict[tparamdesc]:
				if self.checkparammatch(category=tparamdesc.category,name=tparamdesc.name,value=tparamval):
					meetsreq=True
					break #we match one of the accepted req values for this param req
			if(meetsreq==False): #did we meet this one req? If not, then we are done
				return False

		for tparamdesc in prohibdict:
			for tparamval in prohibdict[tparamdesc]:
				if self.checkparammatch(category=tparamdesc.category,name=tparamdesc.name,value=tparamval):
					return False
		return True

	def gethyperparams(self):
		return self.namecat_to_hyperparam.values()

	def printset(self):
		print("----setname----"+self.name+"------trainid------"+self.trainsetid)
		for paramname in self.namecat_to_hyperparam:
			self.namecat_to_hyperparam[paramname].printhyperparam()
		print('')


def getparamsetlists(paramdict):
	pools=[]
	for paramdesc in paramdict:
		#print(paramdesc)
		pool=[]
		for value in paramdict[paramdesc]:
			pool.append(hyperparam(name=paramdesc.name,category=paramdesc.category,value=value))
		pools.append(pool)
	paramsetlists=itertools.product(*pools)
	return paramsetlists

def makeparamdict(paramtuplelist):
	paramdict={}
	for cat,name,values in paramtuplelist:
		paramdict[paramdescrip(category=cat,name=name)]=values
	return paramdict	

class paramcollection():
	def __init__(self,collectionname):
		self.collectionname=collectionname
		self.lastTESTID=0
		self.lastTRAINID=0
		self.paramsets={}
		self.trainids_to_paramsets={}
		self.paramsets_to_trainids={}

	def addtocollection(self,paramtuplelist):
		paramdict=makeparamdict(paramtuplelist)
		for cat,name,values in paramtuplelist:
			paramdict[paramdescrip(category=cat,name=name)]=values
		paramsetlists=getparamsetlists(paramdict)
		for paramsetlist in paramsetlists:
			setid="%06d" % self.lastTESTID
			self.paramsets[setid]=paramset(paramsetlist,setid)
			self.lastTESTID+=1

			matchingtrainsets=self.getexistingtrain(setid)
			if len(matchingtrainsets)==0:
				trainid="%06d" % self.lastTRAINID
				self.trainids_to_paramsets[trainid]=[setid]
				self.paramsets_to_trainids[setid]=trainid
				self.lastTRAINID+=1
			else:
				trainid=self.paramsets_to_trainids[matchingtrainsets[0]]
				self.paramsets_to_trainids[setid]=trainid
				self.trainids_to_paramsets[trainid].append(setid)
			self.paramsets[setid].updatetrainid(trainid)


	def getcollectionname(self):
		return self.collectionname
		
	def getalltrainids(self):
		return self.trainids_to_paramsets.keys()

	def gettestspertrainid(self,trainid):
		return self.trainids_to_paramsets[trainid]

	def gettestgroupspertrainparams(self):
		return self.trainids_to_paramsets.values()


	def displaycollection(self):
		for setid in self.paramsets:
			self.paramsets[setid].printset()

	def checkduplicates(self):
		return 0

	def printsetperid(self,id):
		self.paramsets[id].printset()

	def getsets_isolateddiffsets(self,difftuple,reqlist,prohiblist,printgroups=False):
		reqdict=makeparamdict(reqlist)
		prohibdict=makeparamdict(prohiblist)
		tsetids=[]
		for setid in self.paramsets:
			if self.paramsets[setid].checkreqprohiblist(reqdict=reqdict,prohibdict=prohibdict):
				tsetids.append(setid)

		paramsetgroups=[]
		while tsetids!=[]:
			firstid=tsetids.pop()
			tgroup=[firstid]
			if(difftuple!=None):
				reqparams={paramdescrip(hyperparam.name,hyperparam.category):[hyperparam.value] for hyperparam in self.paramsets[firstid].gethyperparams() if (hyperparam.category,hyperparam.name)!=(difftuple[0],difftuple[1])}
			else:
				reqparams={paramdescrip(hyperparam.name,hyperparam.category):[hyperparam.value] for hyperparam in self.paramsets[firstid].gethyperparams()}
			for tid in tsetids:
				if self.paramsets[tid].checkreqprohiblist(reqdict=reqparams):
					tgroup.append(tid)
			paramsetgroups.append(tgroup)


		if(printgroups):
			for group in paramsetgroups:
				print("======GROUP===============")
				for i in group:
					self.printsetperid(i)
		return paramsetgroups

	def getcategorymatches(self,paramsetid,category):
		reqlist=[(hyperparam.category,hyperparam.name,[hyperparam.value]) for hyperparam in self.paramsets[paramsetid].getcategoryhyperparams(category)]
		tids=self.getsets_isolateddiffsets(
			difftuple=None,
			reqlist=reqlist,
			prohiblist=[]
		)	
		return [j for i in tids for j in i]

	def getparamsets():
		return self.paramsets.values()

	def getexistingtrain(self,paramsetid):
		tids=self.getcategorymatches(paramsetid,'train')
		tids.remove(paramsetid)	
		return tids



if __name__=="__main__":

	mycollection=paramcollection('testcollection')
	mycollection.addtocollection([('train','a',[5,6]),
		                          ('test' ,'b',[1]),
		                          ('test' ,'c',[5]),
		                          ('test' ,'d',[25]),
		                          ('train','q',[55,66])]
		                        )
	mycollection.addtocollection([('train','a',[5,6]),
		                          ('test' ,'b',[11]),
		                          ('test' ,'c',[55]),
		                          ('test' ,'d',[255]),
		                          ('train','q',[55,66])]
		                        )


	tids=mycollection.getsets_isolateddiffsets(
		difftuple=('train','a'),
		reqlist=[('test','b',[1]),('test','c',[5])],
		prohiblist=[('test','d',[25])],
		printgroups=True
	)

	#save to a pkl
	filename="mycollection0.pkl"
	with open(filename, 'wb') as output:  # Overwrites any existing file.
	    dill.dump(mycollection, output, dill.HIGHEST_PROTOCOL)
	#get it later
	with open('mycollection0.pkl', 'rb') as f:
		mymoo=dill.load(f)


	for i in mymoo.getalltrainids():
		for j in mymoo.gettestspertrainid(i):
			mymoo.printsetperid(j)

	for i in mymoo.gettestgroupspertrainparams():
		print(i)




