require_relative 'bank_account.rb'
require_relative 'user.rb'
class Atm
  def initialize(users)
    @users = []
  end
  cmd = ""
  Matt = User.new('Matt', 1899, 0)
  Steve = User.new('Steve', 1999, 0)
  Joe = User.new('Joe', 9999, 0)
  # @users.push(Matt)
  account = BankAccount.new("Matt U")

  puts "***Welcome to #{account.name}'s ATM***\n\n"

  puts "Please input your pin to login."

  Matt.login

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
  
end