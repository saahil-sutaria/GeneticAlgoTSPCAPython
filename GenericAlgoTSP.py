
import numpy as np, random, operator, pandas as pd, time

class City:
    def __init__(self, name):
        self.name = name
        self.distanceToCity = {}
    
    def distance(self, city):
        if city.name in self.distanceToCity:
          return self.distanceToCity[city.name]
        else:
          return city.distanceToCity[self.name]
    
    def setDis(self, city, distan):
        self.distanceToCity[city.name] = distan
        return self.distanceToCity
    
    def __repr__(self):
        return self.name

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.distance ==0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness

def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route

def initPopulation(popSize, cityList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))
    return population

def rankRoutes(population):
    fitResults = {}
    for i in range(0,len(population)):
        fitResults[i] = Fitness(population[i]).routeFitness()
    
    return sorted(fitResults.items(), key = operator.itemgetter(1), reverse = True)

def selection(popRanked, eliteSize):
    selResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    #dataframe with 4 colums 
    
    for i in range(0, eliteSize):
        selResults.append(popRanked[i][0])
        
    for i in range(0, len(popRanked) - eliteSize):
        
        pick = 100*random.random() 
        #random between 0 to 100
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selResults.append(popRanked[i][0])
                break
    return selResults

def matingPool(population, selectionResults):
    matingpool = []

    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])

    return matingpool

def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    gene1 = int(random.random() * len(parent1))
    gene2 = int(random.random() * len(parent2))
    
    
    startGene = min(gene1, gene2)
    endGene = max(gene1, gene2)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    for item in parent2:
        if item not in childP1:
          childP2.append(item)
    child = childP1 + childP2
    return child

def breedPopulation(matPool, eliteSize):
    children = []
    length = len(matPool) - eliteSize
    pool = random.sample(matPool, len(matPool))
    
    for i in range(0,eliteSize):
        children.append(matPool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matPool)-i-1])
        children.append(child)
    return children

def mutate(indi, mutRate):
    for swapped in range(len(indi)):
        if(random.random() < mutRate):
            swapWith = int(random.random() * len(indi))
            
            citySwapped = indi[swapped]
            citySwapWith = indi[swapWith]
         
            indi[swapped] = citySwapWith
            indi[swapWith] = citySwapped
    return indi

def mutatePopulation(popu, mutRate):
    mutPop = []
    
    for ind in range(0, len(popu)):
        mutInd = mutate(popu[ind], mutRate)
        mutPop.append(mutInd)
    return mutPop

def nextGeneration(currentGen, eliteSize, mutationRate):
    
    popRanked = rankRoutes(currentGen)  #tuple (0...100: 1/totalDist) in Decreasing order
    selResults = selection(popRanked, eliteSize)    #list[100].......list of index according to fitness 
    matPool = matingPool(currentGen, selResults)   #size [100x27]....of cities with decreasing fitness
    children = breedPopulation(matPool, eliteSize) #size [100x27].....20 elite rest from parents
    nextGene = mutatePopulation(children, mutationRate) #size[100x27]......New Gen with mutation

    return nextGene

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
    t0 = time.time()
    pop = initPopulation(popSize, population)
    
    for i in range(0,1):
        pop = nextGeneration(pop, eliteSize, mutationRate)
    
    
    print("Min distance: " + str(1 / rankRoutes(pop)[0][1]))
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    print(bestRoute)
    t1 = time.time() - t0
    print("Runtime = " + str(t1) + "s")
    return bestRoute

Bakersfield = City("Bakersfield")
Barstow = City("Barstow")
Carlsbod = City("Carlsbod")
Eureko = City("Eureko")
Fresno = City("Fresno")
LakeTahoe = City("Lake Tahoe")
LasVegas = City("Las Vegas")
LongBeach = City("Long Beach")
LosAngeles = City("Los Angeles")
Merced = City("Merced")
Modesto = City("Modesto")
Monterey = City("Monterey")
Oakland = City("Oakland")
PlamSprings = City("Plam Springs")
Redding = City("Redding")
Sacramento = City("Sacramento")
SanBernardino = City("San Bernardino")
SanDiego = City("San Diego")
SanFrancisco = City("San Francisco")
SanJose = City("SanJose")
SanLuis = City("San Luis")
SantaBarbara = City("Santa Barbara")
SanCruz = City("San Cruz")
SantaRosa = City("Santa Rosa")
SequoiaPark = City("Sequoia Park")
Stockton = City("Stockton")
Yosemite = City("Yosemite")

