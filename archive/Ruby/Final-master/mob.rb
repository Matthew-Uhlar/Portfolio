require "gosu"
require_relative "player"

class Mob

    attr_reader :x, :y

	def initialize
		@img = Gosu::Image.new("images/mob.png")
    @x = rand * 640
    @y = 10
    @vel_y = 1.5
    @gone = 0
	end

	def draw  
    @img.draw(
    	@x - @img.width / 2.0,
    	@y,
      ZOrder::Mobs)
  end

  def fall
    @y += @vel_y
    # @y %= 480
  end

  def update
    if @y > 480
      @gone = 1
    end
  end

  def gone
    @gone
  end
	
end