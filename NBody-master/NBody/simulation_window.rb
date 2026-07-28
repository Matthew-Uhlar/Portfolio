require 'gosu'
require 'texplay'
load 'universe.rb'
class SimulationWindow < Gosu::Window
  def initialize
    super 1366, 768, false
    self.caption = "N-Body Simulation"

    @universe = Universe.new(40,1024,768)
    @universe.iterate

    @img = Gosu::Image.new(self, "atom_2.png")

    @img.paint {
      pixel 1,1, :color => :red
      pixel 1,2, :color => :red
      pixel 2,1, :color => :red
      pixel 2,2, :color => :red
    }

  end
  
  def update
    @universe.iterate
  end
  
  def draw
    @universe.particles.each do |p|
      @img.draw(p.position[:x],p.position[:y],1)  
    end
  end
end

puts "Starting Simulation..."

window = SimulationWindow.new
window.show