require "gosu"
require_relative "player"
require_relative "z_order"

class GameWindow < Gosu::Window
	
	def initialize
		super 640, 480
		@player = Player.new
    @player.warp(320, 455)
    @font = Gosu::Font.new(20)
    @background_image = Gosu::Image.new("images/background.jpg")
	end

	def update
		@player.move_left if Gosu::button_down? Gosu::KbLeft
		@player.move_right if Gosu::button_down? Gosu::KbRight
		@player.accelerate if Gosu::button_down? Gosu::KbRight
		@player.accelerate if Gosu::button_down? Gosu::KbLeft
	end

	def button_down(id)
		close if id == Gosu::KbEscape
	end

	def draw
		@background_image.draw(0, 1, ZOrder::Background)
		@player.draw
		@font.draw("Score: #{@player.score}", 10, 10, ZOrder::UI, 1.0, 1.0, 0xff_000000)
	end

end

window = GameWindow.new
window.show