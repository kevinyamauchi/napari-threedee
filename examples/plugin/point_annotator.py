import napari
from skimage import data

# create a napari viewer
viewer = napari.Viewer(ndisplay=3)

# generate image data
blobs = data.binary_blobs(length=64, volume_fraction=0.1, n_dim=4).astype(float)

# add two image layers and a points layer to the viewer
viewer.add_image(
    blobs,
    name='orange plane',
    rendering='average',
    colormap='bop orange',
    blending='additive',
    opacity=0.5,
    depiction='plane',
    plane={
        'position': (32, 32, 32),
        'normal': (1, 0, 0),
        'thickness': 10,
    })

viewer.add_image(
    blobs,
    name='blue plane',
    rendering='average',
    colormap='bop blue',
    blending='additive',
    opacity=0.5,
    depiction='plane',
    plane={
        'position': (32, 32, 32),
        'normal': (0, 1, 0),
        'thickness': 10,
    })

# add an empty points layer to the viewer
viewer.add_points([], ndim=4, face_color='cornflowerblue', size=3)

# add the plugin dock widget to the viewer
viewer.window.add_plugin_dock_widget(
    plugin_name="napari-threedee", widget_name="point annotator",
)

# run napari
viewer.layers.selection = [viewer.layers[0]]
viewer.axes.visible = True
viewer.camera.angles = (-15, 25, -30)
viewer.camera.zoom *= 0.5
napari.run()
