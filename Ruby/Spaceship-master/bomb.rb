require "gosu"
require_relative 'z_order'
# require_relative 'main'

class Bomb
	
	attr_reader :x, :y
	delta = 3.0

	def initialize
	  @img = Gosu::Image.new("media/bomb.png")
    @x = rand * 640
    @y = rand * 480
    @start_time = Time.now
    @end_time = @start_time + 3
    @explosion = 0
  end

  def draw  
    @img.draw(
    	@x - @img.width / 2.0,
    	@y - @img.height / 2.0,
      ZOrder::Bombs)
  end


 	def update
		if Time.now > @end_time
			@img = Gosu::Image.new("media/explode.png")
		end
		if Time.now > @end_time + 1
			@explosion = 1
		end
	end
	def explosion?
		@explosion
	end

end