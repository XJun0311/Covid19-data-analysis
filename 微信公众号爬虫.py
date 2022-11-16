#https://mp.weixin.qq.com/s/kcJP0FLVozAKQNA3FpQX3w
import json
import re
import requests
import jieba.analyse
import time
import wordcloud
import os
from pyecharts.charts import WordCloud
from pyecharts.components import Image
from pyecharts import options as opts
from pyecharts.globals import SymbolType
from pyecharts.options import ComponentTitleOpts

#通过fiddler找到文章评论区的url和headers
'''urlgz10_23 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2247623671&idx=1&comment_id=2632427614732992515&offset=0&limit=100&send_time=&sessionid=1666531174&enterid=1666531878&uin=MTEwMjg0MTUwMg%3D%3D&key=a6088c6ea55d01fa1d26e846c74d5fe6181fb29d6460af0d939fa5094f03b6ceac9c2900d487a5943ded6ecb726279e173b68eac0761860ddcb14ff8fbf3ebf027400478203a98b22af2e9c2f48778bf7aa98851c656e6250a79e97460295fbbf2ea36037c78e27fa66e99e3c84f906b8a917e0c42412cb1ecde66c771f78e16&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzU2NTA0NTI0Ng%3D%3D&appmsg_token=1188_WtJpp4A7Y5r0kXYMv1jfQW3y0H4-pP19LrLojdQ3ndB7ZR2MsMnKk8CZW0JLY8-bdSIWzNKJzdnPXsfv&x5=0&f=json'
urlgz10_22 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2247623630&idx=1&comment_id=2631669993675603972&offset=0&limit=100&send_time=&sessionid=1666531174&enterid=1666531883&uin=MTEwMjg0MTUwMg%3D%3D&key=e3743bb3a0d660f43841947a9882851051ccc539bfbf9c612be96c42f898b035aced72700d8cca05ca6b2ab54175262016f3e66e68d60806029ad4f66968aeea9fb4aef5d6842d0654b1ec2bca31eb086d40a06a76edc2bf167101537b36d24017bfc59cd086dc4f71e3fde163c8d1bd1a33b4fa539cae58125b44688351c33f&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzU2NTA0NTI0Ng%3D%3D&appmsg_token=1188_KICev6NdvXLjGwI%252Bli86V7kNVXhPBVseDTr9MZgT9raSiPJyUs7w2I3w7qEOCQgWppZ1RrVBGKscaxEs&x5=0&f=json'
urlgz10_21 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2247623580&idx=1&comment_id=2630957991579795458&offset=0&limit=100&send_time=&sessionid=1666531174&enterid=1666531895&uin=MTEwMjg0MTUwMg%3D%3D&key=a6088c6ea55d01faddfb6413e8ecc8648752a2ca6ebcc68b159886365eedd3ba632197734ffc4716bec774cc76839dc5cdf46f074d7d199a9ec33500ab4ee26a4efe59a0bb73235e2ce7bc49b4b8657797be31743ab5a8aef7072b7f3a3a54d4ff243b894289bd3e03857fe026eb2aa22daa50df2c995f5b34dcc1e5955e2723&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzU2NTA0NTI0Ng%3D%3D&appmsg_token=1188_hkzWj77%252Bo97pikOlY63XU069VAZIqOSxmKtLDIKHhE5jEYuIfZsAOS0GQNcGF0xo4FCxANIqe-iJHc-w&x5=0&f=json'
urlgz10_20 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2247623414&idx=1&comment_id=2629530643454148609&offset=0&limit=100&send_time=&sessionid=1666531174&enterid=1666531231&uin=MTEwMjg0MTUwMg%3D%3D&key=5fec8e52ea28606600608a6299a8d7136bd35eb2299a3d7f6ab39b805a6ee2fa6a54405faae188293c4639cbf252d18138c33c7b0e6a1843de8dd3014d2a557022cdf6848f17176df3540fdc785ce9198b2143558bd71aeeb2e137f9c2ca38b49ec470f8b570ec92b3a6c0e54cd5e4ba1f6e692d90b6a3096d9bb3af0e404d84&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzU2NTA0NTI0Ng%3D%3D&appmsg_token=1188_AvJFA4LIpTWezO%252FeKYLhwcsaDD8W6IBRSOIKC01cliIPOzwHg2uAbJd3ccOSlhHhz02uIFvbPJYMM2sE&x5=0&f=json'
urlgz10_19 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2247623315&idx=1&comment_id=2628076146336907265&offset=0&limit=100&send_time=&sessionid=1666531174&enterid=1666531244&uin=MTEwMjg0MTUwMg%3D%3D&key=a6088c6ea55d01fa101309233aebd24ffb7c7dcf3873a82d024130805be72bbd2868322d20a47c0e2d70f49651119b5ee38d250586e73291874d897686da73a8de254f8cb547d89edf4c54f06b9f74494f64f84cd853ead06bac2df3d9f49316021840429f313dbfc3f7e034d1d89bb2bce432747385ef07f7ecaa11b36eaa15&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzU2NTA0NTI0Ng%3D%3D&appmsg_token=1188_EIlzEv64Ogpp074XIB1zf_R-29Ethb4KlPPbUyAnkoz9F-vh9MvvnZdefUVnowesjEriG0iML9SFeOZw&x5=0&f=json'
urlgz10_18 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2247623084&idx=1&comment_id=2626611482696531969&offset=0&limit=100&send_time=&sessionid=1666531241&enterid=1666531263&uin=MTEwMjg0MTUwMg%3D%3D&key=4a14537718758be24a7218b916e7128b98e3496603d6cb5fc6be7e38714f838cb01d586c5d70cc6a1d4a78438910d1ed10e1eb2e9067f2976172f3d3c7cce43b2d7ed0e636b826c33b156e7d6ca92299e27d991380f36688f7994009393b207da4ab404922da4c202b1a92568ace8a945ea00df25768927e7610006b6b26dcce&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzU2NTA0NTI0Ng%3D%3D&appmsg_token=1188_HpA1r1reusBb2DAwOFGGFZPEV1_9rmJ54LC3TAS21qDZfbF86MCkJpn1F9VFyH5o9n26m0aZYss1b56o&x5=0&f=json'
urlgz10_17 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2247622706&idx=1&comment_id=2623680180485799938&offset=0&limit=100&send_time=&sessionid=1666531241&enterid=1666531283&uin=MTEwMjg0MTUwMg%3D%3D&key=89fd73744d9bdce65c38daf2aafdc42a0d3cbf4ce7c573ff22efa2d250535e431c4e488b5170abf7fed51ad664c2e469313056e43af0718ff0c9e9b04e0e087c3a98b073a74ace668f0ae9300a7c857c13afcaa18123d5b8416ab2b79a1d76dbc20870286efbc8b15fb9dfca05163df56779f989b34b19035d5a939539816bf6&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzU2NTA0NTI0Ng%3D%3D&appmsg_token=1188_aldr89ajGcy29hwPSCAMn91LWQ2EtR3JlIuQVUhRhVYUHSWowZXJuZYS-9-PplEoPfEDggSa5Up2CXr6&x5=0&f=json'
urlgz10_16 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2247622534&idx=1&comment_id=2622225909760311300&offset=0&limit=100&send_time=&sessionid=1666531280&enterid=1666531291&uin=MTEwMjg0MTUwMg%3D%3D&key=5fec8e52ea286066f478e8b9d6fb677126c27c04520d097f45bbece5bd9eb7a38ce0c3e8845a46302e96aae54ac62be9dd744597cf6d8fd316601b0867d22b2887c99c844ccf5afb8edbf73050e5497b7c760c8d419b4f0486f82b06e558a522d0ed8715e5fea3193f057c3e0a133d385902d027bd971f7bba0d937c93d7ed62&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzU2NTA0NTI0Ng%3D%3D&appmsg_token=1188_qLitlrHLdWmjYOH4owH71LFAwmemwWPiaJRQj1E2sGwKVA0YgX_-CAK0abcuNjuJaOlhx0Srj9nrapRG&x5=0&f=json'
urlgz10_15 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2247622460&idx=1&comment_id=2620820528983097346&offset=0&limit=100&send_time=&sessionid=1666531280&enterid=1666531297&uin=MTEwMjg0MTUwMg%3D%3D&key=e3743bb3a0d660f42af8dfea0ec43b258e1ade233f8a0a06cc00e254aaeb58b3a9bb345116f618bcf8e3b4556136437c1fbeee6831d7359c9410910a2f92717dbc00877895a8c83e7a61ddb4449fcebd784dbb5bc22d222155a295840bb91db525c5bddfdd0caf68dcd83800ede07422f9dfcc2a6c2d72baa5c8e8c9371dc3b4&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzU2NTA0NTI0Ng%3D%3D&appmsg_token=1188_SLAeQ2k8s3hoT%252BQkzABzPbD2q4gO6kZqGDC3THvqFtyy3vhjUqobY-T23xPVc0yV_0PNvd7eNMqgqnGD&x5=0&f=json'
urlgz10_14 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2247622361&idx=1&comment_id=2619353544936308737&offset=0&limit=100&send_time=&sessionid=1666531280&enterid=1666531321&uin=MTEwMjg0MTUwMg%3D%3D&key=4a14537718758be2910cc1c9e18cd7b3df8ff5d54a69b886b2bdea4f02ba9dd7f2146532830d890231833eaeaadde1360cffc56be81e87b18da0c80215802989300d8c5a1f4aa56133efe3969f288f70c6faa62ed17f1d69113ea386678d056c3ed08fdded50bd5bdb24b2efc353add1c3be0e142dbc54008c27deafd8759150&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzU2NTA0NTI0Ng%3D%3D&appmsg_token=1188_kKrTnmnYJWFgqfJ3LhgmF6AF4o1rSyVoKWbeCBhkh4zsmcspQM8SjOPWiFrLW6ZjqdBOzzCayPte2lIl&x5=0&f=json'
'''

