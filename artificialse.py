from datetime import datetime
import random
import os
import csv
import sqlite3


class App:

  def __init__(self, item, value):
    self.value = value
    self.mag = float(self.value) / 100000000
    self.increase = 50
    self.decrease = 40
    self.flat = 20
    self.fluct = 20
    self.volatileFlat = 20
    self.breakOutUp = 15
    self.breakOutDown = 15
    self.spikeSell = 5
    self.spikeNoSell = 5
    self.crashRecover = 10
    self.crashNoRecover = 10
    self.pattern = ''.join(random.choices(['increase',
                                   'decrease',
                                   'flat',
                                   'fluct',
                                   'volatileFlat',
                                   'breakOutUp',
                                   'breakOutDown',
                                   'spikeSell',
                                   'spikeNoSell',
                                   'crashRecover',
                                   'crashNoRecover'], weights=[self.increase,
                                                               self.decrease,
                                                               self.flat,
                                                               self.fluct,
                                                               self.volatileFlat,
                                                               self.breakOutUp,
                                                               self.breakOutDown,
                                                               self.spikeSell,
                                                               self.spikeNoSell,
                                                               self.crashRecover,
                                                               self.crashNoRecover], k=1))
    self.running = True
    self.item = item
    '''
    if os.path.exists(str(item) + '.txt'):
      pass
    else:
      self.f = open(str(item) + '.txt', 'x')
      self.f.close()'''
    self.currentPeriod = datetime.now().strftime('%H%M')
    self.nextPeriod = str((int(datetime.now().strftime('%H')) + 1) * 100)
    self.volume = random.randint(0,1000) * 1000
    self.currentVolume = 0
    self.distrib = {}
    self.secondDistrib = {}
    self.bid = 0
    self.ask = 0
    self.currentBidAsk = []
    self.price = float(value)
    self.intPrice = int(self.price)
    self.averagedPriceMove = 0.0
    self.currentMin = datetime.now().strftime('%M')
    self.nextMin = str((int(datetime.now().strftime('%M')) + 1))
    self.currentSecond = 0
    self.open = int(value)
    self.high = int(value)
    self.low = int(value)
    self.close = int(value)              #Ask #Bid
    self.patterns = {}
    self.patterns['increase'] = [.5 , .25]
    self.patterns['decrease'] = [.5 , 1]
    self.patterns['flat'] =  [.25 , .25]
    self.patterns['fluct'] = [1 , 1]
    self.patterns['volatileFlat'] = [2 , 2]
    self.patterns['breakOutUp'] = [.5 , .5, 1 , .25]
    self.patterns['breakOutDown'] = [.5 , .5 , .25 , 1]
    self.patterns['spikeSell'] = [1.5 , 1, 1 , 2]
    self.patterns['spikeNoSell'] = [1.5 , 1]
    self.patterns['crashRecover'] = [1 , 2, 1.5 , 1]
    self.patterns['crashNoRecover'] = [1, 2]
    self.trigger = False
    self.triggerTime = 0
    self.multiLg = False
    self.main()

  def priceSet(self):
    if self.secondDistrib[int(datetime.now().strftime('%S'))] < 0 and self.intPrice < self.value:
        self.price += (self.secondDistrib[int(datetime.now().strftime('%S'))] * self.mag) * 0.1
    elif self.secondDistrib[int(datetime.now().strftime('%S'))] < 0 and self.intPrice > self.value * 10:
        self.price += (self.secondDistrib[int(datetime.now().strftime('%S'))] * self.mag) * 0.1
    else:
        self.price += self.secondDistrib[int(datetime.now().strftime('%S'))] * self.mag
    self.intPrice = int(self.price)
    if self.intPrice > self.high:
        self.high = self.intPrice
    if self.intPrice < self.low:
        self.low = self.intPrice

  def bidAsk(self):
    factors = self.patterns[str(self.pattern)]
    if not self.trigger == True:
        askX = factors[0] #ask = increase
        bidX = factors[1] #bid = decrease
    else:
        askX = factors[2]
        bidX = factors[3]
    self.bid = (self.currentVolume - random.randint(0, self.currentVolume + 1)) * bidX
    self.ask = (self.currentVolume - random.randint(0, self.currentVolume + 1)) * askX
    if self.currentBidAsk:
      self.currentBidAsk[0] = self.bid
      self.currentBidAsk[1] = self.ask
    for i in range(0,60):
            totalAction = random.randint(0, int(self.ask)) + -random.randint(0, int(self.bid))
            self.secondDistrib[i] = totalAction

  def reVolume(self):
    self.volume = random.randint(0,1000) * 1000
    self.triggerTime = 0
    self.trigger = False
    self.pattern = ''.join(random.choices(['increase',
                                   'decrease',
                                   'flat',
                                   'fluct',
                                   'volatileFlat',
                                   'breakOutUp',
                                   'breakOutDown',
                                   'spikeSell',
                                   'spikeNoSell',
                                   'crashRecover',
                                   'crashNoRecover'], weights=[self.increase,
                                                               self.decrease,
                                                               self.flat,
                                                               self.fluct,
                                                               self.volatileFlat,
                                                               self.breakOutUp,
                                                               self.breakOutDown,
                                                               self.spikeSell,
                                                               self.spikeNoSell,
                                                               self.crashRecover,
                                                               self.crashNoRecover], k=1))
    if self.pattern == 'breakOutUp' or self.pattern == 'breakOutDown' or self.pattern == 'spikeSell' or self.pattern == 'crashRecover':
        self.multiLeg()

  def multiLeg(self):
      self.triggerTime = random.randint(10,45)

  def minuteUpdate(self):
    self.currentVolume = self.distrib[int(datetime.now().strftime('%M'))]
    self.open = self.close
    self.close = self.intPrice
    #self.high = int(self.secondDistrib[max(self.secondDistrib.keys(), key=(lambda k: self.secondDistrib[k]))] * 0.0001) + self.intPrice
    #self.low = int(self.secondDistrib[min(self.secondDistrib.keys(), key=(lambda k: self.secondDistrib[k]))] * 0.0001) + self.intPrice
    """
    print(self.high)
    print(self.low)
    print(self.secondDistrib)
    """
    self.secondDistrib.clear()
    self.bidAsk()
    '''
    self.f = open(str(self.item) + '.txt' , 'w')
    self.f.write('Current Price: ' + str(self.price) + '\n' +
    'Current Integer Price: ' + str(self.intPrice) + '\n' +
    'Current Hourly Max Volume: ' + str(self.volume) + '\n' +
    'Current Minute Max Volume: ' + str(self.currentVolume) + '\n' +
    'Current Bid/Ask: ' + str(self.currentBidAsk) + '\n' +
    'Current Time: ' + str(self.currentPeriod) + '\n' +
    'Next Period: ' + str(self.nextPeriod))
    self.f.close()'''


    print('Current Price for ' + self.item + ': ' + str(self.intPrice) + '\n')
    print(self.pattern)


    '''
    print('Current Price: ', self.price)
    print('Current Integer Price: ', self.intPrice)
    print('Current Hourly Max Volume: ', self.volume)
    print('Current Minute Max Volume: ', self.currentVolume)
    print('Current Bid/Ask: ', self.currentBidAsk)
    print('Current Time: ', self.currentPeriod)
    print('Next Period: ', self.nextPeriod + '\n')'''

  def main(self):

    for i in range(0,60):
      distribAdd = self.volume - random.randint(0, self.volume + 1)
      self.distrib[i] = distribAdd
    self.currentVolume = self.distrib[int(datetime.now().strftime('%M'))]
    self.bidAsk()
    if not self.currentBidAsk:
        self.currentBidAsk.append(self.bid)
        self.currentBidAsk.append(self.ask)

    if self.currentPeriod >= self.nextPeriod:
      self.reVolume()
      self.main()
      self.nextPeriod = str(int(self.nextPeriod) + 100)



