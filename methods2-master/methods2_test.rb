require 'minitest/autorun'
require "minitest/reporters"
Minitest::Reporters.use! Minitest::Reporters::SpecReporter.new
require_relative 'methods2'

class Methods2Test < MiniTest::Test
	def setup
		@m = Class.new do
     include Methods2
   	end.new
	end

	def test_sleep_in
	  assert_equal true, @m.sleep_in?(false, false)
	  assert_equal false, @m.sleep_in?(true, false)
	  assert_equal true, @m.sleep_in?(false, true)
	  assert_equal true, @m.sleep_in?(true, true)
	end
	
	def test_elevenish
	  assert_equal true, @m.elevenish(22)
	  assert_equal false, @m.elevenish(13)
	  assert_equal true, @m.elevenish(33)
	  assert_equal true, @m.elevenish(11)
	end
  
  def test_ice_cream_party
		assert_equal "good", @m.ice_cream_party(6,5)
	  assert_equal "good", @m.ice_cream_party(5,5)
	  assert_equal "great", @m.ice_cream_party(33,13)
	  assert_equal "bad", @m.ice_cream_party(4,3)
	end
	
end
