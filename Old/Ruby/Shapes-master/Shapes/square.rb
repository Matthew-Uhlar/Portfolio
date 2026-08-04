require_relative 'shapes'
require "gosu"

class Square < Shape

def initialize(x, y, width, z, mode)

		@x = y
		@y = x
		@fill = Gosu::Color.argb(0xff_f00000)
		@stroke = Gosu::Color.argb(0xff_00ff00)
		@width = width
		@mode = mode
		@z = z
		@fillheight = @y + @width
	end

	def draw
		draw_square
		fill_shape
	end

	private
		def draw_square
			Gosu.draw_line(@x, @y, @stroke, @x + @width, @y, @stroke, @z, :default)
			Gosu.draw_line(@x, @y, @stroke, @x, @y + @width, @stroke, @z, :default)
			Gosu.draw_line(@x + @width, @y, @stroke, @x + @width, @y + @width, @stroke, @z, :default)
			Gosu.draw_line(@x, @y + @width, @stroke, @x + @width, @y + @width, @stroke, @z , :default)
		end

		def fill_shape
			for i in (@y..@fillheight) 
				Gosu.draw_line(@x, i, @fill, @x + @width, i, @fill, -1, :default)
			end
		end

end