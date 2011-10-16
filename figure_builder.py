from PIL import Image
import sys

loaded_image = None

def dict_from_image_file(file_loc, figure_size):
  im = Image.open(file_loc)
  im_br = im.size
  print 'image loaded, size:', im_br
  return load_dict_from_image(im, ((0,0), im_br), figure_size)

def load_dict_from_image(im, im_bounds, figure_size):
  result_max_x, result_max_y = figure_size
  image_top_left, image_bottom_right = im_bounds
  return_dict = {}
  for x in range(result_max_x):
    for y in range(result_max_y):
      color_at_loc = color_deref(sample(im, get_sample_loc(im_bounds, figure_size, (x, y)), 1))
      if color_at_loc != None:
        return_dict[(x, y)] = color_at_loc
  return return_dict

def color_deref(color):
  return color
  if color == (0, 0, 0):
    return (255,0,0)
  elif color != 0:
    return (255,0,0)
  else:
    return None

def get_sample_loc(im_bounds, figure_size, loc):
  im_tl, im_br = im_bounds
  res_x, res_y = figure_size
  image_width = im_br[0] - im_tl[0]
  image_height = im_br[1] - im_tl[1]
  grid_x = image_width / res_x
  grid_y = image_height / res_y
  sample_tl_x = im_tl[0] + loc[0] * grid_x
  sample_tl_y = im_tl[1] + loc[1] * grid_y
  return (sample_tl_x + grid_x / 2, sample_tl_y + grid_y / 2)

def sample(im, loc, radius):
  colors = []
  return im.getpixel(loc)
  for i in range(loc[0]-radius, loc[0]+radius):
    for j in range(loc[1]-radius, loc[1]+radius):
      colors.append(im.getpixel((i,j))) 
  return mean_of_colors(colors)

def mean_of_colors(colors):
  r = sum([r for r,g,b in colors]) / len(colors)
  g = sum([g for r,g,b in colors]) / len(colors)
  b = sum([b for r,g,b in colors]) / len(colors)
  return (r,g,b)

if __name__ == "__main__":
  print dict_from_image_file(sys.argv[1], (5, 6))
