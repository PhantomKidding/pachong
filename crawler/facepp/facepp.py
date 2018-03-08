# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Author: Cheng Chen
# # @Email : cchen224@uic.edu
# # @Time  : 2/18/18
# # @File  : [pachong] facepp.py
#
#
# from pachong import Pachong
# from facepp import API, APIError
#
# accounts = [
#     {'key': '_b8u55jpi1xf_Nl2FhYXKrsFW6dJA5Fm',  # ericchen2436
#      'secret': 'lQfOcPVa81nq2neovsMG8KMx_5C0Y79R'},
#     {'key': 'pqLY9sQp07cBuyXXgr3ntl47WY-p8a-F',  # phantomkidding
#      'secret': 'qljRujMaShVUmz1tqByEyjmdrsGMwhxT'},
#     {'key': 'lUcZXvG7SNw2bEMccgtBqNp3UO4SqhQD',  # hui
#      'secret': 'oxB6mP9N_bp2f4CwgOvesSr4wY8kekBF'},
#     {'key': 'ILkSLLIehF3X3mVfVmAPF7cqjXCk5_L8',  # keran
#      'secret': '0Ad3OtUJDf_e-ovTWAhdZgkduuXvtEyo'},
#     {'key': '14MD5kpg0Miv9d4vpwzXFG7jjHKtf4Ip',  # yue
#      'secret': '2Icrw2CBRREALuCBcCuvAmQ4_NU1y1DJ'},
#     {'key': 'W_vjPSC74hkaDxQ7A4b4A16vPfNihDeV',  # xuelong
#      'secret': 'kp_8z3D0tAAdP8u8Yw94ztlY1TJl8Gvh'},
#     {'key': 'SIGhTQvYJwp_aV4z-Sf24EqBjneOSAQj',  # tanyuting419@hotmail.com
#      'secret': 'VhsOOHnVUqbqox4eHY1FFLyY_SkznYj-'},
#     {'key': 'JGffgH16spgYd6dii0p-AFTc7iWhMonX',  # jianguo
#      'secret': 'HJoW4cmcQz_hwYMS7QsqaWzJRDHecZjX'},
#     {'key': 'qIvik3xfaAOI_xOT4CgB0ZY_23i6NTTy',  # yuekun
#      'secret': 'GfvH31kzWLevk8teUk21kAiodbz63ag1'},
#     {'key': 'OXvtKSKPFSz2ls6wi1dK45lxQxRAhE1s',  # shanwang
#      'secret': 'QX9uSPuAV8MliadrGhHSPsjfJiosJGjl'},
#     {'key': '_DsMsOk1B7zgmxTWhgo9J_ilWoU6sHF5',  # readygobilibili
#      'secret': 'D9fc5sQHx_6433J5aZ9BPuTFf5xVFLGE'},
#     {'key': '1AV70HNEaEsVE3oLyaav77sHSwCm4bwM',  # Happycloverxmh@hotmail.com
#      'secret': 'uJ0Ry4aHCgKebHepgW29pQ8Vndf5P1Kw'},
#     {'key': '8gUtFG63s2_R6gpT-p9wgfkaAPbTWp5a',  # chuan
#      'secret': 'jEDm4GHXu03tVl2g209JxRewI9xcFLG1'},
#     {'key': 'Eww1Xq9hYL-lgdWa_4Rv63u8MZJ__jV2',  # miaohe
#      'secret': 'uAjvlsDYPduXxQIcwyobLMmbTuujBcPf'},
#     {'key': 'TLssl-7MHnEL5vdYSwo021c7AxquI-pl',  # Jazzy_guy@hotmail.com
#      'secret': 'dkIJmFJ-jAubphEX11Dj2u3gY1oEVXOO'},
#     {'key': '9dbidWsNs4nmooNApAEGYFqWNmVfT1Q-',  # lingming.cema@gmail.com
#      'secret': 'G5l2SHg07SCpF5UcWYsZwM1lNX98cFJu'},
#     {'key': 'kuCrbSioULNYhzl3Sx0TR5QJLYUH0bcC',  # wangzhu
#      'secret': 'sH6mG3tv6nFjPvU7vEfIPFwlVE1qaOBI'},
#     {'key': 'LOTvbYrNSYqla6T6Ry5hA-ZkcwZD9yhr',  # nanzhi
#      'secret': '504zsq9XHOlOvOO-I1qT1hWYzB4oIpG1'},
#     {'key': 'Mg2_yBRo73vJlx38fzMRru2OkGVcqDAl',  # zhangzhiying
#      'secret': 'k7534bXvaWdPVzh1QqeLaezHrR8ssGsF'},
# ]
#
# api = API(key=accounts[iaccount]['key'],
#           secret=accounts[iaccount]['secret'],
#           srv='https://api-us.faceplusplus.com/facepp/v3/')
#
# class Facepp(Pachong):
#
#     tasks_available = ['detect']
#     detect_attributes = 'gender,age,smiling,headpose,blur,eyestatus,emotion,ethnicity,beauty,eyegaze,skinstatus'
#
#     def detect(self, uid, *args, **kwargs):
#         if 'url_field' not in kwargs:
#             raise LookupError('Facepp detect must specify field of image url.')
#         url = self.input_.get(uid).get(kwargs['url_field'])
#         if url:
#             img = api.detect(image_url=url, return_landmark=2, return_attributes=self.detect_attributes)
#             yield img['faces']
#
#     def compare_with_avatar(self, pid, *args, **kwargs):
#         if 'url_field' not in kwargs:
#             raise LookupError('Facepp detect must specify field of image url.')
