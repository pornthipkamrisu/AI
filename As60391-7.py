# -*- coding: utf-8 -*-
"""As60391-7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lV4nCY4C8ikBaXtS_z_DBMIEN_8ux2qN

# Object Detection

<table class="tfo-notebook-buttons" align="left">
  <td>
    <a target="_blank" href="https://www.tensorflow.org/hub/tutorials/object_detection"><img src="https://www.tensorflow.org/images/tf_logo_32px.png" />View on TensorFlow.org</a>
  </td>
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/tensorflow/hub/blob/master/examples/colab/object_detection.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Run in Google Colab</a>
  </td>
  <td>
    <a target="_blank" href="https://github.com/tensorflow/hub/blob/master/examples/colab/object_detection.ipynb"><img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" />View on GitHub</a>
  </td>
  <td>
    <a href="https://storage.googleapis.com/tensorflow_docs/hub/examples/colab/object_detection.ipynb"><img src="https://www.tensorflow.org/images/download_logo_32px.png" />Download notebook</a>
  </td>
  <td>
    <a href="https://tfhub.dev/s?q=google%2Ffaster_rcnn%2Fopenimages_v4%2Finception_resnet_v2%2F1%20OR%20google%2Ffaster_rcnn%2Fopenimages_v4%2Finception_resnet_v2%2F1"><img src="https://www.tensorflow.org/images/hub_logo_32px.png" />See TF Hub models</a>
  </td>
</table>

เป็นการใช้โมดูล TF-Hub ที่ได้รับการเทรนมาเพื่อทำการตรวจจับวัตถุ

##Setup
"""

#@title Imports and function definitions

# สำหรับการทำงาน inference บน TF-Hub module
import tensorflow as tf

import tensorflow_hub as hub

#สำหรับดาวโหลด image
import matplotlib.pyplot as plt
import tempfile
from six.moves.urllib.request import urlopen
from six import BytesIO

#สำหรับ drawing ไปยัง image
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

#สำหรับการวัด inference time
import time

"""ฟังก์ชั่นตัวช่วยสำหรับการดาวน์โหลดภาพและการแสดงภาพ

Visualization code ดัดแปลงมาจาก [TF object detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/utils/visualization_utils.py) สำหรับการทำงานที่จำเป็นและง่ายที่สุด
"""

def display_image(image):
  fig = plt.figure(figsize=(20, 15))
  plt.grid(False)
  plt.imshow(image)


def download_and_resize_image(url, new_width=256, new_height=256,
                              display=False):
  _, filename = tempfile.mkstemp(suffix=".jpg")
  response = urlopen(url)
  image_data = response.read()
  image_data = BytesIO(image_data)
  pil_image = Image.open(image_data)
  pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
  pil_image_rgb = pil_image.convert("RGB")
  pil_image_rgb.save(filename, format="JPEG", quality=90)
  print("Image downloaded to %s." % filename)
  if display:
    display_image(pil_image)
  return filename


def draw_bounding_box_on_image(image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color,
                               font,
                               thickness=4,
                               display_str_list=()):
  """Adds a bounding box to an image."""
  draw = ImageDraw.Draw(image)
  im_width, im_height = image.size
  (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                ymin * im_height, ymax * im_height)
  draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
             (left, top)],
            width=thickness,
            fill=color)
  # ถ้าความสูงรวมของสตริงการแสดงเพิ่มที่ด้านบนสุดของขอบเขตกล่องเกินด้านบนของรูปภาพวางสตริงไว้
  #ด้านล่างของกรอบแทนด้านบน
  display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
  #display_str แต่ละตัวมีขอบด้านบนและด้านล่าง 0.05x
  total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

  if top > total_display_str_height:
    text_bottom = top
  else:
    text_bottom = top + total_display_str_height
  # ย้อนกลับรายการและพิมพ์จากล่างขึ้นบน
  for display_str in display_str_list[::-1]:
    text_width, text_height = font.getsize(display_str)
    margin = np.ceil(0.05 * text_height)
    draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                    (left + text_width, text_bottom)],
                   fill=color)
    draw.text((left + margin, text_bottom - text_height - margin),
              display_str,
              fill="black",
              font=font)
    text_bottom -= text_height - 2 * margin


