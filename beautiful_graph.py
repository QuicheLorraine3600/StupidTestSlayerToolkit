#Script to draw a beautiful graph
from PIL import Image, ImageDraw, ImageFont
import math

pipeline_stages_input = input("Pipeline Stages: ")
forwarding_paths_input = input("Forwarding Paths: ")
PIPELINE_STAGES_STR = "F-D-E1-E2-E3-M1-M2-M3-M4-W" if pipeline_stages_input == "" else pipeline_stages_input
FORWARDING_PATHS_STR = "E3->E1, M1->E1, M2->E1, M4->E1" if forwarding_paths_input == "" else forwarding_paths_input

pipeline_stages = PIPELINE_STAGES_STR.split("-")
forwarding_paths = list(filter(lambda stage: stage != "E1", FORWARDING_PATHS_STR.replace("->", " ").replace(", ", " ").split(" ")))

IMAGE_MARGINS = 50
NODE_RADIUS = 50
SPACE_BETWEEN_NODES = 100
SPACE_BETWEEN_FORWARDING_PATHS = 10
ARROWHEAD_SIZE = 7
FONT = ImageFont.truetype('Arial.ttf', 40)

IMAGE_WIDTH = 2*IMAGE_MARGINS + 2*NODE_RADIUS*len(pipeline_stages) + SPACE_BETWEEN_NODES*(len(pipeline_stages) - 1)
IMAGE_HEIGHT = 600

def draw_centered_text(x, y, text, fontColor="white"):
    _, _, w, h = draw.textbbox((0, 0), text, font=FONT)
    draw.text((x - w/2, y - h/2), text, font=FONT, fill=fontColor)

def draw_node(x, y, name, fontColor="white"):
	draw.arc((x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS), start=0, end=360, fill=(255, 255, 0))
	draw_centered_text(x, y, name, fontColor=fontColor)

def draw_arrow(ptA, ptB, width=1, color=(0,255,0)):
	"""Draw line from ptA to ptB with arrowhead at ptB from https://stackoverflow.com/questions/63671018/how-can-i-draw-an-arrow-using-pil"""
	  # Draw the line without arrows
	draw.line((ptA,ptB), width=width, fill=color)

	x0, y0 = ptA
	x1, y1 = ptB
	# Now we can work out the x,y coordinates of the bottom of the arrowhead triangle
	xb = x1 if x1 == x0 else (x1 - ARROWHEAD_SIZE) if x1 > x0 else (x1 + ARROWHEAD_SIZE)
	yb = y1 if y1 == y0 else (y1 - ARROWHEAD_SIZE) if y1 > y0 else (y1 + ARROWHEAD_SIZE)

	# Work out the other two vertices of the triangle
	# Check if line is vertical
	if x0==x1:
		vtx0 = (xb-5, yb)
		vtx1 = (xb+5, yb)
	# Check if line is horizontal
	elif y0==y1:
		vtx0 = (xb, yb+5)
		vtx1 = (xb, yb-5)
	else:
		alpha = math.atan2(y1-y0,x1-x0)-90*math.pi/180
		a = 8*math.cos(alpha)
		b = 8*math.sin(alpha)
		vtx0 = (xb+a, yb+b)
		vtx1 = (xb-a, yb-b)

	draw.polygon([vtx0, vtx1, ptB], fill=color)

def draw_arrow_with_waypoints(ptA, ptB, waypoints=[], width=1, color=(0,255,0)):
	waypoints.insert(0, ptA)
	last_waypoint = waypoints[len(waypoints) - 1]
	draw.polygon(waypoints, width=width, fill=color)
	draw_arrow(last_waypoint, ptB, width=width, color=color)

image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), "black")
draw = ImageDraw.Draw(image)

node_positions = {"RF": (IMAGE_WIDTH / 2, IMAGE_MARGINS + NODE_RADIUS)}
e_forwarding_paths_y_offset = 1.3*NODE_RADIUS
m_forwarding_paths_y_offset = 1.3*NODE_RADIUS
for i in range(len(pipeline_stages)):
	stage = pipeline_stages[i]
	x = IMAGE_MARGINS + NODE_RADIUS + i*(SPACE_BETWEEN_NODES + 2 * NODE_RADIUS)
	y = IMAGE_HEIGHT / 2

	node_positions[stage] = (x, y)

	draw_node(x, y, stage, fontColor="white")
	if i < len(pipeline_stages) - 1:
		draw_arrow((x + NODE_RADIUS + 1, y), (x + NODE_RADIUS + SPACE_BETWEEN_NODES - 1, y))
		if stage in forwarding_paths:
			draw_node(x, y, stage, fontColor="red")
			line_x = x + NODE_RADIUS + SPACE_BETWEEN_NODES / 2
			draw.line((line_x, y - 2*NODE_RADIUS, line_x, y + 2*NODE_RADIUS))

			e_x, e_y = node_positions["E1"]
			j = 0
			if stage.startswith("E"):
				j = y - e_forwarding_paths_y_offset
				draw_arrow_with_waypoints((line_x, j), (e_x, e_y - NODE_RADIUS - 1), waypoints=[(e_x, j)])
				e_forwarding_paths_y_offset += SPACE_BETWEEN_FORWARDING_PATHS			
			else:
				j = y + m_forwarding_paths_y_offset
				draw_arrow_with_waypoints((line_x, j), (e_x, e_y + NODE_RADIUS + 1), waypoints=[(e_x, j)])
				m_forwarding_paths_y_offset += SPACE_BETWEEN_FORWARDING_PATHS
			draw.rectangle((line_x - ARROWHEAD_SIZE, j - ARROWHEAD_SIZE, line_x+ARROWHEAD_SIZE, j + ARROWHEAD_SIZE), fill="red")


rf_x, rf_y = node_positions["RF"]
w_x, w_y = node_positions["W"]
d_x, d_y = node_positions["D"]
draw_arrow_with_waypoints((w_x, w_y - NODE_RADIUS - 1), (rf_x + NODE_RADIUS + 1, rf_y), waypoints=[(w_x, rf_y)])
draw_node(rf_x, rf_y, "RF")
draw_arrow_with_waypoints((rf_x - NODE_RADIUS - 1, rf_y), (d_x, d_y - NODE_RADIUS - 1), waypoints=[(d_x, rf_y)])

image.show()