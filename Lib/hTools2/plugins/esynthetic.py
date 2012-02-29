# hTools2.plugins.esynthetic

class ESynthetic:

	pixelSizeInEm = 125 
	# main Elementar parameters
	vstrokewidth = 3
	hstrokewidth =	2
	globalcharwidth = 2
	# vertical dimensions
	baseline = 0
	xheight = 9
	middle = .4
	ascender = 4
	descender = 4
	capheight = xheight + descender - 1
	height = descender + xheight + ascender
	# element parameters
	elementsize = 1 * pixelSizeInEm
	elementspacing = 0 * pixelSizeInEm
	# spacing
	leftsidebearing = 1 
	rightsidebearing = 1 
	# corners rounding
	bottomleft = 1 
	topleft = 1
	bottomright = 1	 
	topright = 1
	middle_left = 1 
	middle_right = 1 
	# effects
	howround = 0
	diagonal = "off"
	slant = 0
	serif = 3

	def __init__(self, f):
		self.font = f
		self.middlebar = int(round(self.xheight * self.middle))
		self.capmiddlebar = int(round(self.capheight * self.middle)) + 1
		self.set_roundness()

	def set_roundness(self):
		self.roundness = self.howround
		while self.roundness > self.vstrokewidth - 1:
			self.roundness = self.roundness - 1
		while self.xheight < 2 * self.roundness + 1:
			self.roundness = self.roundness - 1
		self.roundtempmiddlebar = self.roundness
		while self.hstrokewidth * 3 + self.middlebar - 1 < 2 * self.roundtempmiddlebar + 1:
			self.roundtempmiddlebar = self.roundtempmiddlebar - 1 

	def elementshape(self, glyph, (x, y)):
		element = '_element'
		self.font[glyph.name].appendComponent(element, (x, y))

	def element(self, glyph, x="not", y="not"):
		if x != "not":
			x = x * self.element(glyph)
			y = y * self.element(glyph)
			self.elementshape(glyph, (x, y))
		else:
			return self.elementsize + self.elementspacing

	def howmuchround(self, roundtemp, middle=None):
		if roundtemp > 1:
			if middle:
				return int(round(roundtemp ** (roundtemp / self.roundtempmiddlebar)))
			else:
				return int(round(roundtemp ** (roundtemp / self.roundness)))
		else:
			return roundtemp

	def vstroke(self, glyph, xstart, ystart, yend, rposition="not", bottom=0, top=0, middle=None):
		if rposition == "l":
			bottom = bottom * self.bottomleft
			top = top * self.topleft
		if rposition == "r":
			bottom = bottom * self.bottomright
			top = top * self.topright
		roundtemp = 0
		if rposition == "l":
			if middle:
				roundtemp = self.roundtempmiddlebar
			else:
				roundtemp = self.roundness
		if self.vstrokewidth == 1 and self.howround >= 1:
			roundtemp = 1
		ystartbis = ystart
		yendbis = yend
		for t in range(self.vstrokewidth):
			if rposition == "r" or rposition == "l":
				if bottom:
					ystartbis = ystart + self.howmuchround(roundtemp, middle)
				if top:
					yendbis = yend - self.howmuchround(roundtemp, middle) 
			if roundtemp > 0 and rposition == "l":
				roundtemp = roundtemp - 1
			if t >= (self.vstrokewidth - self.roundness - 1) and rposition == "r":
				roundtemp = roundtemp + 1
			for i in range(yendbis - ystartbis):
				x = (xstart + t)
				y = (ystartbis + i)
				self.element(glyph, x, y)

	def hstroke(self, glyph, ystart, xstart, xend, direction="not", left=0, right=0):
		upordown = 1
		if ystart >= self.xheight - 1:
			upordown = -1
		roundtemp = 0
		# if there is to0 much horizontal roundness, control it with this number
		hroundness = int(round(self.roundness))
		if left:
			roundtemp = hroundness
		if self.vstrokewidth == 1 and self.howround >= 1 and left:
			roundtemp = 1
		for t in range(xend - xstart):
			roundupordown = 1
			if direction == "d":
				roundupordown = - roundupordown
			if right and t > (xend - xstart - hroundness) - 1:
				roundtemp = roundtemp + 1
			if right and t == (xend - xstart - hroundness) - 1 and self.vstrokewidth == 1 and self.howround >= 1:
				roundtemp = roundtemp + 1
			if roundtemp <= 0:
				roundtemp = 0
			for i in range(self.hstrokewidth):
				y = (ystart + self.howmuchround(roundtemp) * roundupordown + (i) * upordown)
				x = (xstart + t)
				self.element(glyph, x, y)
			if left:
				roundtemp = roundtemp - 1

	def spacing(self, glyph, left=leftsidebearing, right=rightsidebearing):
		glyph.leftMargin = left * (self.elementsize + self.elementspacing)
		glyph.rightMargin = right * (self.elementsize + self.elementspacing) + self.elementspacing

	#------------------
	# glyph defintions
	#------------------

	def glyph_space(self, glyph):
		charwidth = self.globalcharwidth + self.hstrokewidth + self.leftsidebearing + self.rightsidebearing
		self.spacing(glyph)

	def glyph_a(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1)
		self.vstroke(glyph, 0, self.baseline, self.hstrokewidth + self.middlebar, "l", 1, 1, True)
		self.vstroke(glyph, charwidth, self.baseline, self.xheight, "r", 0, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth, "u", 0, 1)
		self.hstroke(glyph, self.middlebar, self.vstrokewidth, charwidth, "d", 0, 0)
		self.hstroke(glyph, self.xheight - 1, int(round(self.vstrokewidth / 4)) , charwidth, "d", 1, 0)
		self.spacing(glyph)

	def glyph_b(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1)
		self.vstroke(glyph, 0, self.baseline, self.xheight + self.ascender, "l", 0, 0)
		self.vstroke(glyph, charwidth, self.baseline, self.xheight, "r", 1, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth, "u", 0, 0)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth, "d", 1, 0)
		self.spacing(glyph)

	def glyph_c(self, glyph):
		charwidth = self.globalcharwidth + int(round(self.vstrokewidth / 2))
		self.vstroke(glyph, 0, self.baseline, self.xheight, "l", 1, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth + self.vstrokewidth, "u", 0, 1)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth + self.vstrokewidth, "d", 0, 1)
		self.spacing(glyph)

	def glyph_d(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1) 
		self.vstroke(glyph, charwidth, self.baseline, self.xheight + self.ascender)
		self.vstroke(glyph, 0, self.baseline, self.xheight, "l", 1, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth, "u", 0, 1)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_e(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1) 
		self.vstroke(glyph, 0, self.baseline, self.xheight, "l", 1, 1)
		self.vstroke(glyph, charwidth, self.xheight - self.middlebar - self.hstrokewidth, self.xheight, "r", 0, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth + self.vstrokewidth, "u", 0, 1)
		self.hstroke(glyph, self.xheight - self.middlebar - self.hstrokewidth, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_f(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.xheight + self.ascender, "l", 0, 1)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.xheight - 1, -int(round(charwidth / 4)), 0)
		self.hstroke(glyph, self.xheight + self.ascender - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_g(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1) 
		self.vstroke(glyph, 0, self.baseline, self.xheight, "l", 1, 1)
		self.vstroke(glyph, charwidth, -self.descender, self.xheight, "r", 1, 0)
		self.hstroke(glyph, -self.descender, int(round(self.vstrokewidth / 2)), charwidth)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth, "u", 0, 1)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_h(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1) 
		self.vstroke(glyph, 0, self.baseline, self.xheight + self.ascender)
		self.vstroke(glyph, charwidth, self.baseline, self.xheight, "r", 0, 1)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth, "d", 1, 0)
		self.spacing(glyph)
		
	def glyph_i(self, glyph):
		charwidth = 0
		self.vstroke(glyph, 0, self.baseline, self.xheight)
		self.vstroke(glyph, 0, self.xheight + int(round(self.ascender / 2)), self.xheight + self.ascender)
		self.spacing(glyph)

	def glyph_j(self, glyph):
		charwidth = (self.globalcharwidth + self.vstrokewidth) / 2
		self.vstroke(glyph, 0, -self.descender, self.xheight, "r", 1, 0)
		self.vstroke(glyph, 0, self.xheight + int(round(self.ascender / 2)), self.xheight + self.ascender)
		self.hstroke(glyph, -self.descender, -self.globalcharwidth, 0)
		self.spacing(glyph)

	def glyph_k(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1) 
		self.vstroke(glyph, 0, self.baseline, self.xheight + self.ascender)
		self.vstroke(glyph, charwidth, self.baseline, self.middlebar, "r", 0, 0)
		self.vstroke(glyph, charwidth, self.middlebar, self.xheight, "r", 1, 0)		 
		self.hstroke(glyph, self.middlebar, self.vstrokewidth, charwidth, "d", 0, 0)
		self.spacing(glyph)

	def glyph_l(self, glyph):
		charwidth = 0
		self.vstroke(glyph, 0, self.baseline, self.xheight + self.ascender)
		self.spacing(glyph)

	def glyph_m(self, glyph):
		charwidth = (1 + self.globalcharwidth + (self.vstrokewidth - 1)) * 2
		self.vstroke(glyph, 0, self.baseline, self.xheight)
		self.vstroke(glyph, int(round(charwidth / 2)), self.baseline, self.xheight, "r", 0, 1)
		self.vstroke(glyph, charwidth, self.baseline, self.xheight, "r", 0, 1)
		self.hstroke(glyph, self.xheight - 1, int(round(charwidth / 2)) + self.vstrokewidth, charwidth, "d", 1, 0)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, int(round(charwidth / 2)), "d", 1, 0)
		self.spacing(glyph)

	def glyph_n(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1) 
		self.vstroke(glyph, 0, self.baseline, self.xheight)
		self.vstroke(glyph, charwidth, self.baseline, self.xheight, "r", 0, 1)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth, "d", 1, 0)
		self.spacing(glyph)

	def glyph_o(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1) 
		self.vstroke(glyph, 0, self.baseline, self.xheight, "l", 1, 1)
		self.vstroke(glyph, charwidth, self.baseline, self.xheight, "r", 1, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_p(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1) 
		self.vstroke(glyph, 0, -self.descender, self.xheight)
		self.vstroke(glyph, charwidth, self.baseline, self.xheight, "r", 1, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth, "u", 0, 0)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth, "d", 1, 0)
		self.spacing(glyph)

	def glyph_q(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1)
		self.vstroke(glyph, 0, self.baseline, self.xheight, "l", 1, 1)
		self.vstroke(glyph, charwidth, -self.descender, self.xheight)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth, "u", 0, 1)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth, "d", 0, 0)
		self.spacing(glyph)

	def glyph_r(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.xheight, "r", 0, 0)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth, "d", 1, 0)
		self.spacing(glyph)

	def glyph_s(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.xheight - self.middlebar - self.hstrokewidth, self.xheight, "l", 1, 1, True)
		self.vstroke(glyph, charwidth, 0, self.xheight - self.middlebar, "r", 1, 1, True)
		self.hstroke(glyph, self.baseline, 0, charwidth, "u", 1, 0)
		self.hstroke(glyph, self.xheight - self.middlebar - self.hstrokewidth, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth + self.vstrokewidth, "d", 0, 1)
		self.spacing(glyph)

	def glyph_t(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.xheight + int(round(self.ascender / 2) + 1), "l", 1, 0)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth, "u", 0, 0)
		self.hstroke(glyph, self.xheight - 1, -int(round(charwidth / 4)), 0)
		self.hstroke(glyph, self.xheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)
			
	def glyph_u(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1) 
		self.vstroke(glyph, 0, self.baseline, self.xheight, "l", 1, 0)
		self.vstroke(glyph, charwidth, self.baseline, self.xheight, "r", 0, 0)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth, "u", 0, 1)
		self.spacing(glyph)

	def glyph_v(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth 
		self.vstroke(glyph, 0, self.baseline, self.xheight, "l", 0, 0)
		self.vstroke(glyph, charwidth, self.baseline, self.xheight, "r", 1, 0)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth, "u", 0, 0)
		self.spacing(glyph)

	def glyph_w(self, glyph):
		charwidth = (self.globalcharwidth + self.vstrokewidth) * 2
		self.vstroke(glyph, 0, self.baseline, self.xheight, "l", 1, 0)
		self.vstroke(glyph, int(round(charwidth / 2)), self.baseline, self.xheight, "r", 1, 0)
		self.vstroke(glyph, charwidth, self.baseline, self.xheight, "r", 1, 0)
		self.hstroke(glyph, self.baseline, int(round(charwidth / 2)) + self.vstrokewidth, charwidth, "d", 0, 0)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, int(round(charwidth / 2)), "d", 0, 0)
		self.spacing(glyph)

	def glyph_x(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.middlebar, "l", 0, 0)
		self.vstroke(glyph, 0, self.middlebar, self.xheight, "l", 1, 0)
		self.vstroke(glyph, charwidth, self.baseline, self.middlebar, "r", 0, 0)
		self.vstroke(glyph, charwidth, self.middlebar, self.xheight, "r", 1, 0)		 
		self.hstroke(glyph, self.middlebar, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_y(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.xheight, "l", 1, 0)
		self.vstroke(glyph, charwidth, -self.descender, self.xheight, "r", 1,0)
		self.hstroke(glyph, -self.descender, int(round(self.vstrokewidth / 2)), charwidth)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth, "u", 0, 1)
		self.spacing(glyph)

	def glyph_z(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth - 1
		self.vstroke(glyph, 0, self.baseline, self.xheight - self.middlebar, "l", 0, 1, True)
		self.vstroke(glyph, charwidth, self.xheight - self.middlebar - self.hstrokewidth, self.xheight, "r", 1, 0, True)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth + self.vstrokewidth)
		self.hstroke(glyph, self.xheight - self.middlebar - self.hstrokewidth, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.xheight - 1, 0, charwidth, "d", 0, 0)
		self.spacing(glyph)

	def glyph_A(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight, "l", 0, 1)
		self.vstroke(glyph, charwidth, self.baseline, self.capheight, "r", 0, 1)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_B(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.vstroke(glyph, charwidth, self.baseline, self.capmiddlebar, "r", 1, 0)
		self.vstroke(glyph, charwidth, self.capmiddlebar, self.capheight, "r", 1, 1) 
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_C(self, glyph):
		charwidth = self.globalcharwidth + int(round(self.vstrokewidth / 2))
		self.vstroke(glyph, 0, self.baseline, self.capheight, "l", 1, 1)		
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth + self.vstrokewidth, "u", 0, 1)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth + self.vstrokewidth, "d", 0, 1)
		self.spacing(glyph)

	def glyph_D(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1) 
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.vstroke(glyph, charwidth, self.baseline, self.capheight, "r", 1, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_E(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_F(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_G(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight, "l", 1, 1)		
		self.vstroke(glyph, charwidth, self.baseline, self.capmiddlebar)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth + self.vstrokewidth, "u", 0, 1)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth + self.vstrokewidth, "d", 0, 1)
		self.spacing(glyph)

	def glyph_H(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.vstroke(glyph, charwidth, self.baseline, self.capheight)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_I(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.spacing(glyph)

	def glyph_J(self, glyph):
		charwidth = (self.globalcharwidth + self.vstrokewidth) / 2
		self.vstroke(glyph, 0, self.baseline, self.capheight, "r", 1, 0)
		self.hstroke(glyph, self.baseline, -self.globalcharwidth, 0)
		self.spacing(glyph)

	def glyph_K(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.vstroke(glyph, charwidth, self.baseline, self.capmiddlebar, "r", 0, 0)
		self.vstroke(glyph, charwidth, self.capmiddlebar, self.capheight, "r", 1, 0)		
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth, "d", 0, 0)
		self.spacing(glyph)

	def glyph_L(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_M(self, glyph):
		charwidth = (self.globalcharwidth + self.vstrokewidth) * 2
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.vstroke(glyph, int(round(charwidth / 2)), self.baseline, self.capheight, "r", 0, 1)
		self.vstroke(glyph, charwidth, self.baseline, self.capheight, "r", 0, 1)
		self.hstroke(glyph, self.capheight - 1, int(round(charwidth/2)) + self.vstrokewidth, charwidth, "d", 1, 0)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, int(round(charwidth / 2)), "d", 1, 0)
		self.spacing(glyph)

	def glyph_N(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1) 
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.vstroke(glyph, charwidth, self.baseline, self.capheight, "r", 0, 1)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth, "d", 1, 0)
		self.spacing(glyph)

	def glyph_O(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight, "l", 1, 1)
		self.vstroke(glyph, charwidth, self.baseline, self.capheight, "r", 1, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_P(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.vstroke(glyph, charwidth, self.capmiddlebar - 1, self.capheight, "r", 1, 1)
		self.hstroke(glyph, self.capmiddlebar - 1, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_Q(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth 
		self.vstroke(glyph, 0, self.baseline, self.capheight, "l", 1, 1)
		self.vstroke(glyph, int(charwidth / 2) + 1, -self.descender + 1, self.baseline)
		self.vstroke(glyph, charwidth, self.baseline, self.capheight, "r", 1, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_R(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.vstroke(glyph, charwidth, self.baseline, self.capmiddlebar - 1, "r", 0, 0)
		self.vstroke(glyph, charwidth, self.capmiddlebar - 1, self.capheight, "r", 1, 1) 
		self.hstroke(glyph, self.capmiddlebar - 1, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_S(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.capheight - self.capmiddlebar, self.capheight, "l", 1, 1, True)
		self.vstroke(glyph, charwidth, 0, self.capheight - self.capmiddlebar + self.hstrokewidth, "r", 1, 1, True)
		self.hstroke(glyph, self.baseline, 0, charwidth, "u", 1, 0)
		self.hstroke(glyph, self.capheight - self.capmiddlebar, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth + self.vstrokewidth, "d", 0, 1)
		self.spacing(glyph)

	def glyph_T(self, glyph):
		charwidth = int(self.globalcharwidth / 2) + 1
		self.vstroke(glyph, 0, self.baseline, self.capheight)
		self.hstroke(glyph, self.capheight - 1, -charwidth, 0)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth + self.vstrokewidth)
		self.spacing(glyph)

	def glyph_U(self, glyph):
		charwidth = 1 + self.globalcharwidth + (self.vstrokewidth - 1) 
		self.vstroke(glyph, 0, self.baseline, self.capheight, "l", 1, 0)
		self.vstroke(glyph, charwidth, self.baseline, self.capheight, "r", 1, 0)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_V(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight, "l", 0, 0)
		self.vstroke(glyph, charwidth, self.baseline, self.capheight, "r", 1, 0)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth, "u", 0, 0)
		self.spacing(glyph)

	def glyph_W(self, glyph):
		charwidth = (self.globalcharwidth + self.vstrokewidth) * 2
		self.vstroke(glyph, 0, self.baseline, self.capheight, "l", 1, 0)
		self.vstroke(glyph, int(round(self.charwidth / 2)), self.baseline, self.capheight, "r", 1, 0)
		self.vstroke(glyph, self.charwidth, self.baseline, self.capheight, "r", 1, 0)
		self.hstroke(glyph, self.baseline, int(round(charwidth / 2)) + self.vstrokewidth, charwidth, "d", 0, 0)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, int(round(charwidth / 2)), "d", 0, 0)
		self.spacing(glyph)

	def glyph_X(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capmiddlebar + 1, "l", 0, 1)
		self.vstroke(glyph, 0, self.capmiddlebar, self.capheight, "l", 1, 0)
		self.vstroke(glyph, charwidth, self.baseline, self.capmiddlebar + 1, "r", 0, 1)
		self.vstroke(glyph, charwidth, self.capmiddlebar, self.capheight, "r", 1, 0)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_Y(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth 
		self.vstroke(glyph, 0, self.capmiddlebar, self.capheight, "l", 1, 0)
		self.vstroke(glyph, int(charwidth / 2), self.baseline, self.capmiddlebar)
		self.vstroke(glyph, charwidth, self.capmiddlebar, self.capheight, "r", 1, 0)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_Z(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth - 1
		self.vstroke(glyph, 0, self.baseline, self.capmiddlebar + 1, "l", 0, 1)
		self.vstroke(glyph, self.charwidth, self.capmiddlebar, self.capheight, "r", 1, 0)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth + self.vstrokewidth)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, 0, charwidth, "d", 0, 0)
		self.spacing(glyph)

	def glyph_zero(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth 
		self.vstroke(glyph, 0, self.baseline, self.capheight, "l", 1, 1)
		self.vstroke(glyph, charwidth, self.baseline, self.capheight, "r", 1, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_two(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capmiddlebar + 1, "l", 0, 1)
		self.vstroke(glyph, charwidth, self.capmiddlebar, self.capheight, "r", 1, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth + self.vstrokewidth)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, 0, charwidth, "d", 1, 0)
		self.spacing(glyph)

	def glyph_three(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth 
		self.vstroke(glyph, charwidth, self.baseline, self.capmiddlebar, "r", 1, 0)
		self.vstroke(glyph, charwidth, self.capmiddlebar, self.capheight, "r", 1, 1) 
		self.hstroke(glyph, self.baseline, 0, charwidth, "u", 1, 0)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, 0, charwidth, "d", 1, 0)
		self.spacing(glyph)

	def glyph_four(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.capmiddlebar, self.capheight, "l", 1, 0)
		self.vstroke(glyph, charwidth, self.baseline, self.capheight, "r", 0, 0)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_five(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.capmiddlebar, self.capheight)		 
		self.vstroke(glyph, charwidth, self.baseline, self.capmiddlebar + self.hstrokewidth, "r", 1, 1)
		self.hstroke(glyph, self.baseline, 0, charwidth, "u", 1, 0)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth + self.vstrokewidth)
		self.spacing(glyph)

	def glyph_six(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth
		self.vstroke(glyph, 0, self.baseline, self.capheight, "l", 1, 1)		
		self.vstroke(glyph, charwidth, self.baseline, self.capmiddlebar + self.hstrokewidth, "r", 1, 1)
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth + self.vstrokewidth, "u", 0, 1)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth + self.vstrokewidth, "d", 0, 1)
		self.spacing(glyph)

	def glyph_eight(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth 
		self.vstroke(glyph, 0, self.baseline, self.capmiddlebar, "l", 1, 0)
		self.vstroke(glyph, 0, self.capmiddlebar, self.capheight, "l", 1, 1) 
		self.vstroke(glyph, charwidth, self.baseline, self.capmiddlebar, "r", 1, 0)
		self.vstroke(glyph, charwidth, self.capmiddlebar, self.capheight, "r", 1, 1) 
		self.hstroke(glyph, self.baseline, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_nine(self, glyph):
		charwidth = self.globalcharwidth + self.vstrokewidth 
		self.vstroke(glyph, 0, self.capmiddlebar, self.capheight, "l", 1, 1) 
		self.vstroke(glyph, charwidth, self.baseline, self.capheight, "r", 1, 1) 
		self.hstroke(glyph, self.baseline, 0, charwidth, "u", 1, 0)
		self.hstroke(glyph, self.capmiddlebar, self.vstrokewidth, charwidth)
		self.hstroke(glyph, self.capheight - 1, self.vstrokewidth, charwidth)
		self.spacing(glyph)

	def glyph_period(self, glyph):
		charwidth = 0
		self.vstroke(glyph, 0, self.baseline, self.vstrokewidth)
		self.spacing(glyph)

	def glyph_comma(self, glyph):
		charwidth = int(round(self.vstrokewidth / 2))
		self.vstroke(glyph, 0, -self.descender + 1, self.baseline + self.vstrokewidth, "r", 1, 0)
		self.hstroke(glyph, -self.descender + 1, -charwidth, 0)
		self.spacing(glyph)

	def glyph_exclam(self, glyph):
		charwidth = 0
		self.vstroke(glyph, 0, self.baseline, self.vstrokewidth)
		self.vstroke(glyph, 0, self.vstrokewidth + self.hstrokewidth, self.xheight + self.ascender)
		self.spacing(glyph)

	def glyph_quotesingle(self, glyph):
		charwidth = 0
		self.vstroke(glyph, 0, self.xheight, self.xheight + self.ascender, "l", 0, 0)
		self.spacing(glyph)

	def glyph_quotedbl(self, glyph):
		charwidth = vstrokewidth+1
		vstroke(0, xheight, xheight + ascender, "l", 0, 0)
		vstroke(charwidth, xheight, xheight + ascender, "l", 0, 0)
		spacing()

	def glyph_at(self, glyph):
		charwidth = (globalcharwidth + vstrokewidth) * 2
		vstroke(0, baseline, xheight - 1, "l", 1, 1)
		vstroke(int(charwidth / 2), baseline, xheight - 1, "l", 1, 0)
		vstroke(charwidth, baseline, xheight + ascender, "r", 1, 1)
		hstroke(0, vstrokewidth, int(round(charwidth / 2)), "u", 0, 1)		
		hstroke(0, int(round(charwidth / 2)) + vstrokewidth, charwidth)
		hstroke(xheight - 1 - hstrokewidth, vstrokewidth, int(round(charwidth / 2)))
		hstroke(xheight + ascender - 1, 0, charwidth, "d", 1, 0)
		spacing()

	simpleFont = {
		'space' : glyph_space,
		'a' : glyph_a,
		'b' : glyph_b,
		'c' : glyph_c,
		'd' : glyph_d,
		'e' : glyph_e,
		'f' : glyph_f,
		'g' : glyph_g,
		'h' : glyph_h,
		'i' : glyph_i,
		'j' : glyph_j,
		'k' : glyph_k,
		'l' : glyph_l,
		'm' : glyph_m,
		'n' : glyph_n,
		'o' : glyph_o,
		'p' : glyph_p,
		'q' : glyph_q,
		'r' : glyph_r,
		's' : glyph_s,
		't' : glyph_t,
		'u' : glyph_u,
		'v' : glyph_v,
		'w' : glyph_w,
		'x' : glyph_x,
		'y' : glyph_y,
		'z' : glyph_z,
		'A' : glyph_A,
		'B' : glyph_B,
		'C' : glyph_C,
		'D' : glyph_D,
		'E' : glyph_E,
		'F' : glyph_F,
		'G' : glyph_G,
		'H' : glyph_H,
		'I' : glyph_I,
		'J' : glyph_J,
		'K' : glyph_K,
		'L' : glyph_L,
		'M' : glyph_M,
		'N' : glyph_N,
		'O' : glyph_O,
		'P' : glyph_P,
		'Q' : glyph_Q,
		'R' : glyph_R,
		'S' : glyph_S,
		'T' : glyph_T,
		'U' : glyph_U,
		'V' : glyph_V,
		# 'one' : glyph_one, 
		'two' : glyph_two,
		'three' : glyph_three,
		'four' : glyph_four,
		'five' : glyph_five,
		'six' : glyph_six,
		# 'seven' : glyph_seven,
		'eight' : glyph_eight,
		'nine' : glyph_nine,
	}

	#-------------
	# draw glyphs
	#-------------

	def set_vmetrics(self):
		self.font.info.unitsPerEm = self.height * (self.elementsize + self.elementspacing)
		self.font.info.versionMajor = 2
		self.font.info.versionMinor = 0
		self.font.info.xHeight = self.xheight * (self.elementsize + self.elementspacing)
		self.font.info.ascender = (self.xheight + self.ascender) * (self.elementsize + self.elementspacing)
		self.font.info.descender = self.baseline - self.descender * (self.elementsize + self.elementspacing)
		self.font.info.capHeight = self.capheight * (self.elementsize + self.elementspacing)
		#style = "%s(%s)-%s%s-%s" % (str(height), str(xheight), str(vstrokewidth), str(hstrokewidth), str(globalcharwidth))

	def draw_glyphs(self, names=None, vmetrics=True):
		if names is None:
			names = self.simpleFont.keys()
		if vmetrics:
			self.set_vmetrics()
		for name in names:
			if self.simpleFont.has_key(name):
				glyph = self.font.newGlyph(name, clear=True)
				pen = glyph.getPen()
			 	self.simpleFont[name](self, glyph)
			 	glyph.update()
			else:
			 	print 'no archetype for glyph %s.\n' % name

