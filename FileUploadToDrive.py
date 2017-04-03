#this only works with a client_secret file that is used with the REST API of Google Drive
# Follow the instructions in the below link to create your client_secret file and place it in the working directory of your project
# << https://developers.google.com/drive/v3/web/quickstart/python >>

from __future__ import print_function
import os
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
def FileUpload(regno):
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) 
                if flags else tools.run(flow, store)
    DRIVE = build('drive', 'v3', http=creds.authorize(Http()))
    FILES = (
        ('Timetable of '+regno+'.txt', 'application/vnd.google-apps.document'),
    )

    for filename, mimeType in FILES:
        metadata = {'name': filename}
        if mimeType:
            metadata['mimeType'] = mimeType
        res = DRIVE.files().create(body=metadata, media_body=filename).execute()
        if res:
            print('Uploaded "%s" (%s)' % (filename, res['mimeType']))
    # downloads as pdf
    #if res:
    #    MIMETYPE = 'application/pdf'
    #    data = DRIVE.files().export(fileId=res['id'], mimeType=MIMETYPE).execute()
    #    if data:
    #        fn = '%s.pdf' % os.path.splitext(filename)[0]
    #        with open(fn, 'wb') as fh:
    #            fh.write(data)
    #        print('Downloaded "%s" (%s)' % (fn, MIMETYPE))
