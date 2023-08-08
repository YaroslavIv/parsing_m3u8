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
        self.cap = Cap(self.config.cap, self.folder_ts)

    def update(self, path_config: str) -> None:
        self.config = read_config(path_config)

    def name(self) -> str:
        return self.config.name

    def video_to_img(self) -> None:
        folders = os.listdir(os.path.join(self.config.name, self.folder_ts))
        os.makedirs(os.path.join(self.config.name, self.folder_view), exist_ok=True)
        for folder in folders:
            videos = os.listdir(os.path.join(self.config.name, self.folder_ts, folder))
            if len(videos) == 0:
                continue
            video = videos[0]
            video_path = os.path.join(self.config.name, self.folder_ts, folder, video)
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Cannot open camera: {video_path}")
                continue

            ret, frame = cap.read()
            if not ret:
                continue
            cv2.imwrite(os.path.join(os.path.join(self.config.name, self.folder_view), f'{folder}.jpg'), frame)

    def videos_to_imgs(self, dst: str, view_config: str) -> None:
        if not os.path.isdir(self.config.name):
            raise ValueError(f"not find dir: {self.config.name}")

        if len(view_config) > 0:
            if not os.path.isfile(view_config):
                raise ValueError(f"not find file: {view_config}")
            with open(view_config, 'r') as f:
                view_config = json.load(f)['correct']

        os.makedirs(dst, exist_ok=True)

        N = 30
        for folder in os.listdir(self.config.name):
            if isinstance(view_config, list) and not folder in view_config:
                continue

            os.makedirs(os.path.join(dst, folder), exist_ok=True)

            i = 0
            j = 0
            for video in os.listdir(os.path.join(self.config.name, folder)):
                if video[-3:] != '.ts':
                    continue
                video_path = os.path.join(self.config.name, folder, video)
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
                            dst, folder, f'{video[:-3]}_{str(j).zfill(5)}.jpg'), frame)

                cap.release()
            print(folder)

    def new_json(self, src: str, dst: str) -> None:
        if not os.path.isdir(src):
            raise ValueError(f"not find dir: {src}")

        cap = [img[:-4] for img in os.listdir(src)]
        with open(os.path.join(dst, f'{self.config.name}.json'), 'w') as f:
            json.dump({"name": self.config.name, "correct": cap}, f)

    def check_imgs(self, src: str, dst: str, rec: bool) -> None:
        if not os.path.isdir(src):
            raise ValueError(f"not find dir: {src}")

        out = {}
        K = 40_000
        if not rec:
            name = src.split(os.path.sep)[-1]
            out[name] = []
            algo = cv2.createBackgroundSubtractorMOG2()
            for img in os.listdir(src):
                frame = cv2.imread(os.path.join(src, img))
                frame = cv2.resize(frame, (544, 320))
                fgMask = algo.apply(frame)
                fgMask = cv2.medianBlur(fgMask, 3)
                print(img, fgMask.sum())
                if fgMask.sum() >= K:
                    out[name].append(img)
        else:
            for folder in os.listdir(src):
                if os.path.isdir(os.path.join(src, folder)):
                    out[folder] = []
                    algo = cv2.createBackgroundSubtractorMOG2()
                    decline = 0
                    for img in os.listdir(os.path.join(src, folder)):
                        frame = cv2.imread(os.path.join(src, folder, img))
                        frame = cv2.resize(frame, (544, 320))
                        fgMask = algo.apply(frame)
                        fgMask = cv2.medianBlur(fgMask, 3)

                        if fgMask.sum() >= K:
                            out[folder].append(img)
                        else:
                            decline += 1
                print(f'{folder}, decline: {decline}')

        with open(os.path.join(dst, f'{self.config.name}.json'), 'w') as f:
            json.dump(out, f)

    def copy_check_imgs(self, path_check: str, src: str, dst: str) -> None:
        if not os.path.isfile(path_check):
            raise ValueError(f'not find path_check: {path_check}')

        if not os.path.isdir(src):
            raise ValueError(f'not find src: {src}')

        with open(path_check, 'r') as f:
            check = json.load(f)

        os.makedirs(os.path.join(dst, self.config.name))
        for folder in check:
            for img in check[folder]:
                copyfile(
                    os.path.join(src, folder, img),
                    os.path.join(dst, self.config.name, f'{folder}_{img}')
                )
            print(folder)

    def view_imgs(self, size: List[int]) -> None:

        m = Manager(os.path.join(self.config.name, self.folder_view), os.path.join(self.config.name, self.folder_view), self.config.name, size)
        m.bind()
        m.show()
        m.start()

    def start(self) -> None:
        self.cap.switch(self.config.name)
