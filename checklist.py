# Imports ###############################################################################

import hashlib

import orgparse
import webdav3.client


from utils import get_valid_filename


# Functions #############################################################################

def get_all_checklists():
    return orgparse.load('checklist.org')

def get_all_checklists_items_names():
    """
    Return the names of all the checklists and their children items
    """
    names = []
    for checklist in get_all_checklists():
        names.append(checklist.heading)

    return names

def get_audio_filename(text, extension='ogg'):
    '''
    Return a unique audio filename for a given text string
    '''
    return './audio/{}_{}.{}'.format(get_valid_filename(text),
                                     hashlib.md5(text.encode('utf8')).hexdigest(),
                                     extension)

def update_checklist_orgfile(self):
    # TODO: Fix disabled webdav retrieval
    self.webdav = webdav3.client.Client({
            'webdav_hostname': config['REPOSITORY_WEBDAV_URL'],
            'webdav_login':    config['REPOSITORY_WEBDAV_USER'],
            'webdav_password': config['REPOSITORY_WEBDAV_PASSWORD'],
    })
    self.webdav.check('/checklist_flight_planning.org')
    self.webdav.download_sync(
            remote_path='/checklist_flight_planning.org',
            local_path='/tmp/checklist_flight_planning.org')

