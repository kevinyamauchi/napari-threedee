# Integrate an n3D component in your library

## Summary
This how to describes how to add 3D interactivity into your library by integrating a napari-threedee component. As an example, we add a camera spline annotator to the [`napari-animation`](https://github.com/napari/napari-animation) library. `napari-animation` is a library for generating animations using keyframes in napari. This tutorial assumes you have experience programming GUIs with PyQt.



## Instructions

The napari-animation plugin has a main widget `AnimationWidget` that provides the controls for defining key frames and making the animation. We will add our camera spline widget

First, we will create our widget. To keep the widget compact when it is not in use, we will wrap it in a QCollapsible widget from the [superqt](https://github.com/pyapp-kit/superqt) library. To do so, we will create a subclass of `QWidget` called `CameraSplineWidget`. 

```python
from napari import Viewer
from napari_threedee.visualization import QtCameraSpline
from qtpy.QtWidgets import QVBoxLayout, QWidget
from superqt import QCollapsible


class CameraSplineWidget(QWidget):
    """Wrap the QtCameraSpline widget in a collapsible frame."""

    def __init__(self, viewer: Viewer, parent=None):
        super().__init__(parent=parent)

        self.spline_widget = QtCameraSpline(viewer=viewer)

        self.collapsible_widget = QCollapsible("camera spline path")
        self.collapsible_widget.addWidget(self.spline_widget)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.collapsible_widget)
```


The widget all together looks like this:
```python
from napari import Viewer
from napari_threedee.visualization import QtCameraSpline
from qtpy.QtWidgets import QVBoxLayout, QWidget
from superqt import QCollapsible


class CameraSplineWidget(QWidget):
    """Wrap the QtCameraSpline widget in a collapsible frame."""

    def __init__(self, viewer: Viewer, parent=None):
        super().__init__(parent=parent)

        self.spline_widget = QtCameraSpline(viewer=viewer)

        self.collapsible_widget = QCollapsible("camera spline path")
        self.collapsible_widget.addWidget(self.spline_widget)
        self.collapsible_widget.toggled.connect(self._on_expand_or_collapse)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.collapsible_widget)

    def _on_expand_or_collapse(self, event=None):
        """Make sure the spline widget is deactivated whenever the
        collapsible is toggled.
        """
        self.spline_widget.deactivate()

```


Now we can add our Don't forget to also import 
```python
def __init__(self, viewer: Viewer, parent=None):
    super().__init__(parent=parent)
    # Store reference to viewer and create animation
    self.viewer = viewer
    self.animation = Animation(self.viewer)

    # Initialise User Interface
    self.keyframesListControlWidget = KeyFrameListControlWidget(
        animation=self.animation, parent=self
    )
    self.keyframesListWidget = KeyFramesListWidget(
        self.animation.key_frames, parent=self
    )
    self.frameWidget = FrameWidget(parent=self)
    self.saveButton = QPushButton("Save Animation", parent=self)
    self.saveButton.setEnabled(len(self.animation.key_frames) > 1)
    self.animationSlider = QSlider(Qt.Horizontal, parent=self)
    self.animationSlider.setToolTip("Scroll through animation")
    self.animationSlider.setRange(0, len(self.animation._frames) - 1)

    self.camera_spline_widget = CameraSplineWidget(
        viewer=viewer, parent=self
    )

    # Create layout
    self.setLayout(QVBoxLayout())
    self.layout().addWidget(self.keyframesListControlWidget)
    self.layout().addWidget(self.keyframesListWidget)
    self.layout().addWidget(self.frameWidget)
    self.layout().addWidget(self.saveButton)
    self.layout().addWidget(self.animationSlider)
    self.layout().addWidget(self.camera_spline_widget)

    # establish key bindings and callbacks
    self._add_keybind_callbacks()
    self._add_callbacks()
```

