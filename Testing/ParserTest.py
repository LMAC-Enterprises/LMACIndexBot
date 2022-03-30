from DataHandling.Interpreting.BodyParser import BodyParser
from Io.Networking.PostEntity import PostEntity
import sys

correctBody = "\n<table class=\"lil\">\n" \
"<tr>\n" \
"<td class=\"lil-title\">Titel 1</td>\n" \
"<td class=\"lil-tags\">magic, spell</td>\n" \
"<td class=\"lil-image\"><img src=\"https://images.hive.blog/DQmYhCtumE72pFod8b3AdrKrU7Xe82FxRzQZnkJVdE2GieA/p01.jpg\" width=\"500\"/></td>\n" \
"</tr>\n" \
"<tr>\n" \
"<td class=\"lil-title\">Titel 2</td>\n" \
"<td class=\"lil-tags\">street, car, city, highway</td>\n" \
"<td class=\"lil-image\"><img src=\"https://images.hive.blog/DQmSTg9kg3m7Zc6mpHHcKgrzQupSVkMFT3cgJKjZUDpbjHh/p02.jpg\" width=\"500\"/></td>\n" \
"</tr>\n" \
"</table>\n" \
"test\n<table class=\"lil\">\n" \
"<tr>\n" \
"<td class=\"lil-title\">Titel 3</td>\n" \
"<td class=\"lil-tags\">human, child, school</td>\n" \
"<td class=\"lil-image\"><img src=\"https://images.hive.blog/DQmYhCtumE72pFod8b3AdrKrU7Xe82FxRzQZnkJVdE2GieA/p03.jpg\" width=\"500\"/></td>\n" \
"</tr>\n" \
"<tr>\n" \
"<td class=\"lil-title\">Titel 4</td>\n" \
"<td class=\"lil-tags\">tree, car,  house, shelter</td>\n" \
"<td class=\"lil-image\"><img src=\"https://images.hive.blog/DQmSTg9kg3m7Zc6mpHHcKgrzQupSVkMFT3cgJKjZUDpbjHh/p04.jpg\" width=\"500\"/></td>\n" \
"</tr>\n" \
"</table>\n" \
"test 123 ![LIL: Titel 5 #picture #cool #colors](https://images.hive.blog/DQmSTg9kg.jpg) blup <br/>![LIL: Titel 6. #photo #awesome #colorful](https://images.hive.blog/DQsdfsdfg.jpg).<br/>"
 
print("Starting BodyParser test")

postEntity = PostEntity()
parser = BodyParser()

postEntity.body = correctBody
parserResult = parser.parse(postEntity)
 
assert parserResult != None, "parserResult shouldn't be None for parsing a correct input."
assert len(parserResult) == 6, "The parser should have found 6 image datasets. Found: " + str(len(parserResult))

for imageEntity in parserResult:
    print(imageEntity)

print("BodyParser test successful")
