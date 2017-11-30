import data
import vocal_lpc_phonemes
import rnn_phonems as rp
from pitch_change import pitch_change
from duration_change import duration_change
import numpy as np

from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QSizePolicy, QSlider, QComboBox, \
    QRadioButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from speaker_recognition import speaker_recognition


class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.leftLayout = QVBoxLayout(self)
        self.rightLayout = QVBoxLayout(self)
        self.mouthLayout = QHBoxLayout(self)
        self.data = data.LipSyncData.get_instance()

        self.left_layout_init()
        self.right_layout_init()

        self.dict = {}
        self.initialize_dictionary()

        self.setLayout(self.layout)

    def initialize_dictionary(self):
        self.dict[data.Phonemes.AI.name] = QPixmap('../images/mouth_types/blair_a_i.jpg')
        self.dict[data.Phonemes.E.name] = QPixmap('../images/mouth_types/blair_e.jpg')
        self.dict[data.Phonemes.U.name] = QPixmap('../images/mouth_types/blair_u.jpg')
        self.dict[data.Phonemes.O.name] = QPixmap('../images/mouth_types/blair_o.jpg')
        self.dict[data.Phonemes.etc.name] = QPixmap('../images/mouth_types/blair_c_d_g_k_n_r_s_th_y_z.jpg')
        self.dict[data.Phonemes.FV.name] = QPixmap('../images/mouth_types/blair_f_v_d_th.jpg')
        self.dict[data.Phonemes.MBP.name] = QPixmap('../images/mouth_types/blair_m_b_p.jpg')
        self.dict[data.Phonemes.L.name] = QPixmap('../images/mouth_types/blair_l_d_th.jpg')
        self.dict[data.Phonemes.WQ.name] = QPixmap('../images/mouth_types/blair_w_q.jpg')
        self.dict[data.Phonemes.rest.name] = QPixmap('../images/mouth_types/blair_rest.jpg')

    def change_duration(self):
        speaker_recognition()
        # duration_change(self.sld_duration.value())

    def change_pitch(self):
        pitch_change(self.sld_pitch.value())

    def right_layout_init(self):
        self.radio_mul_speakers = QRadioButton("Show multiple speakers")
        self.radio_mul_speakers.setChecked(True)
        self.radio_mul_speakers.toggled.connect(self.on_radio_button_toggled)
        # Add Duration Slider
        slider_label_duration = QLabel("Duration")
        slider_label_duration.setAlignment(Qt.AlignCenter)
        self.sld_duration = QSlider(Qt.Horizontal, self)
        self.sld_duration.setMinimum(-300)
        self.sld_duration.setMaximum(300)
        self.sld_duration.setValue(0)
        # sld_duration.setTickPosition(QSlider.TicksBelow) # If I want a grid below
        # sld_duration.setTickInterval(1) # Set an interval
        self.sld_duration.sliderReleased.connect(self.change_duration)

        # Add Pitch Slider
        slider_label_pitch = QLabel("Pitch")
        slider_label_pitch.setAlignment(Qt.AlignCenter)
        self.sld_pitch = QSlider(Qt.Horizontal, self)
        self.sld_pitch.setMinimum(-300)
        self.sld_pitch.setMaximum(300)
        self.sld_pitch.setValue(0)
        self.sld_pitch.sliderReleased.connect(self.change_pitch)

        self.mouth_layout_init()

        # Add dropdown list of algorithms
        comboBox = QComboBox(self)
        comboBox.addItem('Algorithm 1')
        comboBox.addItem('Algorithm 2')

        # Button to run algorithm
        run_algorithm_button = QPushButton('Run Algorithm', self)
        run_algorithm_button.setToolTip('Run the selected phoneme recognition algorithm')
        run_algorithm_button.clicked.connect(self.run_phonema_recognition_algorithm)

        self.rightLayout.addWidget(self.radio_mul_speakers)
        self.rightLayout.addWidget(slider_label_duration)
        self.rightLayout.addWidget(self.sld_duration)
        self.rightLayout.addWidget(slider_label_pitch)
        self.rightLayout.addWidget(self.sld_pitch)
        self.rightLayout.addLayout(self.mouthLayout)
        self.rightLayout.addWidget(comboBox)
        self.rightLayout.addWidget(run_algorithm_button)

        self.layout.addLayout(self.rightLayout)

    def mouth_layout_init(self):
        # Add Image of the mouth
        self.mouth1_image = QLabel(self)
        pixmap = QPixmap('../images/mouth_types.jpg')
        self.mouth1_image.setPixmap(pixmap)
        # Add Image of the mouth
        self.mouth2_image = QLabel(self)
        pixmap = QPixmap('../images/mouth_types.jpg')
        self.mouth2_image.setPixmap(pixmap)

        self.mouthLayout.addWidget(self.mouth1_image)
        self.mouthLayout.addWidget(self.mouth2_image)

    def radiobutton_is_checked(self):
        return self.radio_mul_speakers.isChecked()

    def on_radio_button_toggled(self):
        radio_mul_speakers = self.sender()
        self.mouth2_image.setHidden(not radio_mul_speakers.isChecked())

    def update_mouth1(self, phoneme_name):
        # import pdb; pdb.set_trace()
        pixmap = self.dict[phoneme_name]
        self.mouth1_image.setPixmap(pixmap)
        self.mouth1_image.update()

    def update_mouth2(self, phoneme_name):
        # import pdb; pdb.set_trace()
        pixmap = self.dict[phoneme_name]
        self.mouth2_image.setPixmap(pixmap)
        self.mouth2_image.update()

    def left_layout_init(self):
        self.plot_widget = QWidget(self)
        box = QVBoxLayout(self.plot_widget)
        self.canvas = PlotCanvas(self.plot_widget)
        mpl_toolbar = NavigationToolbar(self.canvas, self.plot_widget)

        box.addWidget(self.canvas)
        box.addWidget(mpl_toolbar)
        self.leftLayout.addWidget(self.plot_widget)
        self.layout.addLayout(self.leftLayout)

    def plot_data(self, filename):
        # import pdb; pdb.set_trace()
        self.canvas.plot(filename)

    def run_phonema_recognition_algorithm(self):
        # self.data.example_dat()
        # vocal_lpc_phonemes.vocal_phonemes()
        rp.rnn_phonemes()
        # import pdb; pdb.set_trace()
        for i in range(1, len(self.data.dat)):
            self.add_vertical_line(self.data.dat[i][0] / self.data.fs, remove=False)

    def draw_vertical_line(self, sec, remove=True, color='r'):
        self.canvas.draw_line(sec, remove, color)

    def add_vertical_line(self, sec, remove=True):
        self.canvas.draw_line(sec, remove)

    def remove_line(self):
        self.canvas.remove_line()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.data = data.LipSyncData.get_instance()
        self.fs = 0
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.axes.axis('off')

    def plot(self, name):
        # import pdb; pdb.set_trace()
        ax = self.fig.add_subplot(111)
        ax.cla()
        signal, self.fs = self.data.get_audio_fs()
        time = np.linspace(0, len(signal) / self.fs, num=len(signal))
        ax.plot(time, signal, 'b-')
        ax.set_title(name)
        ax.set_xlabel('seconds')
        self.draw()

    def draw_line(self, sec, remove=True, color='r'):
        # import pdb; pdb.set_trace()
        ax = self.fig.add_subplot(111)
        if remove and len(ax.lines) > 1:
            ax.lines[len(ax.lines)-1].remove()
        ax.axvline(x=sec, color=color)
        self.draw()

    def remove_line(self):
        ax = self.fig.add_subplot(111)
        if len(ax.lines) > 1:
            ax.lines[len(ax.lines)-1].remove()
        self.draw()
