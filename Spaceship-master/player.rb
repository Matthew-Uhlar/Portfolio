require "gosu"
require_relative 'z_order'
require_relative 'star'

class Player

	TURN_INCREMENT = 4.5
	ACCELERATION = 0.5
	COLLISION_DISTANCE = 35

 	def initialize
    @image = Gosu::Image.new("media/starfighter.bmp")
    @beep = Gosu::Sample.new("media/beep.wav")
    @x = @y = @vel_x = @vel_y = @angle = 0.0
    @score = 0
  end

	def warp(x, y)
		@x, @y = x, y
	end

	def turn_left
		@angle -= TURN_INCREMENT
	end

	def turn_right
		@angle += TURN_INCREMENT
	end

	def accelerate
		@vel_x += Gosu::offset_x(@angle, ACCELERATION)
		@vel_y += Gosu::offset_y(@angle, ACCELERATION)
	end

	def move
		@x += @vel_x
		@y += @vel_y
		@x %= 640
		@y %= 480
		
		@vel_x *= 0.95
		@vel_y *= 0.95
	end

	def draw
		@image.draw_rot(@x, @y, ZOrder::Player, @angle)
	end

	def score
		@score
	end

	def collect_stars(stars)
    stars.reject! do |star|
      if Gosu::distance(@x, @y, star.x, star.y) < 35 then
        @score += 10
        @beep.play
        true
      else
        false
      end
    end
  end

  def destroy_bombs(bombs)
  	
  end
	
end