Bakersfield.setDis(Barstow, 129)
Bakersfield.setDis(Carlsbod, 206)
Bakersfield.setDis(Eureko, 569)
Bakersfield.setDis(Fresno, 107)
Bakersfield.setDis(LakeTahoe, 360)
Bakersfield.setDis(LasVegas, 284)
Bakersfield.setDis(LongBeach, 144)
Bakersfield.setDis(LosAngeles, 115)
Bakersfield.setDis(Merced, 162)
Bakersfield.setDis(Modesto, 200)
Bakersfield.setDis(Monterey, 231)
Bakersfield.setDis(Oakland, 288)
Bakersfield.setDis(PlamSprings, 226)
Bakersfield.setDis(Redding, 436)
Bakersfield.setDis(Sacramento, 272)
Bakersfield.setDis(SanBernardino, 174)
Bakersfield.setDis(SanDiego, 231)
Bakersfield.setDis(SanFrancisco, 297)
Bakersfield.setDis(SanJose, 252)
Bakersfield.setDis(SanLuis, 118)
Bakersfield.setDis(SantaBarbara, 146)
Bakersfield.setDis(SanCruz, 258)
Bakersfield.setDis(SantaRosa, 347)
Bakersfield.setDis(SequoiaPark, 121)
Bakersfield.setDis(Stockton, 227)
Bakersfield.setDis(Yosemite, 200)

Barstow.setDis(Carlsbod, 153)
Barstow.setDis(Eureko, 696)
Barstow.setDis(Fresno, 236)
Barstow.setDis(LakeTahoe, 395)
Barstow.setDis(LasVegas, 155)
Barstow.setDis(LongBeach, 139)
Barstow.setDis(LosAngeles, 130)
Barstow.setDis(Merced, 291)
Barstow.setDis(Modesto, 329)
Barstow.setDis(Monterey, 360)
Barstow.setDis(Oakland, 417)
Barstow.setDis(PlamSprings, 123)
Barstow.setDis(Redding, 565)
Barstow.setDis(Sacramento, 401)
Barstow.setDis(SanBernardino, 71)
Barstow.setDis(SanDiego, 176)
Barstow.setDis(SanFrancisco, 426)
Barstow.setDis(SanJose, 381)
Barstow.setDis(SanLuis, 247)
Barstow.setDis(SantaBarbara, 225)
Barstow.setDis(SanCruz, 387)
Barstow.setDis(SantaRosa, 476)
Barstow.setDis(SequoiaPark, 250)
Barstow.setDis(Stockton, 356)
Barstow.setDis(Yosemite, 329)

Carlsbod.setDis(Eureko, 777)
Carlsbod.setDis(Fresno, 315)
Carlsbod.setDis(LakeTahoe, 780)
Carlsbod.setDis(LasVegas, 312)
Carlsbod.setDis(LongBeach, 82)
Carlsbod.setDis(LosAngeles, 93)
Carlsbod.setDis(Merced, 370)
Carlsbod.setDis(Modesto, 406)
Carlsbod.setDis(Monterey, 428)
Carlsbod.setDis(Oakland, 496)
Carlsbod.setDis(PlamSprings, 116)
Carlsbod.setDis(Redding, 644)
Carlsbod.setDis(Sacramento, 480)
Carlsbod.setDis(SanBernardino, 827)
Carlsbod.setDis(SanDiego, 23)
Carlsbod.setDis(SanFrancisco, 505)
Carlsbod.setDis(SanJose, 460)
Carlsbod.setDis(SanLuis, 293)
Carlsbod.setDis(SantaBarbara, 188)
Carlsbod.setDis(SanCruz, 466)
Carlsbod.setDis(SantaRosa, 565)
Carlsbod.setDis(SequoiaPark, 329)
Carlsbod.setDis(Stockton, 435)
Carlsbod.setDis(Yosemite, 408)

Eureko.setDis(Fresno, 462)
Eureko.setDis(LakeTahoe, 398)
Eureko.setDis(LasVegas, 797)
Eureko.setDis(LongBeach, 713)
Eureko.setDis(LosAngeles, 694)
Eureko.setDis(Merced, 407)
Eureko.setDis(Modesto, 369)
Eureko.setDis(Monterey, 388)
Eureko.setDis(Oakland, 291)
Eureko.setDis(PlamSprings, 795)
Eureko.setDis(Redding, 150)
Eureko.setDis(Sacramento, 314)
Eureko.setDis(SanBernardino, 43)
Eureko.setDis(SanDiego, 800)
Eureko.setDis(SanFrancisco, 272)
Eureko.setDis(SanJose, 317)
Eureko.setDis(SanLuis, 504)
Eureko.setDis(SantaBarbara, 609)
Eureko.setDis(SanCruz, 349)
Eureko.setDis(SantaRosa, 222)
Eureko.setDis(SequoiaPark, 544)
Eureko.setDis(Stockton, 356)
Eureko.setDis(Yosemite, 488)

