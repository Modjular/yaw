import json
import napari
import redis
from skimage import data
from magicgui import magicgui
from napari.utils.notifications import show_info

r = redis.Redis(host='localhost', port=6379, db=0)


@magicgui(call_button="Yaw")
def yaw_widget(viewer: napari.Viewer):
    """ Start worker to communicate with device """
    show_info('Starting yaw...')

    # Callback for responding to angle changes
    def callback(message):
        orientation = json.loads(message['data'])

        angles = (
            -orientation['roll'],
            -orientation['yaw'],
            orientation['pitch'] + 90,
        )

        viewer.camera.angles = angles

    pubsub = r.pubsub()
    pubsub.subscribe(**{'orientation': callback})
    pubsub.run_in_thread(sleep_time=1.0 / 24)


if __name__ == "__main__":
    v = napari.Viewer(ndisplay=3)
    v.add_image(data.brain(), colormap='inferno')
    v.window.add_dock_widget(yaw_widget)
    v.dims.ndisplay = 3

    napari.run()
