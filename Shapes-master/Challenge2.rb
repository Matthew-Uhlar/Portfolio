puts "We're trying to write a farily tale, but we could use a litle bit of help. Give us a hand by filling out a few words:"
puts " "
puts "Type in a girl's name and press enter"
girl_name = gets.chomp
puts "Type in a living thing and press enter"
living_thing = gets.chomp
puts "Type in an adjective (big, cold, smelly) and press enter"
adj = gets.chomp
puts "Type in another adjective and press enter"
adj_2 = gets.chomp
puts "Type in a noun (book, cup, muffin) and press enter"
noun = gets.chomp
puts "Type in a verb (smile, punch, sniff) and press enter"
verb = gets.chomp
puts "Type in another verb and press enter"
verb_2 = gets.chomp
puts "Type in a past-tense verb and press enter"
past_verb = gets.chomp


puts "phew! Thanks, we couldn't have done it without you.  Here's the finished story:"
puts " "
puts "THE FAIRLY TALE"
puts "---------------"
puts "Once upon a time there was a poor little girl named " + girl_name + " who lived in the forest with a(n) " + adj + " " + living_thing + ".  She was forced to " + verb + " all day  while the " + living_thing + " sat around " + verb_2 + "ing." 
puts ""
puts "But then one day the little girl found a magic " + noun + ". When " + girl_name +" picked up the " + noun + ", she found that anything she imagined came true. Soon, " + girl_name + " was making the " + living_thing + " " + verb + " while she choose to sit around and " + verb_2 +"." 
puts ""
puts "After a while, the girl realized this was not a very " + adj_2 + " thing to do and released the " + living_thing + " from her spell. They became best friends and " + past_verb + " every day, living happily ever after." 
