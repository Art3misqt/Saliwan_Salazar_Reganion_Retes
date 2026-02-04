import turtle
import sys

# --- Configuration Constants ---
CELL_SIZE = 60 # Size of each square cell in pixels
FONT_SIZE = 14
TITLE_FONT_SIZE = 45
FONT_FAMILY = "Consolas"
PEN_COLOR = "#1f2937" # Dark blue-gray
LINE_THICKNESS = 6

# --- 1. Create the Magic Square Generator ---

def create_magic_square(n):
    """
    Generates an n x n Magic Square using the Siamese method for odd n.

    A Magic Square is a special arrangement of numbers where the sum of
    each row, column, and main diagonal is the same (the 'magic sum').

    Args:
        n (int): The odd size of the square (e.g., 3, 5, 7, 9).

    Returns:
        list: A 2D list representing the generated Magic Square.
    """
    if n % 2 == 0:
        print("Error: The Siamese method only works for odd numbers (n=3, 5, 7, ...).")
        return None

    # Initialize the n x n grid with zeros
    magic_square = [[0] * n for _ in range(n)]

    # Starting position for number 1 (middle of the top row)
    r = 0       # Row index
    c = n // 2  # Column index (integer division for middle)

    # Place numbers from 1 up to n*n
    num = 1
    total_cells = n * n

    while num <= total_cells:
        # 1. Place the current number
        magic_square[r][c] = num

        # Store the current position before moving
        prev_r, prev_c = r, c

        # 2. Move up-right for the next number (r-1, c+1)
        r = (r - 1) % n # Wrap around vertically (new row)
        c = (c + 1) % n # Wrap around horizontally (new column)

        # 3. Check if the new cell is already taken (Siamese rule)
        if magic_square[r][c] != 0:
            # If the cell is taken, the rule is to move down one square
            # relative to the previous position (not the new, blocked one)
            r = (prev_r + 1) % n
            c = prev_c
        
        num += 1

    return magic_square

# --- 2 & 3 & 4. Turtle Canvas, Grid Drawing, and Number Insertion ---

def draw_magic_square(magic_square, n):
    """
    Draws the Magic Square grid and inserts the numbers using Python Turtle.
    """
    s = turtle.Screen()
    s.setup(width=n * CELL_SIZE + 100, height=n * CELL_SIZE + 150)
    s.title(f"Magic Square Generator (n={n})")
    s.bgcolor("white")
    s.tracer(0) # Turn off screen updates for smoother drawing

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0) # Set speed to fastest
    t.pensize(LINE_THICKNESS)
    t.pencolor(PEN_COLOR)

    # Calculate the starting position (top-left corner of the grid)
    # The grid is centered at (0, 0), so the top-left corner is calculated as:
    # (-(Total Grid Width / 2), (Total Grid Height / 2))
    start_x = - (n * CELL_SIZE) / 2
    start_y = (n * CELL_SIZE) / 2

    # --- Add Title ---
    t.penup()
    # Position the title above the grid center
    t.goto(0, start_y + 40)
    t.pendown()
    t.color("#059669") # Green for the title
    t.write(f"The Magic Square (n={n})", align="center", font=("Arial", TITLE_FONT_SIZE, "bold"))
    t.color(PEN_COLOR) # Switch back to pen color

    # --- Draw Grid (Horizontal lines first) ---
    t.penup()
    t.goto(start_x, start_y)
    t.pendown()

    # Draw n+1 horizontal lines
    for _ in range(n + 1):
        t.forward(n * CELL_SIZE)
        t.backward(n * CELL_SIZE)
        t.right(90)
        t.forward(CELL_SIZE)
        t.left(90)

    # Move to the starting point for vertical lines
    t.penup()
    t.goto(start_x, start_y)
    t.setheading(270) # Point the turtle down
    t.pendown()

    # Draw n+1 vertical lines
    for _ in range(n + 1):
        t.forward(n * CELL_SIZE)
        t.backward(n * CELL_SIZE)
        t.left(90)
        t.forward(CELL_SIZE)
        t.right(90)

    # --- Insert the Numbers and Color Cells (Personal Touch) ---
    magic_sum = n* (n * n + 1) / 2
    t.setheading(0) # Reset heading to east

    for r in range(n):
        for c in range(n):
            number = magic_square[r][c]

            # Calculate center position for the number
            center_x = start_x + (c * CELL_SIZE) + (CELL_SIZE / 2)
            # Y-coordinates start from the top, so we subtract to go down
            center_y = start_y - (r * CELL_SIZE) - (CELL_SIZE / 2)

            # --- Color the Cell (Personal Touch: Even/Odd Cells) ---
            t.penup()
            t.goto(start_x + (c * CELL_SIZE), start_y - (r * CELL_SIZE))

            if number % 2 == 0:
                fill_color = "#e0f2f1" # Light Teal for Even
                number_color = "#0e7490"
            else:
                fill_color = "#fef2f2" # Light Red for Odd
                number_color = "#dc2626"

            t.fillcolor(fill_color)
            t.begin_fill()
            
            # Draw a square to fill the cell
            t.pendown()
            for _ in range(4):
                t.forward(CELL_SIZE)
                t.right(90)
            t.end_fill()
            t.penup()

            # --- Write the Number ---
            t.goto(center_x, center_y - FONT_SIZE / 2) # Adjust y slightly for vertical centering
            t.color(number_color)
            t.write(str(number), align="center", font=(FONT_FAMILY, FONT_SIZE, "bold"))


    # --- Display Magic Sum ---
    t.goto(0, start_y - n * CELL_SIZE - 40)
    t.color(PEN_COLOR)
    t.write(f"Magic Sum: {int(magic_sum)}", align="center", font=(FONT_FAMILY, 16, "normal"))

    s.update() # Final screen update to show all drawings
    s.exitonclick() # Keep the window open until clicked

# --- 5. Test With Different Sizes (Main Logic) ---

def get_numeric_input(title, prompt, valid_options=None):
    """
    Safely obtain a numeric input via turtle.numinput when available,
    otherwise fall back to textinput and convert. Returns an int or None.
    """
    # use getattr to avoid static analysis complaining about missing member
    numinput_fn = getattr(turtle, "numinput", None)
    if callable(numinput_fn):
        # use the native numinput (returns float or None)
        val = numinput_fn(title, prompt, minval=None, maxval=None)
        if val is None:
            return None
        try:
            return int(val)
        except (TypeError, ValueError):
            return None

    # fallback: use textinput and parse
    txt = turtle.textinput(title, prompt)
    if txt is None:
        return None
    try:
        return int(txt.strip())
    except (ValueError, TypeError):
        return None

def run_magic_square_app():
    """Handles user input and runs the Magic Square generation and drawing."""
    valid_sizes = [3, 5, 7, 9]

    while True:
        try:
            prompt = f"Enter an odd number (choose one of {', '.join(map(str, valid_sizes))}):"
            user_input = get_numeric_input("Magic Square Size", prompt)
            if user_input is None:
                # User cancelled -> exit cleanly
                sys.exit(0)

            n = int(user_input)
            if n in valid_sizes:
                break

            # Invalid choice: inform user and loop again (avoid opening extra windows)
            turtle.textinput("Invalid", f"Please enter one of: {', '.join(map(str, valid_sizes))}. Press OK to try again.")
        except (turtle.Terminator, SystemExit):
            # If turtle window was closed, exit
            sys.exit(0)

    magic_square = create_magic_square(n)
    if magic_square:
        draw_magic_square(magic_square, n)

if __name__ == "__main__":

    run_magic_square_app()


