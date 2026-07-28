class BankAccount
  attr_reader :name, :balance

  def initialize(name)
    @name = name
    @transactions = []
    @balance = 0.0
  end

  def withdraw(amount)
    if @balance >= amount.to_f
      @balance -= amount.to_f
      puts "$%.2f successfully withdrawn.\n" % amount
    else
      puts "Error: Insufficient Funds."
    end
  end

  def deposit(amount)
    @balance += amount.to_f
    puts "$%.2f successfully deposited.\n" % amount
  end
end