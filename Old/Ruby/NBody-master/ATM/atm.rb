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
  Matt.atm


end