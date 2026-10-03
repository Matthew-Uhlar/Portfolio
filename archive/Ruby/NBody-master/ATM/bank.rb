class BankAccount
  attr_reader :name, :balance

  def initialize(name)
    @name = name
    @transactions = []
    @balance = 0.0
  end

  def withdraw(amount)
    # TODO: check that amount is valid, else error
    @balance -= amount.to_f
    # TODO: check if sufficient funds available
    puts "$%.2f successfully withdrawn.\n" % amount
  end

  def deposit(amount)
    # TODO: check that amount is valid, else error
    @balance += amount.to_f
    puts "$%.2f successfully deposited.\n" % amount
  end
end