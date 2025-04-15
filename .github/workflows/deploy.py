import sys
import yaml
import re

data = yaml.load(open(sys.argv[1]))
print(data)

image = data["spec"]["image"]
print(image)
info = re.compile("(.*/.*):v(\d+)").match(image).groups()
im = info[0]
version = int(info[1]) + 1
print(im, version)
data["spec"]["image"] = f"{im}:v{version}"
print(data)

with open(sys.argv[1], "w") as fp:
    yaml.dump(data, fp)
