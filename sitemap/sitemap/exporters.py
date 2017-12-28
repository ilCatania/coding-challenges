from  scrapy.exporters import BaseItemExporter
import networkx as nx
import plotly.offline as pyo
from plotly.graph_objs import *


class NetworkGraphExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.file = file
        self.G = nx.DiGraph()

    def export_item(self, item):
        for l in item['links']:
            self.G.add_edge(item['path'], l)

    def finish_exporting(self):
        pos = nx.fruchterman_reingold_layout(self.G)
        nodes = list(self.G.nodes())
        Xv = [pos[n][0] for n in nodes]
        Yv = [pos[n][1] for n in nodes]
        Xed = []
        Yed = []
        for edge in self.G.edges:
            Xed += [pos[edge[0]][0], pos[edge[1]][0], None]
            Yed += [pos[edge[0]][1], pos[edge[1]][1], None]

        axis = dict(showline=False,
                    # hide axis line, grid, ticklabels and  title
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    title=''
                    )
        layout = Layout(
            title="Site Map",
            font=Font(size=12),
            showlegend=False,
            autosize=False,
            width=800,
            height=800,
            xaxis=XAxis(axis),
            yaxis=YAxis(axis),
            margin=Margin(
                l=40,
                r=40,
                b=85,
                t=100,
            ),
            hovermode='closest',
            annotations=Annotations([
                Annotation(
                    showarrow=False,
                    text='',
                    xref='path',
                    yref='path',
                    x=0,
                    y=-0.1,
                    xanchor='left',
                    yanchor='bottom',
                    font=Font(
                        size=14
                    )
                )
            ]),
            )
        trace1 = Scatter(x=Xed,
                         y=Yed,
                         mode='lines',
                         line=Line(color='rgb(210,210,210)', width=1),
                         hoverinfo='none'
                         )
        trace2 = Scatter(x=Xv,
                         y=Yv,
                         mode='markers',
                         name='net',
                         marker=Marker(symbol='dot',
                                       size=5,
                                       color='#6959CD',
                                       line=Line(color='rgb(50,50,50)',
                                                 width=0.5)
                                       ),
                         text=list(self.G.nodes),
                         hoverinfo='text'
                         )

        fig1 = Figure(data=Data([trace1, trace2]), layout=layout)
        pyo.plot(fig1, filename=self.file.name)
