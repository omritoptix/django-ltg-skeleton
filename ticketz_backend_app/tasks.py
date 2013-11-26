'''
will hold the async tasks

Created on Nov 26, 2013
@copyright: Nerdeez
@author: ywarezk
@version: 1.0
'''





##############################
# Begin async tasks
#############################

@periodic_task(run_every=timedelta(seconds=60), name='tasks.close_deals')
def close_deals():
    '''
    deal that passed the valid to should be closed
    '''
    
    print 'Closing deals that passed the valid_to'
    Deal.objects.filter(valid_to__lte=datetime.datetime.now()).update(status=3)


##############################
# end async tasks
#############################