urlsz10_22='https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2652200101&idx=1&comment_id=2626443107798171650&offset=0&limit=100&send_time=&sessionid=1666532538&enterid=1666532597&uin=MTEwMjg0MTUwMg%3D%3D&key=4a14537718758be2b210a7259abc3bb74005d552843070614faee8efc3f43cff53878f154db34b961fe08448a13569c4275ddd7226a739e272590588f9fd2d55bc4fa5c0aa56d5f2e22e1fe187e3624a320cfd9ec77afb8f2946214effeedddeee694546a730a19fc28f684da2f18825e1ab249f182bafb4a5807d048064cadb&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzIxNDA0MTExMg%3D%3D&appmsg_token=1188_wZ7EU0XlIt3nTe6TLkHrUFM0b7HAaCQPwieG-pafIGU69vz5w74uPNCkbliYtxFrxYBBSzRkzxiYLNMj&x5=0&f=json'
urlsz10_21 ='https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2652200122&idx=1&comment_id=2627896263056900097&offset=0&limit=100&send_time=&sessionid=1666532538&enterid=1666532577&uin=MTEwMjg0MTUwMg%3D%3D&key=4a14537718758be2c481b2fbf01f05c3bed014c5dcbc3bba9eedd496cd17beb0e7d3814c7bd29902352f87b9ca0ae28c13ce498babe2d19b618b20b73ac79b5aa7a319979bf5d49e7c2b1b4c61341137d995a365fe17ae597c261a9113006b80b0e4aa1c432948a444d3bdea9e8ebe27dd1ca706cae1efe60071c5c1c807128b&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzIxNDA0MTExMg%3D%3D&appmsg_token=1188_YCT600ZycEnL3fY57RkqLC89mPIYqyi7otiKxbRM3Mx4lhmwiQTDoovkT-Ufi81TSK_g3ug1RlWE_yAG&x5=0&f=json'
urlsz10_20 ='https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2652200140&idx=1&comment_id=2629360189758062592&offset=0&limit=100&send_time=&sessionid=1666532538&enterid=1666532567&uin=MTEwMjg0MTUwMg%3D%3D&key=4a14537718758be2cf1b28c191952d952752598d8a79486c5b6b9bbb414329fa4cfb9d1e6bafdf971cf33446bb0246a542864befa89182d6b1dd5647ff0c1323ce90e4eef08ccb3b76d7f422bf3d28705c77eec9986a6a2d65233a05f5918756fdbcd06b05a5776eac00dda18c4157d91978540ba851cd8e5132de8a4bc473a5&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzIxNDA0MTExMg%3D%3D&appmsg_token=1188_8D9y23FjrrOvvKy43sevVDEiDnTxdLfTCyvLOySl2gZpV1tjXyWkvl2qvbtQTPCxQ9a7JVKtWklduaV5&x5=0&f=json'
urlsz10_19 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2652200162&idx=1&comment_id=2630801580564496386&offset=0&limit=100&send_time=&sessionid=1666532538&enterid=1666532556&uin=MTEwMjg0MTUwMg%3D%3D&key=89fd73744d9bdce68b20de01ea8cea55b089bef76e4d943c9f1ee56759764e4f6ebe2eb5f66d2d9e67ffaedc9eca634c2d28772f3bb50647d60a5b7220fcd4551c7bb524af9ea121821ecae01d0a88af1f3cd8b7f43dad297db051b8ef545708280862bdd72a989400f2bf60814c7b7af0a91f797cb93a67bf92bd81f34c29d0&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzIxNDA0MTExMg%3D%3D&appmsg_token=1188_PG%252BiNb0lZ9DzkvgkwEx0Ge44mC9T_JWg5IoY4FsInWb3D2lL8Lv_b6yBiJCQDvR0q1d06-t9e6gO8CEQ&x5=0&f=json'
urlsz10_18 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2652200182&idx=1&comment_id=2632258719086624769&offset=0&limit=100&send_time=&sessionid=1666532538&enterid=1666532550&uin=MTEwMjg0MTUwMg%3D%3D&key=a6088c6ea55d01fa2a587e205fe68d211cbd61cbf7f1c9691006480c4895a7276c2e15723b2a02910822d32067fdbd2a150c7ac3038855e0bd38685305945d4cbe80a17b136adc26860d37fedd8379ea0db466f0d3712eb879e9fa6a71cc7b88ed45b72dcfc24f9f368470a549ece1a1bbac9a7f249c0899d6abcc35c6cf71fe&pass_ticket=mIwCMf5RaKgQZltez%2F0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzIxNDA0MTExMg%3D%3D&appmsg_token=1188_QMGC0amtx%252FXS6sQeiyqOeUWzExnPOIcnGWQnm5eMJgirvW1iN4TD-MtHa2Ezwg6hGez5csTWzbVTTkJA&x5=0&f=json'
urlsz10_17 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2652200003&idx=1&comment_id=2624991535402663936&offset=0&limit=100&send_time=&sessionid=1666064065&enterid=1666064076&uin=MTEwMjg0MTUwMg%3D%3D&key=4a14537718758be2af0ea9fc10fdeb903db1dcd52d790883a18ab1aab43a769aadba8150e4c9dd788c65c64be54a278be7fcdb9d5213a367e66f546659d62b28c7e76c1b44864951cc07a5366f5e76f4be18dfd4df478b4a19f91a1ec3a188933a73f1be5fc8cd3067bdfee218021659176cfd97ca6ea50f9f594a4493a793ed&pass_ticket=SqEP15c29I%2BCP7GT%2FuYzgfUQUSj9qvzzE4ymnKeG93etsnj78RSnYub3F8HP6t6p&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzIxNDA0MTExMg%3D%3D&appmsg_token=1187_AL6hNkKncUu6Rh4A1x93EGCgFFPGuXelAT7i4tUOzJX7Q3L07o7aajrDmvKmjGMzMfta3ib6IIRMoMys&x5=0&f=json'
urlsz10_16 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2652199954&idx=1&comment_id=2623552440222695426&offset=0&limit=100&send_time=&sessionid=1666064065&enterid=1666064200&uin=MTEwMjg0MTUwMg%3D%3D&key=4a14537718758be22c28f69b9c1ee5a92f75b806cba57c5f55c6cf07d7a2f55122f47cddb6fe4a56dd09ca72c3bdb73dbb76224dfffd7db0127a3f91573a2c9231f865ff37fbd43f49a59102a399c870d9798acd2e882dba79d6989bfb4bc1ffc9cfc1aed60720850a79fc12c9a02a9343cc7e63e18d5bae80ee555fff9e759f&pass_ticket=SqEP15c29I%2BCP7GT%2FuYzgfUQUSj9qvzzE4ymnKeG93etsnj78RSnYub3F8HP6t6p&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzIxNDA0MTExMg%3D%3D&appmsg_token=1187_YEHkGvTH86k0vMd0RlLN3tPtq2VBGdy2gkwFxwFpOuLexqLnNiCPGYKUnxu_kNUNOPpkSbhgULZL2g4p&x5=0&f=json'
urlsz10_15 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2652199908&idx=1&comment_id=2622109125606457348&offset=0&limit=100&send_time=&sessionid=1666064065&enterid=1666064377&uin=MTEwMjg0MTUwMg%3D%3D&key=e2d2810cd8560d8bfacfa897ccc66b9b86f0cd7e70b03998816854de7452bf79e763e39ddad6c3c3ff0563fbb541ed66c02b686c7045428ae17654aee9bab3593bbca6fc0c2b42e10dc6016bdf0cdbaf2b086f6c48e849fac0ac314c53a7b6143db36b04c3a50ad29e89d8ac10e0ea3eca0c89c8ea43fc1e00369e059e935f51&pass_ticket=SqEP15c29I%2BCP7GT%2FuYzgfUQUSj9qvzzE4ymnKeG93etsnj78RSnYub3F8HP6t6p&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzIxNDA0MTExMg%3D%3D&appmsg_token=1187_WzRYLk%252BqdL2QpINnOjRzZuoEiG_PLpVnVG_PbdscWOuy8-qqTs8iCCLQqb0ufuM8BBSjBBsFZeTAFgej&x5=0&f=json'
urlsz10_14 = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2652199852&idx=1&comment_id=2620670727352041473&offset=0&limit=100&send_time=&sessionid=1666064065&enterid=1666064565&uin=MTEwMjg0MTUwMg%3D%3D&key=a6088c6ea55d01fa0228c5724beeeb3f2fdce7ce4224e770d91be50a1db4d208606f050c9b15e8b8318c7402903fa69a1a14be5ad10eb6897953d2b851b570337e5578e6e5a0f0b716598c1fe28b5b638880dc4c8223c9c7bb3320c335af132d429a0ac35e179713d94b601b6712957e5b84d4670f6a4bbd3ad998283bedf2d4&pass_ticket=SqEP15c29I%2BCP7GT%2FuYzgfUQUSj9qvzzE4ymnKeG93etsnj78RSnYub3F8HP6t6p&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6307062c&__biz=MzIxNDA0MTExMg%3D%3D&appmsg_token=1187_ZLmkkgvPG%252FqSlwSflBux2JrENTqVBLqHy4bZwgBy3FZAUQLFNfJzTkye_4foWnPxyEH6yCfafl25wZPy&x5=0&f=json'


