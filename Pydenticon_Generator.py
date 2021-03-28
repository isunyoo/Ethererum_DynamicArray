# https://pydenticon.readthedocs.io/en/0.1.1/usage.html
# Import the libraries.
import pydenticon
import hashlib

# Set-up a list of foreground colours (taken from Sigil).
foreground = [ "rgb(45,79,255)",
               "rgb(254,180,44)",
               "rgb(226,121,234)",
               "rgb(30,179,253)",
               "rgb(232,77,65)",
               "rgb(49,203,115)",
               "rgb(141,69,170)" ]

# Set-up a background colour (taken from Sigil).
background = "rgb(224,224,224)"

# Set-up the padding (top, bottom, left, right) in pixels.
padding = (20, 20, 20, 20)

# Instantiate a generator that will create 5x5 block identicons using SHA1
# digest.
# generator = pydenticon.Generator(5, 5, digest=hashlib.sha1, foreground=foreground, background=background)
generator = pydenticon.Generator(5, 5, foreground=foreground, background=background)

# # Generate same identicon in two different formats.
# identicon_png = generator.generate("john.doe@example.com", 200, 200, output_format="png")
# identicon_ascii = generator.generate("john.doe@example.com", 200, 200, output_format="png")

# # Identicon can be easily saved to a file.
# f = open("sample.png", "wb")
# f.write(identicon_png)
# f.close()

# # ASCII identicon can be printed-out to console directly.
# print(identicon_ascii)
