require "gosu"
require_relative 'z_order'

class Lazer
	attr_reader :x, :y

	TURN_INCREMENT = 4.5
	ACCELERATION = 10
	COLLISION_DISTANCE = 30

	def initialize(x, y, angle)
		@x = x
		@y = y
		@vel_x = ACCELERATION
		@vel_y = ACCELERATION
		@angle = angle
		@img = Gosu::Image.new("images/laser.png")
		@mob_score = 0
	end

	def warp(x, y)
		@x, @y = x, y
	end

	def move
		@x += Gosu::offset_x(@angle, ACCELERATION)
		@y += Gosu::offset_y(@angle, ACCELERATION)
	end

	def draw
		@img.draw_rot(@x, @y, ZOrder::LAZER, 90)
	end

	def mob_score
		@mob_score
	end

	def update
		@mob_score = 0
	end

	def destroy_mobs(mobs)
		if mobs.reject! {|mob| colliding?(mob)}
			@mob_score += 1
			true
		else
			false
		end
	end

	private

	def colliding?(mob)
		Gosu::distance(@x, @y, mob.x, mob.y) < COLLISION_DISTANCE
	end

	def offscreen?
		if @x < 0 || @x > 640 || @y < 0 || @y > 480
			true
		else
			false
		end
	end

end