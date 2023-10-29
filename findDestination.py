def findDestination(file_path):
  plus_count = 0
  plus_positions = []

# Read the file and process its content
  try:
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '+':
                    plus_count += 1
                    plus_positions.append((x, y))

    with open("output.txt", 'w') as output_file:
        output_file.write(f"Total '+' characters found: {plus_count}\n")
        if plus_count > 0:
            # output_file.write("Positions of '+' characters (x y 0):\n")
            for x, y in plus_positions:
                output_file.write(f"{x} {y} 0\n")

  except FileNotFoundError:
    print(f"File not found: {file_path}")
  except Exception as e:
    print(f"An error occurred: {str(e)}")

findDestination("/input/level_3/maze_destination2.txt")