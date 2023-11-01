import os
import grequests
from typing import List
import requests

class Cap:
    def __init__(self, cap: List[str], folder_ts: str) -> None:
        self.cap = cap
        self.folder_ts = folder_ts

    def write(self, content: bytes, name: str, extension: str = '.ts') -> None:
        with open(f"{name}.{extension}", 'wb') as f:
            #print(type(content))
            f.write(content)
    
    def switch(self, name) -> None:
        self.name = name
        match name:
            case "yar_net":
                self.yar_net()
            case "sochi":
                self.sochi()
            case "tver":
                self.tver()
            case "podryad":
                self.podryad()
            case "krk":
                self.krk()
            case "stream_is74":
                self.stream_is74()
            case "lipetsk":
                self.lipetsk()
            case "cam_74":
                self.cam_74()
            case "baikal":
                self.default()
            case "511wi":
                self.wi511()
            case "murmansk":
                self.default()
            case "transport_nov":
                self.default(-2)
            case "pskov":
                self.default()
            case "ladamedia":
                self.default(-2)
            case "gorodcamer":
                self.default(-2)
            case "ul":
                self.default(-2)
            case "mass511":
                self.mass511()
            case "la511":
                self.la511()
            case "canlimobase":
                self.canlimobase()
            case "nvroads":
                self.nvroads()
            case "gits_gg":
                self.gits_gg()
            case "spatic":
                self.spatic()
            case "autoroutes":
                self.autoroutes()
            case "livetrafficuk":
                self.livetrafficuk()
            case "autostrate":
                self.autostrade()
            case 'dsat':
                self.dsat()
            case _:
                raise ValueError(f'error cap: {name}')
    
    def yar_net(self) -> None:
        for name in self.cap:
            os.makedirs(os.path.join(self.name, self.folder_ts, name), exist_ok=True)
            mono_url = grequests.map(
                [grequests.get(f'https://yar-net.ru/api/site/cams/stream?url={name}')])[0].text
            x = grequests.map([grequests.get(mono_url)])

            if x[0] is None:
                print(f'ERROR: {name}')
                continue

            x = x[0].text.split('\n')
            mono_list = [y for y in x if y[:1] != '#' and len(y) > 0]

            rs = []
            for url in mono_list:
                u = f"{mono_url.split('/mono.m3u8')[0]}/{url}"
                rs.append(grequests.get(u))

            out = grequests.map(rs)
            for i, url in enumerate(mono_list):
                x = out[i]
                if x.status_code == 200:
                    self.write(x.content, os.path.join(
                        self.name, self.folder_ts, name, url.split('.ts')[0].replace('/', '_')))
                else:
                    print(f'error: {url}')
            print(name)

    def sochi(self) -> None:
        for name in self.cap:
            os.makedirs(os.path.join(self.name, self.folder_ts, name), exist_ok=True)
            url = f'https://sochi.camera/vse-kamery/{name}/?format=json'
            out = grequests.map([grequests.get(url)])[0].json()
            video_url = out['video_url']
            out = grequests.map([grequests.get(video_url)])[0]
            if out is None:
                print(f'ERROR: {name}')
                return
            if out.status_code != 200:
                return
            out = out.text.split('\n')
            mono_list = [y for y in out if y[:1] != '#' and len(y) > 0]

            rs = []
            for url in mono_list:
                suffix = url.split('/')[0]
                rs.append(grequests.get(os.path.join(
                    video_url.split('index')[0], url)))
            outs = grequests.map(rs)

            rs = []
            url_lists = []
            for i, url in enumerate(mono_list):
                out = outs[i]
                if out is None:
                    continue
                if out.status_code != 200:
                    continue
                out = out.text.split('\n')
                url_list = [y for y in out if y[:1] != '#' and len(y) > 0]
                url_lists += url_list
                for url in url_list:
                    rs.append(grequests.get(
                        f"{video_url.split('index')[0]}{suffix}/{url}", verify=False))
            outs = grequests.map(rs)
            for i, url in enumerate(url_lists):
                out = outs[i]
                if out.status_code == 200:
                    self.write(out.content, os.path.join(
                        self.name, self.folder_ts, name, url.split('.ts')[0].replace('/', '_')))
                else:
                    print(f'error: {url}')
            print(name)

    def tver(self) -> None:
        for name in self.cap:
            os.makedirs(os.path.join(self.name, self.folder_ts, name), exist_ok=True)
            url = f'https://video.adm.tver.ru/cameras/{name}/streaming/main.m3u8?authorization=Basic%20d2ViOndlYg%3D%3D'
            mono_url = grequests.map([grequests.get(url)])
            if mono_url[0] is None:
                return
            out = mono_url[0].text.split('\n')
            mono_list = [y for y in out if y[:1] != '#' and len(y) > 0]
            print(mono_list)

            rs = []
            for suffix in mono_list:
                url = f'https://video.adm.tver.ru/cameras/{name}/streaming/{suffix}'
                rs.append(grequests.get(url))
            out = grequests.map(rs)

            for i, suffix in enumerate(mono_list):
                if out[i].status_code == 200:
                    self.write(out[i].content, os.path.join(
                        self.name, self.folder_ts, name, suffix.split('.ts')[0].replace('/', '_')))
                else:
                    print(f'error: {suffix}')
            print(name)

    def podryad(self) -> None:
        for name in self.cap:
            os.makedirs(os.path.join(self.name, self.folder_ts, name), exist_ok=True)
            url = f'https://flussonic0.podryad.net/{name}/tracks-v1/index.fmp4.m3u8?token=2.5rQkkFyJAAEABZPIp7NVRtaxK7n2qq6SCNeogeEF3qg0AQjQ'
            mono_url = grequests.map([grequests.get(url)])
            if mono_url[0] is None:
                return
            out = mono_url[0].text.split('\n')
            mono_list = [y for y in out if y[:1] != '#' and len(y) > 0]

            http = f'https://flussonic0.podryad.net/{name}/tracks-v1/'
            rs = []
            for url in mono_list:
                rs.append(grequests.get(http+url))
            out = grequests.map(rs)

            for i, suffix in enumerate(mono_list):
                if out[i].status_code == 200:
                    self.write(out[i].content, os.path.join(
                        self.name, self.folder_ts, name, suffix.split('.hls.fmp4')[0].replace('/', '_')))
                else:
                    print(f'error: {suffix}')
            print(name)

    def krk(self) -> None:
        for name in self.cap:
            os.makedirs(os.path.join(self.name, self.folder_ts, name), exist_ok=True)
            url = f'http://fluserver.orionnet.online/{name}/tracks-v1/mono.m3u8'
            mono_url = grequests.map([grequests.get(url)])
            if mono_url[0] is None:
                return
            out = mono_url[0].text.split('\n')
            mono_list = [y for y in out if y[:1] != '#' and len(y) > 0]

            http = f'http://fluserver.orionnet.online/{name}/tracks-v1/'
            rs = []
            for url in mono_list:
                rs.append(grequests.get(http+url))
            out = grequests.map(rs)

            for i, suffix in enumerate(mono_list):
                if not out[i] is None and out[i].status_code == 200:
                    self.write(out[i].content, os.path.join(
                        self.name, self.folder_ts, name, suffix.split('.ts')[0].replace('/', '_')))
                else:
                    print(f'error: {suffix}')
            print(name)

    def stream_is74(self) -> None:
        for name in self.cap:
            os.makedirs(os.path.join(self.name, self.folder_ts, name), exist_ok=True)
            url = f'https://cdn.cams.is74.ru/hls/playlists/ts.m3u8?quality=main&uuid={name}'
            mono_url = grequests.map([grequests.get(url)])
            if mono_url[0] is None:
                return
            out = mono_url[0].text.split('\n')
            mono_list = [y for y in out if y[:1] != '#' and len(y) > 0]

            http = f'https://cdn.cams.is74.ru/'
            rs = []
            for url in mono_list:
                rs.append(grequests.get(http+url))
            out = grequests.map(rs)

            for i, suffix in enumerate(mono_list):
                if not out[i] is None and out[i].status_code == 200:
                    self.write(out[i].content, os.path.join(
                        self.name, self.folder_ts, name, suffix.split('.ts')[0].replace('/', '_')))
                else:
                    print(f'error: {suffix}')
            print(name)
    
    def lipetsk(self) -> None:
        for name in self.cap:
            id, name = name.split('_')
            os.makedirs(os.path.join(self.name, self.folder_ts, f'{id}_{name}'), exist_ok=True)
            mono_url = grequests.map(
                [grequests.get(f'https://camera.lipetsk.ru/{id}.camera.lipetsk.ru/live/{name}/playlist.m3u8')])

            if mono_url[0] is None:
                print(f'ERROR: {name}')
                continue

            x = mono_url[0].text.split('\n')
            mono_list = [y for y in x if y[:1] != '#' and len(y) > 0]

            rs = []
            for url in mono_list:
                rs.append(grequests.get(f'https://camera.lipetsk.ru/{id}.camera.lipetsk.ru/live/{name}/{url}'))

            out = grequests.map(rs)
            for i, url in enumerate(mono_list):
                x = out[i]
                if x.status_code == 200:
                    self.write(x.content, os.path.join(
                        self.name, self.folder_ts, f'{id}_{name}', url.split('.ts')[0].replace('/', '_')))
                else:
                    print(f'error: {url}')
            print(name)

    def mass511(self) -> None:
        for name in self.cap:
            os.makedirs(os.path.join(self.name.replace(".", ""), self.folder_ts, name[0]), exist_ok=True)
            url = f'https://restream-5.trafficland.com/live/{name[0]}/{name[1]}'
            print(url)
            mono_url = grequests.map([grequests.get(url)])
            if mono_url[0] is None:
                return
            out = mono_url[0].text.split('\n')
            mono_list = [y for y in out if y[:1] != '#' and len(y) > 0]
            print(mono_url[0].status_code)
            rs = []
            for suffix in mono_list:
                url = f'https://restream-5.trafficland.com/live/{name[0]}/{suffix}'
                rs.append(grequests.get(url))
            out = grequests.map(rs)

            for i, suffix in enumerate(mono_list):
                print(out[i].status_code)
                if out[i].status_code == 200:
                    print(os.path.join(
                        self.name, self.folder_ts, name[0], suffix.split('.ts')[0].replace('/', '_')))
                    self.write(out[i].content, os.path.join(
                        self.name, self.folder_ts, name[0], suffix.split('.ts')[0].replace('/', '_')))
                else:
                    print(f'error: {suffix}')
            print(name)
    def gits_gg(self) -> None:
        token = 'playlist.m3u8?wmsAuthSign=c2VydmVyX3RpbWU9MTAvNS8yMDIzIDExOjU4OjE2IEFNJmhhc2hfdmFsdWU9d2pmbzNxelA5TzJlWVI4SFpKUW1Pdz09JnZhbGlkbWludXRlcz0xMjA=' #token says: "pls update me before up the application("
        for name in self.cap:
            os.makedirs(os.path.join(self.name, self.folder_ts, name[0].replace("/", "_")), exist_ok=True)
            mono_url1 = grequests.map(
                [grequests.get(f'https://gitsview.gg.go.kr:8082/{name[0]}/{token}')])
            x1 = mono_url1[0].text.split('\n')
            mono_list1 = [y for y in x1 if y[:1] != '#' and len(y) > 0]
            if mono_url1[0] is None:
                print(f'ERROR1: {name}')
                continue
            try:
                mono_url = grequests.map(
                    [grequests.get(f'https://gitsview.gg.go.kr:8082/{name[0]}/{mono_list1[0]}')])
            except Exception:
                continue

            if mono_url[0] is None:
                print(f'ERROR2: {name}')
                continue
            x = mono_url[0].text.split('\n')
            mono_list = [y for y in x if y[:1] != '#' and len(y) > 0]

            rs = []
            for url in mono_list:
                rs.append(grequests.get(f'https://gitsview.gg.go.kr:8082/{name[0]}/{url}'))

            out = grequests.map(rs)
            try:
                for i, url in enumerate(mono_list):
                    x = out[i]
                    if x.status_code == 200:
                        st = os.path.join(
                            self.name, self.folder_ts, name[0].replace("/", "_"), url.replace('/', '_').replace('.ts', '')).find('?')
                        self.write(x.content, os.path.join(
                            self.name, self.folder_ts, name[0].replace("/", "_"), url.replace('/', '_').replace('.ts', ''))[:st])
                    else:
                        print(f'error: {url}')
                        print('pls update token')
                        token = input()
            except Exception:
                continue
            print(name)

    def la511(self) -> None:
        for name in self.cap:
            ccv = 'itsstreamingbr2'
            os.makedirs(os.path.join(self.name, self.folder_ts, name.replace("/", "_")), exist_ok=True)
            mono_url1 = grequests.map(
                [grequests.get(f'https://{ccv}.dotd.la.gov/public/{name}/playlist.m3u8')])
            x1 = mono_url1[0].text.split('\n')
            mono_list1 = [y for y in x1 if y[:1] != '#' and len(y) > 0]
            if mono_url1[0] is None:
                ccv = 'itsstreamingbr2'
                os.makedirs(os.path.join(self.name, self.folder_ts, name.replace("/", "_")), exist_ok=True)
                mono_url1 = grequests.map(
                    [grequests.get(f'https://{ccv}.dotd.la.gov/public/{name}/playlist.m3u8')])
                x1 = mono_url1[0].text.split('\n')
                mono_list1 = [y for y in x1 if y[:1] != '#' and len(y) > 0]
                if mono_url1[0] is None:
                    ccv = 'itsstreamingno'
                    os.makedirs(os.path.join(self.name, self.folder_ts, name.replace("/", "_")), exist_ok=True)
                    mono_url1 = grequests.map(
                        [grequests.get(f'https://{ccv}.dotd.la.gov/public/{name}/playlist.m3u8')])
                    x1 = mono_url1[0].text.split('\n')
                    mono_list1 = [y for y in x1 if y[:1] != '#' and len(y) > 0]
                    if mono_url1[0] is None:
                        print(f'ERROR1: {name}')
                        continue
            try:
                mono_url = grequests.map(
                    [grequests.get(f'https://{ccv}.dotd.la.gov/public/{name}/{mono_list1[0]}')])
            except Exception:
                continue

            if mono_url[0] is None:
                print(f'ERROR2: {name}')
                continue
            x = mono_url[0].text.split('\n')
            mono_list = [y for y in x if y[:1] != '#' and len(y) > 0]

            rs = []
            for url in mono_list:
                rs.append(grequests.get(f'https://{ccv}.dotd.la.gov/public/{name}/{url}'))

            out = grequests.map(rs)
            try:
                for i, url in enumerate(mono_list):
                    x = out[i]
                    if x.status_code == 200:
                        self.write(x.content, os.path.join(
                            self.name, self.folder_ts, name.replace("/", "_"), url.replace('/', '_').replace('.ts', '')))
                    else:
                        print(f'error: {url}')
            except Exception:
                continue
            print(name)
            
    def wi511(self) -> None:
        for name in self.cap:
            ccv = 'cctv1'
            os.makedirs(os.path.join(self.name, self.folder_ts, name.replace("/", "_")), exist_ok=True)
            mono_url1 = grequests.map(
                [grequests.get(f'https://{ccv}.dot.wi.gov/rtplive/{name}/playlist.m3u8')])
            x1 = mono_url1[0].text.split('\n')
            mono_list1 = [y for y in x1 if y[:1] != '#' and len(y) > 0]
            if mono_url1[0].status_code==404:
                try:
                    ccv = 'cctv2' if ccv=='cctv1' else 'cctv1'
                    mono_url1 = grequests.map(
                        [grequests.get(f'https://{ccv}.dot.wi.gov/rtplive/{name}/playlist.m3u8')])
                    x1 = mono_url1[0].text.split('\n')
                    mono_list1 = [y for y in x1 if y[:1] != '#' and len(y) > 0]
                    if mono_url1[0].status_code==404:
                        print(f'ERROR1: https://{ccv}.dot.wi.gov/rtplive/{name}/playlist.m3u8')
                        continue
                except Exception:
                    continue
            try:
                mono_url = grequests.map(
                    [grequests.get(f'https://{ccv}.dot.wi.gov/rtplive/{name}/{mono_list1[0]}')])
            except Exception as e:
                print(mono_url1[0])
                continue

            if mono_url[0] is None:
                print(f'ERROR2: {name}')
                continue
            x = mono_url[0].text.split('\n')
            mono_list = [y for y in x if y[:1] != '#' and len(y) > 0]

            rs = []
            for url in mono_list:
                rs.append(grequests.get(f'https://{ccv}.dot.wi.gov/rtplive/{name}/{url}'))

            out = grequests.map(rs)
            try:
                for i, url in enumerate(mono_list):
                    x = out[i]
                    if x.status_code == 200:
                        self.write(x.content, os.path.join(
                            self.name, self.folder_ts, name.replace("/", "_"), url.replace('/', '_').replace('.ts', '')))
                    else:
                        print(f'error: {url}')
            except Exception:
                continue
            print(name)
    def canlimobase(self) -> None:

        for name in self.cap:
            os.makedirs(os.path.join(self.name.replace(".", ""), self.folder_ts, name[0].replace("/", "")), exist_ok=True)
            url = f'https://hls.ibb.gov.tr/{name[0]}/chunklist.m3u8'
            print(url)
            mono_url = requests.get(url, verify=False)
            if mono_url is None:
                continue
            out = mono_url.text.split('\n')
            mono_list = [y for y in out if y[:1] != '#' and len(y) > 0]
            print(mono_url.status_code)
            rs = []
            for suffix in mono_list:
                url = f'https://hls.ibb.gov.tr/{name[0]}/{suffix}'
                rs.append(requests.get(url, verify=False))

            for i, suffix in enumerate(mono_list):
                print(suffix)
                if rs[i].status_code == 200:
                    print(os.path.join(
                        self.name, self.folder_ts, name[0].replace("/", ""), suffix.replace('.ts', '').replace('/', '_')))
                    self.write(rs[i].content, os.path.join(
                        self.name, self.folder_ts, name[0].replace("/", ""), suffix.replace('.ts', '').replace('/', '_')))
                else:
                    print(f'error: {suffix}')
            print(name)
    def autostrade(self) -> None:

        for name in self.cap:
            os.makedirs(os.path.join(self.name.replace(".", ""), self.folder_ts, name[0][0:11].replace("/", "")), exist_ok=True)
            url = f'https://video.autostrade.it/video-mp4_hq/{name[0]}'
            print(url)
            rs = requests.get(url)
            print(rs.content)

            if rs.status_code == 200:
                print(os.path.join(
                    self.name, self.folder_ts, name[0][0:11].replace("/", ""), 'video'))
                self.write(rs.content, os.path.join(
                    self.name, self.folder_ts, name[0][0:11].replace("/", ""), 'video'))
            else:
                print(f'error: {suffix}')
            print(name)

    def dsat(self) -> None:
        for name in self.cap:
            os.makedirs(os.path.join(self.name, self.folder_ts, name.replace('m3u8', "")), exist_ok=True)
            url = f'https://streaming1.dsatmacau.com/traffic/{name}'
            mono_url = grequests.map([grequests.get(url)])
            if mono_url[0] is None:
                return
            out = mono_url[0].text.split('\n')
            mono_list = [y for y in out if y[:1] != '#' and len(y) > 0]
            print(mono_list)

            rs = []
            for suffix in mono_list:
                url = f'https://streaming1.dsatmacau.com/traffic/{suffix}'
                rs.append(grequests.get(url))
            out = grequests.map(rs)

            for i, suffix in enumerate(mono_list):
                if out[i].status_code == 200:
                    self.write(out[i].content, os.path.join(
                        self.name, self.folder_ts, name.replace('m3u8', ""), suffix.split('.ts')[0].replace('/', '_')))
                else:
                    print(f'error: {suffix}')
            print(name)

    def livetrafficuk(self) -> None:

        for name in self.cap:
            os.makedirs(os.path.join(self.name.replace(".", ""), self.folder_ts, name[0][0:11].replace("/", "")), exist_ok=True)
            url = f'https://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/{name[0]}'
            print(url)
            rs = requests.get(url)
            print(rs.content)

            if rs.status_code == 200:
                print(os.path.join(
                    self.name, self.folder_ts, name[0][0:11].replace("/", ""), 'video'))
                self.write(rs.content, os.path.join(
                    self.name, self.folder_ts, name[0][0:11].replace("/", ""), 'video'))
            else:
                print(f'error: {suffix}')
            print(name)
    def nvroads(self) -> None:

        for name in self.cap:
            os.makedirs(os.path.join(self.name, self.folder_ts, name.replace("/", "_")), exist_ok=True)
            base_url = 'https://d2wse.its.nv.gov/'
            if name.startswith('ve'):
                base_url = 'https://d1wse2.its.nv.gov/'
            elif name.startswith('el'):
                base_url = 'https://d3wse.its.nv.gov/'
            mono_url1 = grequests.map(
                [grequests.get(f'{base_url}/{name}/playlist.m3u8')])
            x1 = mono_url1[0].text.split('\n')
            mono_list1 = [y for y in x1 if y[:1] != '#' and len(y) > 0]
            print(mono_list1)
            print(mono_url1[0].content)
            if mono_url1[0] is None:
                print(f'ERROR1: {name}')
                continue
            try:
                mono_url = grequests.map(
                    [grequests.get(f'{base_url}/{name}/{mono_list1[0]}')])
            except Exception as e:
                print(f'{base_url}/{name}/playlist.m3u8')
                print(mono_url1)
                continue

            if mono_url[0] is None:
                print(f'ERROR2: {name}')
                continue
            x = mono_url[0].text.split('\n')
            mono_list = [y for y in x if y[:1] != '#' and len(y) > 0]

            rs = []
            for url in mono_list:
                rs.append(grequests.get(f'{base_url}/{name}/{url}'))

            out = grequests.map(rs)
            try:
                for i, url in enumerate(mono_list):
                    x = out[i]
                    if x.status_code == 200:
                        print('excellent' + url)
                        self.write(x.content, os.path.join(
                            self.name, self.folder_ts, name.replace("/", "_"), url.replace('/', '_').replace('.ts', '')))
                    else:
                        print(f'error: {url}')
            except Exception as ee:
                print(ee)
                print('ee')
                continue
            print(name)

    def cam_74(self) -> None:
        for name in self.cap:
            os.makedirs(os.path.join(self.name, self.folder_ts, name), exist_ok=True)
            mono_url = grequests.map(
                [grequests.get(f'https://streams.cam72.su/1500-{name}/tracks-v1/index.fmp4.m3u8?token=1787711287')])

            if mono_url[0] is None:
                print(f'ERROR: {name}')
                continue

            x = mono_url[0].text.split('\n')
            mono_list = [y for y in x if y[:1] != '#' and len(y) > 0]

            rs = []
            for url in mono_list:
                rs.append(grequests.get(f'https://streams.cam72.su/1500-{name}/tracks-v1/{url}'))

            out = grequests.map(rs)
            for i, url in enumerate(mono_list):
                x = out[i]
                if x.status_code == 200:
                    self.write(x.content, os.path.join(
                        self.name, self.folder_ts, name, url.split('.hls')[0].replace('/', '_')))
                else:
                    print(f'error: {url}')
            print(name)
    def spatic(self) -> None:
        for name1 in range(130, 260):
            name = str(name1)
            os.makedirs(os.path.join(self.name, self.folder_ts, name+'.stream'), exist_ok=True)
            mono_url1 = grequests.map(
                [grequests.get(f'https://strm2.spatic.go.kr/live/{name}.stream/playlist.m3u8')])
            x1 = mono_url1[0].text.split('\n')
            mono_list1 = [y for y in x1 if y[:1] != '#' and len(y) > 0]
            if mono_url1[0] is None:
                print(f'ERROR: {name}')
                continue
            try:
                mono_url = grequests.map(
                    [grequests.get(f'https://strm2.spatic.go.kr/live/{name}.stream/{mono_list1[0]}')])
            except Exception:
                print('false: ' + name)
                continue

            if mono_url[0] is None:
                print(f'ERROR: {name}')
                continue
            x = mono_url[0].text.split('\n')
            mono_list = [y for y in x if y[:1] != '#' and len(y) > 0]

            rs = []
            for url in mono_list:
                rs.append(grequests.get(f'https://strm2.spatic.go.kr/live/{name}.stream/{url}'))

            out = grequests.map(rs)
            for i, url in enumerate(mono_list):
                x = out[i]
                if x.status_code == 200:
                    print(name + ' excellent')
                    self.write(x.content, os.path.join(
                        self.name, self.folder_ts, name+'.stream', url.replace('/', '_').replace('.ts', '')))
                else:
                    print(f'error: {url}')
            print(name)

    def default(self, n=-3) -> None:
        for list_link in self.cap:
            name = list_link[0].split('/')[n]
            os.makedirs(os.path.join(self.name, self.folder_ts, name), exist_ok=True)
            mono_url = grequests.map(
                [grequests.get(list_link[0], verify=False)])

            if mono_url[0] is None:
                print(f'ERROR: {name}')
                continue

            x = mono_url[0].text.split('\n')
            mono_list = [y for y in x if y[:1] != '#' and len(y) > 0]

            rs = []
            for url in mono_list:
                url = url.replace('\r', '') 
                rs.append(grequests.get(list_link[1].format(url), verify=False))

            out = grequests.map(rs)
            for i, url in enumerate(mono_list):
                x = out[i]
                if x.status_code == 200:
                    self.write(x.content, os.path.join(
                        self.name, self.folder_ts, name, url.split('.ts')[0].replace('/', '_')))
                else:
                    print(f'error: {url}')
            print(name)