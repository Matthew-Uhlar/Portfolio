class Account

	def initialize(name, pin)
		@name = nil
		@pin = nil
		@amount = nil
		@people = nil
		@new = false
		people = []
		file = File.open("account.txt")
		people = file.read.split("\n")
		people_final = []
		people.each do |n|
			people_final.push(n.split(", "))
		end
		@people = people_final
		if find_person(name, pin) != nil
			@name = @people[find_person(name, pin)][0]
			@pin = @people[find_person(name, pin)][1]
			@amount = @people[find_person(name, pin)][2].to_i
		else
			@name = name 
			@pin = pin 
			@amount = 0
		end
	end

	def get_name
		@name
	end

	def get_pin
		@pin
	end

	def get_amount
		@amount
	end

	def deposit(amount)
		@amount += amount
	end

	def withdraw(amount)
		if @amount > amount
			@amount -= amount
		else
			puts "You do not have sufficient funds"
		end
	end

	def add_account(name, pin)
		@name = name
		@pin = pin
		@amount = 0
		@new = true
	end

	def exit
		string = ""
		@people.each do |person|
			if person[0] == @name && person[1] == @pin
				string += person[0] + ", " + person[1] + ", " + @amount.to_s
			else
				if person[0] != nil && person[1] != nil && person[2] != nil
					string += person[0] + ", " + person[1] + ", " + person[2]
				end
			end
			string += "\n"
		end
		if @new
			string += @name + ", " + @pin + ", " + @amount.to_s
		end
		File.write("account.txt", string)
	end

	def find_person(name, pin)
		person_f = nil
		@people.each do |person|
			if person[0] == name && person[1] == pin
				person_f = person
			end
		end
		@people.index(person_f)
	end

end