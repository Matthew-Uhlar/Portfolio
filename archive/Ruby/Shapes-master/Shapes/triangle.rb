require_relative 'shapes'
require "gosu"

class Triangle < Shape

def initialize(x, y, width, z, mode)
		@x = y
		@y = x
		@fill = Gosu::Color.argb(0xff_f00000)
		@fillblack = Gosu::Color.argb(0xff_000000)
		@stroke = Gosu::Color.argb(0xff_00ff00)
		@width = width
		@mode = mode
		@z = z
		@fillheight = @y + @width
	end

	def draw
		draw_triangle
		fill_shape
	end

	private
		def draw_triangle
			Gosu.draw_line(@x, @y, @stroke, @x + @width, @y + @width, @stroke, @z, :default)
			Gosu.draw_line(@x, @y, @stroke, @x, @y + @width, @stroke, @z, :default)
			# Gosu.draw_line(@x + @width, @y, @stroke, @x + @width, @y + @width, @stroke, @z, :default)
			Gosu.draw_line(@x, @y + @width, @stroke, @x + @width, @y + @width, @stroke, @z , :default)
		end

		def fill_shape
			for i in (@y..@fillheight) 
				Gosu.draw_line(@x, i, @fill, @x + @width, i + @width, @fill, -1, :default)
				# Gosu.draw_line(@x, i, @fill, @x + @width, i + @width, @fillblack, -1, :default)
			end
		end*Math.sqrt(2)/2,

end