def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.1):
  """Overlay labeled boxes on an image with formatted scores and label names."""
  colors = list(ImageColor.colormap.values())

  try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf",
                              25)
  except IOError:
    print("Font not found, using default font.")
    font = ImageFont.load_default()

  for i in range(min(boxes.shape[0], max_boxes)):
    if scores[i] >= min_score:
      ymin, xmin, ymax, xmax = tuple(boxes[i])
      display_str = "{}: {}%".format(class_names[i].decode("ascii"),
                                     int(100 * scores[i]))
      color = colors[hash(class_names[i]) % len(colors)]
      image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
      draw_bounding_box_on_image(
          image_pil,
          ymin,
          xmin,
          ymax,
          xmax,
          color,
          font,
          display_str_list=[display_str])
      np.copyto(image, np.array(image_pil))
  return image

"""## Apply module

โหลดภาพสาธารณะจาก Open Images v4 บันทึกในเครื่องและแสดง
"""

#import image
image_url = "https://www.chillpainai.com/src/wewakeup/scoop/img_scoop/scoop/kang/travel/10%20saun/SuanBeni_Chill_17.jpg"  #@param
downloaded_image_path = download_and_resize_image(image_url, 1280, 856, True)

"""เลือกโมดูลตรวจจับวัตถุและใช้กับภาพที่ดาวน์โหลด Modules:
*   FasterRCNN + InceptionResNet V2: ความแม่นยำสูง
*   ssd + mobilenet V2: เล็กและเร็ว


"""

module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1" #@param ["https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1", "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"]

detector = hub.load(module_handle).signatures['default']

def load_img(path):
  img = tf.io.read_file(path)
  img = tf.image.decode_jpeg(img, channels=3)
  return img

def run_detector(detector, path):
  img = load_img(path)

  converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
  start_time = time.time()
  result = detector(converted_img)
  end_time = time.time()

  result = {key:value.numpy() for key,value in result.items()}

  print("Found %d objects." % len(result["detection_scores"]))
  print("Inference time: ", end_time-start_time)

  image_with_boxes = draw_boxes(
      img.numpy(), result["detection_boxes"],
      result["detection_class_entities"], result["detection_scores"])

  display_image(image_with_boxes)

run_detector(detector, downloaded_image_path)

"""### More images
Perform inference on some additional images with time tracking.

"""

image_urls = [
  "https://raw.githubusercontent.com/llSourcell/YOLO_Object_Detection/master/sample_img/sample_dog.jpg",
  "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Biblioteca_Maim%C3%B3nides%2C_Campus_Universitario_de_Rabanales_007.jpg/1024px-Biblioteca_Maim%C3%B3nides%2C_Campus_Universitario_de_Rabanales_007.jpg",
  "https://upload.wikimedia.org/wikipedia/commons/0/09/The_smaller_British_birds_%288053836633%29.jpg",
  "https://learning4live.com/wp-content/uploads/2018/09/4-13-810x540.jpg",
  "https://mpics.mgronline.com/pics/Images/560000003492301.JPEG",
  "https://cf.creatrip.com/original/blog/7715/5fq628st0q4o1ebthyu6qk6a0kgrti1y.png?f=webp&q=80&d=500",
  "https://www.bltbangkok.com/wp-content/uploads/2019/03/%E0%B8%A3%E0%B8%A7%E0%B8%A1%E0%B8%AA%E0%B8%A7%E0%B8%99_Body_preset3.jpg",
  "https://www.thaihrhub.com/wp-content/uploads/2015/07/%E0%B8%AB%E0%B8%B2%E0%B8%94%E0%B8%97%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B9%80%E0%B9%80%E0%B8%81%E0%B9%89%E0%B8%A7-1.jpg"
  ]

def detect_img(image_url):
  start_time = time.time()
  image_path = download_and_resize_image(image_url, 640, 480)
  run_detector(detector, image_path)
  end_time = time.time()
  print("Inference time:",end_time-start_time)

detect_img(image_urls[5])

detect_img(image_urls[1])

detect_img(image_urls[2])

detect_img(image_urls[7])