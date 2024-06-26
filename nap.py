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

        # angles = (
        #     -orientation['roll'],
        #     -orientation['yaw'],
        #     orientation['pitch'] + 90,
        # )

        # 𝛼: An angle can range between 0 and 360 degrees
        # 𝛽: An Angle between −180 and 180 degrees
        # 𝛾: An Angle between −90 to 90 degrees

        # Experimentally determined
        angles = (
            # -orientation['roll'],   # gamma Y
            0,
            -orientation['yaw'],     # alpha Z
            # orientation['pitch'],   # beta  X
            90,
        )

        # Vispy Order: ZXY (yaw, pitch, roll), (alpha, beta, gamma)
        # angles = (
        #     orientation['yaw'],     # alpha Z
        #     orientation['pitch'],   # beta  X
        #     orientation['roll'],    # gamma Y
        # )

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
