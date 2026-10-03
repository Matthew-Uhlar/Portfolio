class NumberSummary
	
	class << self

		def return_array(fil)
			file = File.open(fil, "r")
			array = file.read
			array = array.split ","
			# arra = array.to_i
			(0...array.length).each do |n|
				array[n] = array[n].to_f
			end
			array.sort
		end

		def max(array)
			array.max
		end

		def min(array)
			array.min
		end


		def mean(array)
			sum = 0.0
			(0...array.length).each do |n|
				sum += array[n]
			end
			(sum / array.length).round(1)
		end

		def median(array)
			average = 0
			if array.length % 2 == 0
				average = (array[(array.length / 2 - 1)] + array[array.length / 2]) / 2
			else 
				return array[array.length / 2]
			end
			average.round(1)
		end

		def mode(array)
			max = 0
			array_uni = array.uniq
			array_count = []
			array_final = []
			(0...array_uni.length).each do |n|
				array_count.push(0)
			end
			(0...array.length).each do |n|
				(0...array_uni.length).each do |x|
					if array_uni[x] == array[n]
						array_count[x] += 1
					end
				end
			end
			max = array_count.max
			(0...array_count.length).each do |n|
				if array_count[n] == max
					array_final.push(array_uni[n])
				end
			end
			array_final
		end

		def q1(array)
			if array.length % 2 == 0 
				array_final = array[0..(array.length/2 - 1)]
			else
				array_final = array[0..(array.length/2)]
			end	
			
			median(array_final).round(1)
		end

		def q3(array)
			if array.length % 2 == 0
				array_final = array[(array.length/2)...array.length]
			else
				array_final = array[(array.length/2 + 1)...array.length]
			end
			
			median(array_final).round(1)
		end

		def sigma(array)
			variation = mean(array).round(1)
			array_dif = []
			(0...array.length).each do |n|
				array_dif.push(((array[n] - variation)**2).round(1))
			end	
			Math.sqrt(mean(array_dif))
		end

		def summarize(filename)
			array = return_array(filename)
			puts "Number Summary: "
			puts "min: #{NumberSummary.min(NumberSummary.return_array("data.csv"))}"
			puts "max: #{NumberSummary.max(NumberSummary.return_array("data.csv"))}"
			puts "mean: #{NumberSummary.mean(NumberSummary.return_array("data.csv"))}"
			puts "median: #{NumberSummary.median(NumberSummary.return_array("data.csv"))}"
			puts "q1: #{NumberSummary.q1(NumberSummary.return_array("data.csv"))}"
			puts "q3: #{NumberSummary.q3(NumberSummary.return_array("data.csv"))}"
			puts "mode: #{NumberSummary.mode(NumberSummary.return_array("data.csv"))}"
			puts "sigma: #{NumberSummary.sigma(NumberSummary.return_array("data.csv"))}"
		end

	end

end