Fresno.setDis(LakeTahoe, 388)
Fresno.setDis(LasVegas, 408)
Fresno.setDis(LongBeach, 251)
Fresno.setDis(LosAngeles, 222)
Fresno.setDis(Merced, 55)
Fresno.setDis(Modesto, 93)
Fresno.setDis(Monterey, 152)
Fresno.setDis(Oakland, 181)
Fresno.setDis(PlamSprings, 333)
Fresno.setDis(Redding, 329)
Fresno.setDis(Sacramento, 185)
Fresno.setDis(SanBernardino, 281)
Fresno.setDis(SanDiego, 338)
Fresno.setDis(SanFrancisco, 190)
Fresno.setDis(SanJose, 145)
Fresno.setDis(SanLuis, 137)
Fresno.setDis(SantaBarbara, 242)
Fresno.setDis(SanCruz, 151)
Fresno.setDis(SantaRosa, 240)
Fresno.setDis(SequoiaPark, 82)
Fresno.setDis(Stockton, 120)
Fresno.setDis(Yosemite, 93)

LakeTahoe.setDis(LasVegas, 466)
LakeTahoe.setDis(LongBeach, 479)
LakeTahoe.setDis(LosAngeles, 456)
LakeTahoe.setDis(Merced, 194)
LakeTahoe.setDis(Modesto, 156)
LakeTahoe.setDis(Monterey, 266)
LakeTahoe.setDis(Oakland, 195)
LakeTahoe.setDis(PlamSprings, 435)
LakeTahoe.setDis(Redding, 249)
LakeTahoe.setDis(Sacramento, 107)
LakeTahoe.setDis(SanBernardino, 436)
LakeTahoe.setDis(SanDiego, 542)
LakeTahoe.setDis(SanFrancisco, 192)
LakeTahoe.setDis(SanJose, 197)
LakeTahoe.setDis(SanLuis, 197)
LakeTahoe.setDis(SantaBarbara, 492)
LakeTahoe.setDis(SanCruz, 229)
LakeTahoe.setDis(SantaRosa, 199)
LakeTahoe.setDis(SequoiaPark, 335)
LakeTahoe.setDis(Stockton, 131)
LakeTahoe.setDis(Yosemite, 133)

LasVegas.setDis(LongBeach, 314)
LasVegas.setDis(LosAngeles, 302)
LasVegas.setDis(Merced, 446)
LasVegas.setDis(Modesto, 484)
LasVegas.setDis(Monterey, 504)
LasVegas.setDis(Oakland, 567)
LasVegas.setDis(PlamSprings, 276)
LasVegas.setDis(Redding, 640)
LasVegas.setDis(Sacramento, 587)
LasVegas.setDis(SanBernardino, 228)
LasVegas.setDis(SanDiego, 332)
LasVegas.setDis(SanFrancisco, 568)
LasVegas.setDis(SanJose, 524)
LasVegas.setDis(SanLuis, 414)
LasVegas.setDis(SantaBarbara, 354)
LasVegas.setDis(SanCruz, 524)
LasVegas.setDis(SantaRosa, 610)
LasVegas.setDis(SequoiaPark, 408)
LasVegas.setDis(Stockton, 510)
LasVegas.setDis(Yosemite, 435)

LongBeach.setDis(LosAngeles, 29)
LongBeach.setDis(Merced, 306)
LongBeach.setDis(Modesto, 344)
LongBeach.setDis(Monterey, 364)
LongBeach.setDis(Oakland, 432)
LongBeach.setDis(PlamSprings, 112)
LongBeach.setDis(Redding, 580)
LongBeach.setDis(Sacramento, 416)
LongBeach.setDis(SanBernardino, 68)
LongBeach.setDis(SanDiego, 105)
LongBeach.setDis(SanFrancisco, 441)
LongBeach.setDis(SanJose, 396)
LongBeach.setDis(SanLuis, 229)
LongBeach.setDis(SantaBarbara, 124)
LongBeach.setDis(SanCruz, 402)
LongBeach.setDis(SantaRosa, 491)
LongBeach.setDis(SequoiaPark, 265)
LongBeach.setDis(Stockton, 371)
LongBeach.setDis(Yosemite, 344)