'''headersgz10_23 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_WtJpp4A7Y5r0kXYMv1jfQW3y0H4-pP19LrLojdQ3ndB7ZR2MsMnKk8CZW0JLY8-bdSIWzNKJzdnPXsfv; wap_sid2=CJ6N8I0EEooBeV9IRnp0T3RwZzROZzFLSU0xb0FGRUFWQmxjb2ZDZ25lb1RqN203bzBRM3Fic21JaHVKSzh5YUpUaFNDQ1lKYjIydElZNDk3VFhLb285LXNrRkhxSXJ2ZW03S2EwSHJUbE5qWGpEVEdHSnk1ajVLSDhuQV96aDhQMnRZR0Jlenp6aEs0SVNBQUF+MKeE1ZoGOA1AAQ=='
}
headersgz10_22 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_KICev6NdvXLjGwI%2Bli86V7kNVXhPBVseDTr9MZgT9raSiPJyUs7w2I3w7qEOCQgWppZ1RrVBGKscaxEs; wap_sid2=CJ6N8I0EEooBeV9ISlJ6dWlNVFFuZWI2OW5rMXBkU2dHMkJhM19IU1NDMWlmUXlNTVdJLXZoTkw2cEhJS19wS2FfWkVPdnYwWnBnenJ5UFVHT3Jud3hTS010UVRXQTIteGdoLVhNcXFYZXdsS2xuR2ptdnNzN3lWUmk5TWJEMDl5R015cFNTMjhhdTNvSVNBQUF+MKyE1ZoGOA1AAQ=='
}
headersgz10_21 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_hkzWj77%2Bo97pikOlY63XU069VAZIqOSxmKtLDIKHhE5jEYuIfZsAOS0GQNcGF0xo4FCxANIqe-iJHc-w; wap_sid2=CJ6N8I0EEooBeV9IT1BrbFJiXzhwOTFYY1lyZ1lzNmhvRmNEbklnWEJlQy1GTWlwcjBGSDV3eVlTS1pyNVNMd2VaLWtYMDhSOFlSMjVESUdTcHlOYnhSakx5U1lNQmY0RkoxaTJybzFMd016OTF1dE11VXFucUh4UzBsUTR4ZXJXYlJkbnNJbG5QdWNJSVNBQUF+MLeE1ZoGOA1AAQ=='
}
headersgz10_20 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_EIlzEv64Ogpp074XIB1zf_R-29Ethb4KlPPbUyAnkoz9F-vh9MvvnZdefUVnowesjEriG0iML9SFeOZw; wap_sid2=CJ6N8I0EEooBeV9IRzB0dWxsZGN0eWZRaHViNUdxUHFYbk43RGZQaHN5c3RjTXQzdTRGRmJMMTUwa1l3NFBjUG5remg3RHRGT0prOWRHaFZVeDJ2Qmh1QVV1SEdnUGNrUkRYeHptbllDU2h5UENEd0QzeWRQN1BEWVZIcjNWRDlfWmNVWFdONnJWUkQ0SVNBQUF+MK3/1JoGOA1AAQ=='
}
headersgz10_19 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_HpA1r1reusBb2DAwOFGGFZPEV1_9rmJ54LC3TAS21qDZfbF86MCkJpn1F9VFyH5o9n26m0aZYss1b56o; wap_sid2=CJ6N8I0EEooBeV9IRTRrcHVaNk5iZUVpUjFwZjNSTFBBMXhxTE9wQmIyWmE4TTdRWGE0RDR6aU4zc3dnRlhxeTN1cGxmMHNIREx4cjg5YUhTSEVOUVRrRXFGSEtLSkF0WVlxeVJMcklWWTB2SGFsQ1NIUVIzbzEzeHozemRvOXBvR1pWMDlfMDNHQUU0SVNBQUF+MMD/1JoGOA1AAQ=='
}
headersgz10_18 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_Ls5Q15jpOytfWUegUhKJ3WZ1eAsJIbKsTNslCh1TJrjAsc_0tMqIN2mY6PVdtB3EQcFTc9AJHPbYK625; wap_sid2=CJ6N8I0EEooBeV9ITnBPd2ZYQ05oRUZPOWN3bVdiQlhsMXJOQWtPaUYwaHhLeUNtRWZOSUFSZG5tMGQ0blJ1S2syRVRrS0VfaVJiTXlybFl0clgzNC1uY1hDdWx6bXlGMU1TdEZ2OWRieUdsWGZjM3BlWjBYWllDM0NGZElfRy1XY09GMmhnbFlTNHlJSVNBQUF+MMv/1JoGOA1AAQ=='
}
headersgz10_17 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_aldr89ajGcy29hwPSCAMn91LWQ2EtR3JlIuQVUhRhVYUHSWowZXJuZYS-9-PplEoPfEDggSa5Up2CXr6; wap_sid2=CJ6N8I0EEooBeV9IUGpqNlRLb2JlTkhXSmRiZnhLSGdKb1FOZHpxdGFxZFFhMWNiNlBzMmdSMlFCYnkxWUdOX1NuMm1kUHRIQS14OG1LbE1fYjdHNDkwM1dJdXRNNjRGY2RwdU1GLVZpRWZsVlJhcTFpd2ItMTdQcWJMY01rZUh5NG5fX1NNZTA0Sk9JSVNBQUF+MNT/1JoGOA1AAQ=='
}
headersgz10_16 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_qLitlrHLdWmjYOH4owH71LFAwmemwWPiaJRQj1E2sGwKVA0YgX_-CAK0abcuNjuJaOlhx0Srj9nrapRG; wap_sid2=CJ6N8I0EEooBeV9IRUtVaGI2T1h4NF94bElPQ0NxajVNeWtWRXp5cXBGbEx5M0Z2WnQ2UzB0ZDQ3alk3eXpaRGFIUjBROTFrQ1F0cG4xdEQ4WThERkFPZ3ptRm85SUoxUGp5eWpRQzVwVzlzbzhxbnNCRmN1eHhUMXliZ05Gdm5UM2Z5OGFCTnF3STJvSVNBQUF+MNz/1JoGOA1AAQ=='
}
headersgz10_15 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_SLAeQ2k8s3hoT%2BQkzABzPbD2q4gO6kZqGDC3THvqFtyy3vhjUqobY-T23xPVc0yV_0PNvd7eNMqgqnGD; wap_sid2=CJ6N8I0EEooBeV9IR1VyaFBuRXlRanBjY3JvSU5rV2FMWEktRzR1RHVxbUNXNkNlemN1aHl4VjMwelpMTGN2Z2pBbl9FVFNrWkFyay1sV08wU01wdmtaYlZYVTlEWXhVbGRzdVFoSFlzWG92cFUtaEUwYjVxNjFkTVJjSC1sSzJNcTRZUHctRDhIWVhvSVNBQUF+MOL/1JoGOA1AAQ=='
}
headersgz10_14 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_kKrTnmnYJWFgqfJ3LhgmF6AF4o1rSyVoKWbeCBhkh4zsmcspQM8SjOPWiFrLW6ZjqdBOzzCayPte2lIl; wap_sid2=CJ6N8I0EEooBeV9IRTU3bW1nTnhHanJkdFVwRmFhSkcyYWQyUXhFejlFZU81YklGUVJmZ2s3Si1PZE1UcWRsQzNIS1NtUFhINXBGYUR1b2RadEMwckdIUDBlZ2tvTTI5STBNdEYwS0pIc3g3UHVLMHNIa2pDbURzMDA3WlFNQXBZdUR4dnYybWZXZUlvSVNBQUF+MPr/1JoGOA1AAQ=='
}
'''
headerssz10_22={
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_QMGC0amtx%2FXS6sQeiyqOeUWzExnPOIcnGWQnm5eMJgirvW1iN4TD-MtHa2Ezwg6hGez5csTWzbVTTkJA; wap_sid2=CJ6N8I0EEooBeV9IRXRrNXpGTGJwaFp2RjNLTkNRSEZDdDd0R2NBeWtPR2UzQl82RGF1aGZSYUszeU4zZVdJWXlrb040UERST1VzQUtDZlZFV0dmT0p2aTFqTFo3Q3FlbElURjhCMWN2clhIbjBrcFV6TnFfV0djeTNkNWhvQTRrQ0lhTHhta194TkJZSVNBQUF+MMeJ1ZoGOA1AAQ=='
}
headerssz10_21={
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_PG%2BiNb0lZ9DzkvgkwEx0Ge44mC9T_JWg5IoY4FsInWb3D2lL8Lv_b6yBiJCQDvR0q1d06-t9e6gO8CEQ; wap_sid2=CJ6N8I0EEooBeV9IT1lZc1FyR1RxaFJtVGhhNmtISHM4OHo1b2tjZmdxSVBnQVY4UVB0REZpS1FFWmJaVnVUa1NSTmZrLXFnV0s0VHVVXy1aWUtJenVrT0VFVFdkeXotWjd3TzRLclNFZ0cyRjE4S2FiLXEtbWcxVTcyMGl2OUJYNnZpbjY0bnQ4WVpJSVNBQUF+MM2J1ZoGOA1AAQ=='
}
headerssz10_20 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_8D9y23FjrrOvvKy43sevVDEiDnTxdLfTCyvLOySl2gZpV1tjXyWkvl2qvbtQTPCxQ9a7JVKtWklduaV5; wap_sid2=CJ6N8I0EEooBeV9IUGNTejlMNTVUUC1fZ2h0UFRGcTg1TnlHYm1ZWTQzMFR3c04ybm5pamJ2X1I5Vk4zaGhXc0pYYU9VVm16VWhMczJZNGliVzV2anVMak9zLUpRUmw4Nk44a2tmOGNvcjFVOVRkbEwwSDFmVm4zT2RwUVo1UmFMOFZHQzk0UVhJdmFvSVNBQUF+MNiJ1ZoGOA1AAQ=='
}
headerssz10_19 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_YCT600ZycEnL3fY57RkqLC89mPIYqyi7otiKxbRM3Mx4lhmwiQTDoovkT-Ufi81TSK_g3ug1RlWE_yAG; wap_sid2=CJ6N8I0EEooBeV9ISC1malhObDZsNFo0cVJ0YjJYN1lVUHZaMlFaSDlBRndkd2NtamtseFRlMGpic3l0NENRaFJDZVYwN0dGMVpVNFBxUm5kbFBRRHNaSmsyYnZraThpSmpweTBsTTNIdFUxdWZ1Q050ZTRsUlFpUDZ4cWdDUWZqazI2eHdnQUFZMkVJSVNBQUF+MOKJ1ZoGOA1AAQ=='
}
headerssz10_18 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=mIwCMf5RaKgQZltez/0Mh50l5igQfq47us88xD0A1fpjvzA8AYVrqTlY9yUDhpGV; appmsg_token=1188_wZ7EU0XlIt3nTe6TLkHrUFM0b7HAaCQPwieG-pafIGU69vz5w74uPNCkbliYtxFrxYBBSzRkzxiYLNMj; wap_sid2=CJ6N8I0EEooBeV9ITDFFaUlLR2ZBV0ppNGVXQXFOR25fVnN3dXlxbld2NlJYcEZEUnZJRDNzT0NmS2pfOWdzY1N6eHFKR1c5cWlEMjRVUC1HR2ZGSl8wcmszT0xEMjJYTVdjb0xJMnJOeDdXZy05MHM4eGJITWtSc1I2VnIwMjdJMHhIMXJRRWNzZlZJSVNBQUF+MPSJ1ZoGOA1AAQ=='
}
headerssz10_17 = {
    'Cookie': 'appmsg_token=1187_AL6hNkKncUu6Rh4A1x93EGCgFFPGuXelAT7i4tUOzJX7Q3L07o7aajrDmvKmjGMzMfta3ib6IIRMoMys; rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=SqEP15c29I+CP7GT/uYzgfUQUSj9qvzzE4ymnKeG93etsnj78RSnYub3F8HP6t6p; wap_sid2=CJ6N8I0EEooBeV9IREM1dEdhcDRqcDFiMWJEd3JEV3o3YktCMFB2VWFTNVYzdXVCcmZ3Qk81QWhudThXRHBWYV9YdDBqckFISFZWUHVjODFBZ1hkR2g1ZDVhaldteHZuUGNnYUVBTUdWWERMMmNCRk02bUtWNUY0Q2lka1VFb19OMDczUWtFN0NmNlg0RVNBQUF+MMu9uJoGOA1AAQ=='
}
headerssz10_16 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=SqEP15c29I+CP7GT/uYzgfUQUSj9qvzzE4ymnKeG93etsnj78RSnYub3F8HP6t6p; appmsg_token=1187_YEHkGvTH86k0vMd0RlLN3tPtq2VBGdy2gkwFxwFpOuLexqLnNiCPGYKUnxu_kNUNOPpkSbhgULZL2g4p; wap_sid2=CJ6N8I0EEooBeV9ITkQyVDgtUktVS2hfT3YzOXA5N1FyODVqOE9CSzdCY0loTU9ueExVYXpuUTVTNkpxaDlIYlhCT3QwcFRhUVRFTjNseERzd1gxdkYzemNWVjliZWJMbHloUmRnNTlIQzVLazRJMVdEYnV0NG5lNmZzemJBNnp0X3B1R2RNbkMwTE1ZRVNBQUF+MMi+uJoGOA1AAQ=='
}
headerssz10_15 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=SqEP15c29I+CP7GT/uYzgfUQUSj9qvzzE4ymnKeG93etsnj78RSnYub3F8HP6t6p; appmsg_token=1187_WzRYLk%2BqdL2QpINnOjRzZuoEiG_PLpVnVG_PbdscWOuy8-qqTs8iCCLQqb0ufuM8BBSjBBsFZeTAFgej; wap_sid2=CJ6N8I0EEooBeV9ISTBlZDNPNG43eWdianB6MlBuTmFqbjZCTTNHNUYtMjZvQXhKc2I1eWxTZ0Z4MHZ1Q3VBMTNwSVdCYkV6RzZpTHdxQy10SjdnTkIyMmNUUm9GbENvUEtHd2FlbEFZWUpsTTNFa19lX29CNXMwSGZTcDZrSC1vOXg0UkRFSFpNUTJZRVNBQUF+MPm/uJoGOA1AAQ=='
}
headerssz10_14 = {
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1102841502; devicetype=Windows10x64; version=6307062c; lang=zh_CN; pass_ticket=SqEP15c29I+CP7GT/uYzgfUQUSj9qvzzE4ymnKeG93etsnj78RSnYub3F8HP6t6p; appmsg_token=1187_ZLmkkgvPG%2FqSlwSflBux2JrENTqVBLqHy4bZwgBy3FZAUQLFNfJzTkye_4foWnPxyEH6yCfafl25wZPy; wap_sid2=CJ6N8I0EEooBeV9IQzVMclc2VHgteko2dTNsODhlU1Q2Y1FpS0JaNTRBbEY5QTIyc3g4MW5ZOUlNemg2TEY3TlFyQ1pDVHdNRjNyYmlhXzFHbXRUNVM1QU1PdVNudDBpSkJDUklhMTNEVGNSOWRnTjZpTno4dkgyeDhyMVhWeF9YMWRwNkV5aEhkMjk0RVNBQUF+MLXBuJoGOA1AAQ=='
}


