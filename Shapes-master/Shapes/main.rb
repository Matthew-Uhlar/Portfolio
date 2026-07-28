require "gosu"
require_relative 'rect'
require_relative 'square'
require_relative 'triangle'

class GameWindow < Gosu::Window

	def initialize
		super 640, 480
		self.caption = "Shapes"
		@rectangle = Rect.new(10, 20, 50, 20, 0, :default)
		@square = Square.new(100, 100, 50, 0, :defualt)
		@triangle = Triangle.new(200, 200, 50, 0, :defualt)
	end

	def update

	end

	def draw
		@rectangle.draw
		@square.draw
		@triangle.draw
	end

	def button_down(id)
		close if id == Gosu::KbEscape
	end

end

window = GameWindow.new
window.show