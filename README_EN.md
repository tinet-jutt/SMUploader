# SM.MS Image Uploader

This is an Alfred Workflow built with Python and packaged using pyinstaller, designed to quickly upload images from your clipboard or files to [SM.MS](https://sm.ms) image hosting service and retrieve the image links.

[中文](README.md)

## Features

- Direct image upload from clipboard
- View upload history
- Support file-based image upload
- One-click deletion of uploaded images
- Automatic copying of image links to clipboard
- System notifications for upload status

## Supported Image Formats

- PNG
- JPG/JPEG
- GIF
- BMP
- WebP

## System Requirements

- macOS
- Alfred 4 or higher (Powerpack required)
- Python 3.12 or higher

## Installation

1. Download the Alfred Workflow package from the releases page
2. Configure the environment variable in Alfred Workflow settings:
   - `SM_TOKEN`: Set this to your SM.MS API Token

## Usage

1. Upload an image from clipboard:
   - Copy an image to your clipboard
   - Type `smu` in Alfred

2. View upload history:
   - Type `sml` in Alfred
   - Press Enter to copy the selected image link
   - Press Command + Enter to delete the selected image

## Important Notes

- Keep your API Token secure
- Ensure stable internet connection for uploads
- Regularly clean up unused images to save space

## License

MIT License