

			file = File.open("data.csv", 'r')

			array = []

			file.each_line do |line|
				array = line.split(',')
			end

		def min(array)
			puts "min: #{array.min}"
		end

		def max(array)
			puts "max: #{array.max}"	
		end

		def average(array)
			total = 0
			average = 0
			array.each do |element|
			total += element.to_f
		end
			average = total / array.length
			puts "mean: #{average}"
		end

	def mode(array)
		var = 0
		mode = 0
		prevVar = 0
		array.each do |i|
			array.each do |n|
				if i == n
					var += 1
					mode = n if var > prevVar
					prevVar = var
				end
			end
			var = 0
		end
		puts "mode: #{mode}"
	end

	def median(array)
		sorted = array.sort
		length = array.length
		median = 0

		if length%2 == 0
			first = sorted[length/2 - 1]
			second = sorted[length/2] 

			median = (first + second) / 2
		else
			median = sorted[(length-1)/2]
		end
		puts "median: #{median}"
	end

	def quartile(array)
  	array.sort!
  	split = median_split array
  	case n
  	when 1
    	median split[0]
  	when 2
    	median arr
  	when 3
    	median split[1]
  end

	def mode2(array)
		most = array.inject(Hash.new(0)) { |h,v| h[v] += 1; h }
		array.max_by { |v| most[v] }
	end

	def q1(array)
		if array.length % 2 == 0 
			array_final = array[0..(array.length/2 - 1)]
		else
			array_final = array[0..(array.length/2)]
		end	
			
		median(array_final)
	end

	def q3(array)
		if array.length % 2 == 0
			array_final = array[(array.length/2)...array.length]
		else
			array_final = array[(array.length/2 + 1)...array.length]
		end
			
		median(array_final)
		puts "q3: #{q3}"
	end

	def sigma(array)
		variation = mean(array)
		puts variation
		array_dif = []
		(0...array.length).each do |n|
			array_dif.push((array[n] - variation)**2)
		end	
		mean(array_dif)
	end

end

		puts "Number Summary:"
		min(array)
		max(array)
		average(array)
		median(array)  
		mode(array)
		q1(array)
		q3(array)
