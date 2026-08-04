module Utilities
	
SECONDS_IN_A_YEAR = 60 * 60 * 24 * 365.0

	def leap_year(year)
		(year % 4 == 0 unless year % 100 == 0) || year % 400 == 0
	end

	def year_percent(a)
		('%.1f' % ((a / SECONDS_IN_A_YEAR) * 100)) + '%'
	end

	def military_time(x)
		is_am?(x) ? convert_am(x) : convert_pm(x)
	end

	def convert2(x)
		a, b = x.split(":")
		c = ""

		if a.to_i < 12
			c = a + b + " am"
		else
			c = a + b + " pm"
		end

		return c
	end

	def okay(a, b)
		c = false
		if (a.split(":")[0].to_i >= 8 && b || a.split(":")[0].to_i >= 10 && !b) && a.split(":")[1].split(" ")[1] == 'pm'
			c = false
		else
			c = true
		end
		return c
	end

	def span(a, b)
		c = 0
		d = 0
		if a < b
			c = b
			d = a
		else
			c = a
			d = b
		end

		return ('%.1f' % (amount(c)[0..-2].to_f - amount(d)[0..-2].to_f)).to_s + '%'
	end

	def is_am?(x)
		a, b = x.split(":")
		c, d = b.split(" ")

		d.downcase == 'am' ? true : false
	end

	def convert_am(x)
		a, b = x.split(":")
		c, d = b.split(" ")
		e = ""

		a.to_i == 12 ? e = (a.to_i + 12).to_s + ":" + c : e = a + ":" + c

		return e

	end

	def convert_pm(x)
		a, b = x.split(":")
		c, d = b.split(" ")
		e = ""

		a.to_i == 12 ? e = a + ":" + c : e = (a.to_i - 12).to_s + ":" + c

		return e
	end
end