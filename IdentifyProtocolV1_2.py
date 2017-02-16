# coding:utf-8
'''
This is a demo program which implements ACRCloud Identify Protocol V1 all by native python libraries.
'''

import sys
import os
import base64
import hmac
import hashlib
import time
import httplib
import mimetools
import json

def post_multipart(host, selector, fields, files):
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read()

def encode_multipart_formdata(fields, files):
    boundary = mimetools.choose_boundary()
    CRLF = '\r\n'
    L = []
    for (key, value) in fields.items():
        L.append('--' + boundary)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(str(value))
    for (key, value) in files.items():
        L.append('--' + boundary)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, key))
        L.append('Content-Type: application/octet-stream')
        L.append('')
        L.append(value)
    L.append('--' + boundary + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % boundary
    return content_type, body

def get_tracks_artists(artists):
    artists_namelist = []
    for artist in artists:
        artists_namelist.append(artist['name'])
    space = ','
    artists_names = space.join(artists_namelist)
    return artists_names

def add_track(artist, track) :
    with open("/var/lib/mopidy/playlists/like.m3u", "a") as myfile:
        myfile.write("#EXTINF:-1, {} - {} \nhttp://prout\n".format(artist, track))
'''
Replace "###...###" below with your project's host, access_key and access_secret.
'''
host = "eu-west-1.api.acrcloud.com"
access_key = "385440f6e5ef23a2a0ee285485ec4595"
access_secret = "eo0kSdsgsTtFVUdCYXCCbkKYMZQZPnfqKyhrbbzq"

# suported file formats: mp3,wav,wma,amr,ogg, ape,acc,spx,m4a,mp4,FLAC, etc
# File size: < 1M , You'de better cut large file to small file, within 15 seconds data size is better

f = open(sys.argv[1], "rb")
sample_bytes = os.path.getsize(sys.argv[1])
content = f.read()
f.close()

http_method = "POST"
http_uri = "/v1/identify"
data_type = "audio"
signature_version = "1"
timestamp = time.time()

string_to_sign = http_method+"\n"+http_uri+"\n"+access_key+"\n"+data_type+"\n"+signature_version+"\n"+str(timestamp)
sign = base64.b64encode(hmac.new(access_secret, string_to_sign, digestmod=hashlib.sha1).digest())

fields = {'access_key':access_key,
          'sample_bytes':sample_bytes,
          'timestamp':str(timestamp),
          'signature':sign,
          'data_type':data_type,
          "signature_version":signature_version}

res = post_multipart(host, "/v1/identify", fields, {"sample":content})
parsed_resp = json.loads(res)
code = parsed_resp['status']['code']
if code != 0 :
    print('None')
else :
    metadata = parsed_resp['metadata']
    try :
        title = metadata['music'][0]['title'].encode('utf-8')
        album = metadata['music'][0]['album']['name'].encode('utf-8')
        artists = get_tracks_artists(metadata['music'][0]['artists']).encode('utf-8')
        print('Track : {}\nArtist {}\nAlbum : {}'.format(title, artists, album))
        #add_track(title, artists)
    except Exception as e:
        print('None')