#发送请求，获得json文件
def get_comment_json(url,headers,date,city):
    response = requests.get(url=url,headers=headers)
    content = response.json()
    fp = open('comment_json_sz/comment'+city+date+'.json','w',encoding='utf-8')
    json.dump(content,fp,ensure_ascii=False)
    fp.close()
    print(content['elected_comment'])

def get_wc():

    # 获取文件夹中全部评论json文件的路径
    dir_list = os.listdir('comment_json_sz')
    list_back = []

    for file in dir_list:
        path = os.path.join('comment_json_sz', file)

        # 判断是否存在.json文件，如果存在则获取路径信息中的日期写入到list_date中
        if os.path.splitext(path)[1] == '.json':
            json_file = os.path.join('comment_json_sz', file)
            list_back.append(json_file[-12:-5])

    # 将所有评论整理成一个经过结巴分词的字符串
    all_comment = ''

    for back in list_back:
        content = json.load(open('comment_json_sz/comment'+back+'.json','r',encoding='utf-8'))
        for comment in content['elected_comment']:
            if comment["nick_name"] != "HLP" and comment["nick_name"] != "bocan." and comment["nick_name"] != \
                    "AAA (不传销，不推销)" and comment["nick_name"] != "Chen." and comment["nick_name"] != "PJL" \
                    and comment["nick_name"] != "黄斌" :
                all_comment += comment['content']

    with open('stopwords.txt','r+',encoding='utf-8') as fp:   #打开停用词词典
        stopwords = fp.read().split('\n')

    word_dict = {}
    jieba.load_userdict('自定义词典.txt')
    word_list = jieba.cut(all_comment,cut_all=True,HMM=True)  #全分词，识别新词
    for word in word_list:
        if word not in stopwords:
            if word in word_dict.keys():
                word_dict[word] += 1
            else:
                word_dict[word] = 1
    comment_pair = [(word,word_dict[word]) for word in word_dict.keys()]
    # print(comment_pair)

    #生成并储存词云图
    w=wordcloud.WordCloud(width=2000,height=1400,
    font_path="msyh.ttc",colormap='winter',
    background_color='white')
    w.generate(word_list)
    w.to_file('深圳卫健委评论区词云图.png')

    return comment_pair


if __name__ == '__main__':
    # 测试时，请分步执行以下两个操作！

    # step1：获取评论区json文件
    #url_list = [urlsz10_14,urlsz10_15,urlsz10_16,urlsz10_17,urlsz10_18,urlsz10_19,urlsz10_20,urlsz10_21,urlsz10_22,urlsz10_23]
    #headers_list = [headerssz10_14,headerssz10_15,headerssz10_16,headerssz10_17,headerssz10_18,headerssz10_19,headerssz10_20,headerssz10_21,headerssz10_22,headerssz10_23]
    url_list = [urlsz10_18,urlsz10_19,urlsz10_20,urlsz10_21,urlsz10_22]
    headers_list = [headerssz10_18,headerssz10_19,headerssz10_20,headerssz10_21,headerssz10_22]

    '''date = 18
    for i in range(len(url_list)):
        get_comment_json(url_list[i],headers_list[i],'10_'+str(date),'gz')
        date+=1'''

    # step2:生成词云图
    get_wc()
