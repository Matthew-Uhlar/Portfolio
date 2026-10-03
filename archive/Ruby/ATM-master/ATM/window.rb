require "gosu"
require_relative "button"
require_relative "display"
require_relative "account"

class Window < Gosu::Window

	def initialize(background, menu_buttons)
		super 640, 480
		@account = Account.new
		@background = background
		@buttons = menu_buttons
		@screen_main = true
		@screen_withdraw = false
		@display = Display.new("", "Amount", 400, 20)
		@buttons_withdraw = []
		@buttons_withdraw.push(Button.new(20, 20, 75, 75, "*"))
		@buttons_withdraw.push(Button.new(105, 20, 75, 75, "0"))
		@buttons_withdraw.push(Button.new(190, 20, 75, 75, "*"))
		@buttons_withdraw.push(Button.new(20, 105, 75, 75, "1"))
		@buttons_withdraw.push(Button.new(105, 105, 75, 75, "2"))
		@buttons_withdraw.push(Button.new(190, 105, 75, 75, "3"))
		@buttons_withdraw.push(Button.new(20, 190, 75, 75, "4"))
		@buttons_withdraw.push(Button.new(105, 190, 75, 75, "5"))
		@buttons_withdraw.push(Button.new(190, 190, 75, 75, "6"))
		@buttons_withdraw.push(Button.new(20, 275, 75, 75, "7"))
		@buttons_withdraw.push(Button.new(105, 275, 75, 75, "8"))
		@buttons_withdraw.push(Button.new(190, 275, 75, 75, "9"))
		@buttons_withdraw.push(Button.new(40, 400, 200, 75, "Enter"))
	end

	def draw
		@background.draw(0, 0, 0)
		if @screen_main
			@buttons.each do |n|
				n.draw
			end
		elsif @screen_withdraw
			@display.draw
			@buttons_withdraw.each do |button|
				button.draw
			end
		end
	end

	def button_down(id)
		if id == Gosu::MsLeft
			number = nil
			(0...@buttons.length).each do |n|
				if @buttons[n].collide?(self.mouse_x, self.mouse_y)
					number = n
				end
			end
			if @screen_withdraw 
				@buttons_withdraw.each do |button|
					if button.collide?(self.mouse_x, self.mouse_y)
						@display.update(button.text)
					end
				end
			end
			if number == 0
				@screen_main = false
				@screen_withdraw = true
			end
		end
	end

	def needs_cursor?
		true
	end

end