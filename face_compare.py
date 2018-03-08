#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/18/18
# @File  : [pachong] face_compare.py


import json

from facepp import API, APIError
from pymongo import MongoClient
from tqdm import tqdm

accounts = [
        {'key': '_b8u55jpi1xf_Nl2FhYXKrsFW6dJA5Fm',  # ericchen2436
         'secret': 'lQfOcPVa81nq2neovsMG8KMx_5C0Y79R'},
        {'key': 'pqLY9sQp07cBuyXXgr3ntl47WY-p8a-F',  # phantomkidding
         'secret': 'qljRujMaShVUmz1tqByEyjmdrsGMwhxT'},
        {'key': 'lUcZXvG7SNw2bEMccgtBqNp3UO4SqhQD',  # hui
         'secret': 'oxB6mP9N_bp2f4CwgOvesSr4wY8kekBF'},
        {'key': 'ILkSLLIehF3X3mVfVmAPF7cqjXCk5_L8',  # keran
         'secret': '0Ad3OtUJDf_e-ovTWAhdZgkduuXvtEyo'},
        {'key': '14MD5kpg0Miv9d4vpwzXFG7jjHKtf4Ip',  # yue
         'secret': '2Icrw2CBRREALuCBcCuvAmQ4_NU1y1DJ'},
        {'key': 'W_vjPSC74hkaDxQ7A4b4A16vPfNihDeV',  # xuelong
         'secret': 'kp_8z3D0tAAdP8u8Yw94ztlY1TJl8Gvh'},
        {'key': 'SIGhTQvYJwp_aV4z-Sf24EqBjneOSAQj',  # tanyuting419@hotmail.com
         'secret': 'VhsOOHnVUqbqox4eHY1FFLyY_SkznYj-'},
        {'key': 'JGffgH16spgYd6dii0p-AFTc7iWhMonX',  # jianguo
         'secret': 'HJoW4cmcQz_hwYMS7QsqaWzJRDHecZjX'},
        {'key': 'qIvik3xfaAOI_xOT4CgB0ZY_23i6NTTy',  # yuekun
         'secret': 'GfvH31kzWLevk8teUk21kAiodbz63ag1'},
        {'key': 'OXvtKSKPFSz2ls6wi1dK45lxQxRAhE1s',  # shanwang
         'secret': 'QX9uSPuAV8MliadrGhHSPsjfJiosJGjl'},
        {'key': '_DsMsOk1B7zgmxTWhgo9J_ilWoU6sHF5',  # readygobilibili
         'secret': 'D9fc5sQHx_6433J5aZ9BPuTFf5xVFLGE'},
        {'key': '1AV70HNEaEsVE3oLyaav77sHSwCm4bwM',  # Happycloverxmh@hotmail.com
         'secret': 'uJ0Ry4aHCgKebHepgW29pQ8Vndf5P1Kw'},
        {'key': '8gUtFG63s2_R6gpT-p9wgfkaAPbTWp5a',  # chuan
         'secret': 'jEDm4GHXu03tVl2g209JxRewI9xcFLG1'},
        {'key': 'Eww1Xq9hYL-lgdWa_4Rv63u8MZJ__jV2',  # miaohe
         'secret': 'uAjvlsDYPduXxQIcwyobLMmbTuujBcPf'},
        {'key': 'TLssl-7MHnEL5vdYSwo021c7AxquI-pl',  # Jazzy_guy@hotmail.com
         'secret': 'dkIJmFJ-jAubphEX11Dj2u3gY1oEVXOO'},
        {'key': '9dbidWsNs4nmooNApAEGYFqWNmVfT1Q-',  # lingming.cema@gmail.com
         'secret': 'G5l2SHg07SCpF5UcWYsZwM1lNX98cFJu'},
        {'key': 'kuCrbSioULNYhzl3Sx0TR5QJLYUH0bcC',  # wangzhu
         'secret': 'sH6mG3tv6nFjPvU7vEfIPFwlVE1qaOBI'},
        {'key': 'LOTvbYrNSYqla6T6Ry5hA-ZkcwZD9yhr',  # nanzhi
         'secret': '504zsq9XHOlOvOO-I1qT1hWYzB4oIpG1'},
        {'key': 'Mg2_yBRo73vJlx38fzMRru2OkGVcqDAl',  # zhangzhiying
         'secret': 'k7534bXvaWdPVzh1QqeLaezHrR8ssGsF'},
    ]


def detect(iaccount, url):
    detect_attributes = 'gender,age,smiling,headpose,blur,eyestatus,emotion,ethnicity,beauty,eyegaze,skinstatus'
    api = API(key=accounts[iaccount]['key'],
              secret=accounts[iaccount]['secret'],
              srv='https://api-us.faceplusplus.com/facepp/v3/')
    img = api.detect(image_url=url, return_landmark=2, return_attributes=detect_attributes)
    return img['faces']


def significance(res):
    prob = res['confidence']
    thresholds = res['thresholds']
    out = str(prob)
    level1 = thresholds['1e-3']
    level2 = thresholds['1e-4']
    level3 = thresholds['1e-5']
    for level in [level1, level2, level3]:
        if prob > level:
            out += '*'
        else:
            break
    return out


def compare(iaccount, token1, token2):
    api = API(key=accounts[iaccount]['key'],
              secret=accounts[iaccount]['secret'],
              srv='https://api-us.faceplusplus.com/facepp/v3/')
    return significance(api.compare(face_token1=token1, face_token2=token2))


_d = 'instagram'
_c_users = 'users'
_c_media = 'media'


mongo = MongoClient()
users = mongo[_d][_c_users]
media = mongo[_d][_c_media]


with tqdm(users.find()) as bar:
    iaccount = -1
    for row in bar:
        iaccount += 1
        iaccount %= len(iaccount)

        ### avatar
        uid = row['_id']
        url = row['avatar']
        if 'face' not in row:
            try:
                faces = detect(iaccount, url)
            except APIError as e:
                if json.loads(e.body).get('error_message', '') == 'INVALID_IMAGE_URL':
                    users.delete({'_id': uid})
                    media.delete_many({'uid': uid})
                continue
            if len(faces) > 1:
                users.delete_many({'_id': uid})
                media.delete_many({'uid': uid})
            elif len(faces) == 1:
                users.update({'_id': uid}, {'$set': {'face': faces[0], 'iaccount': iaccount}})
            else:
                continue
            avatar_token = faces[0]['face_token']
        else:
            avatar_token = row['face']['face_token']

        ### media
        with tqdm(media.find({'uid': uid})) as subbar:
            for mm in subbar:
                mid = mm['_id']
                murl = mm['url']
                if 'faces' not in mm:
                    try:
                        mfaces = detect(iaccount, url)
                    except APIError as e:
                        if json.loads(e.body).get('error_message', '') == 'INVALID_IMAGE_URL':
                            media.delete({'_id': mid})
                        continue
                    media.update({'_id': mid}, {'$set': {'faces': mfaces}})
                else:
                    mfaces = mm['faces']

                if 'faces_is_avatar' in mm:
                    continue
                try:
                    face_compares = [compare(iaccount, avatar_token, fff['face_token']) for fff in mfaces]
                    media.update({'_id': mid}, {'$set': {'faces_is_avatar': face_compares}})
                except:
                    continue