LosAngeles.setDis(Merced, 277)
LosAngeles.setDis(Modesto, 315)
LosAngeles.setDis(Monterey, 335)
LosAngeles.setDis(Oakland, 403)
LosAngeles.setDis(PlamSprings, 111)
LosAngeles.setDis(Redding, 551)
LosAngeles.setDis(Sacramento, 387)
LosAngeles.setDis(SanBernardino, 59)
LosAngeles.setDis(SanDiego, 116)
LosAngeles.setDis(SanFrancisco, 412)
LosAngeles.setDis(SanJose, 367)
LosAngeles.setDis(SanLuis, 200)
LosAngeles.setDis(SantaBarbara, 95)
LosAngeles.setDis(SanCruz, 373)
LosAngeles.setDis(SantaRosa, 462)
LosAngeles.setDis(SequoiaPark, 236)
LosAngeles.setDis(Stockton, 342)
LosAngeles.setDis(Yosemite, 315)

Merced.setDis(Modesto, 37)
Merced.setDis(Monterey, 118)
Merced.setDis(Oakland, 126)
Merced.setDis(PlamSprings, 388)
Merced.setDis(Redding, 274)
Merced.setDis(Sacramento, 110)
Merced.setDis(SanBernardino, 336)
Merced.setDis(SanDiego, 393)
Merced.setDis(SanFrancisco, 135)
Merced.setDis(SanJose, 114)
Merced.setDis(SanLuis, 192)
Merced.setDis(SantaBarbara, 297)
Merced.setDis(SanCruz, 118)
Merced.setDis(SantaRosa, 185)
Merced.setDis(SequoiaPark, 137)
Merced.setDis(Stockton, 65)
Merced.setDis(Yosemite, 81)

Modesto.setDis(Monterey, 153)
Modesto.setDis(Oakland, 88)
Modesto.setDis(PlamSprings, 426)
Modesto.setDis(Redding, 236)
Modesto.setDis(Sacramento, 72)
Modesto.setDis(SanBernardino, 374)
Modesto.setDis(SanDiego, 431)
Modesto.setDis(SanFrancisco, 97)
Modesto.setDis(SanJose, 82)
Modesto.setDis(SanLuis, 230)
Modesto.setDis(SantaBarbara, 335)
Modesto.setDis(SanCruz, 114)
Modesto.setDis(SantaRosa, 147)
Modesto.setDis(SequoiaPark, 175)
Modesto.setDis(Stockton, 27)
Modesto.setDis(Yosemite, 119)

Monterey.setDis(Oakland, 111)
Monterey.setDis(PlamSprings, 446)
Monterey.setDis(Redding, 325)
Monterey.setDis(Sacramento, 185)
Monterey.setDis(SanBernardino, 394)
Monterey.setDis(SanDiego, 451)
Monterey.setDis(SanFrancisco, 116)
Monterey.setDis(SanJose, 71)
Monterey.setDis(SanLuis, 135)
Monterey.setDis(SantaBarbara, 240)
Monterey.setDis(SanCruz, 45)
Monterey.setDis(SantaRosa, 166)
Monterey.setDis(SequoiaPark, 234)
Monterey.setDis(Stockton, 140)
Monterey.setDis(Yosemite, 199)

Oakland.setDis(PlamSprings, 514)
Oakland.setDis(Redding, 214)
Oakland.setDis(Sacramento, 87)
Oakland.setDis(SanBernardino, 462)
Oakland.setDis(SanDiego, 519)
Oakland.setDis(SanFrancisco, 9)
Oakland.setDis(SanJose, 40)
Oakland.setDis(SanLuis, 227)
Oakland.setDis(SantaBarbara, 332)
Oakland.setDis(SanCruz, 72)
Oakland.setDis(SantaRosa, 59)
Oakland.setDis(SequoiaPark, 263)
Oakland.setDis(Stockton, 75)
Oakland.setDis(Yosemite, 207)

PlamSprings.setDis(Redding, 682)
PlamSprings.setDis(Sacramento, 498)
PlamSprings.setDis(SanBernardino, 52)
PlamSprings.setDis(SanDiego, 139)
PlamSprings.setDis(SanFrancisco, 523)
PlamSprings.setDis(SanJose, 478)
PlamSprings.setDis(SanLuis, 311)
PlamSprings.setDis(SantaBarbara, 206)
PlamSprings.setDis(SanCruz, 484)
PlamSprings.setDis(SantaRosa, 573)
PlamSprings.setDis(SequoiaPark, 347)
PlamSprings.setDis(Stockton, 453)
PlamSprings.setDis(Yosemite, 426)

