import pyvista as pv
from pyvista import examples

mesh = examples.download_st_helens().warp_by_scalar()

p = pv.Plotter(off_screen=True)  # Added off_screen=True to avoid showing the plotter window too early
p.add_mesh(mesh, lighting=False)
p.show_grid()

viewup = [1, 1, 1]
path = p.generate_orbital_path(factor=3, shift=10000, n_points=36)
p.open_movie('orbit.mp4', framerate=5)
p.orbit_on_path(path, write_frames=True, viewup=[0, 0, 1], step=2)
p.close()

# Show the plotter window after the orbit_on_path function has been called
p = pv.Plotter()
p.add_mesh(mesh, lighting=False)



p.show_grid()
p.show(auto_close=True)
