import os
import cv2
import json
from shutil import copyfile
from typing import List
from config import read_config
from view_imgs import Manager
from cap import Cap


class Logic:
    def __init__(self, path_config: str) -> None:
        self.update(path_config)
        self.folder_ts = 'ts'
        self.folder_view = 'view'
        self.folder_check = 'check'
        self.folder_img = 'img'
        self.folder_config = 'config'
        self.cap = Cap(self.config.cap, self.folder_ts)

    def update(self, path_config: str) -> None:
        self.config = read_config(path_config)

    def name(self) -> str:
        return self.config.name

    def start(self) -> None:
        self.cap.switch(self.config.name)

    def video_to_img(self) -> None:
        folders = os.listdir(os.path.join(self.config.name, self.folder_ts))
        os.makedirs(os.path.join(self.config.name,
                    self.folder_view), exist_ok=True)
        for folder in folders:
            videos = os.listdir(os.path.join(
                self.config.name, self.folder_ts, folder))
            if len(videos) == 0:
                continue
            video = videos[0]
            video_path = os.path.join(
                self.config.name, self.folder_ts, folder, video)
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Cannot open camera: {video_path}")
                continue

            ret, frame = cap.read()
            if not ret:
                continue
            cv2.imwrite(os.path.join(os.path.join(self.config.name,
                        self.folder_view), f'{folder}.jpg'), frame)

    def view_imgs(self, size: List[int]) -> None:

        m = Manager(os.path.join(self.config.name, self.folder_view), os.path.join(
            self.config.name, self.folder_view), self.config.name, size)
        m.bind()
        m.show()
        m.start()

    def videos_to_imgs(self) -> None:
        if not os.path.isdir(self.config.name):
            raise ValueError(f"not find dir: {self.config.name}")

        view_config = os.path.join(
            self.config.name, self.folder_view, f'{self.config.name}.json')
        if os.path.isfile(view_config):
            with open(view_config, 'r') as f:
                view_config = json.load(f)['correct']

        os.makedirs(os.path.join(self.config.name,
                    self.folder_check), exist_ok=True)

        N = 30
        for folder in os.listdir(os.path.join(self.config.name, self.folder_ts)):
            if isinstance(view_config, list) and not folder in view_config:
                continue

            os.makedirs(os.path.join(self.config.name,
                        self.folder_check, folder), exist_ok=True)

            i = 0
            j = 0
            for video in os.listdir(os.path.join(self.config.name, self.folder_ts, folder)):
                if video[-3:] != '.ts':
                    continue
                video_path = os.path.join(
                    self.config.name, self.folder_ts, folder, video)
                cap = cv2.VideoCapture(video_path)
                if not cap.isOpened():
                    print(f"Cannot open camera: {video_path}")
                    continue

                while True:
                    ret, frame = cap.read()

                    if not ret:
                        break

                    i += 1

                    if i % N == 0:
                        j += 1
                        cv2.imwrite(os.path.join(
                            self.config.name, self.folder_check, folder, f'{video[:-3]}_{str(j).zfill(5)}.jpg'), frame)

                cap.release()
            print(folder)

    def check_imgs(self) -> None:
        if not os.path.isdir(os.path.join(self.config.name, self.folder_check)):
            raise ValueError(
                f"not find dir: {os.path.join(self.config.name, self.folder_check)}")

        out = {}
        K = 40_000
        for folder in os.listdir(os.path.join(self.config.name, self.folder_check)):
            if os.path.isdir(os.path.join(self.config.name, self.folder_check, folder)):
                out[folder] = []
                algo = cv2.createBackgroundSubtractorMOG2()
                decline = 0
                for img in os.listdir(os.path.join(self.config.name, self.folder_check, folder)):
                    frame = cv2.imread(os.path.join(
                        self.config.name, self.folder_check, folder, img))
                    frame = cv2.resize(frame, (544, 320))
                    fgMask = algo.apply(frame)
                    fgMask = cv2.medianBlur(fgMask, 3)

                    if fgMask.sum() >= K:
                        out[folder].append(img)
                    else:
                        decline += 1
            print(f'{folder}, decline: {decline}')

        with open(os.path.join(self.config.name, self.folder_check, f'{self.config.name}.json'), 'w') as f:
            json.dump(out, f)

    def copy_check_imgs(self) -> None:
        path_check = os.path.join(self.config.name, self.folder_check, f'{self.config.name}.json')
        src = os.path.join(self.config.name, self.folder_check)
        dst = os.path.join(self.config.name, self.folder_img)

        if not os.path.isfile(path_check):
            raise ValueError(f'not find path_check: {path_check}')

        if not os.path.isdir(src):
            raise ValueError(f'not find src: {src}')

        with open(path_check, 'r') as f:
            check = json.load(f)

        os.makedirs(dst, exist_ok=True)
        for folder in check:
            for img in check[folder]:
                copyfile(
                    os.path.join(src, folder, img),
                    os.path.join(dst, f'{folder}_{img}')
                )
            print(folder)

    def new_json(self) -> None:
        src = os.path.join(self.config.name, self.folder_view, f'{self.config.name}.json')
        dst = os.path.join(self.folder_config, f'{self.config.name}.json')

        if not os.path.isfile(src):
            raise ValueError(f"not find file: {src}")

        copyfile(src, dst)
    
    def run(self, size: List[int]) -> None:
        self.start()
        self.video_to_img()
        self.view_imgs(size)
        self.videos_to_imgs()
        self.check_imgs()
        self.copy_check_imgs()
