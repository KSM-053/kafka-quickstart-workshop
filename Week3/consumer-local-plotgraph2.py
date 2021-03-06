from confluent_kafka import Consumer

c = Consumer({
    'bootstrap.servers': 'localhost:9092,localhost:9192,localhost:9292',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['streams-pageviewstats-typed-output'])

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
figure(num=None, figsize=(10, 6), dpi=80, facecolor='w', edgecolor='k')
plt.ion()

lr = {}
while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    value = msg.value()
    if value is None:
        value = 0
    else:
        value = msg.value()[-1]
        
    kvalue = msg.key().decode('utf-8')
    print('Received message: {0} , {1}'.format(kvalue, value))
   
    lr[kvalue] = value    
    plt.scatter(list(lr.keys()),list(lr.values()))
    i = 0
    for x in range(0,len(list(lr.keys()))): 
        plt.annotate(list(lr.keys())[x], (i, list(lr.values())[x]+0.1), rotation=30)
        i = i+1
        
    plt.draw()
    plt.pause(0.1)

plt.show(block=True)
c.close()

