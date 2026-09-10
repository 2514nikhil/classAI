import os


def clear_screen():
	"""Clears the terminal screen so the board updates in place."""
	os.system("cls" if os.name == "nt" else "clear")


def print_board(state):
	"""Prints the board in a simple, easy-to-read way."""
	print("\n-------------")
	for i in range(0, 9, 3):
		row = []
		for number in state[i:i + 3]:
			row.append(" " if number == 0 else str(number))

		print(f"| {row[0]} | {row[1]} | {row[2]} |")
		print("-------------")


def get_possible_moves(state):
	"""Returns the possible Up, Down, Left, and Right moves."""
	moves = []
	zero_index = state.index(0)
	row = zero_index // 3
	col = zero_index % 3

	if row > 0:
		new_state = list(state)
		new_state[zero_index], new_state[zero_index - 3] = (
			new_state[zero_index - 3],
			new_state[zero_index],
		)
		moves.append((tuple(new_state), "Up"))

	if row < 2:
		new_state = list(state)
		new_state[zero_index], new_state[zero_index + 3] = (
			new_state[zero_index + 3],
			new_state[zero_index],
		)
		moves.append((tuple(new_state), "Down"))

	if col > 0:
		new_state = list(state)
		new_state[zero_index], new_state[zero_index - 1] = (
			new_state[zero_index - 1],
			new_state[zero_index],
		)
		moves.append((tuple(new_state), "Left"))

	if col < 2:
		new_state = list(state)
		new_state[zero_index], new_state[zero_index + 1] = (
			new_state[zero_index + 1],
			new_state[zero_index],
		)
		moves.append((tuple(new_state), "Right"))

	return moves


def solve_dfs(start_state):
	"""Finds a path to the goal using Depth-First Search."""
	goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
	stack = [(start_state, [])]
	visited = {start_state}

	while stack:
		current_state, path = stack.pop()

		if current_state == goal_state:
			return path

		for next_state, move_direction in get_possible_moves(current_state):
			if next_state not in visited:
				visited.add(next_state)
				stack.append((next_state, path + [move_direction]))

	return None


def play_game():
	current_state = (1, 2, 3, 4, 5, 6, 7, 0, 8)
	goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
	message = "Welcome to the 8-Puzzle! (DFS Mode)"

	while True:
		clear_screen()
		print_board(current_state)
		print(f"\n{message}\n")

		if current_state == goal_state:
			print("You won!")
			break

		print("Controls: W (Up) | S (Down) | A (Left) | D (Right)")
		print("Type 'H' for Help or 'Q' to Quit.")

		user_input = input("\nEnter move: ").upper()

		if user_input == "Q":
			print("Thanks for playing!")
			break

		if user_input == "H":
			message = "Thinking..."
			clear_screen()
			print_board(current_state)
			print(f"\n{message}\n")

			solution = solve_dfs(current_state)
			if solution is None:
				message = "DFS could not find a solution."
			else:
				message = (
					f"DFS says you can win in {len(solution)} moves!\n"
					f"Path: {solution}"
				)
			continue

		direction = ""
		if user_input == "W":
			direction = "Up"
		elif user_input == "S":
			direction = "Down"
		elif user_input == "A":
			direction = "Left"
		elif user_input == "D":
			direction = "Right"
		else:
			message = "Invalid key! Use W, A, S, D, H, or Q."
			continue

		move_was_successful = False
		for next_state, move_name in get_possible_moves(current_state):
			if move_name == direction:
				current_state = next_state
				move_was_successful = True
				message = f"Moved {direction}."
				break

		if not move_was_successful:
			message = "You can't move that way! You hit a wall."


if __name__ == "__main__":
	play_game()
