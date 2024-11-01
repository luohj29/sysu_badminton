SYSU badminton court reservation system
virtual environment is recommended
simply run

```shell
conda env create -f environment.yml
conda activate badminton
```
or step by step
```shell
conda create -n badminton
conda activate badminton
you need to download
opencv-python
selenium
baidu-aip
Pillow
```
besides
    如果使用 Firefox，请下载 geckodriver。 https://blog.csdn.net/gitblog_01195/article/details/140978206
    如果使用 Chrome，请下载 chromedriver。
    这里我们使用 Firefox。

    baidu-aip 是百度的人脸识别API，需要注册百度云账号，创建应用，获取API Key和Secret Key。