require_relative 'bank_account.rb'
class User
	attr_accessor :name, :pin, :balance
	def initialize(name, pin, login = 0)
		@name = name
		@pin = pin
		@login = 0
	end

	def login
		pin = gets.to_i
		if pin == @pin
			puts "Hello #{name}!"
			@login = 1
		end
	end

	def atm
		if @login == 1
			while cmd != "e" do
				puts "Would you like to (w)ithdraw, (d)eposit or (c)heck your balance?"
				puts "You can also (e)nd your session."
				cmd = gets.chomp

			case cmd
			when "w"
			  puts "How much would you like to withdraw?"
			  amount = gets.chomp
			  account.withdraw(amount)
			 when "d"
			 	puts "How much would you like to deposit?"
		 	 	amount = gets.chomp
		 	 	account.deposit(amount)
			when "c"
		 		puts "Your balance is $%.2f\n" % account.balance
			else
		  	puts "Didn't understand your command. Try again." unless cmd == "e"
			end

		end
		else
			puts "Not logged in"
		end
	end
		

end