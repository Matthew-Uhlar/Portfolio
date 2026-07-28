require "gosu"

class Display

	def initialize(text, title, x, y)
		@text = text
		@title = title
		@x = x
		@y = y
		@box = Gosu::Image.new("display/button.png")
		@font = Gosu::Font.new(12)
		@font2 = Gosu::Font.new(22)
	end

	def draw
		@box.draw(@x, @y, 2, 10, 3)
		@font.draw(@title, @x + 75, @y - 10, 2, 1, 1, 0xff_ffff00)
		@font2.draw(@text, @x + 180 - (@text.length * 10), @y + 20, 3, 1, 1, 0xff_ffffff)
	end

	def update(text)
		@text += text
	end

end