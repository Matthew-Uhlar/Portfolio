require_relative "adapter"
require_relative "window"
require_relative "button"
require "gosu"

class	WindowAdapter < Adapter

	def initialize
		@background = Gosu::Image.new("display/background.png")
		@buttons = []
		@buttons.push(Button.new(20, 20, 100, 100, "Withdraw"))
		@buttons.push(Button.new(140, 20, 100, 100, "Deposit"))
		@buttons.push(Button.new(260, 20, 100, 100, "Balance"))
		@window = Window.new(@background, @buttons)
		@window.show
		
	end

end