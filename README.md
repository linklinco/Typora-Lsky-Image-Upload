# Typora-Lsky-Image-Upload
## 使用说明

此脚本支持在Typora插入图片时自动将图片上传到兰空图床，支持上传本地文件和markdown文件中来自网络的图片。

## 使用步骤

1、克隆仓库到本地

```
git clone git@github.com:linklinco/Typora-Lsky-Image-Upload.git
```

2、配置图床信息

编辑`upload.py`文件，填写图床url、email及密码。

3、在`Typora`中配置自动上传

偏好设置->图像->插入图片时改为【上传图片】->上传服务设定改为【上传服务：Custom Command】【命令：python <下载脚本的位置+"/upload.py">】

点击【验证图片上传选项】，可以测试是否配置成功



