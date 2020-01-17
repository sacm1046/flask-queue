from twilio.rest import Client

class AdminQueue:
    def __init__(self):
        self.account_sid = 'AC1fb45ff7ec95e9becebd48569700fd73'
        self.auth_token = 'd0bf3ef0f1640f627ace3a1efad8de4f'
        self.client = Client(self.account_sid, self.auth_token)
        self._queue = []
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'
    
    def enqueue(self, item):
        self._queue.append(item)
        message = self.client.messages.create(
                              body='Welcome ' +str(item['name'])+ ' usted será atendido después de'+str(self.size())+' personas!',
                              from_='+13373810525',
                              to=str(item['phone'])
                          )
        return message.sid

    def dequeue(self):
        if self.size() > 0:
            if self._mode == 'FIFO':
                item = self._queue.pop()
                message = self.client.messages.create(
                              body='Chaoo ' +str(item['name'])+'!',
                              from_='+13373810525',
                              to=str(item['phone'])
                          ) 
                return item
            elif self._mode == 'LIFO':  
                item = self._queue.pop(-1)
                message = self.client.messages.create(
                              body='Chaoo ' +str(item['name'])+'!',
                              from_='+13373810525',
                              to=str(item['phone'])
                          ) 
                return item
        else:
            msg = {
                "msg":"Empty queue"
            }
             

    def get_queue(self):
        return self._queue

    def size(self):
        return len(self._queue)