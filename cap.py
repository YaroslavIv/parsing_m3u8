import os
import grequests
from typing import List

class Cap:
    def __init__(self, cap: List[str], folder_ts: str) -> None:
        self.cap = cap
        self.folder_ts = folder_ts

    def write(self, content: bytes, name: str) -> None:
        with open(f"{name}.ts", 'wb') as f:
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