import svgwrite
from functools import reduce
from operator import mul


def draw_grid_point(drawing, *, x_offset, y_offset, radius, color, stroke_width=2, fill_color='#ffffff', fill_opacity=0):

    drawing.add(svgwrite.shapes.Circle(
        center=(x_offset, y_offset),
        style='fill: %s; fill-opacity:%d; stroke-width: %d; stroke: %s' % (
            fill_color, 
            fill_opacity, 
            stroke_width, 
            color
        ),
        r=radius,
    ))

def draw_onset_grid(drawing, grid, *, x_offset, y_offset, spacing, radius, color, stroke_width):

    # Draw equidistant circles for each position in the grid
    for position, onset in enumerate(grid):

        fill_opacity = 0

        if onset == 1:
            fill_opacity = 100

        draw_grid_point(
            drawing, 
            x_offset=x_offset + position * spacing,
            y_offset=y_offset,
            radius=radius,
            color=color,
            fill_color=color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width,
        )

    return drawing


def draw_metrical_grid(drawing, length, subdivisions, *, x_offset, y_offset, spacing, radius, color, stroke_width, phase=0):

    for position in range(length):

        for level in range(len(subdivisions)):

            period = reduce(mul, subdivisions[:level+1])

            if (position + phase) % period == 0:

                draw_grid_point(
                    drawing, 
                    x_offset=x_offset + position * spacing,
                    y_offset=y_offset + level * spacing,
                    radius=radius,
                    color=color,
                    fill_color=color,
                    fill_opacity=100,
                    stroke_width=stroke_width,
                )

    return drawing

def test():

    grid = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0]
    grid = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1] * 2
    subdivisions = [1, 3, 2, 2]
    phase = 0

    spacing = 50
    drawing_properties = {
        'stroke_width':2,
        'spacing':spacing,
        'radius':10
    }


    drawing = svgwrite.Drawing(filename='grid.svg', profile='basic')

    drawing = draw_onset_grid(drawing, grid, 
            x_offset=spacing, 
            y_offset=spacing, 
            color='#000000', 
            **drawing_properties)
    drawing = draw_metrical_grid(drawing, len(grid), subdivisions, phase=phase,
            x_offset=spacing, 
            y_offset=2 * spacing, 
            color='#c8c8c8', 
            **drawing_properties)
    drawing.save()

if __name__ == '__main__':
    test()

