require "gosu"
require_relative 'z_order'

class GameWindow < Gosu::Window
	def initialize
		file = File.open("planets.txt", 'r')
		super 640, 480
		self.caption = "Universe Simulation"
		@background_image = Gosu::Image.new("images/space.jpg", :tileable => true)
		file = File.open("planets.txt", 'r')
		file.each_line do |line, index|

		@sun_image = Gosu::Image.new("images/sun.png")

	end

	def draw
		@background_image.draw(0, 0, ZOrder::Background)
		@sun_image.draw(320, 240, ZOrder::Planets)
	end
end

window = GameWindow.new
window.show
