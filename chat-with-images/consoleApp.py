from imageAnalysis import ImageAnalysis
# Usage example
image_analysis = ImageAnalysis()




response = image_analysis.analyze_image("./data/women.jpg","what is the hair color ? Reply only the color")
print(response)
response = image_analysis.analyze_image("./data/women.jpg","what is the age  ? Reply only the age")
print(response)
response = image_analysis.analyze_image("./data/women.jpg","what is the color of skin  ? Reply only Clear or Medium or Dark ")
print(response)
response = image_analysis.analyze_image("./data/women.jpg","Is it a woman or a man  ? Reply only by Woman or Man")
print(response)
response = image_analysis.analyze_image("./data/women.jpg","Is it a hair shape ?  Curly or Wavy or Straight")
print(response)
