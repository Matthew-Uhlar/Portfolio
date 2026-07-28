require "gosu"

class Shape

	attr_accessor :x1, :y1, :x2, :y2, :colorin, :colorout 

	def initialize(x1, x2, y1, y2, colorin, colorout, lines)
		@x1 = x1
		@y1 = y1
		@x2 = x2
		@y2 = y2
		@colorin = colorin
		@colorout = colorout
		@rectangles = Array.new
		@triangles = Array.new
		@squares = Array.new
		@lines = lines
	end

	def draw
		(0...@lines).each |i|
		draw_line(@x1, @y1, @colorout, @x2, @y2, @colorout, z = 0, mode = :default)
	end

end