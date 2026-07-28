require_relative "consoleadapter"
require_relative "windowadapter"

class ATM

  def initialize(specify)
    if specify == "window"
      window = WindowAdapter.new
    elsif specify == "console"
      console = ConsoleAdapter.new
    end
  end

end