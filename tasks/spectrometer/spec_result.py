import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import colorsys

class SpectrometerResultsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._zorder_count = 2


        # --- 1つ目のFigure（スペクトル） ---
        self.fig_spectrum = Figure(figsize=(3, 2), dpi=100)
        self.ax_raw = self.fig_spectrum.add_subplot(111)
        self.ax_raw.set_title("Raw Spectrum")
        self.ax_raw.set_xlabel("Wavelength [nm]")
        self.ax_raw.set_ylabel("Intensity [a.u.]")
        self.ax_raw.set_xlim(450, 750)
        self.ax_raw.set_ylim(0, 1)

        self.canvas_raw = FigureCanvasTkAgg(self.fig_spectrum, master=self)
        self.canvas_raw.draw()
        self.canvas_raw.get_tk_widget().grid(row=0, column=0, padx=0, pady=0)

        # --- 2つ目のFigure（時系列） ---
        self.fig_time = Figure(figsize=(3, 2), dpi=100)
        self.ax_intfere = self.fig_time.add_subplot(111)
        self.ax_intfere.set_title("Interference Spectrum")
        self.ax_intfere.set_xlabel("Wavelength [nm]")
        self.ax_intfere.set_ylabel("Intensity [a.u.]")
        self.ax_intfere.set_xlim(450, 750)
        self.ax_intfere.set_ylim(0, 1)

        self.canvas_intfere = FigureCanvasTkAgg(self.fig_time, master=self)
        self.canvas_intfere.draw()
        self.canvas_intfere.get_tk_widget().grid(row=1, column=0, padx=0, pady=0)

        self.clear_button = tk.Button(self.parent, text="Clear Graphs", command=self.clear_graphs)
        self.clear_button.place(x=0, y=0)

        self.dummy()

    # 1つのグラフを最前列に持ってくる
    def bring_to_front(self, wavelengths, reference, intensities, i, j):
        intfere_ij = intensities[i][j] / reference

        l_raw = self.ax_raw.plot(wavelengths, intensities[i][j], color=self.color_ij(len(intensities), i, j))
        l_intfere =self.ax_intfere.plot(wavelengths, intfere_ij, color=self.color_ij(len(intensities), i, j))

        # self._zorder_count += 1
        # l_raw.set_zorder(self._zorder_count)
        # l_intfere.set_zorder(self._zorder_count)
        
        self.canvas_raw.draw()
        self.canvas_intfere.draw()

    def update_raw(self, wavelengths, reference, intensities):
        """
        スペクトルデータを更新
        重くなりがちなのでなんか変えたい
        """
        self.ax_raw.clear()
        if np.any(reference !=0):
            self.ax_raw.plot(wavelengths, reference, color="black", linestyle="--")
        for i in range(len(intensities)):
            for j in range(len(intensities[i])):
                if np.any(intensities[i][j] != 0):
                    # i: positions,  j: loops
                    self.ax_raw.plot(wavelengths, intensities[i][j])
                    # self.ax_raw.plot(wavelengths, intensities[i][j], color=self.color_ij(len(intensities), i, j))
        # self.ax_raw.plot(wavelengths, intensities)
        self.ax_raw.set_title("Raw Spectrum")
        self.ax_raw.set_xlabel("Wavelength [nm]")
        self.ax_raw.set_ylabel("Intensity [a.u.]")
        self.ax_raw.set_xlim(450, 750)
        self.ax_raw.set_ylim(0, 1)
        self.canvas_raw.draw()

    def update_intfere(self, wavelengths, reference, intensities):
        """時系列データを更新"""
        intfere = intensities
        if np.any(reference !=0):
            intfere = intensities/reference

        self.ax_intfere.clear()
        for i in range(len(intfere)):
            for j in range(len(intfere[i])):
                intfere_ij = intfere[i][j]
                if np.any((intfere_ij!=0) & ~np.isnan(intfere_ij) & np.isfinite(intfere_ij)):
                    # self.ax_intfere.plot(wavelengths, intfere_ij, color=self.color_ij(len(intfere), i, j))
                    self.ax_intfere.plot(wavelengths, intfere_ij)
        # self.ax_intfere.plot(wavelengths, intensities)
        self.ax_intfere.set_title("Interference Spectrum")
        self.ax_intfere.set_xlabel("Wavelength [nm]")
        self.ax_intfere.set_ylabel("Intensity [a.u.]")
        self.ax_intfere.set_xlim(450, 750)
        self.ax_intfere.set_ylim(0, 0.5)
        self.canvas_intfere.draw()

    def color_ij(self, pos_num:int, i: int, j: int):
        # i < pos_num
        f_max = 1.3
        f_min = 0.4
        
        colors = plt.cm.tab10.colors

        r,g,b = colors[i%10]
        h,l,s = colorsys.rgb_to_hls(r,g,b)

        l = (f_max-f_min) * j / pos_num + f_min
        r,g,b = colorsys.hls_to_rgb(h,l,s)
        # print(r,g,b)
        return (r,g,b)

    def clear_graphs(self):
        """両方のグラフをクリア"""
        self.ax_raw.clear()
        self.ax_raw.set_title("Raw Spectrum")
        self.ax_raw.set_xlabel("Wavelength [nm]")
        self.ax_raw.set_ylabel("Intensity [a.u.]")
        self.ax_raw.set_xlim(450, 750)
        self.ax_raw.set_ylim(0, 1)
        self.canvas_raw.draw()

        self.ax_intfere.clear()
        self.ax_intfere.set_title("Interference Spectrum")
        self.ax_intfere.set_xlabel("Wavelength [nm]")
        self.ax_intfere.set_ylabel("Intensity [a.u.]")
        self.ax_intfere.set_xlim(450, 750)
        self.ax_intfere.set_ylim(0, 1)
        self.canvas_intfere.draw()

    def dummy(self):
        self.update_raw(np.array([460, 500, 600, 700]), np.array([1,1,1,1]) ,np.array([[[0.10, 0.50, 0.30, 0.70]]]))
        self.update_intfere(np.array([460, 500, 600, 700]), np.array([1,1,1,1]) ,np.array([[[0.10, 0.50, 0.30, 0.70]]]))

# --- テスト動作用 ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Spectrometer Results Viewer")

    results_frame = SpectrometerResultsFrame(root)
    results_frame.pack(fill="both", expand=True)

    root.mainloop()
