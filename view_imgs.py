from PIL import Image, ImageTk
from tkinter import Label
import cv2
import os
from typing import List
import json
from tkinter import Tk, Label


class Manager:
    def __init__(self, src: str, dst: str, name: str, size: List[int]) -> None:
        if not os.path.isdir(src):
            raise ValueError(f'not find src: {src}')

        self.src = src
        self.dst = dst
        self.name = name
        self.imgs = os.listdir(src)
        self.size = size
        self.max_element = len(self.imgs) - 1
        self.img_index = 0
        self.config = {}
        
        self.win = Tk()
        self.win.geometry(f"{size[0]}x{size[1]}")
        self.label =Label(self.win)
        self.label.grid(row=0, column=0)

    def next(self, event) -> None:
        if self.img_index < self.max_element:
            self.img_index += 1
            self.show()

    def previous(self, event) -> None:
        if self.img_index > 0:
            self.img_index -= 1
            self.show()

    def accept(self, event) -> None:
        self.config[self.img_index] = True
        self.next(event)

    def decline(self, event) -> None:
        self.config[self.img_index] = False
        self.next(event)

    def img(self) -> Image:
        cv2_img_bgr = cv2.imread(os.path.join(
            self.src, self.imgs[self.img_index]))
        cv2_img_rgb = cv2.cvtColor(cv2_img_bgr, cv2.COLOR_BGR2RGB)
        cv2_resize = cv2.resize(cv2_img_rgb, self.size)
        if self.img_index in self.config:
            color = (0, 255, 0) if self.config[self.img_index] else (255, 0, 0)
            cv2.rectangle(cv2_resize, (0, 0), self.size, color, 15)
        return Image.fromarray(cv2_resize)

    def show(self) -> None:
        img = self.img()

        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.win.title(f'{self.img_index+1}/{len(self.imgs)}')
    
    def bind(self) -> None:
        self.win.bind('<Right>', self.next)
        self.win.bind('<Left>', self.previous)
        self.win.bind('<a>', self.accept)
        self.win.bind('<d>', self.decline)
        self.win.bind('<s>', self.save)

    def save(self, event) -> None:
        out_json = {
            "name": self.name,
            "correct": [],
            "not_correct": [],
        }
        accept = 0
        decline = 0
        for index in self.config:
            if self.config[index]:
                accept += 1
                out_json["correct"].append(self.imgs[index][:-4])
            else:
                out_json["not_correct"].append(self.imgs[index][:-4])
                decline += 1

        if len(self.imgs) > len(self.config):
            for i in range(len(self.imgs)):
                if not i in self.config:
                    out_json["not_correct"].append(self.imgs[i][:-4])
        
        with open(os.path.join(self.dst, f'{self.name}.json'), 'w') as f:
            json.dump(out_json, f)
        
        print(f'accept: {accept}, decline: {decline}, all: {len(self.imgs)}, no: {len(self.imgs) -len(self.config)}')

    def start(self) -> None:
        self.win.mainloop()
