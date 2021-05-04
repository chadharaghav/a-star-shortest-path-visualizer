import tkinter as tk
import tkinter.messagebox
from queue import PriorityQueue
import math


def initialise():
	global btn, btn_position, grid_rows, grid_cols, action, wall_list, start, end, g_score, f_score
	btn = []
	btn_position = dict()
	grid_rows = 20
	grid_cols = 20
	action = None
	wall_list = set()
	start = None
	end = None
	g_score = dict()
	f_score = dict()

	for i in range(grid_rows):
		for j in range(grid_cols):
			g_score[(i, j)] = math.inf
			f_score[(i, j)] = math.inf

initialise()


def changeAction(_action):
	global action
	action = _action


def makeCell(idx):
	if action == None:
		pass

	elif action == "wall":
		btn[idx].configure(background="black")
		wall_list.add(btn_position[idx])

	elif action == "remove-wall":
		if btn_position[idx] in wall_list:
			wall_list.remove(btn_position[idx])
			btn[idx].configure(background="white")

	elif action == "start":
		if btn_position[idx] in wall_list:
			return

		global start
		if not start == None:
			btn[start].configure(background="white", text=" ")

		start = idx
		btn[start].configure(background="green", text="S")


	elif action == "end":
		if btn_position[idx] in wall_list:
			return

		global end
		if not end == None:
			btn[end].configure(background="white", text=" ")

		end = idx
		btn[end].configure(background="blue", text="E")



def find_manhattan_distance(cell_one, cell_two):
	return abs(cell_one[0] - cell_two[0]) + abs(cell_one[1] - cell_two[1])



def draw_path(previous):
	current = btn_position[end]
	while current in previous:
		for k in btn_position:
			if btn_position[k] == current:
				btn[k].configure(background="green")
				break
		current = previous[current]
	btn[start].configure(background="green")

	


def a_star_search():
	global start, end, g_score, f_score

	open_cells = PriorityQueue()
	open_cells_set = set()
	done_list = set()
	flag = 0
	previous = dict()

	g_score[btn_position[start]] = 0
	f_score[btn_position[start]] = find_manhattan_distance(btn_position[start], btn_position[end])

	open_cells.put((0, flag, btn_position[start]))
	open_cells_set.add(btn_position[start])
	done_list.add(btn_position[start])

	while not open_cells.empty():
		current = open_cells.get()[2]
		open_cells_set.remove(current)

		if current == btn_position[end]:
			draw_path(previous)
			return True


		neighbours = []
		if current[0] + 1 < grid_rows:
			if (current[0] + 1, current[1]) not in wall_list and (current[0] + 1, current[1]) not in done_list:
				neighbours.append((current[0] + 1, current[1]))

		if current[0] - 1 >= 0:
			if (current[0] - 1, current[1]) not in wall_list and (current[0] - 1, current[1]) not in done_list:
				neighbours.append((current[0] - 1, current[1]))

		if current[1] + 1 < grid_cols:
			if (current[0], current[1] + 1) not in wall_list and (current[0], current[1] + 1) not in done_list:
				neighbours.append((current[0], current[1] + 1))

		if current[1] - 1 >= 0:
			if (current[0], current[1] - 1) not in wall_list and (current[0], current[1] - 1) not in done_list:
				neighbours.append((current[0], current[1] - 1))



		for neighbour in neighbours:
			temp = g_score[current] + 1

			if temp < g_score[neighbour]:
				previous[neighbour] = current
				g_score[neighbour] = temp
				f_score[neighbour] = g_score[neighbour] + find_manhattan_distance(neighbour, btn_position[end])

			if neighbour not in open_cells_set:
				flag += 1
				open_cells.put((f_score[neighbour], flag, neighbour))
				open_cells_set.add(neighbour)
				done_list.add(neighbour)

				for key in btn_position:
					if btn_position[key] == neighbour:
						btn[key].configure(background="red")
						break

	tkinter.messagebox.showinfo(title="PATH NOT FOUND", message="no valid path exists between start and end point")
	return False


def main():
	root = tk.Tk()
	root.title("A* SEARCH VISUALIZER")
	root.resizable(False, False)


	selectorFrame = tk.Frame(root)
	selectorFrame.grid(row=0, column=0)

	wall_button = tk.Button(selectorFrame, text="place wall", width=10, command=lambda: changeAction("wall"))
	wall_button.grid(row=0, column=0, padx=10, pady=10)

	remove_wall_button = tk.Button(selectorFrame, text="remove wall", width=10, command=lambda: changeAction("remove-wall"))
	remove_wall_button.grid(row=0, column=1, padx=10, pady=10)

	start_button = tk.Button(selectorFrame, text="place start", width=10, command=lambda: changeAction("start"))
	start_button.grid(row=0, column=2, padx=10, pady=10)

	end_button = tk.Button(selectorFrame, text="place end", width=10, command=lambda: changeAction("end"))
	end_button.grid(row=0, column=3, padx=10, pady=10)

	reset_button = tk.Button(selectorFrame, text="reset", width=10, command=lambda: reset(root))
	reset_button.grid(row=0, column=4, padx=10, pady=10)

	search_button = tk.Button(selectorFrame, text="find shortest path using a* search", width=50, command=a_star_search)
	search_button.grid(row=1, column=0, columnspan=5, padx=10, pady=10)


	mazeFrame = tk.Frame(root)
	mazeFrame.grid(row=1, column=0, padx=10, pady=10)


	row_flag = 0
	col_flag = 0
	for i in range(grid_rows*grid_cols):
		btn.append(tk.Button(mazeFrame, text=" ", height=1, width=2, background="white", command=lambda c=i: makeCell(c)))
		btn[i].grid(row=row_flag, column=col_flag)

		btn_position[i] = (row_flag, col_flag)

		if col_flag == grid_cols - 1:
			row_flag += 1
			col_flag = 0
		else:
			col_flag += 1


	root.mainloop()


def reset(root):
	root.destroy()
	initialise()
	main()


if __name__ == "__main__":
	main()
