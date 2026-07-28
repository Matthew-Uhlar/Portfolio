require 'minitest/autorun'
require "minitest/reporters"
Minitest::Reporters.use! Minitest::Reporters::SpecReporter.new

require_relative 'utilities'

class Methods2Test < MiniTest::Test
	def setup
		@m = Class.new do
     include Utilities
   	end.new
	end

	# Tests go here
	def test_leap_year
		assert_equal true, @m.leap_year(800)
		assert_equal false, @m.leap_year(799)
		assert_equal true, @m.leap_year(8)
		assert_equal false, @m.leap_year(700)
		assert_equal true, @m.leap_year(888)
	end

	def test_year_percent
		assert_equal '200.0%', @m.year_percent(63072000)
		assert_equal '100.0%', @m.year_percent(31536000)
		assert_equal '50.0%', @m.year_percent(15768000)
		assert_equal '25.0%', @m.year_percent(7884000)
		assert_equal '0.0%', @m.year_percent(0)
	end

	def test_military_time
		assert_equal "8:00", @m.military_time("8:00 am")
		assert_equal "24:00", @m.military_time("12:00 am")
		assert_equal "18:00", @m.military_time("6:00 pm")
		assert_equal "1:00", @m.military_time("1:00 am")
	end

end
