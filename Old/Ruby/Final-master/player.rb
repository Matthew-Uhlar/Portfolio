require "gosu"

class Player

	ACCELERATION = 0.4
	COLLISION_DISTANCE = 35

	def initialize
    @image = Gosu::Image.new("images/hero.png")
    @x = @y = @vel_x = @vel_y = @angle = 0.0
    @score = 0
    @health = 100
    @player_dead = 0
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

	def health
		@health
	end

	def accelerate
		@vel_x += ACCELERATION
	end

	# def kill_mob(mobs)
	# 	mobs.reject! do |mob|
 #      if rand(200) < 35 then
 #        @score += 1
 #        true
 #      else
 #        false
 #      end
 #    end
	# end

	def damage
		@health = @health - 10
	end

	def player_dead?
		if @health == 0
			@player_dead = 1
		end
	end

	def player_dead
		@player_dead
	end

	def get_x
		@x
	end

	def get_y
		@y
	end

	def get_angle
		@angle
	end

end