Redding.setDis(Sacramento, 164)
Redding.setDis(SanBernardino, 610)
Redding.setDis(SanDiego, 667)
Redding.setDis(SanFrancisco, 223)
Redding.setDis(SanJose, 254)
Redding.setDis(SanLuis, 411)
Redding.setDis(SantaBarbara, 546)
Redding.setDis(SanCruz, 286)
Redding.setDis(SantaRosa, 251)
Redding.setDis(SequoiaPark, 411)
Redding.setDis(Stockton, 209)
Redding.setDis(Yosemite, 355)

Sacramento.setDis(SanBernardino, 446)
Sacramento.setDis(SanDiego, 503)
Sacramento.setDis(SanFrancisco, 87)
Sacramento.setDis(SanJose, 114)
Sacramento.setDis(SanLuis, 301)
Sacramento.setDis(SantaBarbara, 406)
Sacramento.setDis(SanCruz, 146)
Sacramento.setDis(SantaRosa, 103)
Sacramento.setDis(SequoiaPark, 247)
Sacramento.setDis(Stockton, 45)
Sacramento.setDis(Yosemite, 191)

SanBernardino.setDis(SanDiego, 105)
SanBernardino.setDis(SanFrancisco, 471)
SanBernardino.setDis(SanJose, 426)
SanBernardino.setDis(SanLuis, 259)
SanBernardino.setDis(SantaBarbara, 254)
SanBernardino.setDis(SanCruz, 432)
SanBernardino.setDis(SantaRosa, 521)
SanBernardino.setDis(SequoiaPark, 295)
SanBernardino.setDis(Stockton, 401)
SanBernardino.setDis(Yosemite, 374)

SanDiego.setDis(SanFrancisco, 528)
SanDiego.setDis(SanJose, 483)
SanDiego.setDis(SanLuis, 316)
SanDiego.setDis(SantaBarbara, 211)
SanDiego.setDis(SanCruz, 489)
SanDiego.setDis(SantaRosa, 578)
SanDiego.setDis(SequoiaPark, 352)
SanDiego.setDis(Stockton, 458)
SanDiego.setDis(Yosemite, 431)

SanFrancisco.setDis(SanJose, 45)
SanFrancisco.setDis(SanLuis, 232)
SanFrancisco.setDis(SantaBarbara, 337)
SanFrancisco.setDis(SanCruz, 77)
SanFrancisco.setDis(SantaRosa, 50)
SanFrancisco.setDis(SequoiaPark, 272)
SanFrancisco.setDis(Stockton, 84)
SanFrancisco.setDis(Yosemite, 216)

SanJose.setDis(SanLuis, 187)
SanJose.setDis(SantaBarbara, 292)
SanJose.setDis(SanCruz, 32)
SanJose.setDis(SantaRosa, 95)
SanJose.setDis(SequoiaPark, 227)
SanJose.setDis(Stockton, 69)
SanJose.setDis(Yosemite, 195)

SanLuis.setDis(SantaBarbara, 105)
SanLuis.setDis(SanCruz, 180)
SanLuis.setDis(SantaRosa, 282)
SanLuis.setDis(SequoiaPark, 174)
SanLuis.setDis(Stockton, 256)
SanLuis.setDis(Yosemite, 230)

SantaBarbara.setDis(SanCruz, 285)
SantaBarbara.setDis(SantaRosa, 387)
SantaBarbara.setDis(SequoiaPark, 287)
SantaBarbara.setDis(Stockton, 361)
SantaBarbara.setDis(Yosemite, 335)

SanCruz.setDis(SantaRosa, 127)
SanCruz.setDis(SequoiaPark, 233)
SanCruz.setDis(Stockton, 101)
SanCruz.setDis(Yosemite, 199)

SantaRosa.setDis(SequoiaPark, 322)
SantaRosa.setDis(Stockton, 134)
SantaRosa.setDis(Yosemite, 266)

SequoiaPark.setDis(Stockton, 202)
SequoiaPark.setDis(Yosemite, 175)

Stockton.setDis(Yosemite, 146)


cityList = [Bakersfield, Barstow, Carlsbod, Eureko, Fresno, LakeTahoe, LasVegas, LongBeach, LosAngeles, Merced, Modesto, Monterey, Oakland, PlamSprings, Redding, Sacramento, SanBernardino, SanDiego, SanFrancisco, SanJose, SanLuis, SantaBarbara, SanCruz, SantaRosa, SequoiaPark, Stockton, Yosemite]

geneticAlgorithm(population = cityList, popSize = 100, eliteSize = 20, mutationRate = 0.01, generations = 500)
