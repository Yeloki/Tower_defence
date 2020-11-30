import math

def draw_better_line(screen, point1, point2, color, width):
    x1, y1 = point1
    x2, y2 = point2
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    udx = dx / length
    udy = dy / length
    perpendicular_x = -udy * width
    perpendicular_y = udx * width

    # "left" line start
    x1_ = x1 + perpendicular_x
    y1_ = y1 + perpendicular_y

    # "left" line end
    x2_ = x1_ + dx
    y2_ = y1_ + dy

    # "right" line start
    x1__ = x1 - perpendicular_x
    y1__ = y1 - perpendicular_y

    # "right" line start
    x2__ = x1__ + dx
    y2__ = y1__ + dy
    pygame.draw.polygon(screen, color, ((x1_, y1_), (x2_, y2_), (x2__, y2__), (x1__, y1__)))