import datetime
from twisted.internet import reactor

from async_notify import AsyncNotify
dsn = "dbname={0} host={1} user={2} password={3}".format(
            'dbname',
            'dbhost',
            'dbuser',
            'dbpassword'
            )

def errorHandler(self, error):
    print('{0}'.format(error))
    reactor.stop()

def shutdown(notifier):
    print('shutting down the reactor')
    reactor.stop()



class AbsorbNotifications(AsyncNotify):

    def gotNotify(self, pid, notify):
        if notify.payload:
            # run this one only when the params have values 
            print('PID: {0} \nCHANNEL:{1} \nPAYLOAD:{2}  \nTIMESTAMP:{3}'.format(notify.pid, notify.channel, notify.payload, datetime.datetime.now()))
            self.respondNotify(notify)


    def respondNotify(self, notify):
        if notify.payload:
            notify_payload = notify.payload.split('|')
            populate_respond = "INSERT INTO ddc_notification_respond(responder, timestamp, id) VALUES('{0}', now(), {1});".format(self.app_name, notify_payload[0])
            print('Confirming the notification for param: {0} notification_id: {1}'.format(notify_payload[1], notify_payload[0]))
            self.curs.execute(populate_respond)



notifier = AbsorbNotifications(dsn)

#set App Name
notifier.app_name = 'Status Manager'

#run the listener
listener = notifier.run()

#notifier add notification 
notifier.addNotify('BOOKING_STATUS_UPDATED')

#remove notifications after 60 seconds
reactor.callLater(60, notifier.removeNotify, 'BOOKING_STATUS_UPDATED')
reactor.callLater(60, notifier.stop)

if __name__ == '__main__':
    reactor.run()
