"""Module providing visualization objects for Matplotlib."""
import inspect
import sys
from typing import Optional

from ansys.fluent.core.meta import PyLocalContainer

from ansys.fluent.visualization.matplotlib.matplot_windows_manager import (
    matplot_windows_manager,
)
from ansys.fluent.visualization.post_object_defns import MonitorDefn, XYPlotDefn


class Plots:
    """Matplotlib Plot objects manager.

    It provides access to plot object containers for a given session,
    from which plot objects can be created.
    It takes session object as argument. Additionally local surface provider
    can also be passed to access surfaces created in other modules e.g. pyVista.

    Attributes
    ----------
    XYPlots : dict
        Container for xyplot objects.
    MonitorPlots : dict
        Container for monitor plot objects.
    """

    _sessions_state = {}

    def __init__(self, session, local_surfaces_provider=None):
        """Instantiate Plots, container of plot objects.

        Parameters
        ----------
        session :
            Session object.
        local_surfaces_provider : object, optional
            Object providing local surfaces.
        """
        session_state = Plots._sessions_state.get(session.id if session else 1)
        if not session_state:
            session_state = self.__dict__
            Plots._sessions_state[session.id if session else 1] = session_state
            self.session = session
            self._init_module(self, sys.modules[__name__])
        else:
            self.__dict__ = session_state
        self._local_surfaces_provider = lambda: local_surfaces_provider or getattr(
            self, "Surfaces", []
        )

    def _init_module(self, obj, mod):
        from ansys.fluent.visualization.post_helper import PostAPIHelper

        for name, cls in mod.__dict__.items():

            if cls.__class__.__name__ in (
                "PyLocalNamedObjectMetaAbstract",
            ) and not inspect.isabstract(cls):
                setattr(
                    obj,
                    cls.PLURAL,
                    PyLocalContainer(self, cls, PostAPIHelper),
                )


class XYPlot(XYPlotDefn):
    """XY Plot.

    .. code-block:: python

        from ansys.fluent.visualization.matplotlib import Plots

        matplotlib_plots =  Plots(session)
        plot1 = matplotlib_plots.XYPlots["plot-1"]
        plot1.surfaces_list = ['symmetry', 'wall']
        plot1.y_axis_function = "temperature"
        plot1.plot("window-0")
    """

    def plot(self, window_id: Optional[str] = None):
        """Draw XYPlot.

        Parameters
        ----------
        window_id : str, optional
            Window id. If not specified unique id is used.
        """
        matplot_windows_manager.plot(self, window_id)


class MonitorPlot(MonitorDefn):
    """Monitor Plot.

    .. code-block:: python

        from ansys.fluent.visualization.matplotlib import Plots

        matplotlib_plots =  Plots(session)
        plot1 = matplotlib_plots.Monitors["plot-1"]
        plot1.monitor_set_name = 'residuals'
        plot1.plot("window-0")
    """

    def plot(self, window_id: Optional[str] = None):
        """Draw Monitor Plot.

        Parameters
        ----------
        window_id : str, optional
            Window id. If not specified unique id is used.
        """
        matplot_windows_manager.plot(self, window_id)
