from PIL import Image

filenames = ['camera_feed.png']
for x in xrange(1, 6):
    filenames.append('factory_cam_{}.png'.format(x))

print filenames

images = []
for filename in filenames:
    curr_image = Image.open(filename).convert('RGB')
    images.append(curr_image)

print images

new_image = Image.new('RGB', (1024, 768))

for x in xrange(1024):
    for y in xrange(768):
        # Reset current pixel
        r, g, b = None, None, None

        for curr_image in images:
            red, green, blue = curr_image.getpixel((x, y))
            if not r:
                r, g, b = red, green, blue
            else:
                r ^= red
                g ^= green
                b ^= blue

        new_image.putpixel((x, y), (r, g, b))


print 'Saving'
new_image.save('xored.png')
