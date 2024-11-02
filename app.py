from flask import Flask, render_template, jsonify, request
import plotly.graph_objects as go
import numpy as np

app = Flask(__name__)

def get_bloch_sphere(theta, phi):
    # Convert spherical angles to Cartesian coordinates for the Bloch vector
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    # Create the Bloch sphere plot with Plotly
    fig = go.Figure()

    # Add the sphere surface
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 50)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))

    fig.add_surface(x=x_sphere, y=y_sphere, z=z_sphere, opacity=0.2, colorscale='Blues', showscale=False)

    # Add the Bloch vector
    fig.add_trace(go.Scatter3d(x=[0, x], y=[0, y], z=[0, z], mode='lines+markers',
                               line=dict(color='red', width=5), marker=dict(size=4)))

    # Configure layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-1, 1], showbackground=False),
            yaxis=dict(range=[-1, 1], showbackground=False),
            zaxis=dict(range=[-1, 1], showbackground=False),
        ),
        margin=dict(l=0, r=0, b=0, t=0),
    )
    return fig

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_plot', methods=['POST'])
def update_plot():
    theta = float(request.json['theta'])
    phi = float(request.json['phi'])

    fig = get_bloch_sphere(theta, phi)
    graph_html = fig.to_html(full_html=False)
    return jsonify({'graph_html': graph_html})

if __name__ == '__main__':
    app.run(debug=True)