class Manager:
    def __init__(self):
        self.names = []
        self.values = {}
        self.running = True
        self.currentPeriod = datetime.now().strftime('%H%M')
        self.nextPeriod = str((int(datetime.now().strftime('%H')) + 1) * 100)
        self.currentMin = datetime.now().strftime('%M')
        self.nextMin = str((int(datetime.now().strftime('%M')) + 1))
        self.currentSecond = datetime.now().strftime('%S')
        self.nextSecond = str((int(datetime.now().strftime('%S')) + 1))
        self.classes = {}
        self.conn = sqlite3.connect('artificialStock.db')
        self.c = self.conn.cursor()
        self.main()

    def databaseCreation(self):
        #self.c.execute('CREATE TABLE if not EXISTS mainTable(name text, volume int, bid int, ask int, open int, high int, low int, close int)')
        pass

    def printDB(self):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(self.c.fetchall())

    def main(self):
        #self.databaseCreation()
        #self.printDB()
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        name = [str(j[0]) for j in self.c.fetchall()]
        print(name)
        for i in name:
            self.names.append(i)
            self.c.execute('SELECT value FROM ' + i + ' ORDER BY value DESC LIMIT 1;')
            self.values[i] = [j[0] for j in self.c.fetchall()][0]
        print(self.values)
        for i in self.names:
            self.classes[i] = App(i, self.values[i])
            try:
                self.c.execute('CREATE TABLE if not EXISTS ' + str(i) + '(date text, time text, volume int, bid int, ask int, open int, high int, low int, close int, value int)')
            except:
                print('Table Already Exists')

            try:
                self.c.execute('SELECT close FROM ' + str(i) + ' ORDER BY time DESC LIMIT 1;')
                listed = [float(j[0]) for j in self.c.fetchall()]
                self.classes[i].price = listed[0]
                print(' Previous price for ' + str(i) + ': ' + str(self.classes[i].price))
            except:
                print('No Previous Close')
        while self.running:

            if int(self.nextSecond) >= 60:
                self.nextSecond = str(int(self.currentSecond) + 1)
            if int(self.nextMin) >= 60:
                self.nextMin = str(int(self.currentMin) + 1)
            self.currentSecond = datetime.now().strftime('%S')
            self.currentMin = datetime.now().strftime('%M')
            self.currentPeriod = datetime.now().strftime('%H%M')
            #Hourly Operations
            if int(self.currentPeriod) >= int(self.nextPeriod) or (int(self.currentPeriod) == 0 and int(self.nextPeriod) != '0100'):
                for i in self.names:
                    self.classes[i].reVolume()
                    self.classes[i].main()
                    self.nextPeriod = str(int(self.nextPeriod) + 100)
            #Minutely Operations
            if int(self.currentMin) >= int(self.nextMin) or (int(self.currentMin) == 0 and int(self.nextMin) != 1):
                for i in self.names:
                    self.classes[i].minuteUpdate()
                    self.c.execute("INSERT INTO " + str(i) + " VALUES(" + datetime.now().strftime('%Y-%m-%d') + ',' + str(datetime.now().strftime('%d%m%Y%H%M')) + ',' + str(self.classes[i].currentVolume) + ',' + str(self.classes[i].currentBidAsk[0]) + ',' + str(self.classes[i].currentBidAsk[1]) + ',' + str(self.classes[i].open) + ',' + str(self.classes[i].high) + ',' + str(self.classes[i].low) + ',' + str(self.classes[i].close) + ',' + str(self.classes[i].value) + ')')
                    self.conn.commit()
                    self.classes[i].high = self.classes[i].intPrice
                    self.classes[i].low = self.classes[i].intPrice
                    if self.classes[i].multiLg == True:
                        if self.classes[i].triggerTime >= int(self.currentMin):
                            self.classes[i].trigger == True
                self.nextMin = str(int(self.nextMin) + 1)
            #Secondly Operations
            if int(self.currentSecond) >= int(self.nextSecond) or (int(self.currentSecond) == 0 and int(self.nextSecond) != 1):
                for i in self.names:
                    self.classes[i].priceSet()
                self.nextSecond = str(int(self.nextSecond) + 1)


Manager()
