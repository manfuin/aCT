import sys
import os
from act.common.aCTLogger import aCTLogger
from act.common.aCTConfig import aCTConfigARC, aCTConfigAPP
from act.arc.aCTDBArc import aCTDBArc
from act.condor.aCTDBCondor import aCTDBCondor
from act.atlas.aCTDBPanda import aCTDBPanda

from act.client.clientdb import ClientDB


def bootstrap_conf():
    '''Check config is ok'''
    try:
        arcconf = aCTConfigARC()
    except Exception as e:
        print('Error processing ARC config file: %s' % str(e))
        sys.exit(1)

    try:
        atlasconf = aCTConfigAPP()
    except Exception as e:
        print('Error processing APP config file: %s' % str(e))
        sys.exit(1)

def bootstrap_dirs():
    '''Make necessary directories'''
    arcconf = aCTConfigARC()
    os.makedirs(arcconf.get(['tmp', 'dir']), mode=0o755, exist_ok=True)
    os.makedirs(arcconf.get(['logger', 'logdir']), mode=0o755, exist_ok=True)

def bootstrap_db():
    '''Set up the DB tables'''
    # TODO: setup only what is needed based on config and app
    logger = aCTLogger('aCTBootstrap')
    log = logger()
    dbarc = aCTDBArc(log)
    dbclient = ClientDB(log)
    dbcondor = aCTDBCondor(log)
    dbpanda = aCTDBPanda(log)
    if not dbarc.createTables():
        print('Error creating arc tables, see aCTBootstrap.log for details')
    if not dbclient.createTables():
        print('Error creating client tables, see aCTBootstrap.log for details')
    if not dbcondor.createTables():
        print('Error creating condor tables, see aCTBootstrap.log for details')
    if not dbpanda.createTables():
        print('Error creating panda tables, see aCTBootstrap.log for details')


def main():

    bootstrap_conf()
    bootstrap_dirs()
    bootstrap_db()


if __name__ == '__main__':
    main()
