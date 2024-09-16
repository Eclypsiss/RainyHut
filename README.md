# RainyHut -- 小型餐馆运营系统

## 项目介绍
本项目为山东大学软件工程专业数据库系统的课程设计，选题为小型餐馆运营系统，计划开发一款集菜品管理、餐桌管理、堂食管理、外卖管理、原材料管理、费用管理以及其他功能与一体的管理系统，应用于类似海底捞、咖啡厅、茶餐厅的电子点餐系统，运行在iPad上便于顾客浏览点餐，以及方便后勤服务人员查看餐厅当前运营情况等。

PS: 第一次上传GitHub项目，还不太清楚README.MD应该怎么写，先按照课程设计报告的样子写吧（大概。

## 项目架构
本项目使用B/S架构的前后端分离开发，后端使用Django + Django REST Framework，数据库使用Django连接MySQL，前端则使用Vue3 + Element Plus开发。

项目部署需求：  
- Python3环境下安装的Django框架和Django REST Framework
- 透过Node.js安装的Vue3
- MySQL 8.0

项目运行：安装好所需环境后分别运行RainyHut和RainyHut_Vue项目，并在RainyHut（后端）控制台输入
```
python manage.py makemigrations

python manage.py migrate
```
进行数据库的迁移后即可通过 http://localhost:5173/dishes 来访问菜单页面。

## 项目总结
因为是第一次进行前后端分离开发项目的尝试，项目还存在许多不足，同时也是第一次尝试将项目开源至GitHub上，因此此README.MD也写的非常...简陋，见谅，详细的的开发报告与项目功能介绍请查看Doc文件夹下的数据库课程设计报告。