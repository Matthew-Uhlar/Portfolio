require "gosu"

class Planet

	attr_reader :xpos, :ypos, :xvel, :yvel, :mass

	G = 6.67408e-11.to_f
	
	def initialize data, system_size, window_size
		@system_size, @window_size = system_size, window_size
		@xpos, @ypos = data[0].to_f, data[1].to_f
		@xvel, @yvel = data[2].to_f, data[3].to_f
		@force = 0.0
		@mass = data[4].to_f
		@image = Gosu::Image.new("images/#{data[5]}")
	end

	def warp x, y
		@x, @y = x, y
	end

	def draw
		@image.draw(@xpos/@system_size*@window_size + @window_size/2,@ypos/@system_size*@window_size + @window_size/2,1)
	end

	def move planets
		planets.each do |planet|
			@dx = planet.xpos - @xpos
			@dy = planet.ypos - @ypos
			@r = Math.sqrt(@dx**2 + @dy**2)

			if @r == 0
				@force = 0	
			elsif @dx > 0
				@force = -G*@mass*planet.mass/@r**2
				@xvel += Gosu::offset_x(Math.cos(@dx/@r), @force*@dx/@r/@mass)
				@yvel += Gosu::offset_y(Math.sin(@dy/@r), @force*@dy/@r/@mass)
			else
				@force = G*@mass*planet.mass/@r**2
				@xvel += Gosu::offset_x(Math.cos(@dx/@r), @force*@dx/@r/@mass)
				@yvel += Gosu::offset_y(Math.sin(@dy/@r), @force*@dy/@r/@mass)
			end
		end
		@xpos += @xvel*10000
		@ypos += @yvel*10000
	end

end
