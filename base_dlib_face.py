#!/usr/bin/env python
"""机器人大、小头像单张处理模块"""
# -*- coding: utf-8 -*-
# @Time    : 2019/9/29 9:28
# @Author  : Wind
# @Des     : 1、利用dlib库，识别图片中的人脸 2、按人脸剪裁正方形头像 3、按指定长宽比剪裁并缩放
# @File    : base_dlib_face.py
# @Software: PyCharm
import cv2
import dlib


# dlib检测器初始化
def dlib_init(dlib_path):
    """
    :param dlib_path:dlib数据文件的存放位置
    :return: 返回检测器初始化数据
    """
    print('dlib初始化开始')
    init_detector = dlib.get_frontal_face_detector()
    path = dlib_path
    dlib.shape_predictor(path)
    print('dlib初始化结束\n')
    return init_detector


# 读取图片，识别人脸
def get_faces(detector, img_res_path):
    """
    :param detector: 初始化完毕的检测器
    :param img_res_path: 要检测的图片存放路径
    :return:faces: 检测到的人脸列表，None表示无效的图片文件，0表示图片中未能识别出人脸
    :return:img: 检测图片数据信息,使用img.shape可获取图片尺寸
    """

    # 读取图片文件
    img = cv2.imread(img_res_path)
    if img is None:
        print('图片无效')
        return None, None

    # print(f'图片原始尺寸:  {img.shape}')
    faces = detector(img, 1)

    # print("人脸数", len(faces))
    if len(faces) == 0:
        print('未识别出人脸')
        return 0, 0

    # print(f'人脸数据:\n{faces}\n')
    return faces, img


# 按人脸剪裁正方形头像
def crop_face(faces, img, save_path):
    """
    按人脸区域，剪裁出正方形头像
    :param faces:
    :param img:
    :param save_path:
    """
    # 数据初始化
    # 定义剪裁类
    class Crop:
        pass

    # 头像剪裁类实例化
    crop_para = Crop()
    crop_para.w = 300  # 保存图片高度
    crop_para.h = 300  # 保存图片宽度
    crop_para.m = 150  # 脸轮廓外部区域，最小值为0，表示刚好取脸部大小
    crop_para.faces = faces  # 人脸列表
    crop_para.img = img  # 图片数据
    crop_para.path_save = save_path  # 以检测的文件名为输出路径
    crop_para.name_prefix = save_path.split('/')[-1].split('.')[0]  # 如识别出多张脸，会输出多张图，以原文件名为前缀。

    img_height = crop_para.img.shape[0]
    img_width = crop_para.img.shape[1]
    # 初始化结束

    for k, v in enumerate(crop_para.faces):
        # 脸轮廓外部区域处理
        if (v.left() - crop_para.m) >= 0:   # 人脸左边界检查
            x0 = v.left() - crop_para.m
        else:
            x0 = 0

        if (v.top() - crop_para.m) >= 0:    # 人脸上边界检查
            y0 = v.top() - crop_para.m
        else:
            y0 = 0

        if (v.bottom() + crop_para.m) <= img_height:    # 人脸下边界检查
            y1 = v.bottom() + crop_para.m
        else:
            y1 = crop_para.img.shape[0]

        if (v.right() + crop_para.m) <= img_width:      # 人脸右边界检查
            x1 = v.right() + crop_para.m
        else:
            x1 = crop_para.img.shape[1]

        # 脸部区域高度与宽度
        height = y1 - y0
        width = x1 - x0

        # 处理为正方形
        if height > width:
            y1 = y1 - (height - width)
            height = width
        else:
            x1 = x1 - (width - height)
            width = height

        # print(f'cropped_height:  {height}')
        # print(f"cropped_width: {width}")

        # 图片剪裁
        img_cropped = crop_para.img[y0:y1, x0:x1]
        # 图片缩放
        img_resized = cv2.resize(img_cropped, (crop_para.w, crop_para.h), interpolation=cv2.INTER_CUBIC)

        # 图片保存
        save_pic = crop_para.path_save + crop_para.name_prefix + '_' + f"{k}.jpg"
        cv2.imwrite(save_pic, img_resized)


# 按指定长宽比剪裁，缩放至指定尺寸
def crop_by_ratio(res_path):
    """
    保存宽高的参数，目前未放在外部
    剪裁模式目前是居中，可调整为顶部、底部、左侧、右侧
    :param res_path:待剪裁图片的资源路径
    """

    # 定义剪裁类
    class Crop:
        pass

    # 实例化剪裁类
    crop_para = Crop()
    crop_para.img = None  # 准备剪裁图片对象
    crop_para.set_h = 200  # 保存的高度
    crop_para.set_w = 650  # 保存的宽度
    crop_para.img_h = 0  # 剪裁对象原始高度
    crop_para.img_w = 0  # 剪裁对象原始宽度
    crop_para.y0 = 0  # 剪裁对象原始上边界
    crop_para.x0 = 0  # 剪裁对象原始左边界
    crop_para.y1 = 0  # 剪裁对象原始下边界
    crop_para.x1 = 0  # 剪裁对象原始右边界
    crop_para.path_save = './outfile/tmp.jpg'  # 剪裁后的保存目录

    # 初始化待剪裁图片
    crop_para.img = cv2.imread(res_path)

    crop_para.img_h = crop_para.img.shape[0]
    crop_para.img_w = crop_para.img.shape[1]

    crop_para.y1 = crop_para.img.shape[0]
    crop_para.x1 = crop_para.img.shape[1]
    # 初始化结束

    # 设定长宽比
    set_ratio = crop_para.set_h / crop_para.set_w
    img_ratio = crop_para.img_h / crop_para.img_w

    if img_ratio > set_ratio:
        # 图片高度需要剪裁
        img_set_h = crop_para.img_w * set_ratio
        adjust_h = abs(crop_para.img_h - img_set_h)
        crop_para.y0 = int(crop_para.y0 + adjust_h / 2)  # 除以2居中剪裁
        crop_para.y1 = int(crop_para.y1 - adjust_h / 2)
    else:
        if img_ratio < set_ratio:
            # 图片宽度需要剪裁
            img_set_w = crop_para.img_h / set_ratio
            adjust_w = abs(crop_para.img_w - img_set_w)
            crop_para.x0 = int(crop_para.x0 + adjust_w / 2)  # 除以2居中剪裁
            crop_para.x1 = int(crop_para.x1 - adjust_w / 2)

    # 图片剪裁
    img_cropped = crop_para.img[crop_para.y0:crop_para.y1, crop_para.x0:crop_para.x1]
    # 图片缩放
    img_resized = cv2.resize(img_cropped, (crop_para.set_w, crop_para.set_h), interpolation=cv2.INTER_CUBIC)

    # 图片保存
    cv2.imwrite(crop_para.path_save, img_resized)
    print('剪裁完毕!')
