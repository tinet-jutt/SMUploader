# SM.MS 图片上传工具

这是一个基于 [SM.MS](https://sm.ms) 图床服务的 Alfred Workflow，使用pyinstaller打包，可以快速上传剪贴板中的图片或图片文件到 SM.MS，并获取图片链接。

## 功能特点

- 支持从剪贴板直接上传图片
- 支持查看历史上传记录
- 支持复制图片文件上传
- 支持一键删除已上传的图片
- 上传成功后自动复制图片链接到剪贴板
- 支持系统通知提示上传状态

## 支持的图片格式

- PNG
- JPG/JPEG
- GIF
- BMP
- WebP

## 系统要求

- macOS 系统
- Alfred 4 或更高版本（需要 Powerpack）
- Python 3.12 或更高版本

## 安装步骤
1. 从release下载本项目的Alfred Workflow包
5. 在 Alfred Workflow 的配置中设置环境变量：
   - `SM_TOKEN`: 设置为你的 SM.MS API Token

## 使用方法

1. 上传剪贴板图片：
   - 复制一张图片到剪贴板
   - 在 Alfred 中输入 `smu`

2. 查看上传历史：
   - 在 Alfred 中输入 `sml`
   - 按 Enter 复制选中图片的链接
   - 按住 Command + Enter 删除选中的图片

## 注意事项

- 请妥善保管你的 API Token
- 上传图片需要确保网络连接正常
- 建议定期清理不需要的图片以节省空间

## 许可证

本项目采用 MIT 许可证