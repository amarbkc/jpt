from flask import Flask, request, render_template, jsonify
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def check_cubes(ver, a, b, c, d):
    t_sum = 0
    for v in ver[0]:
        if (a*v[0]+b*v[1]+c*v[2]+d) > 0:
            t_sum += 1
    return t_sum  

def check_side(face, a, b, c, d):
    t_sum = 0
    for points in face:
        if (a*points[0]+b*points[1]+c*points[2]+d) > 0:
            t_sum += 1
    return t_sum   

def projec(face, a, b, c, d):
    projection = []
    for points in face:
        t = (-d-a*points[0]-b*points[1]-c*points[2])/(a**2+b**2+c**2)
        projection.append((points[0]+a*t, points[1]+b*t))
    return projection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    try:
        a = float(request.form['a'])
        b = float(request.form['b'])
        c = float(request.form['c'])
        d = float(request.form['d'])
    except ValueError:
        return jsonify({'error': 'Invalid input. Please provide numeric values for a, b, c, and d.'})

    cubes = np.empty((1, 8, 3))
    for x in range(-10, 10):
        for y in range(-10, 10):
            for z in range(-15, 15):
                vertice = [[[x, y, z], [x+1, y, z], [x+1, y+1, z], [x, y+1, z],
                            [x, y, z+1], [x+1, y, z+1], [x+1, y+1, z+1], [x, y+1, z+1]]]
                if check_cubes(vertice, a, b, c, d) != 0 and check_cubes(vertice, a, b, c, d) != 8:
                    cubes = np.append(cubes, vertice, axis=0)

    pro_tials =[[],[],[],[],[],[]]
    for square in cubes:
        bottom = [square[0], square[1], square[2], square[3]]
        if check_side(bottom, a, b, c, d) == 0:
            pro_tials[0].append(projec(bottom, a, b, c, d))     
        top = [square[4], square[5], square[6], square[7]]
        if check_side(top, a, b, c, d) == 0:
            pro_tials[1].append(projec(top, a, b, c, d))
        front = [square[0], square[1], square[5], square[4]]
        if check_side(front, a, b, c, d) == 0:
            pro_tials[2].append(projec(front, a, b, c, d))
        back = [square[2], square[3], square[7], square[6]]
        if check_side(back, a, b, c, d) == 0:
            pro_tials[3].append(projec(back, a, b, c, d))
        right = [square[1], square[2], square[6], square[5]]
        if check_side(right, a, b, c, d) == 0:
            pro_tials[4].append(projec(right, a, b, c, d))
        left = [square[3], square[0], square[4], square[7]]
        if check_side(left, a, b, c, d) == 0:
            pro_tials[5].append(projec(left, a, b, c, d))      

    colour = ["red", "yellow", "blue"]
    for i in range(6):
        if i == 0 or i == 1:
            co = colour[0]
        elif i == 2 or i == 4:
            co = colour[1]    
        elif i == 3 or i == 5:
            co = colour[2]    
        for quad in pro_tials[i]:
            if len(pro_tials[i]) != 0:
                x_coords, y_coords = zip(*quad)
                plt.plot(x_coords + (x_coords[0],), y_coords + (y_coords[0],), color='black')
                plt.fill(x_coords + (x_coords[0],), y_coords + (y_coords[0],), color=co, alpha=0.5)

    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.xlim([-10, 10])
    plt.ylim([-10, 10])

    png_image = io.BytesIO()
    plt.savefig(png_image, format='png')
    png_image.seek(0)
    png_base64 = base64.b64encode(png_image.getvalue()).decode('ascii')

    plt.close()
    return jsonify({'plot': png_base64})

if __name__ == '__main__':
    app.run(debug=True)
