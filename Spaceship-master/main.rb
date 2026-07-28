require "gosu"
require_relative "player"
require_relative 'star'
require_relative 'z_order'
require_relative 'bomb'

class GameWindow < Gosu::Window
	
	def initialize
		super 640, 480
    self.caption = "Gosu Tutorial Game"

    @background_image = Gosu::Image.new("media/space.png", :tileable => true)

    @player = Player.new
    @player.warp(320, 240)

    @star_anim = Gosu::Image::load_tiles("media/star.png", 25, 25)
    @stars = Array.new
    @font = Gosu::Font.new(20)
    @bombs = Array.new
	end

	def update
		@player.turn_left if Gosu::button_down? Gosu::KbLeft
		@player.turn_right if Gosu::button_down? Gosu::KbRight
		@player.accelerate if Gosu::button_down? Gosu::KbUp
		@player.move
		@player.collect_stars(@stars)

		if rand(100) < 4 and @stars.size < 25 then
      @stars.push(Star.new(@star_anim))
    end

    if rand(200) < 2 and @bombs.size < 25 then
      @bombs.push(Bomb.new)
    end

    @bombs.each do |bomb|
			bomb.update
			@bombs.delete(bomb) if bomb.explosion? == 1
		end
    
	end

	def draw
		@background_image.draw(0, 0, ZOrder::Background)
    @player.draw
    @stars.each { |star| star.draw }
    @bombs.each { |bomb| bomb.draw}
    @font.draw("Score: #{@player.score}", 10, 10, ZOrder::UI, 1.0, 1.0, 0xff_ffff00)

	end

	def button_down(id)
		close if id == Gosu::KbEscape
	end


end

window = GameWindow.new
window.show