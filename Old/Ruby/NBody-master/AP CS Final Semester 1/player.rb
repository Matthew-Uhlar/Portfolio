require "gosu"

class Player

	ACCELERATION = 0.5
	COLLISION_DISTANCE = 35

	def initialize
    @image = Gosu::Image.new("images/hero.png")
    @x = @y = @vel_x = @vel_y = @angle = 0.0
    @score = 0
  end

  def warp(x, y)
		@x, @y = x, y
	end

	def move_left
		@x -= @vel_x
		@x %= 640
		
		@vel_x *= 0.95
	end

	def move_right
		@x += @vel_x
		@x %= 640
		
		@vel_x *= 0.95
	end

	def draw
		@image.draw_rot(@x, @y, ZOrder::Player, @angle)
	end

	def score
		@score
	end

	def accelerate
		@vel_x += ACCELERATION
	end

end

