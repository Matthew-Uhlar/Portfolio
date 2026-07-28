# ATM

---

#### Purpose:
To provide the user with an ATM that allows them to store their information and view it by entering their pin in order to make deposits and withdraws provided they have enough money.


---
#### Getting Started:
Open Git Bash inside of the ATM file. Then inside the command line enter the command to run the program.
```sh
$ ruby atm.rb
```

---
#### Questions
- More clarification on how classes inherit specific code from the parent class. For example, when making a child class how would you change an initialize variable that overlaps with one of the parent.
```sh
def initialize(x, y, width, height, z, mode)

		@x = y
		@y = x
		@fill = Gosu::Color.argb(0xff_f00000)
		@stroke = Gosu::Color.argb(0xff_00ff00)
		@width = width
		@height = height
		@mode = mode
		@z = z
		@fillheight = @y + @height
	end
```
- Saving information to a text file then refrencing it later in the code.
```sh
 File.open(yourfile, 'w') { |file| file.write("your text") }
```
- Filling in a triangle by drawing multiple lines to fill the area.
```sh
		def draw_triangle
			Gosu.draw_line(@x, @y, @stroke, @x + @width, @y + @width, @stroke, @z, :default)
			Gosu.draw_line(@x, @y, @stroke, @x, @y + @width, @stroke, @z, :default)
			# Gosu.draw_line(@x + @width, @y, @stroke, @x + @width, @y + @width, @stroke, @z, :default)
			Gosu.draw_line(@x, @y + @width, @stroke, @x + @width, @y + @width, @stroke, @z , :default)
		end

		def fill_shape
			for i in (@y..@fillheight) 
				Gosu.draw_line(@x, i, @fill, @x + @width, i + @width, @fill, -1, :default)
				# Gosu.draw_line(@x, i, @fill, @x + @width, i + @width, @fillblack, -1, :default)
			end
		end*Math.sqrt(2)/2,
```