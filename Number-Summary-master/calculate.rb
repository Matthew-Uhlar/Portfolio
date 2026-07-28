require_relative 'number_summary'

a = (1..6).map { |i| i }
print a, "\n"

puts NumberSummary.summarize('data.csv')