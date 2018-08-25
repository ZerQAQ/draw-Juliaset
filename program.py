import matplotlib.pyplot as plt
import imageio
import os

class Julia_set_drawer(object):
	def __init__(self, C = [0.75, 0], max_time = 24, _range = 2, xsmd = 150, index = 2, pic_size = 10, ticket= 0.1):
		self.C = C
		self.max_time = max_time
		self._range = _range
		self.xsmd = xsmd
		self.index = index
		self.pic_size = pic_size
		self.ticket = ticket
		self.pic_div_name = "pics"
		self.gif_div_name = "gif"
		try: os.mkdir(self.pic_div_name)
		except: pass
		try: os.mkdir(self.gif_div_name)
		except: pass
		self.midp_x = 0
		self.midp_y = 0
		self.area_szie = 1.7


	def set(self, C = [0.75, 0], max_time = 24, _range = 2, xsmd = 150, index = 2, pic_size = 10, ticket= 0.1):
		self.C = C
		self.max_time = max_time
		self._range = _range
		self.xsmd = xsmd
		self.index = index
		self.pic_size = pic_size
		self.ticket = ticket

	def mul(self, a, b):
		return [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];

	def _sqr(self, x):
		n = self.index

		res = x;
		for i in range(n - 1):
			res = self.mul(res, x)
		return res

	def fun(self, x):
		C = self.C

		res = self._sqr(x);
		res[0] -= C [0];
		res[1] -= C [1];
		return res;

	def tysj(self, x):
		max_time = self.max_time
		_range = self._range

		for i in range(max_time):
			x = self.fun(x);
			if(x[0]*x[0] + x[1]*x[1] > _range * _range): return i;
		return max_time;

	def draw(self, save_path = 'Julia_set.png', r_v = None, i_v = None, index = None, xsmd = None):
		max_time = self.max_time
		_range = self._range
		xsmd = self.xsmd

		if(r_v != None): self.C[0] = r_v
		if(i_v != None): self.C[1] = i_v
		if(index != None): self.index = index
		if(xsmd != None): self.xsmd = xsmd

		x = []
		y = []
		c = []

		print("drawing", save_path)
		for _i in range(xsmd * -1, xsmd + 1):
			for _j in range(xsmd * -1, xsmd + 1):
				i = self.midp_x + _i / xsmd * self.area_szie;
				j = self.midp_y + _j / xsmd * self.area_szie;
				x.append(i);
				y.append(j);
				c.append(self.tysj([i, j]) / max_time)

		plt.figure(figsize = (10, 10))
		plt.xticks([])
		plt.yticks([])
		fig = plt.scatter(x, y, c = c, edgecolors = 'face')
		fig.axes.get_xaxis().set_visible(False)
		fig.axes.get_yaxis().set_visible(False)
		plt.axis('off')
		x_mi = self.midp_x - self.area_szie
		x_ma = self.midp_x + self.area_szie
		y_mi = self.midp_y - self.area_szie
		y_ma = self.midp_y + self.area_szie
		plt.axis([x_mi, x_ma, y_mi, y_ma])
		if(save_path == None): plt.show()
		else: plt.savefig(save_path, bbox_inches = 'tight', pad_inches = 0, dpi = 200)
		print(save_path, "is drawn.")
		plt.close("all")


	def create_gif(self, img_list, save_path):
		ticket = self.ticket

		print("makeing", save_path)
		fr = []
		for x in img_list:
			fr.append(imageio.imread(x))
		imageio.mimsave(save_path, fr, 'GIF', duration = ticket)

		print(save_path, 'is finish.')

	def draw_pics(self, real_start, real_end, real_time, imagine_start, imagine_end, imagine_time):
		r_s = real_start
		r_e = real_end
		r_t = real_time
		i_s = imagine_start
		i_e = imagine_end
		i_t = imagine_time
		try: r_a = (r_e - r_s) / (r_t - 1)
		except: r_a = 0

		try: i_a = (i_e - i_s) / (i_t - 1)
		except: i_a = 0

		for i in range(r_t):
			r_v = r_s + r_a * i
			for j in range(i_t):
				i_v = i_s + i_a * i
				png_name = "real = %.2lf, imagine = %.2lf, index = %d.png" % (r_v, i_v, self.index)
				C = [r_v, i_v]

		self.draw(self.pic_div_name + "/" + png_name)

	def change_imagine_to_draw_pics(self, real_start, real_end, real_time, imagine_value):
		self.draw_pics(real_start, real_end, real_time, imagine_value, imagine_value, 1)

	def change_real_to_draw_pics(self, real_vaule, imagine_start, imagine_end, imagine_time):
		self.draw_pics(real_vaule, real_vaule, 1, imagine_start, imagine_end, imagine_time)


	def draw_gif(self, real_start, real_end, imagine_start, imagine_end, zs, pic_drawn = 0):
		r_s = real_start
		r_e = real_end
		i_s = imagine_start
		i_e = imagine_end

		try: r_a = (r_e - r_s) / (zs - 1)
		except: r_a = 0

		try: i_a = (i_e - i_s) / (zs - 1)
		except: i_a = 0

		img_list = []
		r_v = r_s
		i_v = i_s

		for i in range(zs):
			png_path = self.pic_div_name + "/" + "real = %.2lf, imagine = %.2lf, index = %d, xsmd = %d.png" % (r_v, i_v, self.index, self.xsmd)
			if (os.path.exists(png_path) == 0):
				self.C = [r_v, i_v]
				self.draw(png_path)
			img_list.append(png_path)
			r_v += r_a
			i_v += i_a

		gif_name = "r_in = [%.2f,%.2f], i_in[%.2f,%.2f], index = %d, zs = %d, ticket = %.2lf.gif" % (r_s, r_e, i_s, i_e, self.index, zs, self.ticket)
		gif_path = self.gif_div_name + "/" + gif_name
		self.create_gif(img_list, gif_path)

	def change_imagine_to_draw_gif(self, real_vaule, imagine_start, imagine_end, zs, pic_drawn = 0):
		self.draw_gif(real_vaule, real_vaule, imagine_start, imagine_end, zs, pic_drawn)

	def change_real_to_draw_gif(self, imagine_value, real_start, real_end, zs, pic_drawn = 0):
		self.draw_gif(real_start, real_end, imagine_value, imagine_value, zs, pic_drawn)


drawer = Julia_set_drawer()
drawer.set(index = 2, ticket = 1 / 24, xsmd = 300)

re = [-0.4, 0.8]
im = [-0.8, 0, -0.6]

#drawer.change_imagine_to_draw_gif(real_vaule = -0.4, imagine_start = -1.5, imagine_end = 1.5, zs = 151)

drawer.change_real_to_draw_gif(imagine_value = -1, real_start = -0.65, real_end = 0, zs = 101)

'''
for x in re:
	drawer.change_imagine_to_draw_gif(real_vaule = x, imagine_start = -1.5, imagine_end = 1.5, zs = 151)

for x in im:
	drawer.change_real_to_draw_gif(imagine_value = x, real_start = -1.5, real_end = 1.5, zs = 151)
'''