import json
import napari
import redis
from tifffile import imread
from magicgui import magicgui
from napari.utils.notifications import show_info
# from napari._vispy.utils.quaternion import quaternion2euler
# from vispy.util.quaternion import Quaternion

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

        # # TODO: Is this necessary now that jank is solved?
        # # Convert to a quaternion to regularize the angles
        # q = Quaternion.create_from_euler_angles(
        #     *angles,
        #     degrees=True
        # )

        # angles = quaternion2euler(q, degrees=True)

        viewer.camera.angles = angles

    pubsub = r.pubsub()
    pubsub.subscribe(**{'orientation': callback})
    pubsub.run_in_thread(sleep_time=1.0 / 24)


if __name__ == "__main__":
    data = imread('/Users/tony/Documents/Translucence/Atlas/annotation_25_right_int.tif')
    data = data.squeeze()

    v = napari.Viewer(ndisplay=3)
    v.add_image(data, contrast_limits=[300, 2000], colormap='inferno')
    v.window.add_dock_widget(yaw_widget)

    napari.run()
