require "gosu"
require_relative "player"
require_relative "z_order"
require_relative "mob"
require_relative "laser"

class GameWindow < Gosu::Window
	
	def initialize
		super 640, 480
		@player = Player.new
    @player.warp(320, 455)
    @font = Gosu::Font.new(30)
    @background_image = Gosu::Image.new("images/background.jpg")
    @mobs = Array.new
    @stagenumber = 1
    @cooldown = 0
		@mob_score = 0
		@lazers = []
	end

	def update
		@player.move_left if Gosu::button_down? Gosu::KbLeft
		@player.move_right if Gosu::button_down? Gosu::KbRight
		@player.accelerate if Gosu::button_down? Gosu::KbRight
		@player.accelerate if Gosu::button_down? Gosu::KbLeft
		if rand(100) < @stagenumber and @mobs.size < (5 * @stagenumber) then
      		@mobs.push(Mob.new)
   		end
    	if @mob_score >= (@stagenumber * 10)
    		@stagenumber += 1
   		end
    	# @player.kill_mob(@mobs)
    	@mobs.each { |mob| mob.fall}
    	@mobs.each do |mob|
			mob.update
			@player.damage if mob.gone == 1
			@mobs.delete(mob) if mob.gone == 1
		end
		@player.player_dead?
		if @player.player_dead == 1
			close
			print "Your score was #{@mob_score}!"
		end
		if Gosu::button_down? Gosu::KbSpace
			if @cooldown == 0
					@lazers.push(Lazer.new(@player.get_x, @player.get_y, 0))
					@cooldown = 15
			end
		end
		@cooldown -= 1
		if @cooldown < 0
			@cooldown = 0
		end

		@lazers.each do |lazer|
			lazer.move
			if @lazers.length > 50
				@lazers.delete(0)
			end
		end
		@lazers.each do |lazer|
			lazer.destroy_mobs(@mobs)
		end

		@lazers.each do |lazer|
			@mob_score += lazer.mob_score
			lazer.update
		end
	end

	def button_down(id)
		close if id == Gosu::KbEscape
	end

	def draw
		@background_image.draw(0, 1, ZOrder::Background)
		@player.draw
		@font.draw("Score: #{@mob_score}", 10, 10, ZOrder::UI, 1.0, 1.0, 0xff_000000)
		@font.draw("Stage: #{@stagenumber}", 10, 30, ZOrder::UI, 1.0, 1.0, 0xff_000000)
		@font.draw("Health: #{@player.health}", 10, 50, ZOrder::UI, 1.0, 1.0, 0xff_000000)
		@mobs.each { |mob| mob.draw}
		@lazers.each {|lazer| lazer.draw}
	end

end

window = GameWindow.new
window.show